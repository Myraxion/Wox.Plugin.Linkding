# Assign Stable Semantic Result IDs and Retain Wox Auto-Scoring

We decided to assign explicit, stable, and semantic `Result.id` attributes across all plugin query results, while keeping the plugin's initial result score at `0.0` and opting out of `ignoreAutoScore` (retaining Wox's native frequency-based auto-scoring).

In Wox, leaving `Result.id` empty causes the launcher core to assign a newly generated random UUID to each item on every query stroke. This churn prevents cross-query identity tracking and makes dynamic result updates via `update_result` impossible. Assigning deterministic IDs (`bookmark:<id>`, `tag:<name>`, `prompt:*`, `error:*`) ensures stable entity identity across typing queries.

Concurrently, we evaluated whether to declare the `ignoreAutoScore` feature or compute custom local relevance scores. Linkding is a search-oriented bookmark launcher where users frequently revisit a small subset of bookmarks. Retaining Wox's default auto-scoring allows the launcher to adapt to usage patterns (using time-decayed Fibonacci weights) so high-frequency bookmarks naturally float to the top, while initial zero scoring ensures strict adherence to Linkding's server-side ranking for new queries.

## Considered Options

- **Omit `Result.id` and let Wox assign random UUIDs**: Simplest plugin code, but causes unstable item identity across query keystrokes and impedes stateful launcher interactions.
- **Enable `ignoreAutoScore` and compute client-side relevance scores**: Forces strict sorting by plugin logic, but duplicates Linkding server-side fuzzy matching and disables Wox's adaptive learning for frequently used bookmarks.
- **Assign stable semantic IDs and retain native Wox auto-scoring (chosen)**: Gives every item a deterministic, namespaced ID based on Linkding entities, preserves server-side API ranking as the baseline, and benefits from Wox's frequency-based learning for frequently launched bookmarks.
