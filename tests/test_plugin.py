import asyncio
import json
import unittest
from pathlib import Path

from wox_plugin import Context, PluginInitParams, Query, QueryType, Result, WoxImage, WoxImageType
from wox_plugin.models.query import QueryEnv, Selection


class MockPublicAPI:
    def __init__(self, initial_settings=None):
        self.settings = initial_settings or {}
        self.setting_changed_callbacks = []
        self.translations = {
            "prompt_empty_search": "Type to search bookmarks, or paste a URL to save..."
        }

    async def get_setting(self, ctx: Context, key: str) -> str:
        return self.settings.get(key, "")

    async def save_setting(self, ctx: Context, key: str, value: str, is_platform_specific: bool = False) -> None:
        self.settings[key] = value

    async def on_setting_changed(self, ctx: Context, callback) -> None:
        self.setting_changed_callbacks.append(callback)

    async def get_translation(self, ctx: Context, key: str) -> str:
        return self.translations.get(key, key)


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


if __name__ == "__main__":
    unittest.main()
