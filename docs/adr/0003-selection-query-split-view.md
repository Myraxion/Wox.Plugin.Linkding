# Consolidate Selection Query Matches into Single Aggregation Entry with Split Preview

We decided to return a single persistent aggregation entry immediately during keyword Selection Queries, with a 0.4:0.6 split preview panel. Bookmark searches run in the background and update that entry in place. Pressing Enter expands the query into `<trigger> <keyword>` for interactive bookmark selection in Wox. The action panel (`Ctrl+J`) provides Linkding web search as a secondary action.

## Context & Problem Statement

When a user invokes Wox via text selection (`QueryType.SELECTION`), Wox broadcasts the query across all installed plugins supporting the `querySelection` feature (e.g. Translation, Search, Linkding). Returning multiple individual bookmark items directly into the global selection result list clutters the UI and pushes other plugins out of view. Conversely, hiding matches or returning a plain text prompt loses immediate visibility into whether relevant bookmarks exist.

Furthermore, Wox's preview panel (`WoxPreview`) is a read-only presentation view where keyboard focus cannot directly navigate individual rows.

## Considered Options

1. **Flat multi-item return**: Return every matched bookmark directly into the selection result list.
   - *Pros*: Direct Enter key opens individual bookmarks immediately.
   - *Cons*: Clutters the multi-plugin selection interface; pushes other plugins' results down.
2. **Single aggregation entry with split preview (`WoxPreviewType.LIST`) & query expansion**:
   - Left list immediately contains one entry with a fixed title (`Linkding Bookmarks`). Match counts and search state appear in its subtitle.
   - Right preview panel (ratio 0.6) renders structured items with titles, URLs, and tag badges (`tails`).
   - Enter expands the query (`api.change_query("<trigger> <keyword>")`) so users can select and open a bookmark in Wox.
   - `Ctrl+J` action panel retains Linkding web search as a secondary action.
   - *Pros*: Clean integration with global selection UI, instant visual feedback of matches, and a discoverable keyboard path to bookmark selection.
   - *Cons*: Opening a specific bookmark requires entering the expanded query first.

## Decision

We chose Option 2. This maintains a clean launcher footprint in multi-plugin environments while leveraging Wox's native preview panel and `change_query` capability for a cohesive, fast user experience.

On 2026-10-20, we revised the default action from opening Linkding web search to query expansion. The primary task is selecting a matched bookmark in Wox; placing expansion behind the action panel made that task harder to discover. The single aggregation entry and read-only preview remain unchanged.

We also made the entry persistent across loading, matched, empty, and failed states. Waiting for the network before returning the entry caused it to be inserted late among other plugins' results. The entry now uses the same identity (`selection:bookmarks`), title, and baseline score throughout. Background completion uses `UpdateResult` to patch its subtitle, preview, and actions without adding or removing rows or changing the title or score.

## Agreed Interaction

This interaction applies to keyword searches invoked through Selection Query. Selected URLs continue to use the existing duplicate-checking and bookmark-saving flow.

| Matched bookmarks | Selection entry | Default Enter action |
| --- | --- | --- |
| Query in progress | One entry showing that bookmarks are being searched | Continue the same pending query, then expand; do not issue another request |
| Multiple | One aggregation entry with a read-only bookmark preview | Expand into `<trigger> <keyword>` for bookmark selection |
| One | The same aggregation entry and preview | Expand first; do not open the bookmark directly |
| None | One entry showing no matches | Expand into `<trigger> <keyword>` so the user can edit the search terms |
| Query failed | The same entry showing a translated error in its subtitle and preview | No bookmark actions are offered |

Loading and successful entries have exactly two actions: expand the bookmark query (default) and search in the Linkding web interface (secondary). Individual bookmark actions remain available on the expanded results.

The title remains “Linkding Bookmarks” in every state. Loading uses “Searching bookmarks…”; matched bookmarks show the count and “Press Enter to select a bookmark”; no matches use “No bookmarks found · Press Enter to edit search terms”. Provide both English and Chinese translations.

Query expansion must keep Wox visible (`prevent_hide_after_action=True`) so the user can immediately navigate or edit the expanded query.

Successful selection searches populate the existing 30-second bookmark response cache, including empty responses. Expanding the same search reuses that response while it is fresh instead of issuing another HTTP request. Changed search terms, expired entries, and existing settings or bookmark-save invalidation rules continue to govern subsequent requests.

The trigger must honor the user's Wox configuration. Use the query's trigger when present. Unscoped selection queries carry no trigger, so resolve the `TriggerKeywords` setting while building the aggregation entry and choose the first non-global keyword. Capture that resolved trigger in the action so pressing Enter only changes the query, without waiting for a settings read. Configuration changes take effect on the next aggregation query. Use the metadata default `ld` only when no custom trigger is configured.

The initial loading entry returns before network or settings calls. Trigger resolution is part of the background query; completed entries capture the resolved trigger. An early Enter shares the pending task. A new plugin query, leaving the plugin, or changing connection credentials or result limits cancels obsolete selection work. Image updates wait until the initial content update has been published. If that update exhausts its retries or the host disconnects, subsequent image updates for the entry stop as well. Pending expansion stops if the host rejects the original row update or the launcher is hidden.

Wox controls cross-plugin query transitions and ordering. Unscoped selection queries do not always receive plugin-leave callbacks, and Wox can retain an old row for roughly 200 ms during a query transition. Its update API checks the row ID rather than the current query ID, so the plugin cannot fully eliminate that host transition window. Strict cross-plugin transition guarantees require a host change.
