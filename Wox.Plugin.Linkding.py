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
#       "prompt_empty_search": "Type to search bookmarks, or paste a URL to save...",
#       "action_open_url": "Open in Browser",
#       "action_copy_url": "Copy URL",
#       "action_open_in_linkding": "Open in Linkding",
#       "no_bookmarks_found": "No bookmarks found",
#       "no_bookmarks_found_sub": "Press Enter to search in Linkding web interface",
#       "error_auth_failed": "Authentication Failed",
#       "error_auth_failed_sub": "Please check your Linkding API token in settings",
#       "error_network": "Network Connection Error",
#       "error_timeout": "Request Timed Out",
#       "error_timeout_sub": "Connection to Linkding server timed out"
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
#       "prompt_empty_search": "输入关键字搜索书签，或粘贴 URL 保存...",
#       "action_open_url": "在浏览器中打开",
#       "action_copy_url": "复制链接",
#       "action_open_in_linkding": "在 Linkding 中打开",
#       "no_bookmarks_found": "未找到相关书签",
#       "no_bookmarks_found_sub": "按回车在 Linkding 网页中搜索",
#       "error_auth_failed": "认证失败",
#       "error_auth_failed_sub": "请在设置中检查 Linkding API 令牌",
#       "error_network": "网络连接错误",
#       "error_timeout": "请求超时",
#       "error_timeout_sub": "连接 Linkding 服务器超时"
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

from typing import Any, Callable, Dict, List, Optional
import asyncio
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

from wox_plugin import (
    ActionContext,
    Context,
    CopyParams,
    CopyType,
    Plugin,
    PluginInitParams,
    PublicAPI,
    Query,
    QueryResponse,
    Result,
    ResultAction,
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

        # Smart pattern recognition (ADR-0002)
        # URLs trigger bookmark creation; # prefixes trigger tag exploration
        if re.match(r"^https?://", search_text, re.IGNORECASE) or search_text.startswith("#"):
            return QueryResponse(results=[])

        return await self._search_bookmarks(ctx, search_text)

    async def _search_bookmarks(self, ctx: Context, search_text: str) -> QueryResponse:
        encoded_q = urllib.parse.quote(search_text)
        req_url = f"{self.linkding_url}/api/bookmarks/?q={encoded_q}&limit={self.max_results}"
        req = urllib.request.Request(
            req_url,
            headers={
                "Authorization": f"Token {self.api_token}",
                "Accept": "application/json",
            },
        )

        try:
            resp_data = await asyncio.to_thread(self._fetch_bookmarks_http, req)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return QueryResponse(
                    results=[
                        Result(
                            title="i18n:error_auth_failed",
                            sub_title="i18n:error_auth_failed_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )
            return QueryResponse(
                results=[
                    Result(
                        title=f"Linkding API Error (HTTP {e.code})",
                        sub_title=str(e.reason),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )
        except urllib.error.URLError as e:
            reason_str = str(e.reason)
            if "timed out" in reason_str.lower() or isinstance(e.reason, TimeoutError):
                return QueryResponse(
                    results=[
                        Result(
                            title="i18n:error_timeout",
                            sub_title="i18n:error_timeout_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )
            return QueryResponse(
                results=[
                    Result(
                        title="i18n:error_network",
                        sub_title=reason_str,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )
        except TimeoutError:
            return QueryResponse(
                results=[
                    Result(
                        title="i18n:error_timeout",
                        sub_title="i18n:error_timeout_sub",
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )
        except Exception as e:
            return QueryResponse(
                results=[
                    Result(
                        title="Error searching bookmarks",
                        sub_title=str(e),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )

        raw_bookmarks: List[Dict[str, Any]] = resp_data.get("results", [])
        web_search_url = f"{self.linkding_url}/bookmarks?q={encoded_q}"

        if not raw_bookmarks:
            return QueryResponse(
                results=[
                    Result(
                        title="i18n:no_bookmarks_found",
                        sub_title="i18n:no_bookmarks_found_sub",
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        actions=[
                            ResultAction(
                                name="i18n:action_open_in_linkding",
                                icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                                is_default=True,
                                action=self._create_open_url_action(web_search_url),
                            )
                        ],
                    )
                ]
            )

        results: List[Result] = []
        for item in raw_bookmarks:
            bm_url = item.get("url", "")
            title = item.get("title") or item.get("website_title") or bm_url
            tags = item.get("tag_names") or []
            if tags:
                tags_str = " ".join(f"#{tag}" for tag in tags)
                sub_title = f"{bm_url} · {tags_str}"
            else:
                sub_title = bm_url

            actions = [
                ResultAction(
                    name="i18n:action_open_url",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=True,
                    action=self._create_open_url_action(bm_url),
                ),
                ResultAction(
                    name="i18n:action_copy_url",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=False,
                    action=self._create_copy_url_action(bm_url),
                ),
                ResultAction(
                    name="i18n:action_open_in_linkding",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=False,
                    action=self._create_open_url_action(web_search_url),
                ),
            ]

            results.append(
                Result(
                    title=title,
                    sub_title=sub_title,
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    actions=actions,
                )
            )

        return QueryResponse(results=results)

    def _fetch_bookmarks_http(self, req: urllib.request.Request) -> Dict[str, Any]:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
            return json.loads(data.decode("utf-8"))

    def _create_open_url_action(self, target_url: str):
        async def _action(ctx: Context, action_ctx: ActionContext) -> None:
            webbrowser.open(target_url)

        return _action

    def _create_copy_url_action(self, target_url: str):
        async def _action(ctx: Context, action_ctx: ActionContext) -> None:
            if self.api:
                await self.api.copy(ctx, CopyParams(type=CopyType.TEXT, text=target_url))

        return _action


plugin = LinkdingPlugin()

