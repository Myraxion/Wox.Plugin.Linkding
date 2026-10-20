# {
#   "Id": "9d7b4e96-a81d-44a3-a75a-bc828cf5668e",
#   "Name": "i18n:plugin_name",
#   "Description": "i18n:plugin_desc",
#   "Author": "Myraxion",
#   "Version": "1.2.0",
#   "MinWoxVersion": "2.4.2",
#   "Runtime": "PYTHON",
#   "Icon": "svg:<svg clip-rule=\"evenodd\" fill-rule=\"evenodd\" height=\"512\" stroke-linejoin=\"round\" stroke-miterlimit=\"1.5\" viewBox=\"0 0 512 512\" width=\"512\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"255.0164\" cy=\"254.9236\" fill=\"#5856e0\" r=\"224.78528\" stroke-width=\"1.18\"/><g fill=\"none\" stroke=\"#fff\" stroke-width=\"31.25\"><path d=\"m1244.39 1293.95v199.64s-.81 67.89 74.9 68.88c75.98.99 74.88-68.88 74.88-68.88v-199.64\" transform=\"matrix(.70710678 .70710678 -.70710678 .70710678 284.139117 -1684.198509)\"/><path d=\"m1244.39 1293.95v199.64s-.81 67.89 74.9 68.88c75.98.99 74.88-68.88 74.88-68.88v-199.64\" transform=\"matrix(-.70957074 -.70463421 .70463421 -.70957074 235.113139 2195.434643)\"/></g></svg>",
#   "TriggerKeywords": ["ld"],
#   "SupportedOS": ["Windows", "Linux", "Darwin"],
#   "Features": [
#     {
#       "Name": "querySelection"
#     },
#     {
#       "Name": "debounce",
#       "Params": {
#         "IntervalMs": 200
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
#       "tag_action_select": "Filter bookmarks by this tag",
#       "selection_bookmarks_found": "Linkding: {count} bookmarks found",
#       "selection_press_enter_to_expand": "Press Enter to select a bookmark",
#       "selection_press_enter_to_edit": "No bookmarks found · Press Enter to edit search terms",
#       "selection_action_expand": "Expand Bookmark List",
#       "toolbar_tags_found": "{count} tags found",
#       "toolbar_bookmarks_found": "{count} bookmarks found"
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
#       "tag_action_select": "按回车筛选此标签下的书签",
#       "selection_bookmarks_found": "Linkding: 找到 {count} 个相关书签",
#       "selection_press_enter_to_expand": "按回车选择书签",
#       "selection_press_enter_to_edit": "未找到书签 · 按回车修改搜索词",
#       "selection_action_expand": "展开书签列表",
#       "toolbar_tags_found": "共 {count} 个标签",
#       "toolbar_bookmarks_found": "共 {count} 个书签"
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
import base64
import http.client
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
    QueryLayout,
    QueryResponse,
    QueryType,
    Result,
    ResultAction,
    ResultTail,
    ResultTailTextCategory,
    ResultTailType,
    SelectionType,
    ToolbarMsg,
    UpdatableResult,
    WoxImage,
    WoxImageType,
    WoxPreview,
    WoxPreviewListData,
    WoxPreviewListItem,
    WoxPreviewType,
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

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Wox.Plugin.Linkding/1.2.0"

IPV4_REGEX = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(?::\d+)?(?:[/?#].*)?$"
)
DOMAIN_REGEX = re.compile(
    r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9_-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(?::\d+)?(?:[/?#].*)?$",
    re.IGNORECASE,
)
LOCALHOST_REGEX = re.compile(
    r"^localhost(?::\d+)?(?:[/?#].*)?$",
    re.IGNORECASE,
)


ACTION_SEARCH_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
    'fill="none" stroke="var(--wox-theme-icon-color)" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>'
)
ACTION_OPEN_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
    'fill="none" stroke="var(--wox-theme-icon-color)" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M14 5h5v5M19 5l-9 9"/>'
    '<path d="M13 7H6a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2-2v-7"/></svg>'
)


class LinkdingPlugin(Plugin):
    def __init__(self) -> None:
        self.api: Optional[PublicAPI] = None
        self.linkding_url: str = ""
        self.api_token: str = ""
        self.max_results: int = 10
        self._tag_cache: Optional[List[str]] = None
        self._tag_cache_time: float = 0.0
        self.TAG_CACHE_TTL: float = 300.0
        self._cooccurring_tag_cache: Dict[str, tuple[float, Dict[str, int]]] = {}
        self.COOCCURRING_TAG_CACHE_TTL: float = 30.0
        self._bookmark_cache: Dict[str, tuple[float, Dict[str, Any]]] = {}
        self.BOOKMARK_CACHE_TTL: float = 30.0
        self._last_bookmark_query: str = ""
        self._last_bookmarks: List[Dict[str, Any]] = []
        self._query_generation = 0
        self._favicon_cache: Dict[str, tuple[float, Optional[WoxImage]]] = {}
        self._favicon_downloads: Dict[str, asyncio.Task[Optional[WoxImage]]] = {}
        self._favicon_refreshes: set[asyncio.Task[None]] = set()
        self.FAVICON_CACHE_TTL = 300.0

    TOOLBAR_MSG_ID = "linkding:status"

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
        if hasattr(self.api, "on_leave_plugin_query"):
            await self.api.on_leave_plugin_query(ctx, self._on_leave_plugin_query)

        raw_url = await self.api.get_setting(ctx, "linkding_url")
        self.linkding_url = raw_url.strip().rstrip("/") if raw_url else ""

        raw_token = await self.api.get_setting(ctx, "api_token")
        self.api_token = raw_token.strip() if raw_token else ""

        raw_max = await self.api.get_setting(ctx, "max_results")
        self.max_results = int(raw_max) if raw_max and raw_max.strip().isdigit() else 10

    async def _on_leave_plugin_query(self, ctx: Context) -> None:
        self._query_generation += 1
        await self._clear_status(ctx)

    async def _show_status(self, ctx: Context, text: str) -> None:
        if self.api and hasattr(self.api, "show_toolbar_msg"):
            msg = ToolbarMsg(
                id=self.TOOLBAR_MSG_ID,
                title=text,
                icon=WoxImage.new_svg(LINKDING_ICON_SVG),
            )
            await self.api.show_toolbar_msg(ctx, msg)

    async def _clear_status(self, ctx: Context) -> None:
        if self.api and hasattr(self.api, "clear_toolbar_msg"):
            await self.api.clear_toolbar_msg(ctx, self.TOOLBAR_MSG_ID)

    async def _on_setting_changed(self, ctx: Context, key: str, value: str) -> None:
        if key in ("linkding_url", "api_token"):
            self._query_generation += 1
            self._favicon_cache.clear()
            for task in self._favicon_downloads.values():
                task.cancel()
            self._favicon_downloads.clear()
        if key == "linkding_url":
            self.linkding_url = value.strip().rstrip("/") if value else ""
            self._tag_cache = None
            self._tag_cache_time = 0.0
            self._cooccurring_tag_cache.clear()
            self._bookmark_cache.clear()
            self._last_bookmark_query = ""
            self._last_bookmarks = []
        elif key == "api_token":
            self.api_token = value.strip() if value else ""
            self._tag_cache = None
            self._tag_cache_time = 0.0
            self._cooccurring_tag_cache.clear()
            self._bookmark_cache.clear()
            self._last_bookmark_query = ""
            self._last_bookmarks = []
        elif key == "max_results":
            self.max_results = int(value) if value and value.strip().isdigit() else 10
            self._cooccurring_tag_cache.clear()
            self._bookmark_cache.clear()

    async def query(self, ctx: Context, query: Query) -> QueryResponse:
        self._query_generation += 1
        generation = self._query_generation
        response = await self._query(ctx, query)
        self._prepare_favicons(ctx, response, generation)
        return response

    def _bookmark_icon(self, bookmark: Dict[str, Any]) -> WoxImage:
        url = bookmark.get("favicon_url")
        return WoxImage.new_url(url) if url else WoxImage.new_svg(LINKDING_ICON_SVG)

    def _prepare_favicons(self, ctx: Context, response: QueryResponse, generation: int) -> None:
        # URL icons are internal markers until replaced with cached data or the
        # Linkding SVG. Never delegate the fallback to Wox's generic placeholder.
        for result in response.results:
            preview_data = (
                WoxPreviewListData.from_json(json.loads(result.preview.preview_data))
                if result.preview.preview_type == WoxPreviewType.LIST
                else None
            )
            icons = [result.icon]
            if preview_data:
                icons.extend(item.icon for item in preview_data.items if item.icon)
            pending: List[tuple[WoxImage, str]] = []
            for icon in icons:
                if icon.image_type != WoxImageType.URL:
                    continue
                url = icon.image_data
                cached = self._favicon_cache.get(url)
                fresh = cached is not None and time.time() - cached[0] < self.FAVICON_CACHE_TTL
                replacement = cached[1] if fresh and cached else None
                replacement = replacement or WoxImage.new_svg(LINKDING_ICON_SVG)
                icon.image_type, icon.image_data = replacement.image_type, replacement.image_data
                if not fresh:
                    pending.append((icon, url))
            if preview_data:
                result.preview.preview_data = preview_data.to_json()
            if pending and generation == self._query_generation:
                task = asyncio.create_task(
                    self._refresh_favicons(ctx, result, preview_data, pending, generation)
                )
                self._favicon_refreshes.add(task)
                task.add_done_callback(self._favicon_refreshes.discard)

    async def _refresh_favicons(
        self, ctx: Context, result: Result, preview_data: Optional[WoxPreviewListData],
        pending: List[tuple[WoxImage, str]], generation: int,
    ) -> None:
        images = await asyncio.gather(*(self._get_favicon(url) for _, url in pending))
        if generation != self._query_generation or not self.api:
            return
        changed = False
        for (icon, _), image in zip(pending, images):
            if image:
                icon.image_type, icon.image_data = image.image_type, image.image_data
                changed = True
        if not changed:
            return
        if preview_data:
            result.preview.preview_data = preview_data.to_json()
        try:
            update = UpdatableResult(
                id=result.id,
                icon=result.icon if any(icon is result.icon for icon, _ in pending) else None,
                preview=result.preview if preview_data else None,
            )
            # A fast download can finish before Wox has displayed the initial
            # response. Retry briefly without refreshing or reopening the query.
            for _ in range(5):
                if generation != self._query_generation:
                    return
                if await self.api.update_result(ctx, update):
                    return
                await asyncio.sleep(0.1)
        except Exception:
            # A closed launcher or disconnected host must not break future queries.
            return

    async def _get_favicon(self, url: str) -> Optional[WoxImage]:
        cached = self._favicon_cache.get(url)
        if cached and time.time() - cached[0] < self.FAVICON_CACHE_TTL:
            return cached[1]
        task = self._favicon_downloads.get(url)
        if task is None:
            task = asyncio.create_task(self._download_favicon(url))
            self._favicon_downloads[url] = task
        return await asyncio.shield(task)

    async def _download_favicon(self, url: str) -> Optional[WoxImage]:
        try:
            image = await asyncio.to_thread(self._fetch_favicon_http, url)
            self._favicon_cache[url] = (time.time(), image)
            return image
        finally:
            if self._favicon_downloads.get(url) is asyncio.current_task():
                self._favicon_downloads.pop(url, None)

    def _fetch_favicon_http(self, url: str) -> Optional[WoxImage]:
        # Favicons are static resources, not API calls. In particular, never send
        # the API token to a favicon URL or its redirects.
        request = urllib.request.Request(url, headers={"Accept": "image/*", "User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                data = response.read()
                mime = response.headers.get_content_type()
            if not data or not mime.startswith("image/"):
                return None
            if mime == "image/svg+xml":
                return WoxImage.new_svg(data.decode("utf-8"))
            encoded = base64.b64encode(data).decode("ascii")
            return WoxImage.new_base64(f"data:{mime};base64,{encoded}")
        except (OSError, ValueError, http.client.HTTPException):
            return None

    async def _query(self, ctx: Context, query: Query) -> QueryResponse:
        is_selection = query.type == QueryType.SELECTION
        if is_selection:
            raw_search = (
                query.selection.text
                if query.selection and query.selection.type == SelectionType.TEXT
                else ""
            )
        else:
            raw_search = query.search or ""
        search_text = raw_search.strip()

        if not search_text:
            await self._clear_status(ctx)
            sub_title = (
                f"Linkding: {self.linkding_url}"
                if self.linkding_url
                else "i18n:prompt_empty_search"
            )
            layout = QueryLayout(result_preview_width_ratio=0.6) if is_selection else QueryLayout()
            return QueryResponse(
                results=[
                    Result(
                        id="prompt:empty",
                        title="i18n:prompt_empty_search",
                        sub_title=sub_title,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )

        # Smart pattern recognition (ADR-0002)
        # URLs trigger bookmark creation; # prefixes trigger tag exploration
        url, _ = self._parse_url_and_tags(search_text)
        if url:
            await self._clear_status(ctx)
            if is_selection:
                return await self._handle_url_input(ctx, search_text, is_selection=True)
            return await self._handle_url_input(ctx, search_text)

        if not is_selection:
            tokens = raw_search.split()
            is_typing_tag = False
            tag_prefix = ""
            selected_tags: set[str] = set()
            raw_prefix = ""

            if search_text == "#":
                is_typing_tag = True
                tag_prefix = ""
                raw_prefix = ""
            elif not raw_search.endswith(" ") and tokens and tokens[-1].startswith("#"):
                is_typing_tag = True
                last_token = tokens[-1]
                tag_prefix = last_token[1:]
                last_hash_idx = raw_search.rfind("#")
                raw_prefix = raw_search[:last_hash_idx]
                selected_tags = set(re.findall(r"#([^\s#]+)", raw_prefix))

            if is_typing_tag:
                return await self._handle_tag_browsing(
                    ctx, query, tag_prefix, selected_tags=selected_tags, raw_prefix=raw_prefix
                )

        if is_selection:
            await self._clear_status(ctx)
            return await self._handle_selection_bookmark_search(ctx, query, search_text)

        return await self._search_bookmarks(ctx, search_text)

    async def _search_bookmarks(self, ctx: Context, search_text: str) -> QueryResponse:
        encoded_q = urllib.parse.quote(search_text)
        cache_key = search_text.strip()
        now = time.time()
        cached = self._bookmark_cache.get(cache_key)
        if cached is not None and (now - cached[0]) < self.BOOKMARK_CACHE_TTL:
            resp_data = cached[1]
        else:
            req_url = f"{self.linkding_url}/api/bookmarks/?q={encoded_q}&limit={self.max_results}"
            req = self._create_request(req_url)

            try:
                resp_data = await asyncio.to_thread(self._fetch_bookmarks_http, req)
                self._bookmark_cache[cache_key] = (now, resp_data)
            except urllib.error.HTTPError as e:
                await self._clear_status(ctx)
                if e.code in (401, 403):
                    return QueryResponse(
                        results=[
                            Result(
                                id="error:auth",
                                title="i18n:error_auth_failed",
                                sub_title="i18n:error_auth_failed_sub",
                                icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                            )
                        ]
                    )
                return QueryResponse(
                    results=[
                        Result(
                            id="error:api",
                            title=f"Linkding API Error (HTTP {e.code})",
                            sub_title=str(e.reason),
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )
            except urllib.error.URLError as e:
                await self._clear_status(ctx)
                reason_str = str(e.reason)
                if "timed out" in reason_str.lower() or isinstance(e.reason, TimeoutError):
                    return QueryResponse(
                        results=[
                            Result(
                                id="error:timeout",
                                title="i18n:error_timeout",
                                sub_title="i18n:error_timeout_sub",
                                icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                            )
                        ]
                    )
                return QueryResponse(
                    results=[
                        Result(
                            id="error:network",
                            title="i18n:error_network",
                            sub_title=reason_str,
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )
            except TimeoutError:
                await self._clear_status(ctx)
                return QueryResponse(
                    results=[
                        Result(
                            id="error:timeout",
                            title="i18n:error_timeout",
                            sub_title="i18n:error_timeout_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )
            except Exception as e:
                await self._clear_status(ctx)
                return QueryResponse(
                    results=[
                        Result(
                            id="error:generic",
                            title="Error searching bookmarks",
                            sub_title=str(e),
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )

        raw_bookmarks: List[Dict[str, Any]] = resp_data.get("results", [])
        self._last_bookmark_query = search_text
        self._last_bookmarks = raw_bookmarks
        total_count = resp_data.get("count", len(raw_bookmarks))
        bm_template = (
            await self.api.get_translation(ctx, "toolbar_bookmarks_found")
            if self.api
            else "{count} bookmarks found"
        )
        await self._show_status(ctx, bm_template.format(count=total_count))

        web_search_url = f"{self.linkding_url}/bookmarks?q={encoded_q}"

        if not raw_bookmarks:
            return QueryResponse(
                results=[
                    Result(
                        id="bookmark:empty",
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

        page_count = len(raw_bookmarks)
        results: List[Result] = []
        for index, item in enumerate(raw_bookmarks):
            bm_id = item.get("id")
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

            result_id = f"bookmark:{bm_id}" if bm_id is not None else f"bookmark:{bm_url}"
            initial_score = float(page_count - index)
            results.append(
                Result(
                    id=result_id,
                    title=title,
                    sub_title=sub_title,
                    icon=self._bookmark_icon(item),
                    score=initial_score,
                    actions=actions,
                )
            )

        return QueryResponse(results=results)

    async def _handle_selection_bookmark_search(
        self, ctx: Context, query: Query, search_text: str
    ) -> QueryResponse:
        layout = QueryLayout(result_preview_width_ratio=0.6)
        encoded_q = urllib.parse.quote(search_text)
        req_url = f"{self.linkding_url}/api/bookmarks/?q={encoded_q}&limit={self.max_results}"
        req = self._create_request(req_url)

        try:
            resp_data = await asyncio.to_thread(self._fetch_bookmarks_http, req)
            # Query expansion uses the same response through the regular search cache.
            self._bookmark_cache[search_text] = (time.time(), resp_data)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                return QueryResponse(
                    results=[
                        Result(
                            id="error:auth",
                            title="i18n:error_auth_failed",
                            sub_title="i18n:error_auth_failed_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ],
                    layout=layout,
                )
            return QueryResponse(
                results=[
                    Result(
                        id="error:api",
                        title=f"Linkding API Error (HTTP {e.code})",
                        sub_title=str(e.reason),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )
        except urllib.error.URLError as e:
            reason_str = str(e.reason)
            if "timed out" in reason_str.lower() or isinstance(e.reason, TimeoutError):
                return QueryResponse(
                    results=[
                        Result(
                            id="error:timeout",
                            title="i18n:error_timeout",
                            sub_title="i18n:error_timeout_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ],
                    layout=layout,
                )
            return QueryResponse(
                results=[
                    Result(
                        id="error:network",
                        title="i18n:error_network",
                        sub_title=reason_str,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )
        except TimeoutError:
            return QueryResponse(
                results=[
                    Result(
                        id="error:timeout",
                        title="i18n:error_timeout",
                        sub_title="i18n:error_timeout_sub",
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )
        except Exception as e:
            return QueryResponse(
                results=[
                    Result(
                        id="error:generic",
                        title="Error searching bookmarks",
                        sub_title=str(e),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )

        raw_bookmarks: List[Dict[str, Any]] = resp_data.get("results", [])
        web_search_url = f"{self.linkding_url}/bookmarks?q={encoded_q}"
        trigger_keyword = query.trigger_keyword
        actions = [
            ResultAction(
                name="i18n:selection_action_expand",
                icon=WoxImage.new_svg(ACTION_SEARCH_SVG),
                is_default=True,
                prevent_hide_after_action=True,
                action=self._create_change_query_action(trigger_keyword, search_text),
            ),
            ResultAction(
                name="i18n:action_open_in_linkding",
                icon=WoxImage.new_svg(ACTION_OPEN_SVG),
                is_default=False,
                action=self._create_open_url_action(web_search_url),
            ),
        ]

        if not raw_bookmarks:
            empty_item = WoxPreviewListItem(
                icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                title="i18n:no_bookmarks_found",
                subtitle="i18n:selection_press_enter_to_edit",
            )
            preview = WoxPreview(
                preview_type=WoxPreviewType.LIST,
                preview_data=WoxPreviewListData(items=[empty_item]).to_json(),
            )
            return QueryResponse(
                results=[
                    Result(
                        id="bookmark:empty",
                        title="i18n:no_bookmarks_found",
                        sub_title="i18n:selection_press_enter_to_edit",
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        preview=preview,
                        actions=actions,
                    )
                ],
                layout=layout,
            )

        preview_items: List[WoxPreviewListItem] = []
        for bm in raw_bookmarks[: self.max_results]:
            tails = [
                ResultTail(type=ResultTailType.TEXT, text=f"#{t}")
                for t in bm.get("tag_names", [])
            ]
            bm_title = bm.get("title") or bm.get("website_title") or bm.get("url") or ""
            bm_url = bm.get("url", "")
            preview_items.append(
                WoxPreviewListItem(
                    icon=self._bookmark_icon(bm),
                    title=bm_title,
                    subtitle=bm_url,
                    tails=tails,
                )
            )

        preview = WoxPreview(
            preview_type=WoxPreviewType.LIST,
            preview_data=WoxPreviewListData(items=preview_items).to_json(),
        )

        found_template = (
            await self.api.get_translation(ctx, "selection_bookmarks_found")
            if self.api
            else "Linkding: {count} bookmarks found"
        )
        count = len(raw_bookmarks)
        try:
            title = found_template.format(count=count)
        except Exception:
            title = f"Linkding: {count} bookmarks found"

        return QueryResponse(
            results=[
                Result(
                    id="selection:bookmarks",
                    title=title,
                    sub_title="i18n:selection_press_enter_to_expand",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    preview=preview,
                    actions=actions,
                )
            ],
            layout=layout,
        )

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

    def _create_change_query_action(self, trigger_keyword: str, search_text: str):
        async def _action(ctx: Context, action_ctx: ActionContext) -> None:
            if self.api:
                kw = trigger_keyword
                if not kw:
                    # Unscoped selection queries do not carry a trigger keyword.
                    configured_keywords = json.loads(
                        await self.api.get_setting(ctx, "TriggerKeywords") or "[]"
                    )
                    kw = next((keyword for keyword in configured_keywords if keyword != "*"), "ld")
                await self.api.change_query(
                    ctx,
                    ChangeQueryParam(
                        query_type=QueryType.INPUT,
                        query_text=f"{kw} {search_text}",
                    ),
                )

        return _action

    def _normalize_url(self, token: str) -> Optional[str]:
        if re.match(r"^https?://", token, re.IGNORECASE):
            return token
        if LOCALHOST_REGEX.match(token) or token.startswith("127.0.0.1"):
            if IPV4_REGEX.match(token) or LOCALHOST_REGEX.match(token):
                return f"http://{token}"
        if IPV4_REGEX.match(token) or DOMAIN_REGEX.match(token):
            return f"https://{token}"
        return None

    def _parse_url_and_tags(self, input_text: str) -> tuple[str, List[str]]:
        parts = input_text.strip().split()
        if not parts:
            return "", []

        first = parts[0]
        normalized = self._normalize_url(first)
        if not normalized:
            return "", []

        is_explicit_scheme = bool(re.match(r"^https?://", first, re.IGNORECASE))
        remaining = parts[1:]

        tags: List[str] = []
        for p in remaining:
            if p.startswith("#"):
                if len(p) > 1:
                    tag = p[1:].strip()
                    if tag and tag not in tags:
                        tags.append(tag)
            else:
                if not is_explicit_scheme:
                    return "", []

        return normalized, tags

    async def _handle_url_input(
        self, ctx: Context, search_text: str, is_selection: bool = False
    ) -> QueryResponse:
        layout = QueryLayout(result_preview_width_ratio=0.6) if is_selection else QueryLayout()
        url, tags = self._parse_url_and_tags(search_text)
        if not url:
            return QueryResponse(results=[], layout=layout)

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
                            id="error:auth",
                            title="i18n:error_auth_failed",
                            sub_title="i18n:error_auth_failed_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ],
                    layout=layout,
                )
            return QueryResponse(
                results=[
                    Result(
                        id="error:api",
                        title=f"Linkding API Error (HTTP {e.code})",
                        sub_title=str(e.reason),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )
        except urllib.error.URLError as e:
            reason_str = str(e.reason)
            if "timed out" in reason_str.lower() or isinstance(e.reason, TimeoutError):
                return QueryResponse(
                    results=[
                        Result(
                            id="error:timeout",
                            title="i18n:error_timeout",
                            sub_title="i18n:error_timeout_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ],
                    layout=layout,
                )
            return QueryResponse(
                results=[
                    Result(
                        id="error:network",
                        title="i18n:error_network",
                        sub_title=reason_str,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )
        except TimeoutError:
            return QueryResponse(
                results=[
                    Result(
                        id="error:timeout",
                        title="i18n:error_timeout",
                        sub_title="i18n:error_timeout_sub",
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )
        except Exception as e:
            return QueryResponse(
                results=[
                    Result(
                        id="error:generic",
                        title="Error checking bookmark",
                        sub_title=str(e),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ],
                layout=layout,
            )

        existing_bookmark = check_data.get("bookmark")
        if existing_bookmark:
            existing_id = existing_bookmark.get("id")
            result_id = f"bookmark:{existing_id}" if existing_id is not None else f"bookmark:{url}"
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

            preview = WoxPreview()
            if is_selection:
                tags_md = " ".join(f"`#{t}`" for t in bm_tags) if bm_tags else "无"
                md_content = (
                    "### ⚠️ 该 URL 已收藏\n"
                    f"- **标题**：{title}\n"
                    f"- **网址**：`{url}`\n"
                    f"- **已有标签**：{tags_md}"
                )
                preview = WoxPreview(
                    preview_type=WoxPreviewType.MARKDOWN,
                    preview_data=md_content,
                )

            return QueryResponse(
                results=[
                    Result(
                        id=result_id,
                        title=title,
                        sub_title=sub_title,
                        icon=self._bookmark_icon(existing_bookmark),
                        preview=preview,
                        actions=actions,
                    )
                ],
                layout=layout,
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

        preview = WoxPreview()
        if is_selection:
            tags_md = " ".join(f"`#{t}`" for t in tags) if tags else "无"
            md_content = (
                "### 🔖 保存书签至 Linkding\n"
                f"- **目标网址**：`{url}`\n"
                f"- **标签**：{tags_md}\n"
                "> 按 Enter 立即保存，Linkding 将在后台自动抓取网页标题和描述"
            )
            preview = WoxPreview(
                preview_type=WoxPreviewType.MARKDOWN,
                preview_data=md_content,
            )

        return QueryResponse(
            results=[
                Result(
                    id=f"bookmark:save:{url}",
                    title="i18n:prompt_save_bookmark",
                    sub_title=sub_title,
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    preview=preview,
                    actions=actions,
                )
            ],
            layout=layout,
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
                self._bookmark_cache.clear()
                self._cooccurring_tag_cache.clear()
                self._last_bookmark_query = ""
                self._last_bookmarks = []
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

    async def _get_cooccurring_tags(self, ctx: Context, raw_prefix: str) -> Dict[str, int]:
        prefix_query = raw_prefix.strip()
        if not prefix_query:
            return {}

        now = time.time()
        cached = self._cooccurring_tag_cache.get(prefix_query)
        if cached is not None and (now - cached[0]) < self.COOCCURRING_TAG_CACHE_TTL:
            return cached[1]

        if self._last_bookmark_query == prefix_query and self._last_bookmarks:
            bookmarks = self._last_bookmarks
        else:
            encoded_q = urllib.parse.quote(prefix_query)
            req_url = f"{self.linkding_url}/api/bookmarks/?q={encoded_q}&limit=100"
            req = self._create_request(req_url)
            resp_data = await asyncio.to_thread(self._fetch_bookmarks_http, req)
            bookmarks = resp_data.get("results", [])

        tag_counts: Dict[str, int] = {}
        for bm in bookmarks:
            for tag in bm.get("tag_names", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        self._cooccurring_tag_cache[prefix_query] = (now, tag_counts)
        return tag_counts

    async def _handle_tag_browsing(
        self,
        ctx: Context,
        query: Query,
        tag_prefix: str,
        selected_tags: Optional[set[str]] = None,
        raw_prefix: str = "",
    ) -> QueryResponse:
        is_cooccurring = bool(raw_prefix.strip())
        tag_counts: Dict[str, int] = {}

        try:
            if is_cooccurring:
                tag_counts = await self._get_cooccurring_tags(ctx, raw_prefix)
                tags = list(tag_counts.keys())
            else:
                tags = await self._get_tags(ctx)
        except urllib.error.HTTPError as e:
            await self._clear_status(ctx)
            if e.code in (401, 403):
                return QueryResponse(
                    results=[
                        Result(
                            id="error:auth",
                            title="i18n:error_auth_failed",
                            sub_title="i18n:error_auth_failed_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )
            return QueryResponse(
                results=[
                    Result(
                        id="error:api",
                        title=f"Linkding API Error (HTTP {e.code})",
                        sub_title=str(e.reason),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )
        except urllib.error.URLError as e:
            await self._clear_status(ctx)
            reason_str = str(e.reason)
            if "timed out" in reason_str.lower() or isinstance(e.reason, TimeoutError):
                return QueryResponse(
                    results=[
                        Result(
                            id="error:timeout",
                            title="i18n:error_timeout",
                            sub_title="i18n:error_timeout_sub",
                            icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                        )
                    ]
                )
            return QueryResponse(
                results=[
                    Result(
                        id="error:network",
                        title="i18n:error_network",
                        sub_title=reason_str,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )
        except TimeoutError:
            await self._clear_status(ctx)
            return QueryResponse(
                results=[
                    Result(
                        id="error:timeout",
                        title="i18n:error_timeout",
                        sub_title="i18n:error_timeout_sub",
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )
        except Exception as e:
            await self._clear_status(ctx)
            return QueryResponse(
                results=[
                    Result(
                        id="error:generic",
                        title="Error fetching tags",
                        sub_title=str(e),
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )

        selected_lower = {s.lower() for s in selected_tags} if selected_tags else set()
        if tag_prefix:
            prefix_lower = tag_prefix.lower()
            filtered_tags = [
                t for t in tags
                if t.lower().startswith(prefix_lower) and t.lower() not in selected_lower
            ]
        else:
            filtered_tags = [t for t in tags if t.lower() not in selected_lower]

        if is_cooccurring:
            matching_tags = sorted(filtered_tags, key=lambda t: (-tag_counts.get(t, 0), t.lower()))
        else:
            matching_tags = filtered_tags

        tags_template = (
            await self.api.get_translation(ctx, "toolbar_tags_found")
            if self.api
            else "{count} tags found"
        )
        await self._show_status(ctx, tags_template.format(count=len(matching_tags)))

        if not matching_tags:
            if not is_cooccurring and not tags:
                title = "i18n:no_tags_found"
                sub_title = "i18n:no_tags_found_sub"
            else:
                title = "i18n:no_matching_tags"
                sub_title = f"{raw_prefix}#{tag_prefix}" if is_cooccurring else f"#{tag_prefix}"

            return QueryResponse(
                results=[
                    Result(
                        id="tag:empty",
                        title=title,
                        sub_title=sub_title,
                        icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    )
                ]
            )

        trigger = query.trigger_keyword or "ld"
        results: List[Result] = []
        total_matching = len(matching_tags)
        for index, tag in enumerate(matching_tags[: self.max_results]):
            actions = [
                ResultAction(
                    name="i18n:tag_action_select",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    is_default=True,
                    prevent_hide_after_action=True,
                    action=self._create_select_tag_action(tag, trigger, raw_prefix),
                ),
            ]
            tails: List[ResultTail] = []
            if is_cooccurring and tag in tag_counts:
                tails.append(
                    ResultTail(
                        type=ResultTailType.TEXT,
                        text=str(tag_counts[tag]),
                        text_category=ResultTailTextCategory.DEFAULT,
                    )
                )

            tag_score = float(tag_counts.get(tag, 0)) if is_cooccurring else float(total_matching - index)

            results.append(
                Result(
                    id=f"tag:{tag}",
                    title=f"#{tag}",
                    sub_title="",
                    icon=WoxImage.new_svg(LINKDING_ICON_SVG),
                    tails=tails,
                    score=tag_score,
                    actions=actions,
                )
            )

        return QueryResponse(results=results)

    def _create_select_tag_action(self, tag: str, trigger_keyword: str, raw_prefix: str = ""):
        async def _action(ctx: Context, action_ctx: ActionContext) -> None:
            if self.api:
                kw = trigger_keyword or "ld"
                await self.api.change_query(
                    ctx,
                    ChangeQueryParam(
                        query_type=QueryType.INPUT,
                        query_text=f"{kw} {raw_prefix}#{tag} ",
                    ),
                )

        return _action


plugin = LinkdingPlugin()


