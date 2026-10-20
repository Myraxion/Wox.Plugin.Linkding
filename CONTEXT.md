# Linkding Plugin

A Wox launcher integration for searching, saving, and managing bookmarks from a self-hosted linkding service.

## Language

**Bookmark**:
A saved web destination containing a URL, descriptive metadata, and optional tags stored within linkding.
_Avoid_: Link, URL, favorite, webmark

**Tag**:
A named text label assigned to bookmarks for categorization and filtering.
_Avoid_: Category, label, folder, topic

**Bundle**:
A dynamic saved search grouping bookmarks based on tag filters and search queries.
_Avoid_: Collection, group, smart folder, playlist

**Asset**:
A stored artifact associated with a bookmark, such as an archived HTML snapshot or an uploaded file.
_Avoid_: Attachment, snapshot, download, media

**Selection Aggregation Entry**:
A consolidated single launcher result representing multiple matched bookmarks when invoking Wox via text selection, avoiding visual clutter in multi-plugin selection menus.
_Avoid_: Group, folder, category result

**Preview Panel**:
A read-only side panel rendered beside the launcher results (via result preview width ratio) displaying structured item lists, tags, or detailed markdown cards.
_Avoid_: Detail window, right column, tooltip

**Query Expansion**:
The interaction of pressing Enter on an aggregation entry to populate the launcher search bar with `ld <keyword>` and immediately execute it as an interactive bookmark query.
_Avoid_: Drill-down, sub-search, page jump

**Result Identity**:
A deterministic, namespaced identifier assigned to launcher results (`bookmark:<id>`, `tag:<name>`, etc.) that preserves item identity across query keystrokes and supports stateful launcher interactions.
_Avoid_: Key, hash, temporary UUID, item index

**Toolbar Status**:
A transient status indicator displayed in the Wox launcher toolbar showing the total count of matched tags or bookmarks for the active query.
_Avoid_: Status bar, bottom tooltip, counter badge

**Co-occurring Tag**:
A tag associated with one or more bookmarks in the currently filtered query subset, ensuring subsequent tag selections never yield zero results.
_Avoid_: Related tag, sub-tag, candidate tag, child tag

**Query Debounce Interval**:
The host-level delay in milliseconds after the user stops typing before the launcher invokes the plugin query, balancing keystroke responsiveness against redundant network requests.
_Avoid_: Delay, debounce time, search pause, typing lag
