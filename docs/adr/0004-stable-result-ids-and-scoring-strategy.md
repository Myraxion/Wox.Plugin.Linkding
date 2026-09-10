# Assign Stable Semantic Result IDs and Retain Wox Auto-Scoring with Positional Baselines

We decided to assign explicit, stable, and semantic `Result.id` attributes across all plugin query results, assign baseline initial scores (`Result.score`) for bookmarks and tags, and opt out of `ignoreAutoScore` (retaining Wox's native frequency-based auto-scoring).

In Wox, leaving `Result.id` empty causes the launcher core to assign a newly generated random UUID to each item on every query stroke. This churn prevents cross-query identity tracking and makes dynamic result updates via `update_result` impossible. Assigning deterministic IDs (`bookmark:<id>`, `tag:<name>`, `prompt:*`, `error:*`) ensures stable entity identity across typing queries.

Furthermore, internal examination of Wox's `compareQueryResultCachesForDisplay` reveals that Wox stores query results in a hash map and sorts them by `Result.Score` descending. When scores are equal (e.g. all 0.0), Wox falls back to `strings.Compare(a.Result.Title, b.Result.Title)` (ascending alphabetical sort). This fallback inadvertently destroyed Linkding's native order (newest-added bookmarks first, or API search relevance) and broke frequency-based co-occurring tag rankings.

To address this without disabling Wox's adaptive learning:
1. **Co-occurring Tags**: Map associated bookmark counts directly to `Result.score = float(tag_counts[tag])`. Tags with higher counts naturally rank higher, and equal-count tags gracefully fall back to Wox's alphabetical tie-breaking.
2. **Global Tags**: Assign descending positional baseline scores (`score = float(len(matching_tags) - index)`) to preserve the order returned by Linkding's tags API against arbitrary alphabetical shuffling.
3. **Bookmarks**: Assign descending positional baseline scores (`score = float(len(raw_bookmarks) - index)`). This guarantees that initial/fresh search results faithfully preserve Linkding's server-side ranking (latest added or relevance), while allowing frequently actioned bookmarks to accumulate Wox's 7-day Fibonacci historical usage weights (+5 to +89 per action) and float toward the top.

## Considered Options

- **Omit `Result.id` and keep initial score at 0.0**: Simplest code, but causes unstable item identity and triggers Wox's alphabetical Title sort fallback, wiping out Linkding's recency and relevance rankings.
- **Enable `ignoreAutoScore` and compute client-side relevance scores**: Forces strict adherence to Linkding API results without any Wox intervention, but disables launcher-wide frequency learning for frequently revisited bookmarks.
- **Assign stable semantic IDs, baseline positional scores, and retain native Wox auto-scoring (chosen)**: Gives every item a deterministic ID, preserves Linkding's server-side API ranking as the baseline via positional/frequency scores, and retains Wox's frequency-based learning for frequently launched bookmarks.

