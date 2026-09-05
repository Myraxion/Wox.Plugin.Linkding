import asyncio
import json
import unittest
from pathlib import Path

from wox_plugin import Context, PluginInitParams, Query, QueryResponse, QueryType, Result, WoxImage, WoxImageType
from wox_plugin.models.query import QueryEnv, Selection


class MockPublicAPI:
    def __init__(self, initial_settings=None):
        self.settings = initial_settings or {}
        self.setting_changed_callbacks = []
        self.translations = {
            "prompt_empty_search": "Type to search bookmarks, or paste a URL to save...",
            "bookmark_already_exists": "⚠️ Already bookmarked",
            "prompt_save_bookmark": "Press Enter to save bookmark",
            "action_save_bookmark": "Save Bookmark",
            "notify_bookmark_created": "Bookmark saved successfully",
            "notify_bookmark_failed": "Failed to save bookmark",
        }
        self.copied_params = []
        self.notifications = []

    async def get_setting(self, ctx: Context, key: str) -> str:
        return self.settings.get(key, "")

    async def save_setting(self, ctx: Context, key: str, value: str, is_platform_specific: bool = False) -> None:
        self.settings[key] = value

    async def on_setting_changed(self, ctx: Context, callback) -> None:
        self.setting_changed_callbacks.append(callback)

    async def get_translation(self, ctx: Context, key: str) -> str:
        return self.translations.get(key, key)

    async def copy(self, ctx: Context, params) -> None:
        self.copied_params.append(params)

    async def notify(self, ctx: Context, message: str) -> None:
        self.notifications.append(message)


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

        # Debounce feature
        features = meta.get("Features", [])
        debounce_features = [f for f in features if f.get("Name") == "debounce"]
        self.assertEqual(len(debounce_features), 1, "Debounce feature must be declared")
        self.assertEqual(debounce_features[0].get("Params", {}).get("IntervalMs"), 300)

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
            self.assertIn("error_timeout", i18n[lang])
            self.assertIn("error_timeout_sub", i18n[lang])
            self.assertIn("bookmark_already_exists", i18n[lang])
            self.assertIn("prompt_save_bookmark", i18n[lang])
            self.assertIn("action_save_bookmark", i18n[lang])
            self.assertIn("notify_bookmark_created", i18n[lang])
            self.assertIn("notify_bookmark_failed", i18n[lang])


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
             patch.object(self.plugin, "_handle_url_input", new_callable=AsyncMock) as mock_handle_url:
            mock_handle_url.return_value = QueryResponse(results=[])

            res1 = await self.plugin.query(self.ctx, self._make_query("https://example.com/page"))
            mock_handle_url.assert_called_with(self.ctx, "https://example.com/page")

            res2 = await self.plugin.query(self.ctx, self._make_query("http://insecure.org"))
            mock_handle_url.assert_called_with(self.ctx, "http://insecure.org")

            res3 = await self.plugin.query(self.ctx, self._make_query("#python"))
            self.assertEqual(res3.results, [])

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


if __name__ == "__main__":
    unittest.main()


