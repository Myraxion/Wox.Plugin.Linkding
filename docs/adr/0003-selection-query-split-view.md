# Consolidate Selection Query Matches into Single Aggregation Entry with Split Preview

We decided to present matched bookmarks during Wox Selection Query as a single consolidated aggregation entry with a 0.4:0.6 split preview panel, rather than flooding the multi-plugin selection list with individual bookmark items. Pressing Enter opens search in the Linkding web interface, while the action panel (`Ctrl+J`) provides query expansion into `ld <keyword>` for full interactive navigation.

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
   - Enter key opens Linkding web search directly, consistent with no-match selection queries.
   - `Ctrl+J` action panel provides immediate access to expand query (`api.change_query("ld <keyword>")`), open first match, or copy URL.
   - *Pros*: Clean integration with global selection UI, instant visual feedback of matches, zero clutter, consistent Enter behavior across all selection queries.
   - *Cons*: Opening a specific bookmark from launcher requires expanding via `Ctrl+J` or clicking.

## Decision

We chose Option 2. This maintains a clean launcher footprint in multi-plugin environments while leveraging Wox's native preview panel and `change_query` capability for a cohesive, fast user experience.
