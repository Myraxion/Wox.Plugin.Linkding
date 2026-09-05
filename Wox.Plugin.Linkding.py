# {
#   "Id": "9d7b4e96-a81d-44a3-a75a-bc828cf5668e",
#   "Name": "i18n:plugin_name",
#   "Description": "i18n:plugin_desc",
#   "Author": "Myraxion",
#   "Version": "1.0.0",
#   "MinWoxVersion": "2.4.2",
#   "Runtime": "PYTHON",
#   "Icon": "svg:<svg clip-rule=\"evenodd\" fill-rule=\"evenodd\" height=\"512\" stroke-linejoin=\"round\" stroke-miterlimit=\"1.5\" viewBox=\"0 0 512 512\" width=\"512\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"255.0164\" cy=\"254.9236\" fill=\"#5856e0\" r=\"224.78528\" stroke-width=\"1.18\"/><g fill=\"none\" stroke=\"#fff\" stroke-width=\"31.25\"><path d=\"m1244.39 1293.95v199.64s-.81 67.89 74.9 68.88c75.98.99 74.88-68.88 74.88-68.88v-199.64\" transform=\"matrix(.70710678 .70710678 -.70710678 .70710678 284.139117 -1684.198509)\"/><path d=\"m1244.39 1293.95v199.64s-.81 67.89 74.9 68.88c75.98.99 74.88-68.88 74.88-68.88v-199.64\" transform=\"matrix(-.70957074 -.70463421 .70463421 -.70957074 235.113139 2195.434643)\"/></g></svg>",
#   "TriggerKeywords": ["ld"],
#   "SupportedOS": ["Windows", "Linux", "Darwin"],
#   "Features": [
#     {
#       "Name": "debounce",
#       "Params": {
#         "IntervalMs": 300
#       }
#     }
#   ],
#   "I18n": {
#     "en_US": {
#       "plugin_name": "Linkding",
#       "plugin_desc": "Search, save, and manage bookmarks from your Linkding instance",
#       "setting_linkding_url_label": "Linkding URL",
#       "setting_linkding_url_tooltip": "Base URL of your Linkding server (e.g. https://linkding.example.com)",
#       "setting_linkding_url_required": "Please configure your Linkding server URL",
#       "setting_api_token_label": "API Token",
#       "setting_api_token_tooltip": "REST API Authorization Token from your Linkding Settings",
#       "setting_api_token_required": "Please configure your Linkding API token",
#       "setting_max_results_label": "Max Results",
#       "setting_max_results_tooltip": "Maximum number of search results to display (default: 10)",
#       "prompt_empty_search": "Type to search bookmarks, or paste a URL to save..."
#     },
#     "zh_CN": {
#       "plugin_name": "Linkding",
#       "plugin_desc": "在 Linkding 中搜索、保存和管理书签",
#       "setting_linkding_url_label": "Linkding 地址",
#       "setting_linkding_url_tooltip": "Linkding 服务端基础地址（如 https://linkding.example.com）",
#       "setting_linkding_url_required": "请配置 Linkding 服务端地址",
#       "setting_api_token_label": "API Token",
#       "setting_api_token_tooltip": "从 Linkding 设置页面获取的 REST API 认证令牌",
#       "setting_api_token_required": "请配置 Linkding API 令牌",
#       "setting_max_results_label": "最大显示数量",
#       "setting_max_results_tooltip": "搜索结果最大显示条数（默认：10）",
#       "prompt_empty_search": "输入关键字搜索书签，或粘贴 URL 保存..."
#     }
#   },
#   "SettingDefinitions": [
#     {
#       "Type": "textbox",
#       "Value": {
#         "Key": "linkding_url",
#         "Label": "i18n:setting_linkding_url_label",
#         "DefaultValue": "",
#         "Tooltip": "i18n:setting_linkding_url_tooltip",
#         "Validators": [
#           {
#             "Type": "not_empty",
#             "Value": {}
#           }
#         ]
#       },
#       "IsPlatformSpecific": false
#     },
#     {
#       "Type": "textbox",
#       "Value": {
#         "Key": "api_token",
#         "Label": "i18n:setting_api_token_label",
#         "DefaultValue": "",
#         "Tooltip": "i18n:setting_api_token_tooltip",
#         "Validators": [
#           {
#             "Type": "not_empty",
#             "Value": {}
#           }
#         ]
#       },
#       "IsPlatformSpecific": false
#     },
#     {
#       "Type": "textbox",
#       "Value": {
#         "Key": "max_results",
#         "Label": "i18n:setting_max_results_label",
#         "DefaultValue": "10",
#         "Tooltip": "i18n:setting_max_results_tooltip",
#         "Validators": [
#           {
#             "Type": "is_number",
#             "Value": {
#               "IsInteger": true,
#               "IsFloat": false
#             }
#           }
#         ]
#       },
#       "IsPlatformSpecific": false
#     }
#   ],
#   "QueryRequirements": {
#     "AnyQuery": [
#       {
#         "SettingKey": "linkding_url",
#         "Validators": [
#           {
#             "Type": "not_empty",
#             "Value": {}
#           }
#         ],
#         "Message": "i18n:setting_linkding_url_required"
#       },
#       {
#         "SettingKey": "api_token",
#         "Validators": [
#           {
#             "Type": "not_empty",
#             "Value": {}
#           }
#         ],
#         "Message": "i18n:setting_api_token_required"
#       }
#     ],
#     "QueryWithoutCommand": [],
#     "QueryWithCommand": {}
#   }
# }

"""
Wox Linkding Plugin

Single-file Python SDK plugin integrating Wox launcher with Linkding.
"""

from typing import Optional

from wox_plugin import (
    Context,
    Plugin,
    PluginInitParams,
    PublicAPI,
    Query,
    QueryResponse,
    Result,
    WoxImage,
)

LINKDING_ICON_SVG = (
    '<svg clip-rule="evenodd" fill-rule="evenodd" height="512" stroke-linejoin="round" '
    'stroke-miterlimit="1.5" viewBox="0 0 512 512" width="512" xmlns="http://www.w3.org/2000/svg">'
    '<circle cx="255.0164" cy="254.9236" fill="#5856e0" r="224.78528" stroke-width="1.18"/>'
    '<g fill="none" stroke="#fff" stroke-width="31.25">'
    '<path d="m1244.39 1293.95v199.64s-.81 67.89 74.9 68.88c75.98.99 74.88-68.88 74.88-68.88v-199.64" '
    'transform="matrix(.70710678 .70710678 -.70710678 .70710678 284.139117 -1684.198509)"/>'
    '<path d="m1244.39 1293.95v199.64s-.81 67.89 74.9 68.88c75.98.99 74.88-68.88 74.88-68.88v-199.64" '
    'transform="matrix(-.70957074 -.70463421 .70463421 -.70957074 235.113139 2195.434643)"/>'
    '</g></svg>'
)


class LinkdingPlugin(Plugin):
    def __init__(self) -> None:
        self.api: Optional[PublicAPI] = None
        self.linkding_url: str = ""
        self.api_token: str = ""
        self.max_results: int = 10

    async def init(self, ctx: Context, params: PluginInitParams) -> None:
        self.api = params.api
        await self.api.on_setting_changed(ctx, self._on_setting_changed)

        raw_url = await self.api.get_setting(ctx, "linkding_url")
        self.linkding_url = raw_url.strip().rstrip("/") if raw_url else ""

        raw_token = await self.api.get_setting(ctx, "api_token")
        self.api_token = raw_token.strip() if raw_token else ""

        raw_max = await self.api.get_setting(ctx, "max_results")
        self.max_results = int(raw_max) if raw_max and raw_max.strip().isdigit() else 10

    async def _on_setting_changed(self, ctx: Context, key: str, value: str) -> None:
        if key == "linkding_url":
            self.linkding_url = value.strip().rstrip("/") if value else ""
        elif key == "api_token":
            self.api_token = value.strip() if value else ""
        elif key == "max_results":
            self.max_results = int(value) if value and value.strip().isdigit() else 10

    async def query(self, ctx: Context, query: Query) -> QueryResponse:
        search_text = (query.search or "").strip()

        if not search_text:
            sub_title = (
                f"Linkding: {self.linkding_url}"
                if self.linkding_url
                else "i18n:prompt_empty_search"
            )
            return QueryResponse(
                results=[
                    Result(
                        title="i18n:prompt_empty_search",
                        sub_title=sub_title,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )

        return QueryResponse(results=[])


plugin = LinkdingPlugin()
