import asyncio
import json
import unittest
from pathlib import Path

from wox_plugin import (
    Context,
    PluginInitParams,
    Query,
    QueryLayout,
    QueryResponse,
    QueryType,
    Result,
    ResultTail,
    ResultTailType,
    SelectionType,
    WoxImage,
    WoxImageType,
    WoxPreview,
    WoxPreviewListData,
    WoxPreviewListItem,
    WoxPreviewType,
)
from wox_plugin.models.query import QueryEnv, Selection


class MockPublicAPI:
    def __init__(self, initial_settings=None):
        self.settings = initial_settings or {}
        self.setting_reads = []
        self.setting_changed_callbacks = []
        self.translations = {
            "prompt_empty_search": "Type to search bookmarks, or paste a URL to save...",
            "bookmark_already_exists": "⚠️ Already bookmarked",
            "prompt_save_bookmark": "Press Enter to save bookmark",
            "action_save_bookmark": "Save Bookmark",
            "notify_bookmark_created": "Bookmark saved successfully",
            "notify_bookmark_failed": "Failed to save bookmark",
            "no_tags_found": "No tags found",
            "no_tags_found_sub": "No tags found in your Linkding instance",
            "no_matching_tags": "No matching tags",
            "tag_action_select": "Filter bookmarks by this tag",
            "selection_bookmarks_found": "{count} bookmarks found",
            "selection_press_enter_to_expand": "Press Enter to select a bookmark",
            "selection_press_enter_to_edit": "No bookmarks found · Press Enter to edit search terms",
            "selection_action_expand": "Expand Bookmark List",
            "toolbar_tags_found": "{count} tags found",
            "toolbar_bookmarks_found": "{count} bookmarks found",
        }
        self.copied_params = []
        self.notifications = []
        self.changed_queries = []
        self.leave_plugin_query_callbacks = []
        self.toolbar_messages = []
        self.cleared_toolbar_msg_ids = []
        self.result_updates = []
        self.result_updated = asyncio.Event()
        self.hidden_update_attempts = 0
        self.accept_updates = True
        self.visible = True

    async def update_result(self, ctx, result):
        import copy
        if not self.accept_updates:
            return False
        if self.hidden_update_attempts:
            self.hidden_update_attempts -= 1
            return False
        self.result_updates.append(copy.deepcopy(result))
        self.result_updated.set()
        return True

    async def is_visible(self, ctx):
        return self.visible

    async def wait_for_result_update(self, since=0):
        while True:
            updates = [update for update in self.result_updates[since:] if update.sub_title is not None]
            if updates:
                return updates[-1]
            self.result_updated.clear()
            await asyncio.wait_for(self.result_updated.wait(), timeout=2)

    async def get_setting(self, ctx: Context, key: str) -> str:
        self.setting_reads.append(key)
        return self.settings.get(key, "")

    async def save_setting(self, ctx: Context, key: str, value: str, is_platform_specific: bool = False) -> None:
        self.settings[key] = value

    async def on_setting_changed(self, ctx: Context, callback) -> None:
        self.setting_changed_callbacks.append(callback)

    async def on_leave_plugin_query(self, ctx: Context, callback) -> None:
        self.leave_plugin_query_callbacks.append(callback)

    async def get_translation(self, ctx: Context, key: str) -> str:
        return self.translations.get(key, key)

    async def copy(self, ctx: Context, params) -> None:
        self.copied_params.append(params)

    async def notify(self, ctx: Context, message: str) -> None:
        self.notifications.append(message)

    async def change_query(self, ctx: Context, param) -> None:
        self.changed_queries.append(param)

    async def show_toolbar_msg(self, ctx: Context, msg) -> None:
        self.toolbar_messages.append(msg)

    async def clear_toolbar_msg(self, ctx: Context, toolbar_msg_id: str) -> None:
        self.cleared_toolbar_msg_ids.append(toolbar_msg_id)


def extract_header_metadata(plugin_file_path: Path) -> dict:
    content = plugin_file_path.read_text(encoding="utf-8")
    header_lines = []
    for line in content.splitlines():
        if line.startswith("#"):
            header_lines.append(line.lstrip("#").strip())
        elif line.strip() == "":
            continue
        else:
            break
    json_text = "\n".join(header_lines)
    return json.loads(json_text)


async def query_selection_and_wait(plugin, api, ctx, query):
    """Apply the host's background row update at the public launcher seam."""
    since = len(api.result_updates)
    response = await plugin.query(ctx, query)
    update = await api.wait_for_result_update(since)
    result = response.results[0]
    for field in ("sub_title", "preview", "actions", "tails"):
        value = getattr(update, field)
        if value is not None:
            setattr(result, field, value)
    return response


class TestPluginMetadata(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plugin_path = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"

    def test_file_exists(self):
        self.assertTrue(self.plugin_path.is_file(), "Wox.Plugin.Linkding.py must exist")

    def test_header_metadata_fields(self):
        meta = extract_header_metadata(self.plugin_path)

        # Basic metadata
        self.assertEqual(meta.get("MinWoxVersion"), "2.4.2")
        self.assertEqual(meta.get("Runtime"), "PYTHON")
        self.assertEqual(meta.get("TriggerKeywords"), ["ld"])
        self.assertTrue(meta.get("Id"), "Plugin Id must be present")
        self.assertEqual(meta.get("Name"), "i18n:plugin_name")

        # Official Linkding SVG icon
        icon = meta.get("Icon", "")
        self.assertTrue(icon.startswith("svg:<svg"), "Icon must be an inline SVG string starting with 'svg:<svg'")
        self.assertIn("#5856e0", icon, "Icon must contain Linkding theme color")

        # Features: debounce and querySelection
        features = meta.get("Features", [])
        debounce_features = [f for f in features if f.get("Name") == "debounce"]
        self.assertEqual(len(debounce_features), 1, "Debounce feature must be declared")
        self.assertEqual(debounce_features[0].get("Params", {}).get("IntervalMs"), 200)

        query_selection_features = [f for f in features if f.get("Name") == "querySelection"]
        self.assertEqual(len(query_selection_features), 1, "querySelection feature must be declared")

        # SettingDefinitions
        setting_defs = {s.get("Value", {}).get("Key"): s for s in meta.get("SettingDefinitions", [])}
        self.assertIn("linkding_url", setting_defs)
        self.assertIn("api_token", setting_defs)
        self.assertIn("max_results", setting_defs)

        # linkding_url validators
        url_setting = setting_defs["linkding_url"]
        self.assertEqual(url_setting.get("Type"), "textbox")
        url_validators = [v.get("Type") for v in url_setting.get("Value", {}).get("Validators", [])]
        self.assertIn("not_empty", url_validators)

        # api_token validators
        token_setting = setting_defs["api_token"]
        self.assertEqual(token_setting.get("Type"), "textbox")
        token_validators = [v.get("Type") for v in token_setting.get("Value", {}).get("Validators", [])]
        self.assertIn("not_empty", token_validators)

        # max_results validators and default
        max_results_setting = setting_defs["max_results"]
        self.assertEqual(max_results_setting.get("Type"), "textbox")
        self.assertEqual(max_results_setting.get("Value", {}).get("DefaultValue"), "10")
        max_validators = [v.get("Type") for v in max_results_setting.get("Value", {}).get("Validators", [])]
        self.assertIn("is_number", max_validators)

        # QueryRequirements
        query_reqs = meta.get("QueryRequirements", {})
        any_query_reqs = {r.get("SettingKey") for r in query_reqs.get("AnyQuery", [])}
        self.assertIn("linkding_url", any_query_reqs)
        self.assertIn("api_token", any_query_reqs)

        # Inline I18n
        i18n = meta.get("I18n", {})
        self.assertIn("en_US", i18n)
        self.assertIn("zh_CN", i18n)
        for lang in ("en_US", "zh_CN"):
            self.assertIn("plugin_name", i18n[lang])
            self.assertIn("setting_linkding_url_label", i18n[lang])
            self.assertIn("setting_api_token_label", i18n[lang])
            self.assertIn("setting_max_results_label", i18n[lang])
            self.assertIn("prompt_empty_search", i18n[lang])
            self.assertIn("action_open_url", i18n[lang])
            self.assertIn("action_copy_url", i18n[lang])
            self.assertIn("action_open_in_linkding", i18n[lang])
            self.assertIn("no_bookmarks_found", i18n[lang])
            self.assertIn("no_bookmarks_found_sub", i18n[lang])
            self.assertIn("error_auth_failed", i18n[lang])
            self.assertIn("error_auth_failed_sub", i18n[lang])
            self.assertIn("error_network", i18n[lang])
            self.assertIn("error_api", i18n[lang])
            self.assertIn("error_search_bookmarks", i18n[lang])
            self.assertIn("error_check_bookmark", i18n[lang])
            self.assertIn("error_fetch_tags", i18n[lang])
            self.assertIn("error_timeout", i18n[lang])
            self.assertIn("error_timeout_sub", i18n[lang])
            self.assertIn("bookmark_already_exists", i18n[lang])
            self.assertIn("prompt_save_bookmark", i18n[lang])
            self.assertIn("action_save_bookmark", i18n[lang])
            self.assertIn("notify_bookmark_created", i18n[lang])
            self.assertIn("notify_bookmark_failed", i18n[lang])
            self.assertIn("no_tags_found", i18n[lang])
            self.assertIn("no_tags_found_sub", i18n[lang])
            self.assertIn("no_matching_tags", i18n[lang])
            self.assertIn("tag_action_select", i18n[lang])
            self.assertIn("selection_bookmarks_found", i18n[lang])
            self.assertIn("selection_entry_title", i18n[lang])
            self.assertIn("selection_searching", i18n[lang])
            self.assertIn("selection_search_failed", i18n[lang])
            self.assertIn("selection_press_enter_to_expand", i18n[lang])
            self.assertIn("selection_press_enter_to_edit", i18n[lang])
            self.assertIn("selection_action_expand", i18n[lang])
            self.assertIn("toolbar_tags_found", i18n[lang])
            self.assertIn("toolbar_bookmarks_found", i18n[lang])


class TestPluginLifecycle(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib
        import sys

        # Dynamically import plugin module
        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        if not plugin_file.is_file():
            self.skipTest("Wox.Plugin.Linkding.py does not exist yet")

        import importlib.util
        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

    async def test_init_loads_settings_and_registers_callback(self):
        mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "20",
        })
        ctx = Context()
        params = PluginInitParams(api=mock_api, plugin_directory=str(Path.cwd()))

        await self.plugin.init(ctx, params)

        self.assertEqual(self.plugin.linkding_url, "https://linkding.example.com")
        self.assertEqual(self.plugin.api_token, "secret_token")
        self.assertEqual(self.plugin.max_results, 20)
        self.assertEqual(len(mock_api.setting_changed_callbacks), 1)

    async def test_init_falls_back_to_default_max_results(self):
        mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "",
        })
        ctx = Context()
        params = PluginInitParams(api=mock_api, plugin_directory=str(Path.cwd()))

        await self.plugin.init(ctx, params)
        self.assertEqual(self.plugin.max_results, 10)

    async def test_on_setting_changed_updates_attributes(self):
        mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://old.example.com",
            "api_token": "old_token",
            "max_results": "10",
        })
        ctx = Context()
        params = PluginInitParams(api=mock_api, plugin_directory=str(Path.cwd()))

        await self.plugin.init(ctx, params)
        callback = mock_api.setting_changed_callbacks[0]

        await callback(ctx, "linkding_url", "https://new.example.com")
        self.assertEqual(self.plugin.linkding_url, "https://new.example.com")

        await callback(ctx, "api_token", "new_token")
        self.assertEqual(self.plugin.api_token, "new_token")

        await callback(ctx, "max_results", "25")
        self.assertEqual(self.plugin.max_results, 25)


class TestPluginQuery(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        if not plugin_file.is_file():
            self.skipTest("Wox.Plugin.Linkding.py does not exist yet")

        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

        mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "10",
        })
        self.ctx = Context()
        params = PluginInitParams(api=mock_api, plugin_directory=str(Path.cwd()))
        await self.plugin.init(self.ctx, params)

    async def test_empty_search_returns_ready_prompt(self):
        query = Query(
            id="q1",
            type=QueryType.INPUT,
            raw_query="ld",
            selection=Selection(),
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="",
        )

        response = await self.plugin.query(self.ctx, query)

        self.assertIsNotNone(response)
        self.assertEqual(len(response.results), 1)
        result = response.results[0]
        self.assertEqual(result.title, "i18n:prompt_empty_search")
        self.assertIn("linkding.example.com", result.sub_title)
        self.assertIsNotNone(result.icon)
        self.assertEqual(result.icon.image_type, WoxImageType.SVG)


class TestBookmarkSearch(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys
        from unittest.mock import patch

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

        self.mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "10",
        })
        self.ctx = Context()
        params = PluginInitParams(api=self.mock_api, plugin_directory=str(Path.cwd()))
        await self.plugin.init(self.ctx, params)

    def _make_query(self, search: str) -> Query:
        return Query(
            id="q_test",
            type=QueryType.INPUT,
            raw_query=f"ld {search}",
            selection=Selection(),
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search=search,
        )

    async def test_routing_ignores_url_and_tag(self):
        # Queries matching URL pattern route to _handle_url_input, not _search_bookmarks
        # Queries matching # tag prefix do not trigger bookmark search
        from unittest.mock import AsyncMock, patch

        with patch.object(self.plugin, "_search_bookmarks") as mock_search, \
             patch.object(self.plugin, "_handle_url_input", new_callable=AsyncMock) as mock_handle_url, \
             patch.object(self.plugin, "_handle_tag_browsing", new_callable=AsyncMock) as mock_handle_tag:
            mock_handle_url.return_value = QueryResponse(results=[])
            mock_handle_tag.return_value = QueryResponse(results=[])

            res1 = await self.plugin.query(self.ctx, self._make_query("https://example.com/page"))
            mock_handle_url.assert_called_with(self.ctx, "https://example.com/page")

            res2 = await self.plugin.query(self.ctx, self._make_query("http://insecure.org"))
            mock_handle_url.assert_called_with(self.ctx, "http://insecure.org")

            q3 = self._make_query("#python")
            res3 = await self.plugin.query(self.ctx, q3)
            mock_handle_tag.assert_called_with(self.ctx, q3, "python", selected_tags=set(), raw_prefix="")

            mock_search.assert_not_called()

    async def test_search_normal_results_and_formatting(self):
        from unittest.mock import patch, MagicMock
        import io

        mock_response_data = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "url": "https://python.org",
                    "title": "Python Programming",
                    "website_title": "Welcome to Python.org",
                    "tag_names": ["python", "dev"],
                },
                {
                    "id": 2,
                    "url": "https://github.com",
                    "title": "",
                    "website_title": "GitHub Homepage",
                    "tag_names": [],
                },
            ],
        }

        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
            response = await self.plugin.query(self.ctx, self._make_query("python"))

            self.assertEqual(len(response.results), 2)

            # Check HTTP request call details
            self.assertEqual(mock_urlopen.call_count, 1)
            req = mock_urlopen.call_args[0][0]
            self.assertIn("https://linkding.example.com/api/bookmarks/?q=python&limit=10", req.full_url)
            self.assertEqual(req.headers.get("Authorization"), "Token secret_token")
            self.assertEqual(req.headers.get("Accept"), "application/json")
            self.assertTrue(req.headers.get("User-agent"), "User-Agent must be set to prevent Cloudflare blocks")

            # Check result 1 formatting
            r1 = response.results[0]
            self.assertEqual(r1.title, "Python Programming")
            self.assertEqual(r1.sub_title, "https://python.org · #python #dev")
            self.assertEqual(r1.icon.image_type, WoxImageType.SVG)
            self.assertEqual(len(r1.actions), 3)

            # Check actions on result 1
            act_default = r1.actions[0]
            self.assertTrue(act_default.is_default)
            self.assertEqual(act_default.name, "i18n:action_open_url")

            act_copy = r1.actions[1]
            self.assertFalse(act_copy.is_default)
            self.assertEqual(act_copy.name, "i18n:action_copy_url")

            act_linkding = r1.actions[2]
            self.assertFalse(act_linkding.is_default)
            self.assertEqual(act_linkding.name, "i18n:action_open_in_linkding")

            # Check result 2 formatting (fallback to website_title when title is empty, no tags)
            r2 = response.results[1]
            self.assertEqual(r2.title, "GitHub Homepage")
            self.assertEqual(r2.sub_title, "https://github.com")

    async def test_search_actions_dispatch(self):
        from unittest.mock import patch, MagicMock
        from wox_plugin import ActionContext

        mock_response_data = {
            "count": 1,
            "results": [
                {
                    "id": 1,
                    "url": "https://python.org",
                    "title": "Python Programming",
                    "tag_names": ["python"],
                }
            ],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        with patch("urllib.request.urlopen", return_value=mock_http_response):
            response = await self.plugin.query(self.ctx, self._make_query("python"))
            result = response.results[0]

            act_open = result.actions[0]
            act_copy = result.actions[1]
            act_web = result.actions[2]

            with patch("webbrowser.open") as mock_browser_open:
                # Test default open action
                await act_open.action(self.ctx, ActionContext())
                mock_browser_open.assert_called_once_with("https://python.org")

            # Test copy action
            await act_copy.action(self.ctx, ActionContext())
            self.assertEqual(len(self.mock_api.copied_params), 1)
            self.assertEqual(self.mock_api.copied_params[0].text, "https://python.org")

            with patch("webbrowser.open") as mock_browser_open:
                # Test open in linkding web action
                await act_web.action(self.ctx, ActionContext())
                mock_browser_open.assert_called_once_with("https://linkding.example.com/bookmarks?q=python")

    async def test_search_empty_results(self):
        from unittest.mock import patch, MagicMock

        mock_response_data = {"count": 0, "results": []}
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        with patch("urllib.request.urlopen", return_value=mock_http_response):
            response = await self.plugin.query(self.ctx, self._make_query("nonexistent"))

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:no_bookmarks_found")
            self.assertEqual(res.sub_title, "i18n:no_bookmarks_found_sub")
            self.assertEqual(len(res.actions), 1)
            self.assertEqual(res.actions[0].name, "i18n:action_open_in_linkding")

    async def test_search_auth_error_handling(self):
        import urllib.error
        from unittest.mock import patch

        http_error = urllib.error.HTTPError(
            url="https://linkding.example.com/api/bookmarks/",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=None,
        )

        with patch("urllib.request.urlopen", side_effect=http_error):
            response = await self.plugin.query(self.ctx, self._make_query("test"))

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:error_auth_failed")
            self.assertEqual(res.sub_title, "i18n:error_auth_failed_sub")

    async def test_search_network_error_and_timeout(self):
        import urllib.error
        from unittest.mock import patch

        url_error = urllib.error.URLError(reason="Connection refused")
        with patch("urllib.request.urlopen", side_effect=url_error):
            response = await self.plugin.query(self.ctx, self._make_query("test"))
            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:error_network")
            self.assertIn("Connection refused", res.sub_title)

        timeout_error = TimeoutError("timed out")
        with patch("urllib.request.urlopen", side_effect=timeout_error):
            response = await self.plugin.query(self.ctx, self._make_query("test"))
            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:error_timeout")
            self.assertEqual(res.sub_title, "i18n:error_timeout_sub")



    async def test_query_paths_map_request_errors_consistently(self):
        import urllib.error
        from unittest.mock import patch

        paths = [
            ("python", False, "i18n:error_search_bookmarks"),
            ("#", False, "i18n:error_fetch_tags"),
            ("#github #", False, "i18n:error_fetch_tags"),
            ("https://example.com", False, "i18n:error_check_bookmark"),
            ("https://example.com", True, "i18n:error_check_bookmark"),
            ("python", True, "i18n:selection_search_failed"),
        ]
        errors = [
            (urllib.error.HTTPError("url", 401, "Unauthorized", {}, None), "auth", "i18n:error_auth_failed", "i18n:error_auth_failed_sub"),
            (urllib.error.HTTPError("url", 403, "Forbidden", {}, None), "auth", "i18n:error_auth_failed", "i18n:error_auth_failed_sub"),
            (urllib.error.HTTPError("url", 500, "Server Error", {}, None), "api", "i18n:error_api", "HTTP 500: Server Error"),
            (urllib.error.URLError("offline"), "network", "i18n:error_network", "offline"),
            (TimeoutError("timed out"), "timeout", "i18n:error_timeout", "i18n:error_timeout_sub"),
            (urllib.error.URLError(TimeoutError()), "timeout", "i18n:error_timeout", "i18n:error_timeout_sub"),
            (urllib.error.URLError("timed out"), "timeout", "i18n:error_timeout", "i18n:error_timeout_sub"),
            (ValueError("invalid JSON"), "generic", None, "invalid JSON"),
        ]
        for search, selected, generic_title in paths:
            for error, category, title, subtitle in errors:
                with self.subTest(search=search, selected=selected, category=category):
                    query = Query(
                        id="q_errors", type=QueryType.SELECTION if selected else QueryType.INPUT,
                        raw_query="" if selected else f"ld {search}",
                        selection=Selection(type=SelectionType.TEXT, text=search) if selected else Selection(),
                        env=QueryEnv(), trigger_keyword="" if selected else "ld", command="",
                        search="" if selected else search,
                    )
                    with patch("urllib.request.urlopen", side_effect=error):
                        if selected and search == "python":
                            response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, query)
                            result = response.results[0]
                            expected_status = title if category in ("auth", "network", "timeout") else generic_title
                            self.assertEqual(result.id, "selection:bookmarks")
                            self.assertEqual(result.title, "i18n:selection_entry_title")
                            self.assertEqual(result.sub_title, expected_status)
                            preview = WoxPreviewListData.from_json(json.loads(result.preview.preview_data))
                            self.assertEqual(preview.items[0].title, expected_status)
                        else:
                            response = await self.plugin.query(self.ctx, query)
                            result = response.results[0]
                            self.assertEqual(result.id, f"error:{category}")
                            self.assertEqual(result.title, title or generic_title)
                            self.assertEqual(result.sub_title, subtitle)
                        self.assertEqual(result.actions, [])
                        self.assertEqual(result.icon.image_type, WoxImageType.SVG)
                        expected_ratio = 0.6 if selected else QueryLayout().result_preview_width_ratio
                        self.assertEqual(response.layout.result_preview_width_ratio, expected_ratio)


class TestBookmarkFavicons(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import base64
        import importlib.util
        import sys
        import threading

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_favicons", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_favicons"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()
        self.api = MockPublicAPI({
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
        })
        self.ctx = Context()
        await self.plugin.init(self.ctx, PluginInitParams(api=self.api, plugin_directory=str(Path.cwd())))
        self.bookmarks = [{
            "id": 1, "title": "Python", "url": "https://python.org",
            "tag_names": ["dev"],
            "favicon_url": "https://linkding.example.com/static/python.png",
        }]
        self.png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/iZk9HQAAAABJRU5ErkJggg=="
        )
        self.image_data = self.png
        self.image_type = "image/png"
        self.image_error = None
        self.image_requests = []
        self.image_gate = threading.Event()
        self.image_gate.set()

    def _query(self, text="python", selection=False):
        return Query(
            id="q_favicon", type=QueryType.SELECTION if selection else QueryType.INPUT,
            raw_query=f"ld {text}", search=text, trigger_keyword="ld", command="",
            selection=Selection(type=SelectionType.TEXT, text=text) if selection else Selection(),
            env=QueryEnv(),
        )

    def _urlopen(self, request, **kwargs):
        from email.message import Message
        from unittest.mock import MagicMock

        response = MagicMock()
        response.__enter__.return_value = response
        if "/api/bookmarks/" in request.full_url:
            payload = (
                {"bookmark": self.bookmarks[0]}
                if "/check/" in request.full_url
                else {"count": len(self.bookmarks), "results": self.bookmarks}
            )
            response.read.return_value = json.dumps(payload).encode()
        else:
            self.image_requests.append(request)
            self.image_gate.wait(timeout=5)
            if self.image_error:
                raise self.image_error
            response.read.return_value = self.image_data
            response.headers = Message()
            response.headers["Content-Type"] = self.image_type
        return response

    async def _finish_images(self):
        # Synchronize background work; assertions below stay at the launcher/API seam.
        await asyncio.gather(*tuple(self.plugin._favicon_refreshes))

    async def test_nonblocking_download_updates_rows_and_reuses_cached_image(self):
        from unittest.mock import patch
        from wox_plugin import ActionContext

        self.bookmarks.append(dict(self.bookmarks[0], id=2))
        self.image_gate.clear()
        with patch("urllib.request.urlopen", side_effect=self._urlopen), \
             patch("webbrowser.open") as open_url:
            try:
                response = await asyncio.wait_for(self.plugin.query(self.ctx, self._query()), timeout=1)
                self.assertTrue(all(r.icon.image_type == WoxImageType.SVG for r in response.results))
                self.assertEqual(self.api.result_updates, [])
                await response.results[0].actions[0].action(self.ctx, ActionContext())
                open_url.assert_called_once_with("https://python.org")
            finally:
                self.image_gate.set()
                await self._finish_images()
            self.assertEqual(len(self.image_requests), 1)
            self.assertNotIn("Authorization", self.image_requests[0].headers)
            self.assertEqual({u.id for u in self.api.result_updates}, {"bookmark:1", "bookmark:2"})
            self.assertTrue(all(u.icon.image_type == WoxImageType.BASE64 for u in self.api.result_updates))
            import base64
            encoded = self.api.result_updates[0].icon.image_data.split(",", 1)[1]
            self.assertEqual(base64.b64decode(encoded), self.png)
            self.assertTrue(all(u.title is None and u.actions is None for u in self.api.result_updates))
            cached = await self.plugin.query(self.ctx, self._query("#dev "))
            await self._finish_images()
            self.assertEqual(cached.results[0].icon.image_type, WoxImageType.BASE64)
            self.assertEqual(len(self.image_requests), 1)

    async def test_missing_favicon_uses_linkding_without_image_requests(self):
        from unittest.mock import patch

        self.bookmarks = [dict(self.bookmarks[0], id=index, favicon_url=value)
                          for index, value in enumerate([None, ""])]
        self.bookmarks.append({"id": 3, "url": "https://example.org"})
        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            response = await self.plugin.query(self.ctx, self._query())
            await self._finish_images()
        self.assertTrue(all(r.icon.image_data == self.module.LINKDING_ICON_SVG for r in response.results))
        self.assertEqual(self.image_requests, [])
        self.assertEqual(self.api.result_updates, [])

    async def test_download_errors_keep_linkding_and_cache_failure(self):
        import http.client
        import urllib.error
        from unittest.mock import patch

        errors = [
            urllib.error.HTTPError("https://linkding.example.com/icon", 404, "Not found", {}, None),
            urllib.error.URLError("offline"),
            TimeoutError("timed out"),
            http.client.IncompleteRead(b"partial image"),
        ]
        for index, error in enumerate(errors):
            with self.subTest(error=type(error).__name__):
                self.bookmarks[0]["favicon_url"] = f"https://linkding.example.com/static/{index}.png"
                self.image_error = error
                with patch("urllib.request.urlopen", side_effect=self._urlopen):
                    response = await self.plugin.query(self.ctx, self._query(str(index)))
                    await self._finish_images()
                    cached = await self.plugin.query(self.ctx, self._query(str(index)))
                    await self._finish_images()
                self.assertEqual(response.results[0].icon.image_data, self.module.LINKDING_ICON_SVG)
                self.assertEqual(cached.results[0].icon.image_data, self.module.LINKDING_ICON_SVG)
        self.assertEqual(len(self.image_requests), len(errors))
        self.assertEqual(self.api.result_updates, [])

    async def test_svg_favicon_uses_native_svg_image(self):
        from unittest.mock import patch

        self.image_type = "image/svg+xml"
        self.image_data = b'<svg xmlns="http://www.w3.org/2000/svg"><circle r="8"/></svg>'
        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            await self.plugin.query(self.ctx, self._query())
            await self._finish_images()
        self.assertEqual(self.api.result_updates[0].icon.image_type, WoxImageType.SVG)
        self.assertEqual(self.api.result_updates[0].icon.image_data, self.image_data.decode())

    async def test_html_response_and_empty_image_keep_linkding(self):
        from unittest.mock import patch

        for index, (mime, data) in enumerate([("text/html", b"<html>Login</html>"), ("image/png", b"")]):
            with self.subTest(mime=mime, data=data):
                self.image_type, self.image_data = mime, data
                self.bookmarks[0]["favicon_url"] = f"https://linkding.example.com/static/invalid{index}"
                with patch("urllib.request.urlopen", side_effect=self._urlopen):
                    response = await self.plugin.query(self.ctx, self._query(str(index)))
                    await self._finish_images()
                self.assertEqual(response.results[0].icon.image_data, self.module.LINKDING_ICON_SVG)
        self.assertEqual(self.api.result_updates, [])

    async def test_selection_preview_updates_bookmark_icons_only(self):
        from unittest.mock import patch

        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            response = await query_selection_and_wait(self.plugin, self.api, self.ctx, self._query(selection=True))
            initial = WoxPreviewListData.from_json(json.loads(response.results[0].preview.preview_data))
            self.assertEqual(initial.items[0].icon.image_type, WoxImageType.SVG)
            await self._finish_images()
            update = self.api.result_updates[-1]
            self.assertEqual(update.id, "selection:bookmarks")
            self.assertIsNone(update.icon)
            preview = WoxPreviewListData.from_json(json.loads(update.preview.preview_data))
            self.assertEqual(preview.items[0].icon.image_type, WoxImageType.BASE64)
            self.assertEqual(preview.items[0].title, "Python")
            self.assertEqual(preview.items[0].tails[0]["Text"], "#dev")
            cached = await query_selection_and_wait(self.plugin, self.api, self.ctx, self._query(selection=True))
            cached_preview = WoxPreviewListData.from_json(json.loads(cached.results[0].preview.preview_data))
            self.assertEqual(cached_preview.items[0].icon.image_type, WoxImageType.BASE64)
            self.assertEqual(cached.results[0].icon.image_data, self.module.LINKDING_ICON_SVG)
            self.assertEqual(len(self.image_requests), 1)

    async def test_selection_icons_wait_for_initial_content_update(self):
        from unittest.mock import patch

        started, release, downloaded = asyncio.Event(), asyncio.Event(), asyncio.Event()
        loop = asyncio.get_running_loop()

        class DelayedUpdateAPI(MockPublicAPI):
            async def update_result(self, ctx, result):
                if result.sub_title is not None:
                    started.set()
                    await release.wait()
                return await super().update_result(ctx, result)

        api = DelayedUpdateAPI(self.api.settings)
        await self.plugin.init(self.ctx, PluginInitParams(api=api, plugin_directory=str(Path.cwd())))

        def urlopen(request, **kwargs):
            response = self._urlopen(request, **kwargs)
            if "/api/bookmarks/" not in request.full_url:
                loop.call_soon_threadsafe(downloaded.set)
            return response

        with patch("urllib.request.urlopen", side_effect=urlopen):
            try:
                await self.plugin.query(self.ctx, self._query(selection=True))
                await asyncio.wait_for(started.wait(), timeout=1)
                await asyncio.wait_for(downloaded.wait(), timeout=1)
                images = asyncio.create_task(self._finish_images())
                with self.assertRaises(asyncio.TimeoutError):
                    await asyncio.wait_for(asyncio.shield(images), timeout=0.05)
                self.assertEqual(api.result_updates, [])
            finally:
                release.set()
            await api.wait_for_result_update()
            await images
        self.assertEqual(len(api.result_updates), 2)
        self.assertIsNotNone(api.result_updates[0].sub_title)
        self.assertIsNone(api.result_updates[1].sub_title)
        preview = json.loads(api.result_updates[1].preview.preview_data)
        self.assertEqual(preview["items"][0]["icon"]["ImageType"], "base64")

    async def test_selection_settings_change_discards_pending_icon_update(self):
        from unittest.mock import patch

        self.image_gate.clear()
        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            try:
                await query_selection_and_wait(self.plugin, self.api, self.ctx, self._query(selection=True))
                await self.api.setting_changed_callbacks[0](self.ctx, "max_results", "5")
            finally:
                self.image_gate.set()
                await self._finish_images()
        self.assertEqual(len(self.api.result_updates), 1)

    async def test_duplicate_bookmark_icons_for_input_and_selection(self):
        from unittest.mock import patch

        for selection in (False, True):
            with self.subTest(selection=selection):
                self.bookmarks[0]["favicon_url"] = f"https://linkding.example.com/static/{selection}.png"
                with patch("urllib.request.urlopen", side_effect=self._urlopen):
                    response = await self.plugin.query(self.ctx, self._query("https://python.org", selection))
                    self.assertEqual(response.results[0].icon.image_type, WoxImageType.SVG)
                    await self._finish_images()
                self.assertEqual(self.api.result_updates[-1].id, "bookmark:1")
                self.assertEqual(self.api.result_updates[-1].icon.image_type, WoxImageType.BASE64)

    async def test_new_query_suppresses_old_update_and_shares_download(self):
        from unittest.mock import patch

        self.image_gate.clear()
        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            try:
                await self.plugin.query(self.ctx, self._query("first"))
                await self.plugin.query(self.ctx, self._query("second"))
            finally:
                self.image_gate.set()
                await self._finish_images()
        self.assertEqual(len(self.image_requests), 1)
        self.assertEqual(len(self.api.result_updates), 1)

    async def test_leaving_query_prevents_background_update(self):
        from unittest.mock import patch

        self.image_gate.clear()
        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            try:
                await self.plugin.query(self.ctx, self._query())
                await self.api.leave_plugin_query_callbacks[0](self.ctx)
            finally:
                self.image_gate.set()
                await self._finish_images()
        self.assertEqual(self.api.result_updates, [])

    async def test_settings_and_ttl_invalidate_favicon_cache(self):
        from unittest.mock import patch
        import time

        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            await self.plugin.query(self.ctx, self._query())
            await self._finish_images()
            for key, value in [("linkding_url", "https://other.example.com"), ("api_token", "new_token")]:
                await self.api.setting_changed_callbacks[0](self.ctx, key, value)
                response = await self.plugin.query(self.ctx, self._query())
                self.assertEqual(response.results[0].icon.image_type, WoxImageType.SVG)
                await self._finish_images()
            future = time.time() + 301
            with patch("time.time", return_value=future):
                response = await self.plugin.query(self.ctx, self._query())
                self.assertEqual(response.results[0].icon.image_type, WoxImageType.SVG)
                await self._finish_images()
        self.assertEqual(len(self.image_requests), 4)

    async def test_fast_download_retries_until_initial_result_is_visible(self):
        from unittest.mock import patch

        self.api.hidden_update_attempts = 1
        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            await self.plugin.query(self.ctx, self._query())
            await self._finish_images()
        self.assertEqual(len(self.api.result_updates), 1)
        self.assertEqual(len(self.image_requests), 1)

    async def test_settings_change_during_download_does_not_restore_old_cache(self):
        from unittest.mock import patch

        self.image_gate.clear()
        with patch("urllib.request.urlopen", side_effect=self._urlopen):
            try:
                await self.plugin.query(self.ctx, self._query())
                # Let the background download start before changing settings.
                while not self.image_requests:
                    await asyncio.sleep(0)
                await self.api.setting_changed_callbacks[0](self.ctx, "api_token", "replacement")
            finally:
                self.image_gate.set()
                await asyncio.gather(*tuple(self.plugin._favicon_refreshes), return_exceptions=True)
            self.assertEqual(self.api.result_updates, [])
            response = await self.plugin.query(self.ctx, self._query())
            self.assertEqual(response.results[0].icon.image_type, WoxImageType.SVG)
            await self._finish_images()
        self.assertEqual(len(self.image_requests), 2)


class TestBookmarkCreationAndDuplicateCheck(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

        self.mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "10",
        })
        self.ctx = Context()
        params = PluginInitParams(api=self.mock_api, plugin_directory=str(Path.cwd()))
        await self.plugin.init(self.ctx, params)

    def _make_query(self, search: str) -> Query:
        return Query(
            id="q_url",
            type=QueryType.INPUT,
            raw_query=f"ld {search}",
            selection=Selection(),
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search=search,
        )

    def test_parse_url_and_tags(self):
        # Plain URL
        url, tags = self.plugin._parse_url_and_tags("https://example.com")
        self.assertEqual(url, "https://example.com")
        self.assertEqual(tags, [])

        # URL with multiple space-separated #tags
        url, tags = self.plugin._parse_url_and_tags("https://example.com #tech #news")
        self.assertEqual(url, "https://example.com")
        self.assertEqual(tags, ["tech", "news"])

        # URL with fragment and deduplicated tags
        url, tags = self.plugin._parse_url_and_tags("https://example.com/docs#intro #python #python #dev")
        self.assertEqual(url, "https://example.com/docs#intro")
        self.assertEqual(tags, ["python", "dev"])

        # Unprefixed URLs: domains (https)
        url, tags = self.plugin._parse_url_and_tags("woxlauncher.com")
        self.assertEqual(url, "https://woxlauncher.com")
        self.assertEqual(tags, [])

        url, tags = self.plugin._parse_url_and_tags("woxlauncher.com #dev #tool")
        self.assertEqual(url, "https://woxlauncher.com")
        self.assertEqual(tags, ["dev", "tool"])

        url, tags = self.plugin._parse_url_and_tags("github.com/Wox-launcher/Wox")
        self.assertEqual(url, "https://github.com/Wox-launcher/Wox")
        self.assertEqual(tags, [])

        # Unprefixed URLs: localhost and 127.0.0.1 (http)
        url, tags = self.plugin._parse_url_and_tags("localhost:8080")
        self.assertEqual(url, "http://localhost:8080")
        self.assertEqual(tags, [])

        url, tags = self.plugin._parse_url_and_tags("localhost:8080/api #local")
        self.assertEqual(url, "http://localhost:8080/api")
        self.assertEqual(tags, ["local"])

        url, tags = self.plugin._parse_url_and_tags("127.0.0.1:8000")
        self.assertEqual(url, "http://127.0.0.1:8000")
        self.assertEqual(tags, [])

        # Unprefixed URLs: other IPv4 (https)
        url, tags = self.plugin._parse_url_and_tags("192.168.1.1:8080")
        self.assertEqual(url, "https://192.168.1.1:8080")
        self.assertEqual(tags, [])

        # Negative cases: plain text, single words, version numbers, or trailing non-tag words
        self.assertEqual(self.plugin._parse_url_and_tags("hello world"), ("", []))
        self.assertEqual(self.plugin._parse_url_and_tags("python sdk"), ("", []))
        self.assertEqual(self.plugin._parse_url_and_tags("wox"), ("", []))
        self.assertEqual(self.plugin._parse_url_and_tags("version 1.0.0"), ("", []))
        self.assertEqual(self.plugin._parse_url_and_tags("1.0.0"), ("", []))
        self.assertEqual(self.plugin._parse_url_and_tags("e.g."), ("", []))
        self.assertEqual(self.plugin._parse_url_and_tags("woxlauncher.com is great"), ("", []))
        self.assertEqual(self.plugin._parse_url_and_tags(""), ("", []))

    async def test_duplicate_check_unprefixed_url(self):
        from unittest.mock import MagicMock, patch

        check_data = {
            "bookmark": None,
            "metadata": {"title": "Wox Launcher"},
            "auto_tags": [],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(check_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
            response = await self.plugin.query(self.ctx, self._make_query("woxlauncher.com #tool"))

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:prompt_save_bookmark")
            self.assertEqual(res.sub_title, "https://woxlauncher.com · #tool")

            # Check normalized URL was queried in Linkding check API
            req = mock_urlopen.call_args[0][0]
            self.assertIn("/api/bookmarks/check/?url=https%3A%2F%2Fwoxlauncher.com", req.full_url)

    async def test_duplicate_check_already_bookmarked(self):
        from unittest.mock import MagicMock, patch

        check_data = {
            "bookmark": {
                "id": 10,
                "url": "https://example.com/existing",
                "title": "Existing Title",
                "website_title": "Web Title",
                "tag_names": ["tech", "saved"],
            },
            "metadata": {"title": "Web Title"},
            "auto_tags": [],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(check_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
            response = await self.plugin.query(self.ctx, self._make_query("https://example.com/existing"))

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "Existing Title")
            self.assertIn("https://example.com/existing", res.sub_title)
            self.assertTrue(
                "⚠️ Already bookmarked" in res.sub_title or "bookmark_already_exists" in res.sub_title,
                f"SubTitle should mention already bookmarked warning, got: {res.sub_title}",
            )
            self.assertIn("#tech #saved", res.sub_title)

            # Check actions
            self.assertEqual(len(res.actions), 3)
            self.assertEqual(res.actions[0].name, "i18n:action_open_url")
            self.assertTrue(res.actions[0].is_default)
            self.assertEqual(res.actions[1].name, "i18n:action_copy_url")
            self.assertEqual(res.actions[2].name, "i18n:action_open_in_linkding")

            # Check GET /api/bookmarks/check/?url=... call
            req = mock_urlopen.call_args[0][0]
            self.assertIn("/api/bookmarks/check/?url=https%3A%2F%2Fexample.com%2Fexisting", req.full_url)
            self.assertEqual(req.headers.get("Authorization"), "Token secret_token")

    async def test_duplicate_check_not_bookmarked_shows_save_prompt(self):
        from unittest.mock import MagicMock, patch

        check_data = {
            "bookmark": None,
            "metadata": {"title": "Some Scraped Title"},
            "auto_tags": [],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(check_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        with patch("urllib.request.urlopen", return_value=mock_http_response):
            response = await self.plugin.query(
                self.ctx, self._make_query("https://newsite.com/docs #reading #ai")
            )

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:prompt_save_bookmark")
            self.assertIn("https://newsite.com/docs", res.sub_title)
            self.assertIn("#reading #ai", res.sub_title)

            # Check actions
            self.assertTrue(len(res.actions) >= 1)
            save_action = res.actions[0]
            self.assertEqual(save_action.name, "i18n:action_save_bookmark")
            self.assertTrue(save_action.is_default)

    async def test_submit_new_bookmark_action_posts_payload_and_notifies(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        check_data = {
            "bookmark": None,
            "metadata": {},
            "auto_tags": [],
        }
        created_data = {
            "id": 99,
            "url": "https://newsite.com/docs",
            "tag_names": ["reading", "ai"],
        }

        mock_check_resp = MagicMock()
        mock_check_resp.read.return_value = json.dumps(check_data).encode("utf-8")
        mock_check_resp.__enter__.return_value = mock_check_resp

        mock_create_resp = MagicMock()
        mock_create_resp.read.return_value = json.dumps(created_data).encode("utf-8")
        mock_create_resp.__enter__.return_value = mock_create_resp

        with patch("urllib.request.urlopen", return_value=mock_check_resp):
            response = await self.plugin.query(
                self.ctx, self._make_query("https://newsite.com/docs #reading #ai")
            )

        res = response.results[0]
        save_action = res.actions[0]

        # Trigger save action
        with patch("urllib.request.urlopen", return_value=mock_create_resp) as mock_post_urlopen:
            await save_action.action(self.ctx, ActionContext())

            self.assertEqual(mock_post_urlopen.call_count, 1)
            post_req = mock_post_urlopen.call_args[0][0]
            self.assertEqual(post_req.full_url, "https://linkding.example.com/api/bookmarks/")
            self.assertEqual(post_req.get_method(), "POST")
            self.assertEqual(post_req.headers.get("Authorization"), "Token secret_token")
            self.assertEqual(post_req.headers.get("Content-type"), "application/json")

            post_body = json.loads(post_req.data.decode("utf-8"))
            self.assertEqual(post_body.get("url"), "https://newsite.com/docs")
            self.assertEqual(post_body.get("tag_names"), ["reading", "ai"])

            # Verify notification was triggered
            self.assertEqual(len(self.mock_api.notifications), 1)
            self.assertIn("https://newsite.com/docs", self.mock_api.notifications[0])

    async def test_saving_bookmark_refreshes_bookmarks_and_tags(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        saved = False

        def urlopen(request, **kwargs):
            nonlocal saved
            bookmark = {
                "id": 2 if saved else 1,
                "url": "https://example.com",
                "title": "New" if saved else "Old",
                "tag_names": ["github", "new" if saved else "old"],
            }
            if request.get_method() == "POST":
                saved = True
                data = {"id": 2}
            elif "/check/" in request.full_url:
                data = {"bookmark": None}
            elif "/api/tags/" in request.full_url:
                data = {"results": [{"name": "new" if saved else "old"}]}
            else:
                data = {"count": 1, "results": [bookmark]}
            response = MagicMock()
            response.read.return_value = json.dumps(data).encode("utf-8")
            response.__enter__.return_value = response
            return response

        with patch("urllib.request.urlopen", side_effect=urlopen):
            await self.plugin.query(self.ctx, self._make_query("#"))
            await self.plugin.query(self.ctx, self._make_query("example"))
            await self.plugin.query(self.ctx, self._make_query("#github #"))

            prompt = await self.plugin.query(self.ctx, self._make_query("https://example.com #new"))
            await prompt.results[0].actions[0].action(self.ctx, ActionContext())

            tags = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual([result.title for result in tags.results], ["#new"])
            bookmarks = await self.plugin.query(self.ctx, self._make_query("example"))
            self.assertEqual([result.title for result in bookmarks.results], ["New"])
            cooccurring = await self.plugin.query(self.ctx, self._make_query("#github #"))
            self.assertEqual([result.title for result in cooccurring.results], ["#new"])

    async def test_submit_new_bookmark_action_failure_notifies(self):
        from unittest.mock import patch
        from wox_plugin import ActionContext
        import urllib.error

        save_action = self.plugin._create_save_bookmark_action("https://error.com", ["tag"])
        http_error = urllib.error.HTTPError(
            url="https://linkding.example.com/api/bookmarks/",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None,
        )
        with patch("urllib.request.urlopen", side_effect=http_error):
            await save_action(self.ctx, ActionContext())
            self.assertEqual(len(self.mock_api.notifications), 1)
            self.assertTrue(
                "Failed to save bookmark" in self.mock_api.notifications[0]
                or "notify_bookmark_failed" in self.mock_api.notifications[0]
            )

    async def test_url_input_auth_and_network_errors(self):
        import urllib.error
        from unittest.mock import patch

        http_error = urllib.error.HTTPError(
            url="https://linkding.example.com/api/bookmarks/check/",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=None,
        )
        with patch("urllib.request.urlopen", side_effect=http_error):
            response = await self.plugin.query(self.ctx, self._make_query("https://example.com"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "i18n:error_auth_failed")

        url_error = urllib.error.URLError(reason="Connection refused")
        with patch("urllib.request.urlopen", side_effect=url_error):
            response = await self.plugin.query(self.ctx, self._make_query("https://example.com"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "i18n:error_network")


class TestTagBrowsingAndSearch(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

        self.mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "10",
        })
        self.ctx = Context()
        params = PluginInitParams(api=self.mock_api, plugin_directory=str(Path.cwd()))
        await self.plugin.init(self.ctx, params)

    def _make_query(self, search: str) -> Query:
        return Query(
            id="q_tag",
            type=QueryType.INPUT,
            raw_query=f"ld {search}",
            selection=Selection(),
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search=search,
        )

    async def test_tag_browsing_empty_prefix_returns_all_tags(self):
        from unittest.mock import MagicMock, patch

        tags_data = {
            "count": 3,
            "results": [
                {"id": 1, "name": "dev"},
                {"id": 2, "name": "python"},
                {"id": 3, "name": "ai"},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp) as mock_urlopen:
            response = await self.plugin.query(self.ctx, self._make_query("#"))

            self.assertEqual(len(response.results), 3)
            self.assertEqual(response.results[0].title, "#dev")
            self.assertEqual(response.results[1].title, "#python")
            self.assertEqual(response.results[2].title, "#ai")

            # Check that GET /api/tags/ was requested
            self.assertEqual(mock_urlopen.call_count, 1)
            req = mock_urlopen.call_args[0][0]
            self.assertEqual(req.full_url, "https://linkding.example.com/api/tags/")
            self.assertEqual(req.headers.get("Authorization"), "Token secret_token")

    async def test_tag_browsing_prefix_filtering(self):
        from unittest.mock import MagicMock, patch

        tags_data = {
            "count": 4,
            "results": [
                {"id": 1, "name": "dev"},
                {"id": 2, "name": "development"},
                {"id": 3, "name": "design"},
                {"id": 4, "name": "python"},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            # Query #dev filters to "dev" and "development"
            response = await self.plugin.query(self.ctx, self._make_query("#dev"))
            self.assertEqual(len(response.results), 2)
            self.assertEqual(response.results[0].title, "#dev")
            self.assertEqual(response.results[1].title, "#development")

            # Case-insensitive matching: #DEV
            response_upper = await self.plugin.query(self.ctx, self._make_query("#DEV"))
            self.assertEqual(len(response_upper.results), 2)
            self.assertEqual(response_upper.results[0].title, "#dev")
            self.assertEqual(response_upper.results[1].title, "#development")

    async def test_tag_browsing_placeholders(self):
        from unittest.mock import MagicMock, patch

        # Case 1: Empty tag list in Linkding
        empty_tags_data = {"count": 0, "results": []}
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(empty_tags_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "i18n:no_tags_found")

        # Reset cache for Case 2
        self.plugin._tag_cache = None
        self.plugin._tag_cache_time = 0.0

        # Case 2: Tags exist, but none match user prefix
        tags_data = {"count": 1, "results": [{"id": 1, "name": "python"}]}
        mock_http_resp2 = MagicMock()
        mock_http_resp2.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_http_resp2.__enter__.return_value = mock_http_resp2

        with patch("urllib.request.urlopen", return_value=mock_http_resp2):
            response2 = await self.plugin.query(self.ctx, self._make_query("#ruby"))
            self.assertEqual(len(response2.results), 1)
            self.assertEqual(response2.results[0].title, "i18n:no_matching_tags")
            self.assertIn("#ruby", response2.results[0].sub_title)

    async def test_tag_cache_ttl_and_lazy_refresh(self):
        import time
        from unittest.mock import MagicMock, patch

        tags_v1 = {"count": 1, "results": [{"id": 1, "name": "initial"}]}
        tags_v2 = {"count": 2, "results": [{"id": 1, "name": "initial"}, {"id": 2, "name": "refreshed"}]}

        mock_resp_v1 = MagicMock()
        mock_resp_v1.read.return_value = json.dumps(tags_v1).encode("utf-8")
        mock_resp_v1.__enter__.return_value = mock_resp_v1

        mock_resp_v2 = MagicMock()
        mock_resp_v2.read.return_value = json.dumps(tags_v2).encode("utf-8")
        mock_resp_v2.__enter__.return_value = mock_resp_v2

        start_time = 1000.0

        # Initial fetch at start_time
        with patch("time.time", return_value=start_time), \
             patch("urllib.request.urlopen", return_value=mock_resp_v1) as mock_urlopen:
            res1 = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(len(res1.results), 1)
            self.assertEqual(res1.results[0].title, "#initial")
            self.assertEqual(mock_urlopen.call_count, 1)

            # Query at start_time + 100s (within 300s TTL): uses cache, no new HTTP call
            with patch("time.time", return_value=start_time + 100.0):
                res2 = await self.plugin.query(self.ctx, self._make_query("#"))
                self.assertEqual(len(res2.results), 1)
                self.assertEqual(mock_urlopen.call_count, 1)

        # Query at start_time + 301s (TTL expired): lazy refresh makes HTTP call
        with patch("time.time", return_value=start_time + 301.0), \
             patch("urllib.request.urlopen", return_value=mock_resp_v2) as mock_urlopen_refresh:
            res3 = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(len(res3.results), 2)
            self.assertEqual(res3.results[1].title, "#refreshed")
            self.assertEqual(mock_urlopen_refresh.call_count, 1)

    async def test_tag_cache_invalidation_on_settings_change(self):
        from unittest.mock import MagicMock, patch

        tags_data = {"count": 1, "results": [{"id": 1, "name": "tag1"}]}
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
            await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(mock_urlopen.call_count, 1)

            callback = self.mock_api.setting_changed_callbacks[0]
            for key, value, expected_calls in (
                ("api_token", "new_token", 2),
                ("linkding_url", "https://other.example.com", 3),
                ("max_results", "20", 3),
            ):
                with self.subTest(key=key):
                    await callback(self.ctx, key, value)
                    response = await self.plugin.query(self.ctx, self._make_query("#"))
                    self.assertEqual([result.title for result in response.results], ["#tag1"])
                    self.assertEqual(mock_urlopen.call_count, expected_calls)

    async def test_cooccurring_tags_cache_expires_after_bookmark_search(self):
        from unittest.mock import MagicMock, patch

        responses = []
        for tag in ("python", "python", "refreshed"):
            response = MagicMock()
            response.read.return_value = json.dumps({
                "count": 1,
                "results": [{"id": 1, "url": "https://example.com", "tag_names": ["github", tag]}],
            }).encode("utf-8")
            response.__enter__.return_value = response
            responses.append(response)

        with patch("time.time", return_value=1000.0) as clock, \
             patch("urllib.request.urlopen", side_effect=responses) as http:
            await self.plugin.query(self.ctx, self._make_query("#github "))
            initial = await self.plugin.query(self.ctx, self._make_query("#github #"))
            self.assertEqual([result.title for result in initial.results], ["#python"])

            clock.return_value = 1029.0
            cached = await self.plugin.query(self.ctx, self._make_query("#github #py"))
            self.assertEqual([result.title for result in cached.results], ["#python"])
            self.assertEqual(http.call_count, 2)

            clock.return_value = 1031.0
            refreshed = await self.plugin.query(self.ctx, self._make_query("#github #"))
            self.assertEqual([result.title for result in refreshed.results], ["#refreshed"])
            self.assertEqual(http.call_count, 3)

    async def test_tag_selection_invokes_change_query(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        tags_data = {"count": 1, "results": [{"id": 1, "name": "dev"}]}
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#"))
            result = response.results[0]
            self.assertEqual(result.title, "#dev")
            self.assertTrue(len(result.actions) >= 1)

            action = result.actions[0]
            self.assertTrue(action.is_default)
            await action.action(self.ctx, ActionContext())

            self.assertEqual(len(self.mock_api.changed_queries), 1)
            change_param = self.mock_api.changed_queries[0]
            self.assertEqual(change_param.query_type, QueryType.INPUT)
            # Must update launcher input to "ld #<selected_tag> " with trailing space
            self.assertEqual(change_param.query_text, "ld #dev ")

    async def test_tag_trailing_space_triggers_bookmark_search(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {
            "count": 1,
            "results": [
                {
                    "id": 1,
                    "url": "https://dev.example.com",
                    "title": "Dev Site",
                    "tag_names": ["dev"],
                }
            ],
        }
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
            # ld #dev with trailing space
            response = await self.plugin.query(self.ctx, self._make_query("#dev "))

            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "Dev Site")

            self.assertEqual(mock_urlopen.call_count, 1)
            req = mock_urlopen.call_args[0][0]
            # Route to bookmark search using #<tag> as filter query: GET /api/bookmarks/?q=%23dev&limit=10
            self.assertIn("/api/bookmarks/?q=%23dev&limit=10", req.full_url)
            self.assertEqual(req.headers.get("Authorization"), "Token secret_token")

    async def test_tag_trailing_space_with_additional_query(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {"count": 0, "results": []}
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp

        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
            response = await self.plugin.query(self.ctx, self._make_query("#dev python"))

            self.assertEqual(mock_urlopen.call_count, 1)
            req = mock_urlopen.call_args[0][0]
            self.assertIn("/api/bookmarks/?q=%23dev%20python&limit=10", req.full_url)

    async def test_tag_browsing_error_handling(self):
        import urllib.error
        from unittest.mock import patch

        # 401 Unauthorized
        http_error = urllib.error.HTTPError(
            url="https://linkding.example.com/api/tags/",
            code=401,
            msg="Unauthorized",
            hdrs={},
            fp=None,
        )
        with patch("urllib.request.urlopen", side_effect=http_error):
            response = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "i18n:error_auth_failed")

        # Reset cache
        self.plugin._tag_cache = None
        self.plugin._tag_cache_time = 0.0

        # Timeout
        timeout_error = TimeoutError("timed out")
        with patch("urllib.request.urlopen", side_effect=timeout_error):
            response = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "i18n:error_timeout")

        # Reset cache
        self.plugin._tag_cache = None
        self.plugin._tag_cache_time = 0.0

        # Network error
        url_error = urllib.error.URLError(reason="Connection refused")
        with patch("urllib.request.urlopen", side_effect=url_error):
            response = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "i18n:error_network")

    async def test_tag_browsing_subtitle_empty_and_prevent_hide(self):
        from unittest.mock import MagicMock, patch

        tags_data = {
            "count": 1,
            "results": [{"id": 1, "name": "github"}],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertEqual(len(response.results), 1)
            result = response.results[0]
            self.assertEqual(result.title, "#github")
            # SubTitle must be empty string
            self.assertEqual(result.sub_title, "")
            # Action must have prevent_hide_after_action=True
            self.assertTrue(result.actions[0].prevent_hide_after_action)

    async def test_multi_tag_browsing_and_exclusion(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        bookmarks_data = {
            "count": 2,
            "results": [
                {"id": 1, "url": "https://a.com", "title": "A", "tag_names": ["github", "python"]},
                {"id": 2, "url": "https://b.com", "title": "B", "tag_names": ["github", "python", "ai"]},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            # User types "ld #github #" -> enters tag browsing, excluding "github"
            response = await self.plugin.query(self.ctx, self._make_query("#github #"))
            self.assertEqual(len(response.results), 2)
            self.assertEqual(response.results[0].title, "#python")
            self.assertEqual(response.results[1].title, "#ai")

            # Selecting python appends to existing "#github " prefix and adds trailing space
            action = response.results[0].actions[0]
            self.assertTrue(action.prevent_hide_after_action)
            await action.action(self.ctx, ActionContext())

            self.assertEqual(len(self.mock_api.changed_queries), 1)
            self.assertEqual(self.mock_api.changed_queries[0].query_text, "ld #github #python ")

    async def test_multi_tag_browsing_with_prefix(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        bookmarks_data = {
            "count": 2,
            "results": [
                {"id": 1, "url": "https://a.com", "title": "A", "tag_names": ["github", "python", "pytest"]},
                {"id": 2, "url": "https://b.com", "title": "B", "tag_names": ["github", "python", "ai"]},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            # User types "ld #github #py" -> enters tag browsing with prefix "py", excluding "github"
            response = await self.plugin.query(self.ctx, self._make_query("#github #py"))
            self.assertEqual(len(response.results), 2)
            self.assertEqual(response.results[0].title, "#python")
            self.assertEqual(response.results[1].title, "#pytest")

            action = response.results[0].actions[0]
            await action.action(self.ctx, ActionContext())

            self.assertEqual(len(self.mock_api.changed_queries), 1)
            self.assertEqual(self.mock_api.changed_queries[0].query_text, "ld #github #python ")

    async def test_toolbar_msg_lifecycle(self):
        from unittest.mock import MagicMock, patch

        tags_data = {
            "count": 2,
            "results": [
                {"id": 1, "name": "dev"},
                {"id": 2, "name": "design"},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        # 1. Tag browsing shows matching tags count
        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            await self.plugin.query(self.ctx, self._make_query("#"))
            self.assertTrue(len(self.mock_api.toolbar_messages) > 0)
            latest_msg = self.mock_api.toolbar_messages[-1]
            self.assertEqual(latest_msg.id, "linkding:status")
            self.assertEqual(latest_msg.title, "2 tags found")

        # 2. Bookmark search shows matching bookmarks count
        bookmarks_data = {
            "count": 42,
            "results": [{"id": 1, "url": "https://example.com", "title": "Example"}],
        }
        mock_bm_resp = MagicMock()
        mock_bm_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_bm_resp.__enter__.return_value = mock_bm_resp

        with patch("urllib.request.urlopen", return_value=mock_bm_resp):
            await self.plugin.query(self.ctx, self._make_query("example"))
            latest_msg = self.mock_api.toolbar_messages[-1]
            self.assertEqual(latest_msg.id, "linkding:status")
            self.assertEqual(latest_msg.title, "42 bookmarks found")

        # 3. Empty query clears toolbar msg
        await self.plugin.query(self.ctx, self._make_query(""))
        self.assertIn("linkding:status", self.mock_api.cleared_toolbar_msg_ids)

        # 4. On leaving plugin query clears toolbar msg
        self.mock_api.cleared_toolbar_msg_ids.clear()
        leave_callback = self.mock_api.leave_plugin_query_callbacks[0]
        await leave_callback(self.ctx)
        self.assertIn("linkding:status", self.mock_api.cleared_toolbar_msg_ids)

    async def test_cooccurring_tags_filtering_and_exclusion(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {
            "count": 2,
            "results": [
                {"id": 1, "url": "https://a.com", "title": "A", "tag_names": ["github", "python", "ai"]},
                {"id": 2, "url": "https://b.com", "title": "B", "tag_names": ["github", "python", "backend"]},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#github #"))
            self.assertEqual(len(response.results), 3)
            self.assertEqual(response.results[0].title, "#python")
            self.assertEqual(len(response.results[0].tails), 1)
            self.assertEqual(response.results[0].tails[0].text, "2")

            titles = [r.title for r in response.results]
            self.assertIn("#ai", titles)
            self.assertIn("#backend", titles)
            self.assertNotIn("#vue", titles)

    async def test_cooccurring_tags_with_typing_prefix(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {
            "count": 2,
            "results": [
                {"id": 1, "url": "https://a.com", "title": "A", "tag_names": ["github", "python", "pytest"]},
                {"id": 2, "url": "https://b.com", "title": "B", "tag_names": ["github", "python", "ai"]},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#github #py"))
            self.assertEqual(len(response.results), 2)
            self.assertEqual(response.results[0].title, "#python")
            self.assertEqual(response.results[1].title, "#pytest")

    async def test_cooccurring_tags_include_bookmarks_beyond_display_limit(self):
        from unittest.mock import MagicMock, patch

        bookmarks = [
            {"id": i, "url": f"https://example.com/{i}", "tag_names": ["github", "python"]}
            for i in range(10)
        ]
        bookmarks.append({"id": 10, "url": "https://example.com/10", "tag_names": ["github", "rare"]})
        responses = []
        for items in (bookmarks[:10], bookmarks):
            response = MagicMock()
            response.read.return_value = json.dumps({"count": 11, "results": items}).encode("utf-8")
            response.__enter__.return_value = response
            responses.append(response)

        with patch("urllib.request.urlopen", side_effect=responses) as mock_urlopen:
            await self.plugin.query(self.ctx, self._make_query("#github "))

            res = await self.plugin.query(self.ctx, self._make_query("#github #"))
            self.assertEqual([result.title for result in res.results], ["#python", "#rare"])
            self.assertEqual([result.tails[0].text for result in res.results], ["10", "1"])
            self.assertIn("limit=100", mock_urlopen.call_args[0][0].full_url)

    async def test_bookmark_and_tag_queries_share_responses_only_at_same_limit(self):
        from unittest.mock import MagicMock, patch
        from urllib.parse import parse_qs, urlsplit

        bookmarks = [
            {"id": index, "url": f"https://example.com/{index}", "tag_names": ["github", "python"]}
            for index in range(10)
        ]
        bookmarks.append({"id": 10, "url": "https://example.com/10", "tag_names": ["github", "rare"]})

        def urlopen(request, **kwargs):
            limit = int(parse_qs(urlsplit(request.full_url).query)["limit"][0])
            response = MagicMock()
            response.read.return_value = json.dumps({"count": 11, "results": bookmarks[:limit]}).encode("utf-8")
            response.__enter__.return_value = response
            return response

        for limit, expected_count, expected_requests in ((10, 10, 2), (100, 11, 1)):
            with self.subTest(limit=limit):
                await self.mock_api.setting_changed_callbacks[0](self.ctx, "max_results", str(limit))
                with patch("urllib.request.urlopen", side_effect=urlopen) as http:
                    tags = await self.plugin.query(self.ctx, self._make_query("#github #"))
                    self.assertEqual([result.title for result in tags.results], ["#python", "#rare"])
                    flat = await self.plugin.query(self.ctx, self._make_query("#github "))
                    self.assertEqual(len(flat.results), expected_count)
                    self.assertEqual(http.call_count, expected_requests)

    async def test_cooccurring_tags_empty_when_no_bookmarks(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {"count": 0, "results": []}
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#nonexistent #"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].title, "i18n:no_matching_tags")
            self.assertEqual(self.mock_api.toolbar_messages[-1].title, "0 tags found")



class TestSelectionQuery(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

        self.mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "10",
        })
        self.ctx = Context()
        params = PluginInitParams(api=self.mock_api, plugin_directory=str(Path.cwd()))
        await self.plugin.init(self.ctx, params)

    def _make_selection_query(self, selection: Selection, trigger_keyword: str = "") -> Query:
        return Query(
            id="q_sel",
            type=QueryType.SELECTION,
            raw_query="",
            selection=selection,
            env=QueryEnv(),
            trigger_keyword=trigger_keyword,
            command="",
            search="",
        )

    async def test_selection_entry_appears_before_network_and_updates_in_place(self):
        import threading
        from unittest.mock import MagicMock, patch

        gate = threading.Event()
        started = asyncio.Event()
        loop = asyncio.get_running_loop()

        def urlopen(request, **kwargs):
            loop.call_soon_threadsafe(started.set)
            gate.wait(timeout=2)
            response = MagicMock()
            response.__enter__.return_value = response
            response.read.return_value = json.dumps({
                "count": 1, "results": [{"id": 7, "url": "https://example.com", "title": "Example"}]
            }).encode()
            return response

        with patch("urllib.request.urlopen", side_effect=urlopen) as http:
            try:
                self.mock_api.setting_reads.clear()
                response = await asyncio.wait_for(self.plugin.query(
                    self.ctx, self._make_selection_query(Selection(type=SelectionType.TEXT, text="Example"))
                ), timeout=0.5)
                entry = response.results[0]
                self.assertEqual(entry.id, "selection:bookmarks")
                self.assertEqual(entry.title, "i18n:selection_entry_title")
                self.assertEqual(entry.sub_title, "i18n:selection_searching")
                self.assertEqual(self.mock_api.setting_reads, [])
                await asyncio.wait_for(started.wait(), timeout=1)
                self.assertEqual(self.mock_api.result_updates, [])
            finally:
                gate.set()
            update = await self.mock_api.wait_for_result_update()
            self.assertEqual(update.id, entry.id)
            self.assertIsNone(update.title)
            self.assertEqual(len(json.loads(update.preview.preview_data)["items"]), 1)
            self.assertEqual(http.call_count, 1)

    async def test_loading_entry_enter_reuses_pending_request(self):
        import threading
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        gate = threading.Event()
        started = asyncio.Event()
        loop = asyncio.get_running_loop()
        self.mock_api.settings["TriggerKeywords"] = '["bookmarks"]'

        def urlopen(request, **kwargs):
            loop.call_soon_threadsafe(started.set)
            gate.wait(timeout=2)
            response = MagicMock()
            response.__enter__.return_value = response
            response.read.return_value = json.dumps({
                "count": 1, "results": [{"id": 7, "url": "https://example.com", "title": "Example"}]
            }).encode()
            return response

        with patch("urllib.request.urlopen", side_effect=urlopen) as http:
            try:
                response = await self.plugin.query(
                    self.ctx, self._make_selection_query(Selection(type=SelectionType.TEXT, text="Example"))
                )
                await asyncio.wait_for(started.wait(), timeout=1)
                action = response.results[0].actions[0]
                self.assertTrue(action.prevent_hide_after_action)
                expand = asyncio.create_task(action.action(self.ctx, ActionContext()))
                await asyncio.sleep(0)
                self.assertFalse(expand.done())
                self.assertEqual(self.mock_api.changed_queries, [])
            finally:
                gate.set()
            await asyncio.wait_for(expand, timeout=1)
            self.assertEqual(self.mock_api.changed_queries[0].query_text, "bookmarks Example")
            expanded = await self.plugin.query(self.ctx, Query(
                id="expanded", type=QueryType.INPUT, raw_query="bookmarks Example", search="Example",
                selection=None, env=QueryEnv(), trigger_keyword="bookmarks", command="",
            ))
            self.assertEqual(expanded.results[0].id, "bookmark:7")
            self.assertEqual(http.call_count, 1)

    async def test_new_selection_cancels_old_update_and_pending_expansion(self):
        import threading
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        gate = threading.Event()
        started, finished = asyncio.Event(), asyncio.Event()
        loop = asyncio.get_running_loop()

        def urlopen(request, **kwargs):
            old = "q=old" in request.full_url
            if old:
                loop.call_soon_threadsafe(started.set)
                gate.wait(timeout=2)
            response = MagicMock()
            response.__enter__.return_value = response
            response.read.return_value = json.dumps({
                "count": 1, "results": [{"id": 1, "url": "https://example.com", "title": "old" if old else "new"}]
            }).encode()
            if old:
                loop.call_soon_threadsafe(finished.set)
            return response

        with patch("urllib.request.urlopen", side_effect=urlopen):
            try:
                old = await self.plugin.query(
                    self.ctx, self._make_selection_query(Selection(type=SelectionType.TEXT, text="old"))
                )
                await asyncio.wait_for(started.wait(), timeout=1)
                expand = asyncio.create_task(old.results[0].actions[0].action(self.ctx, ActionContext()))
                await asyncio.sleep(0)
                new = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx,
                    self._make_selection_query(Selection(type=SelectionType.TEXT, text="new")))
                await asyncio.wait_for(expand, timeout=1)
            finally:
                gate.set()
            await asyncio.wait_for(finished.wait(), timeout=1)
            self.assertEqual(self.mock_api.changed_queries, [])
            updates = [update for update in self.mock_api.result_updates if update.sub_title is not None]
            self.assertEqual(len(updates), 1)
            self.assertEqual(new.results[0].id, old.results[0].id)
            self.assertEqual(json.loads(updates[0].preview.preview_data)["items"][0]["title"], "new")

    async def test_leaving_or_settings_change_discards_pending_selection(self):
        import threading
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        for key, value in [
            ("leave", ""), ("linkding_url", "https://other.example.com"),
            ("api_token", "replacement"), ("max_results", "5"),
        ]:
            with self.subTest(change=key):
                search_text = f"Example {key}"
                gate = threading.Event()
                started, finished = asyncio.Event(), asyncio.Event()
                loop = asyncio.get_running_loop()
                requests = []
                since = len(self.mock_api.result_updates)

                def urlopen(request, **kwargs):
                    requests.append(request)
                    old = len(requests) == 1
                    if old:
                        loop.call_soon_threadsafe(started.set)
                        gate.wait(timeout=2)
                    response = MagicMock()
                    response.__enter__.return_value = response
                    response.read.return_value = json.dumps({
                        "count": 1, "results": [{"id": 1 if old else 2, "url": "https://example.com"}]
                    }).encode()
                    if old:
                        loop.call_soon_threadsafe(finished.set)
                    return response

                with patch("urllib.request.urlopen", side_effect=urlopen):
                    try:
                        response = await self.plugin.query(self.ctx, self._make_selection_query(
                            Selection(type=SelectionType.TEXT, text=search_text)))
                        await asyncio.wait_for(started.wait(), timeout=1)
                        expand = asyncio.create_task(response.results[0].actions[0].action(self.ctx, ActionContext()))
                        await asyncio.sleep(0)
                        if key == "leave":
                            await self.mock_api.leave_plugin_query_callbacks[0](self.ctx)
                        else:
                            await self.mock_api.setting_changed_callbacks[0](self.ctx, key, value)
                    finally:
                        gate.set()
                    await asyncio.wait_for(expand, timeout=1)
                    await asyncio.wait_for(finished.wait(), timeout=1)
                    fresh = await self.plugin.query(self.ctx, Query(
                        id="input", type=QueryType.INPUT, raw_query=f"ld {search_text}", search=search_text,
                        selection=None, env=QueryEnv(), trigger_keyword="ld", command="",
                    ))
                self.assertEqual(self.mock_api.result_updates[since:], [])
                self.assertEqual(self.mock_api.changed_queries, [])
                self.assertEqual(fresh.results[0].id, "bookmark:2")
                self.assertEqual(len(requests), 2)

    async def test_selection_update_retries_until_entry_is_visible(self):
        from unittest.mock import MagicMock, patch

        self.mock_api.hidden_update_attempts = 1
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"count": 0, "results": []}'
        with patch("urllib.request.urlopen", return_value=response):
            result = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx,
                self._make_selection_query(Selection(type=SelectionType.TEXT, text="Example")))
        self.assertEqual(result.results[0].sub_title, "i18n:selection_press_enter_to_edit")
        self.assertEqual(len(self.mock_api.result_updates), 1)

    async def test_pending_expansion_does_not_reopen_a_departed_host_query(self):
        import threading
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        for hidden in (False, True):
            with self.subTest(hidden=hidden):
                search_text = f"Example {hidden}"
                gate = threading.Event()
                started = asyncio.Event()
                loop = asyncio.get_running_loop()
                self.mock_api.visible = True
                self.mock_api.accept_updates = True

                def urlopen(request, **kwargs):
                    loop.call_soon_threadsafe(started.set)
                    gate.wait(timeout=2)
                    response = MagicMock()
                    response.__enter__.return_value = response
                    response.read.return_value = b'{"count": 0, "results": []}'
                    return response

                with patch("urllib.request.urlopen", side_effect=urlopen):
                    try:
                        response = await self.plugin.query(self.ctx, self._make_selection_query(
                            Selection(type=SelectionType.TEXT, text=search_text)))
                        await asyncio.wait_for(started.wait(), timeout=1)
                        expand = asyncio.create_task(response.results[0].actions[0].action(self.ctx, ActionContext()))
                        await asyncio.sleep(0)
                        # Global selection queries may not get a plugin-leave callback.
                        self.mock_api.visible = not hidden
                        self.mock_api.accept_updates = hidden
                    finally:
                        gate.set()
                    await asyncio.wait_for(expand, timeout=1)
                self.assertEqual(self.mock_api.changed_queries, [])

    async def test_new_query_during_visibility_check_cancels_pending_expansion(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        started, release = asyncio.Event(), asyncio.Event()

        class DelayedVisibilityAPI(MockPublicAPI):
            async def is_visible(self, ctx):
                started.set()
                await release.wait()
                return True

        api = DelayedVisibilityAPI(self.mock_api.settings)
        await self.plugin.init(self.ctx, PluginInitParams(api=api, plugin_directory=str(Path.cwd())))
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b'{"count": 0, "results": []}'
        with patch("urllib.request.urlopen", return_value=response):
            try:
                loading = await self.plugin.query(self.ctx, self._make_selection_query(
                    Selection(type=SelectionType.TEXT, text="Example")))
                expand = asyncio.create_task(loading.results[0].actions[0].action(self.ctx, ActionContext()))
                await asyncio.wait_for(started.wait(), timeout=1)
                await self.plugin.query(self.ctx, Query(
                    id="new", type=QueryType.INPUT, raw_query="ld ", search="",
                    selection=None, env=QueryEnv(), trigger_keyword="ld", command="",
                ))
            finally:
                release.set()
            await asyncio.wait_for(expand, timeout=1)
        self.assertEqual(api.changed_queries, [])

    async def test_selection_errors_update_the_existing_entry(self):
        import urllib.error
        from unittest.mock import patch

        errors = [
            (urllib.error.HTTPError("https://example.com", 401, "Unauthorized", {}, None), "i18n:error_auth_failed"),
            (urllib.error.HTTPError("https://example.com", 500, "Server Error", {}, None), "i18n:selection_search_failed"),
            (urllib.error.URLError("offline"), "i18n:error_network"),
            (TimeoutError("timed out"), "i18n:error_timeout"),
        ]
        for error, subtitle in errors:
            with self.subTest(error=subtitle), patch("urllib.request.urlopen", side_effect=error):
                response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx,
                    self._make_selection_query(Selection(type=SelectionType.TEXT, text="Example")))
                entry = response.results[0]
                self.assertEqual(entry.id, "selection:bookmarks")
                self.assertEqual(entry.title, "i18n:selection_entry_title")
                self.assertEqual(entry.sub_title, subtitle)
                self.assertEqual(entry.actions, [])
                self.assertTrue(all(update.title is None for update in self.mock_api.result_updates))

    async def test_selection_query_plain_text_search_aggregated(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        mock_response_data = {
            "count": 2,
            "results": [
                {
                    "id": 1,
                    "url": "https://woxlauncher.com",
                    "title": "Wox Launcher",
                    "website_title": "Wox Launcher Official",
                    "tag_names": ["launcher", "python"],
                },
                {
                    "id": 2,
                    "url": "https://github.com/Wox-launcher/Wox",
                    "title": "Wox GitHub",
                    "website_title": "GitHub Repo",
                    "tag_names": ["oss"],
                },
            ],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        selection = Selection(type=SelectionType.TEXT, text="Wox launcher")
        query = self._make_selection_query(selection)

        with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
            response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, query)

            # 1. Consolidated single aggregation item
            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:selection_entry_title")
            self.assertEqual(res.sub_title, "2 bookmarks found · Press Enter to select a bookmark")

            # 2. Split layout ratio 0.6
            self.assertIsNotNone(response.layout)
            self.assertEqual(response.layout.result_preview_width_ratio, 0.6)

            # 3. Native List preview with tags in tails
            self.assertEqual(res.preview.preview_type, WoxPreviewType.LIST)
            preview_dict = json.loads(res.preview.preview_data)
            items = preview_dict.get("items", [])
            self.assertEqual(len(items), 2)
            self.assertEqual(items[0]["title"], "Wox Launcher")
            self.assertEqual(items[0]["subtitle"], "https://woxlauncher.com")
            first_item_tails = [t["Text"] for t in items[0].get("tails", [])]
            self.assertIn("#launcher", first_item_tails)
            self.assertIn("#python", first_item_tails)

            # 4. Enter expands the query and keeps Wox visible
            self.assertEqual(len(res.actions), 2)
            expand_action = res.actions[0]
            self.assertEqual(expand_action.name, "i18n:selection_action_expand")
            self.assertTrue(expand_action.is_default)
            self.assertTrue(expand_action.prevent_hide_after_action)
            await expand_action.action(self.ctx, ActionContext())
            self.assertEqual(len(self.mock_api.changed_queries), 1)
            cq = self.mock_api.changed_queries[0]
            self.assertEqual(cq.query_type, QueryType.INPUT)
            self.assertEqual(cq.query_text, "ld Wox launcher")

            # 5. Web search is the only secondary action
            web_search_action = res.actions[1]
            self.assertEqual(web_search_action.name, "i18n:action_open_in_linkding")
            self.assertFalse(web_search_action.is_default)
            with patch("webbrowser.open") as mock_browser_open:
                await web_search_action.action(self.ctx, ActionContext())
            mock_browser_open.assert_called_once_with(
                "https://linkding.example.com/bookmarks?q=Wox%20launcher"
            )

            req = mock_urlopen.call_args[0][0]
            self.assertIn("/api/bookmarks/?q=Wox%20launcher&limit=10", req.full_url)

    async def test_selection_query_no_bookmarks_found_guidance(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        mock_response_data = {"count": 0, "results": []}
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        selection = Selection(type=SelectionType.TEXT, text="NonExistentTopic")
        query = self._make_selection_query(selection)

        with patch("urllib.request.urlopen", return_value=mock_http_response):
            response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, query)

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:selection_entry_title")
            self.assertEqual(res.sub_title, "i18n:selection_press_enter_to_edit")

            # Split layout ratio 0.6 and List preview
            self.assertIsNotNone(response.layout)
            self.assertEqual(response.layout.result_preview_width_ratio, 0.6)
            self.assertEqual(res.preview.preview_type, WoxPreviewType.LIST)

            preview_items = json.loads(res.preview.preview_data)["items"]
            self.assertEqual(preview_items[0]["subtitle"], "i18n:selection_press_enter_to_edit")

            # Enter opens an editable query even without matches
            self.assertEqual(len(res.actions), 2)
            self.assertEqual(res.actions[0].name, "i18n:selection_action_expand")
            self.assertTrue(res.actions[0].is_default)
            self.assertTrue(res.actions[0].prevent_hide_after_action)
            await res.actions[0].action(self.ctx, ActionContext())
            self.assertEqual(len(self.mock_api.changed_queries), 1)
            self.assertEqual(self.mock_api.changed_queries[0].query_type, QueryType.INPUT)
            self.assertEqual(self.mock_api.changed_queries[0].query_text, "ld NonExistentTopic")
            self.assertEqual(res.actions[1].name, "i18n:action_open_in_linkding")
            self.assertFalse(res.actions[1].is_default)
            with patch("webbrowser.open") as mock_browser_open:
                await res.actions[1].action(self.ctx, ActionContext())
            mock_browser_open.assert_called_once_with(
                "https://linkding.example.com/bookmarks?q=NonExistentTopic"
            )

    async def test_selection_query_single_match_expands_before_bookmark_actions(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps({
            "count": 1,
            "results": [{
                "id": 7,
                "url": "https://example.com/wox",
                "title": "Wox guide",
                "tag_names": ["guide"],
            }],
        }).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response
        self.mock_api.settings["TriggerKeywords"] = '["bookmarks"]'
        query = self._make_selection_query(Selection(type=SelectionType.TEXT, text="Wox guide"))

        with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
            response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, query)
            self.assertEqual(len(response.results), 1)
            entry = response.results[0]
            self.assertEqual(entry.id, "selection:bookmarks")
            self.assertEqual(entry.sub_title, "1 bookmarks found · Press Enter to select a bookmark")
            self.assertEqual([action.name for action in entry.actions], [
                "i18n:selection_action_expand", "i18n:action_open_in_linkding"
            ])
            self.assertTrue(entry.actions[0].is_default)
            self.assertTrue(entry.actions[0].prevent_hide_after_action)
            with patch("webbrowser.open") as mock_browser_open:
                await entry.actions[0].action(self.ctx, ActionContext())
            mock_browser_open.assert_not_called()
            changed_query = self.mock_api.changed_queries[0]
            self.assertEqual(changed_query.query_type, QueryType.INPUT)
            self.assertEqual(changed_query.query_text, "bookmarks Wox guide")

            expanded_query = Query(
                id="q_expanded",
                type=changed_query.query_type,
                raw_query=changed_query.query_text,
                selection=None,
                env=QueryEnv(),
                trigger_keyword="bookmarks",
                command="",
                search="Wox guide",
            )
            expanded_response = await self.plugin.query(self.ctx, expanded_query)
            self.assertEqual(mock_urlopen.call_count, 1, "Expansion must reuse the selection response")
            self.assertEqual(len(expanded_response.results), 1)
            self.assertIsNone(expanded_response.layout.result_preview_width_ratio)
            bookmark = expanded_response.results[0]
            self.assertEqual(bookmark.id, "bookmark:7")
            self.assertEqual(bookmark.actions[0].name, "i18n:action_open_url")
            self.assertTrue(bookmark.actions[0].is_default)
            with patch("webbrowser.open") as mock_browser_open:
                await bookmark.actions[0].action(self.ctx, ActionContext())
            mock_browser_open.assert_called_once_with("https://example.com/wox")
            await bookmark.actions[1].action(self.ctx, ActionContext())
            self.assertEqual(self.mock_api.copied_params[0].text, "https://example.com/wox")

    async def test_selection_query_resolves_configured_keyword_before_expansion(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        for match_count in (0, 2):
            with self.subTest(match_count=match_count):
                search_text = f"Wox guide {match_count}"
                self.mock_api.changed_queries.clear()
                self.mock_api.setting_reads.clear()
                self.mock_api.settings["TriggerKeywords"] = '["*", "bookmarks", "bm"]'
                mock_http_response = MagicMock()
                mock_http_response.read.return_value = json.dumps({
                    "count": match_count,
                    "results": [
                        {"id": index, "url": f"https://example.com/{index}", "title": "Wox guide"}
                        for index in range(match_count)
                    ],
                }).encode("utf-8")
                mock_http_response.__enter__.return_value = mock_http_response
                query = self._make_selection_query(Selection(type=SelectionType.TEXT, text=search_text))

                with patch("urllib.request.urlopen", return_value=mock_http_response):
                    response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, query)
                self.assertEqual(len(response.results), 1)
                self.assertEqual(self.mock_api.setting_reads, ["TriggerKeywords"])
                # Enter uses the resolved configuration without another host read.
                self.mock_api.settings["TriggerKeywords"] = '["bm"]'
                action = response.results[0].actions[0]
                self.assertTrue(action.is_default)
                self.assertTrue(action.prevent_hide_after_action)
                await action.action(self.ctx, ActionContext())
                self.assertEqual(self.mock_api.setting_reads, ["TriggerKeywords"])
                self.assertEqual(len(self.mock_api.changed_queries), 1)
                self.assertEqual(self.mock_api.changed_queries[0].query_type, QueryType.INPUT)
                self.assertEqual(self.mock_api.changed_queries[0].query_text, f"bookmarks {search_text}")

                # The next aggregation query picks up configuration changes.
                with patch("urllib.request.urlopen", return_value=mock_http_response):
                    response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, query)
                await response.results[0].actions[0].action(self.ctx, ActionContext())
                self.assertEqual(self.mock_api.changed_queries[-1].query_text, f"bm {search_text}")
                self.assertEqual(self.mock_api.setting_reads, ["TriggerKeywords", "TriggerKeywords"])

    async def test_selection_query_expansion_reuses_empty_and_multiple_matches(self):
        from unittest.mock import MagicMock, patch
        from wox_plugin import ActionContext

        for match_count in (0, 2):
            with self.subTest(match_count=match_count):
                search_text = f"Wox guide {match_count}"
                mock_http_response = MagicMock()
                mock_http_response.read.return_value = json.dumps({
                    "count": match_count,
                    "results": [
                        {"id": index, "url": f"https://example.com/{index}", "title": "Wox guide"}
                        for index in range(match_count)
                    ],
                }).encode("utf-8")
                mock_http_response.__enter__.return_value = mock_http_response
                selection_query = self._make_selection_query(
                    Selection(type=SelectionType.TEXT, text=f" {search_text} ")
                )
                with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
                    response = await self.plugin.query(self.ctx, selection_query)
                    await response.results[0].actions[0].action(self.ctx, ActionContext())
                    changed_query = self.mock_api.changed_queries[-1]
                    expanded_query = Query(
                        id="q_expanded",
                        type=changed_query.query_type,
                        raw_query=changed_query.query_text,
                        selection=None,
                        env=QueryEnv(),
                        trigger_keyword="ld",
                        command="",
                        search=search_text,
                    )
                    expanded = await self.plugin.query(self.ctx, expanded_query)
                    expected_ids = ["bookmark:0", "bookmark:1"] if match_count else ["bookmark:empty"]
                    self.assertEqual([result.id for result in expanded.results], expected_ids)
                    self.assertEqual(mock_urlopen.call_count, 1)

                    expanded_query.search = "different keyword"
                    expanded_query.raw_query = "ld different keyword"
                    await self.plugin.query(self.ctx, expanded_query)
                    self.assertEqual(mock_urlopen.call_count, 2)

                    # Changing credentials invalidates the response seeded by selection.
                    await self.mock_api.setting_changed_callbacks[0](self.ctx, "api_token", "new_token")
                    expanded_query.search = search_text
                    expanded_query.raw_query = changed_query.query_text
                    await self.plugin.query(self.ctx, expanded_query)
                    self.assertEqual(mock_urlopen.call_count, 3)

    async def test_selection_query_unprefixed_url(self):
        from unittest.mock import MagicMock, patch

        check_data = {
            "bookmark": None,
            "metadata": {"title": "Wox Launcher"},
            "auto_tags": [],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(check_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        selection = Selection(type=SelectionType.TEXT, text="woxlauncher.com")
        query = self._make_selection_query(selection)

        with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
            response = await self.plugin.query(self.ctx, query)

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:prompt_save_bookmark")
            self.assertEqual(res.sub_title, "https://woxlauncher.com")

            # Split layout 0.6 and Markdown preview
            self.assertIsNotNone(response.layout)
            self.assertEqual(response.layout.result_preview_width_ratio, 0.6)
            self.assertEqual(res.preview.preview_type, WoxPreviewType.MARKDOWN)
            self.assertIn("### 🔖 保存书签至 Linkding", res.preview.preview_data)
            self.assertIn("https://woxlauncher.com", res.preview.preview_data)

            req = mock_urlopen.call_args[0][0]
            self.assertIn("/api/bookmarks/check/?url=https%3A%2F%2Fwoxlauncher.com", req.full_url)

    async def test_selection_query_prefixed_url_with_tags(self):
        from unittest.mock import MagicMock, patch

        check_data = {
            "bookmark": None,
            "metadata": {"title": "Example Doc"},
            "auto_tags": [],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(check_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        selection = Selection(type=SelectionType.TEXT, text="https://example.com/docs #docs #dev")
        query = self._make_selection_query(selection)

        with patch("urllib.request.urlopen", return_value=mock_http_response) as mock_urlopen:
            response = await self.plugin.query(self.ctx, query)

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "i18n:prompt_save_bookmark")
            self.assertEqual(res.sub_title, "https://example.com/docs · #docs #dev")

            # Split layout 0.6 and Markdown preview with tags
            self.assertIsNotNone(response.layout)
            self.assertEqual(response.layout.result_preview_width_ratio, 0.6)
            self.assertEqual(res.preview.preview_type, WoxPreviewType.MARKDOWN)
            self.assertIn("#docs", res.preview.preview_data)
            self.assertIn("#dev", res.preview.preview_data)

            req = mock_urlopen.call_args[0][0]
            self.assertIn("/api/bookmarks/check/?url=https%3A%2F%2Fexample.com%2Fdocs", req.full_url)

    async def test_selection_query_existing_url(self):
        from unittest.mock import MagicMock, patch

        check_data = {
            "bookmark": {
                "id": 10,
                "url": "https://example.com/existing",
                "title": "Existing Doc",
                "tag_names": ["fav", "tools"],
            }
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(check_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        selection = Selection(type=SelectionType.TEXT, text="https://example.com/existing")
        query = self._make_selection_query(selection)

        with patch("urllib.request.urlopen", return_value=mock_http_response):
            response = await self.plugin.query(self.ctx, query)

            self.assertEqual(len(response.results), 1)
            res = response.results[0]
            self.assertEqual(res.title, "Existing Doc")

            # Split layout 0.6 and Markdown preview for duplicate bookmark
            self.assertIsNotNone(response.layout)
            self.assertEqual(response.layout.result_preview_width_ratio, 0.6)
            self.assertEqual(res.preview.preview_type, WoxPreviewType.MARKDOWN)
            self.assertIn("### ⚠️ 该 URL 已收藏", res.preview.preview_data)
            self.assertIn("Existing Doc", res.preview.preview_data)
            self.assertIn("#fav", res.preview.preview_data)

    async def test_selection_query_non_text_or_empty(self):
        # Empty text selection
        query_empty = self._make_selection_query(Selection(type=SelectionType.TEXT, text="   "))
        response = await self.plugin.query(self.ctx, query_empty)
        self.assertEqual(len(response.results), 1)
        self.assertEqual(response.results[0].title, "i18n:prompt_empty_search")
        self.assertIsNotNone(response.layout)
        self.assertEqual(response.layout.result_preview_width_ratio, 0.6)

        # File selection
        query_file = self._make_selection_query(Selection(type=SelectionType.FILE, file_paths=["C:\\file.txt"]))
        response_file = await self.plugin.query(self.ctx, query_file)
        self.assertEqual(len(response_file.results), 1)
        self.assertEqual(response_file.results[0].title, "i18n:prompt_empty_search")
        self.assertIsNotNone(response_file.layout)
        self.assertEqual(response_file.layout.result_preview_width_ratio, 0.6)

    async def test_regular_input_query_maintains_flat_and_no_preview_ratio(self):
        from unittest.mock import MagicMock, patch

        mock_response_data = {
            "count": 2,
            "results": [
                {"id": 1, "url": "https://wox1.com", "title": "Wox 1", "tag_names": []},
                {"id": 2, "url": "https://wox2.com", "title": "Wox 2", "tag_names": []},
            ],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        input_query = Query(
            id="q_input",
            type=QueryType.INPUT,
            raw_query="ld wox",
            selection=None,
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="wox",
        )

        with patch("urllib.request.urlopen", return_value=mock_http_response):
            response = await self.plugin.query(self.ctx, input_query)
            # Regular input returns multiple flat results
            self.assertEqual(len(response.results), 2)
            # Layout ratio should NOT be set (None or no layout)
            if response.layout is not None:
                self.assertIsNone(response.layout.result_preview_width_ratio)


class TestResultIdStabilityAndSemantics(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_plugin_id_test", plugin_file)
        assert spec is not None and spec.loader is not None
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin_id_test"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()
        self.mock_api = MockPublicAPI(
            {
                "linkding_url": "https://linkding.test",
                "api_token": "secret_token",
                "max_results": "10",
            }
        )
        self.ctx = Context()
        await self.plugin.init(self.ctx, PluginInitParams(api=self.mock_api, plugin_directory="."))

    async def test_empty_query_result_id(self):
        query = Query(
            id="q_empty",
            type=QueryType.INPUT,
            raw_query="ld",
            selection=None,
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="",
        )
        response = await self.plugin.query(self.ctx, query)
        self.assertEqual(len(response.results), 1)
        self.assertEqual(response.results[0].id, "prompt:empty")

    async def test_bookmark_search_result_ids(self):
        from unittest.mock import MagicMock, patch

        mock_response_data = {
            "count": 2,
            "results": [
                {"id": 42, "url": "https://github.com", "title": "GitHub", "tag_names": ["git"]},
                {"url": "https://python.org", "title": "Python", "tag_names": []},  # fallback without id
            ],
        }
        mock_http_response = MagicMock()
        mock_http_response.read.return_value = json.dumps(mock_response_data).encode("utf-8")
        mock_http_response.__enter__.return_value = mock_http_response

        query = Query(
            id="q_bm",
            type=QueryType.INPUT,
            raw_query="ld git",
            selection=None,
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="git",
        )

        with patch("urllib.request.urlopen", return_value=mock_http_response):
            response = await self.plugin.query(self.ctx, query)
            self.assertEqual(len(response.results), 2)
            self.assertEqual(response.results[0].id, "bookmark:42")
            self.assertEqual(response.results[1].id, "bookmark:https://python.org")

    async def test_empty_bookmarks_and_error_result_ids(self):
        from unittest.mock import MagicMock, patch
        import urllib.error

        # Empty bookmarks
        mock_empty_resp = MagicMock()
        mock_empty_resp.read.return_value = json.dumps({"count": 0, "results": []}).encode("utf-8")
        mock_empty_resp.__enter__.return_value = mock_empty_resp

        def _make_query(search_text: str) -> Query:
            return Query(
                id="q_none",
                type=QueryType.INPUT,
                raw_query=f"ld {search_text}",
                selection=Selection(),
                env=QueryEnv(),
                trigger_keyword="ld",
                command="",
                search=search_text,
            )

        with patch("urllib.request.urlopen", return_value=mock_empty_resp):
            response = await self.plugin.query(self.ctx, _make_query("notfound"))
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].id, "bookmark:empty")

        # Auth error
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError("url", 401, "Unauthorized", {}, None)):
            response = await self.plugin.query(self.ctx, _make_query("auth_error"))
            self.assertEqual(response.results[0].id, "error:auth")

        # Network error
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
            response = await self.plugin.query(self.ctx, _make_query("net_error"))
            self.assertEqual(response.results[0].id, "error:network")

        # Timeout error
        with patch("urllib.request.urlopen", side_effect=TimeoutError()):
            response = await self.plugin.query(self.ctx, _make_query("timeout_error"))
            self.assertEqual(response.results[0].id, "error:timeout")

    async def test_url_save_and_duplicate_result_ids(self):
        from unittest.mock import MagicMock, patch

        # Check existing bookmark
        existing_data = {
            "bookmark": {
                "id": 99,
                "url": "https://example.com",
                "title": "Example",
                "tag_names": ["web"],
            }
        }
        mock_resp_exist = MagicMock()
        mock_resp_exist.read.return_value = json.dumps(existing_data).encode("utf-8")
        mock_resp_exist.__enter__.return_value = mock_resp_exist

        query_exist = Query(
            id="q_url1",
            type=QueryType.INPUT,
            raw_query="ld https://example.com",
            selection=None,
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="https://example.com",
        )
        with patch("urllib.request.urlopen", return_value=mock_resp_exist):
            response = await self.plugin.query(self.ctx, query_exist)
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].id, "bookmark:99")

        # Check non-existing (save prompt)
        mock_resp_new = MagicMock()
        mock_resp_new.read.return_value = json.dumps({"bookmark": None}).encode("utf-8")
        mock_resp_new.__enter__.return_value = mock_resp_new

        query_new = Query(
            id="q_url2",
            type=QueryType.INPUT,
            raw_query="ld https://newsite.com",
            selection=None,
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="https://newsite.com",
        )
        with patch("urllib.request.urlopen", return_value=mock_resp_new):
            response = await self.plugin.query(self.ctx, query_new)
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].id, "bookmark:save:https://newsite.com")

    async def test_tag_browsing_result_ids(self):
        from unittest.mock import MagicMock, patch

        tags_data = {
            "count": 2,
            "results": [
                {"id": 1, "name": "python"},
                {"id": 2, "name": "linux"},
            ],
        }
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp

        query_tag = Query(
            id="q_tag",
            type=QueryType.INPUT,
            raw_query="ld #py",
            selection=None,
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="#py",
        )
        with patch("urllib.request.urlopen", return_value=mock_resp):
            response = await self.plugin.query(self.ctx, query_tag)
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].id, "tag:python")

        # No matching tag
        query_notag = Query(
            id="q_notag",
            type=QueryType.INPUT,
            raw_query="ld #nonexistent",
            selection=None,
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="#nonexistent",
        )
        response_notag = await self.plugin.query(self.ctx, query_notag)
        self.assertEqual(len(response_notag.results), 1)
        self.assertEqual(response_notag.results[0].id, "tag:empty")

    async def test_selection_query_aggregate_result_id(self):
        from unittest.mock import MagicMock, patch

        mock_data = {
            "count": 1,
            "results": [{"id": 101, "url": "https://sel.com", "title": "Selected", "tag_names": []}],
        }
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(mock_data).encode("utf-8")
        mock_resp.__enter__.return_value = mock_resp

        query = Query(
            id="q_sel",
            type=QueryType.SELECTION,
            raw_query="",
            selection=Selection(type=SelectionType.TEXT, text="sel keyword"),
            env=QueryEnv(),
            trigger_keyword="ld",
            command="",
            search="",
        )
        with patch("urllib.request.urlopen", return_value=mock_resp):
            response = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, query)
            self.assertEqual(len(response.results), 1)
            self.assertEqual(response.results[0].id, "selection:bookmarks")


class TestScoringStrategy(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

        self.mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "10",
        })
        self.ctx = Context()
        params = PluginInitParams(api=self.mock_api, plugin_directory=str(Path.cwd()))
        await self.plugin.init(self.ctx, params)

    def _make_query(self, search: str, trigger_keyword: str = "ld") -> Query:
        raw_query = f"{trigger_keyword} {search}" if trigger_keyword else search
        return Query(
            id="q_scoring",
            type=QueryType.INPUT,
            raw_query=raw_query,
            selection=Selection(),
            env=QueryEnv(),
            trigger_keyword=trigger_keyword,
            command="",
            search=search,
        )

    async def test_cooccurring_tag_frequency_score_mapping(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {
            "count": 3,
            "results": [
                {"id": 1, "url": "https://a.com", "title": "A", "tag_names": ["github", "python", "ai"]},
                {"id": 2, "url": "https://b.com", "title": "B", "tag_names": ["github", "python", "backend"]},
                {"id": 3, "url": "https://c.com", "title": "C", "tag_names": ["github", "python"]},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#github #"))
            # python has frequency 3 -> score 3.0
            # ai has frequency 1 -> score 1.0
            # backend has frequency 1 -> score 1.0
            results = response.results
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0].title, "#python")
            self.assertEqual(results[0].score, 3.0)
            self.assertEqual(results[1].score, 1.0)
            self.assertEqual(results[2].score, 1.0)

    async def test_bookmark_search_positional_scoring(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {
            "count": 3,
            "results": [
                {"id": 10, "url": "https://latest.com", "title": "Latest Bookmark"},
                {"id": 9, "url": "https://middle.com", "title": "Middle Bookmark"},
                {"id": 8, "url": "https://oldest.com", "title": "Oldest Bookmark"},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("bookmark"))
            results = response.results
            # Scores should be strictly descending to preserve API ranking in Wox
            self.assertGreater(results[0].score, results[1].score)
            self.assertGreater(results[1].score, results[2].score)
            self.assertGreaterEqual(results[2].score, 1.0)

    async def test_global_tag_positional_scoring(self):
        from unittest.mock import MagicMock, patch

        tags_data = {
            "count": 3,
            "results": [
                {"id": 1, "name": "tag-c"},
                {"id": 2, "name": "tag-a"},
                {"id": 3, "name": "tag-b"},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(tags_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp):
            response = await self.plugin.query(self.ctx, self._make_query("#"))
            results = response.results
            self.assertEqual(len(results), 3)
            # Scores should be strictly descending to preserve API tag order in Wox
            self.assertGreater(results[0].score, results[1].score)
            self.assertGreater(results[1].score, results[2].score)
            self.assertEqual(results[0].title, "#tag-c")


class TestBookmarkSearchCache(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        import importlib.util
        import sys

        plugin_file = Path(__file__).resolve().parent.parent / "Wox.Plugin.Linkding.py"
        spec = importlib.util.spec_from_file_location("linkding_plugin", plugin_file)
        self.module = importlib.util.module_from_spec(spec)
        sys.modules["linkding_plugin"] = self.module
        spec.loader.exec_module(self.module)
        self.plugin = self.module.LinkdingPlugin()

        self.mock_api = MockPublicAPI(initial_settings={
            "linkding_url": "https://linkding.example.com",
            "api_token": "secret_token",
            "max_results": "10",
        })
        self.ctx = Context()
        params = PluginInitParams(api=self.mock_api, plugin_directory=str(Path.cwd()))
        await self.plugin.init(self.ctx, params)

    def _make_query(self, search: str, trigger_keyword: str = "ld") -> Query:
        raw_query = f"{trigger_keyword} {search}" if trigger_keyword else search
        return Query(
            id="q_cache",
            type=QueryType.INPUT,
            raw_query=raw_query,
            selection=Selection(),
            env=QueryEnv(),
            trigger_keyword=trigger_keyword,
            command="",
            search=search,
        )

    async def test_search_bookmarks_caches_responses_and_normalizes_whitespace(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {
            "count": 1,
            "results": [
                {"id": 1, "url": "https://example.com", "title": "Example Bookmark"},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp) as mock_urlopen:
            # First query performs network request
            res1 = await self.plugin.query(self.ctx, self._make_query("github"))
            self.assertEqual(mock_urlopen.call_count, 1)
            self.assertEqual(len(res1.results), 1)

            # Query with trailing space hits cache without network call
            res2 = await self.plugin.query(self.ctx, self._make_query("github "))
            self.assertEqual(mock_urlopen.call_count, 1)
            self.assertEqual(len(res2.results), 1)
            self.assertEqual(res2.results[0].id, "bookmark:1")

            # Tag search ending with space also routes to bookmark search and caches
            res3 = await self.plugin.query(self.ctx, self._make_query("#tag "))
            self.assertEqual(mock_urlopen.call_count, 2)
            self.assertEqual(len(res3.results), 1)

            res4 = await self.plugin.query(self.ctx, self._make_query("#tag  "))
            self.assertEqual(mock_urlopen.call_count, 2)
            self.assertEqual(len(res4.results), 1)
            self.assertEqual(res4.results[0].id, "bookmark:1")

    async def test_input_and_selection_share_fresh_responses(self):
        from unittest.mock import MagicMock, patch

        for bookmarks in ([], [
            {"id": 1, "url": "https://example.com/1", "title": "First"},
            {"id": 2, "url": "https://example.com/2", "title": "Second"},
        ]):
            with self.subTest(count=len(bookmarks)):
                search_text = f"example{len(bookmarks)}"
                selection = Query(
                    id="q_shared_selection", type=QueryType.SELECTION, raw_query="",
                    selection=Selection(type=SelectionType.TEXT, text=search_text),
                    env=QueryEnv(), trigger_keyword="", command="", search="",
                )
                response = MagicMock()
                response.read.return_value = json.dumps({
                    "count": len(bookmarks), "results": bookmarks,
                }).encode("utf-8")
                response.__enter__.return_value = response

                with patch("urllib.request.urlopen", return_value=response) as http:
                    flat = await self.plugin.query(self.ctx, self._make_query(search_text))
                    for _ in range(2):
                        aggregated = await query_selection_and_wait(
                            self.plugin, self.mock_api, self.ctx, selection,
                        )
                        self.assertEqual(aggregated.results[0].id, "selection:bookmarks")
                        self.assertEqual(len(aggregated.results[0].actions), 2)
                    expanded = await self.plugin.query(self.ctx, self._make_query(search_text))
                    self.assertEqual([result.id for result in expanded.results], [result.id for result in flat.results])
                    self.assertEqual(http.call_count, 1)

    async def test_selection_refreshes_expired_shared_response(self):
        from unittest.mock import MagicMock, patch

        selection = Query(
            id="q_expired_selection", type=QueryType.SELECTION, raw_query="",
            selection=Selection(type=SelectionType.TEXT, text="python"),
            env=QueryEnv(), trigger_keyword="", command="", search="",
        )
        responses = []
        for bookmarks in ([], [{"id": 1, "url": "https://example.com", "title": "Refreshed"}]):
            response = MagicMock()
            response.read.return_value = json.dumps({"count": len(bookmarks), "results": bookmarks}).encode("utf-8")
            response.__enter__.return_value = response
            responses.append(response)

        with patch("time.time", return_value=1000.0) as clock, \
             patch("urllib.request.urlopen", side_effect=responses) as http:
            await self.plugin.query(self.ctx, self._make_query("python"))
            clock.return_value = 1029.0
            cached = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, selection)
            self.assertEqual(cached.results[0].sub_title, "i18n:selection_press_enter_to_edit")
            self.assertEqual(http.call_count, 1)

            clock.return_value = 1031.0
            refreshed = await query_selection_and_wait(self.plugin, self.mock_api, self.ctx, selection)
            preview = WoxPreviewListData.from_json(json.loads(refreshed.results[0].preview.preview_data))
            self.assertEqual(preview.items[0].title, "Refreshed")
            flat = await self.plugin.query(self.ctx, self._make_query("python"))
            self.assertEqual(flat.results[0].title, "Refreshed")
            self.assertEqual(http.call_count, 2)

    async def test_search_bookmarks_cache_invalidates_on_setting_changed(self):
        from unittest.mock import MagicMock, patch

        bookmarks_data = {
            "count": 1,
            "results": [
                {"id": 1, "url": "https://example.com", "title": "Example Bookmark"},
            ],
        }
        mock_http_resp = MagicMock()
        mock_http_resp.read.return_value = json.dumps(bookmarks_data).encode("utf-8")
        mock_http_resp.__enter__.return_value = mock_http_resp

        with patch("urllib.request.urlopen", return_value=mock_http_resp) as mock_urlopen:
            await self.plugin.query(self.ctx, self._make_query("test"))
            self.assertEqual(mock_urlopen.call_count, 1)

            # Change a setting
            callback = self.mock_api.setting_changed_callbacks[0]
            await callback(self.ctx, "api_token", "new_token")

            # Subsequent query should trigger a new network call
            await self.plugin.query(self.ctx, self._make_query("test"))
            self.assertEqual(mock_urlopen.call_count, 2)


if __name__ == "__main__":
    unittest.main()




