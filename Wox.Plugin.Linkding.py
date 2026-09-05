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
#       "error_timeout_sub": "Connection to Linkding server timed out",
#       "bookmark_already_exists": "⚠️ Already bookmarked",
#       "prompt_save_bookmark": "Press Enter to save bookmark",
#       "action_save_bookmark": "Save Bookmark",
#       "notify_bookmark_created": "Bookmark saved successfully",
#       "notify_bookmark_failed": "Failed to save bookmark",
#       "no_tags_found": "No tags found",
#       "no_tags_found_sub": "No tags found in your Linkding instance",
#       "no_matching_tags": "No matching tags",
#       "tag_action_select": "Filter bookmarks by this tag"
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
#       "error_timeout_sub": "连接 Linkding 服务器超时",
#       "bookmark_already_exists": "⚠️ 该 URL 已收藏",
#       "prompt_save_bookmark": "按回车添加书签",
#       "action_save_bookmark": "保存书签",
#       "notify_bookmark_created": "书签添加成功",
#       "notify_bookmark_failed": "书签保存失败",
#       "no_tags_found": "未找到标签",
#       "no_tags_found_sub": "Linkding 实例中暂无标签",
#       "no_matching_tags": "未找到匹配的标签",
#       "tag_action_select": "按回车筛选此标签下的书签"
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
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

from wox_plugin import (
    ActionContext,
    ChangeQueryParam,
    Context,
    CopyParams,
    CopyType,
    Plugin,
    PluginInitParams,
    PublicAPI,
    Query,
    QueryResponse,
    QueryType,
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

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Wox.Plugin.Linkding/1.0.0"


class LinkdingPlugin(Plugin):
    def __init__(self) -> None:
        self.api: Optional[PublicAPI] = None
        self.linkding_url: str = ""
        self.api_token: str = ""
        self.max_results: int = 10
        self._tag_cache: Optional[List[str]] = None
        self._tag_cache_time: float = 0.0
        self.TAG_CACHE_TTL: float = 300.0

    def _create_request(
        self,
        url: str,
        data: Optional[bytes] = None,
        method: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> urllib.request.Request:
        headers = {
            "Authorization": f"Token {self.api_token}",
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        }
        if content_type:
            headers["Content-Type"] = content_type
        if method:
            return urllib.request.Request(url, data=data, headers=headers, method=method)
        return urllib.request.Request(url, data=data, headers=headers)

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
            self._tag_cache = None
            self._tag_cache_time = 0.0
        elif key == "api_token":
            self.api_token = value.strip() if value else ""
            self._tag_cache = None
            self._tag_cache_time = 0.0
        elif key == "max_results":
            self.max_results = int(value) if value and value.strip().isdigit() else 10

    async def query(self, ctx: Context, query: Query) -> QueryResponse:
        raw_search = query.search or ""
        search_text = raw_search.strip()

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
        if re.match(r"^https?://", search_text, re.IGNORECASE):
            return await self._handle_url_input(ctx, search_text)

        if search_text.startswith("#"):
            tag_content = search_text[1:]
            # If no tag name yet (e.g. '#' or '# '), or no trailing space and no space after tag name (e.g. '#dev')
            if not tag_content or (not raw_search.endswith(" ") and " " not in tag_content):
                return await self._handle_tag_browsing(ctx, query, tag_content)
            else:
                return await self._search_bookmarks(ctx, search_text)

        return await self._search_bookmarks(ctx, search_text)

    async def _search_bookmarks(self, ctx: Context, search_text: str) -> QueryResponse:
        encoded_q = urllib.parse.quote(search_text)
        req_url = f"{self.linkding_url}/api/bookmarks/?q={encoded_q}&limit={self.max_results}"
        req = self._create_request(req_url)

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

    def _parse_url_and_tags(self, input_text: str) -> tuple[str, List[str]]:
        parts = input_text.strip().split()
        if not parts:
            return "", []
        url = parts[0]
        tags: List[str] = []
        for p in parts[1:]:
            if p.startswith("#") and len(p) > 1:
                tag = p[1:].strip()
                if tag and tag not in tags:
                    tags.append(tag)
        return url, tags

    async def _handle_url_input(self, ctx: Context, search_text: str) -> QueryResponse:
        url, tags = self._parse_url_and_tags(search_text)
        if not url:
            return QueryResponse(results=[])

        encoded_url = urllib.parse.quote(url, safe="")
        req_url = f"{self.linkding_url}/api/bookmarks/check/?url={encoded_url}"
        req = self._create_request(req_url)

        try:
            check_data = await asyncio.to_thread(self._fetch_bookmarks_http, req)
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
                        title="Error checking bookmark",
                        sub_title=str(e),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )

        existing_bookmark = check_data.get("bookmark")
        if existing_bookmark:
            title = (
                existing_bookmark.get("title")
                or existing_bookmark.get("website_title")
                or url
            )
            warning_text = (
                await self.api.get_translation(ctx, "bookmark_already_exists")
                if self.api
                else "⚠️ Already bookmarked"
            )
            bm_tags = existing_bookmark.get("tag_names") or []
            tags_str = " ".join(f"#{t}" for t in bm_tags)
            if tags_str:
                sub_title = f"{warning_text} · {url} · {tags_str}"
            else:
                sub_title = f"{warning_text} · {url}"

            web_search_url = f"{self.linkding_url}/bookmarks?q={urllib.parse.quote(url)}"
            actions = [
                ResultAction(
                    name="i18n:action_open_url",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=True,
                    action=self._create_open_url_action(url),
                ),
                ResultAction(
                    name="i18n:action_copy_url",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=False,
                    action=self._create_copy_url_action(url),
                ),
                ResultAction(
                    name="i18n:action_open_in_linkding",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=False,
                    action=self._create_open_url_action(web_search_url),
                ),
            ]

            return QueryResponse(
                results=[
                    Result(
                        title=title,
                        sub_title=sub_title,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        actions=actions,
                    )
                ]
            )

        # Not bookmarked yet: show prompt to save
        tags_str = " ".join(f"#{t}" for t in tags)
        sub_title = f"{url} · {tags_str}" if tags_str else url
        actions = [
            ResultAction(
                name="i18n:action_save_bookmark",
                icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                is_default=True,
                action=self._create_save_bookmark_action(url, tags),
            ),
            ResultAction(
                name="i18n:action_open_url",
                icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                is_default=False,
                action=self._create_open_url_action(url),
            ),
        ]

        return QueryResponse(
            results=[
                Result(
                    title="i18n:prompt_save_bookmark",
                    sub_title=sub_title,
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    actions=actions,
                )
            ]
        )

    def _create_save_bookmark_action(self, target_url: str, tags: List[str]):
        async def _action(ctx: Context, action_ctx: ActionContext) -> None:
            post_url = f"{self.linkding_url}/api/bookmarks/"
            payload = json.dumps({"url": target_url, "tag_names": tags}).encode("utf-8")
            req = self._create_request(
                post_url,
                data=payload,
                method="POST",
                content_type="application/json",
            )
            try:
                await asyncio.to_thread(self._fetch_bookmarks_http, req)
                if self.api:
                    msg = await self.api.get_translation(ctx, "notify_bookmark_created")
                    await self.api.notify(ctx, f"{msg}: {target_url}")
            except Exception as e:
                if self.api:
                    msg = await self.api.get_translation(ctx, "notify_bookmark_failed")
                    await self.api.notify(ctx, f"{msg}: {e}")

        return _action

    async def _get_tags(self, ctx: Context) -> List[str]:
        now = time.time()
        if self._tag_cache is not None and (now - self._tag_cache_time) < self.TAG_CACHE_TTL:
            return self._tag_cache

        req_url = f"{self.linkding_url}/api/tags/"
        req = self._create_request(req_url)
        resp_data = await asyncio.to_thread(self._fetch_bookmarks_http, req)
        raw_tags = resp_data.get("results", [])
        tags = [t["name"] for t in raw_tags if isinstance(t, dict) and "name" in t]
        self._tag_cache = tags
        self._tag_cache_time = now
        return tags

    async def _handle_tag_browsing(
        self, ctx: Context, query: Query, tag_prefix: str
    ) -> QueryResponse:
        try:
            tags = await self._get_tags(ctx)
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
                        title="Error fetching tags",
                        sub_title=str(e),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )

        if tag_prefix:
            prefix_lower = tag_prefix.lower()
            matching_tags = [t for t in tags if t.lower().startswith(prefix_lower)]
        else:
            matching_tags = list(tags)

        if not matching_tags:
            if not tags:
                title = "i18n:no_tags_found"
                sub_title = "i18n:no_tags_found_sub"
            else:
                title = "i18n:no_matching_tags"
                sub_title = f"#{tag_prefix}"

            return QueryResponse(
                results=[
                    Result(
                        title=title,
                        sub_title=sub_title,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )

        trigger = query.trigger_keyword or "ld"
        results: List[Result] = []
        for tag in matching_tags[: self.max_results]:
            actions = [
                ResultAction(
                    name="i18n:tag_action_select",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=True,
                    action=self._create_select_tag_action(tag, trigger),
                ),
            ]
            results.append(
                Result(
                    title=f"#{tag}",
                    sub_title="i18n:tag_action_select",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    actions=actions,
                )
            )

        return QueryResponse(results=results)

    def _create_select_tag_action(self, tag: str, trigger_keyword: str):
        async def _action(ctx: Context, action_ctx: ActionContext) -> None:
            if self.api:
                kw = trigger_keyword or "ld"
                await self.api.change_query(
                    ctx,
                    ChangeQueryParam(
                        query_type=QueryType.INPUT,
                        query_text=f"{kw} #{tag} ",
                    ),
                )

        return _action


plugin = LinkdingPlugin()


