# Consolidate Selection Query Matches into Single Aggregation Entry with Split Preview

We decided to present matched bookmarks during Wox Selection Query as a single consolidated aggregation entry with a 0.4:0.6 split preview panel, rather than flooding the multi-plugin selection list with individual bookmark items. Pressing Enter on the aggregation entry expands the query into `<trigger> <keyword>` for interactive bookmark selection in Wox. The action panel (`Ctrl+J`) provides Linkding web search as a secondary action.

## Context & Problem Statement

When a user invokes Wox via text selection (`QueryType.SELECTION`), Wox broadcasts the query across all installed plugins supporting the `querySelection` feature (e.g. Translation, Search, Linkding). Returning multiple individual bookmark items directly into the global selection result list clutters the UI and pushes other plugins out of view. Conversely, hiding matches or returning a plain text prompt loses immediate visibility into whether relevant bookmarks exist.

Furthermore, Wox's preview panel (`WoxPreview`) is a read-only presentation view where keyboard focus cannot directly navigate individual rows.

## Considered Options

1. **Flat multi-item return**: Return every matched bookmark directly into the selection result list.
   - *Pros*: Direct Enter key opens individual bookmarks immediately.
   - *Cons*: Clutters the multi-plugin selection interface; pushes other plugins' results down.
2. **Single aggregation entry with split preview (`WoxPreviewType.LIST`) & query expansion**:
   - Left list contains 1 entry (`Linkding: X bookmarks found`).
   - Right preview panel (ratio 0.6) renders structured items with titles, URLs, and tag badges (`tails`).
   - Enter expands the query (`api.change_query("<trigger> <keyword>")`) so users can select and open a bookmark in Wox.
   - `Ctrl+J` action panel retains Linkding web search as a secondary action.
   - *Pros*: Clean integration with global selection UI, instant visual feedback of matches, and a discoverable keyboard path to bookmark selection.
   - *Cons*: Opening a specific bookmark requires entering the expanded query first.

## Decision

We chose Option 2. This maintains a clean launcher footprint in multi-plugin environments while leveraging Wox's native preview panel and `change_query` capability for a cohesive, fast user experience.

On 2026-10-20, we revised the default action from opening Linkding web search to query expansion. The primary task is selecting a matched bookmark in Wox; placing expansion behind the action panel made that task harder to discover. The single aggregation entry and read-only preview remain unchanged.

## Agreed Interaction

This interaction applies to keyword searches invoked through Selection Query. Selected URLs continue to use the existing duplicate-checking and bookmark-saving flow.

| Matched bookmarks | Selection entry | Default Enter action |
| --- | --- | --- |
| Multiple | One aggregation entry with a read-only bookmark preview | Expand into `<trigger> <keyword>` for bookmark selection |
| One | The same aggregation entry and preview | Expand first; do not open the bookmark directly |
| None | One entry showing no matches | Expand into `<trigger> <keyword>` so the user can edit the search terms |

Every entry above has exactly two actions: expand the bookmark query (default) and search in the Linkding web interface (secondary). Remove actions that open or copy the first match from the aggregation entry. Individual bookmark actions remain available on the expanded results.

For matched bookmarks, the subtitle should communicate “Press Enter to select a bookmark”; for no matches, it should communicate “No bookmarks found · Press Enter to edit search terms”. Provide both English and Chinese translations.

Query expansion must keep Wox visible (`prevent_hide_after_action=True`) so the user can immediately navigate or edit the expanded query.

The trigger must honor the user's Wox configuration. Use the query's trigger when present. Unscoped selection queries carry no trigger, so expansion reads the `TriggerKeywords` setting at action time and chooses the first non-global keyword. Use the metadata default `ld` only when no custom trigger is configured.
