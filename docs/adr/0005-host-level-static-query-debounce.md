# Use Host-Level Static Query Debounce of 200ms Instead of Dynamic Setting

We decided to set the query debounce interval to 200ms directly in the plugin manifest (`Features.debounce.Params.IntervalMs: 200`) rather than exposing it as a user setting in `SettingDefinitions`. Wox manages typing debounce at the launcher UI host level via static metadata declarations; the Public API does not support dynamic reconfiguration of host features from plugin settings. A 200ms interval achieves the optimal trade-off between perceived input responsiveness and network traffic throttling to self-hosted Linkding instances, while avoiding redundant application-level debounce layers.

## Considered Options

- **Dynamic Setting via Plugin-Level Debounce**: Setting host debounce to 0ms and implementing software debounce inside the Python `query()` coroutine. Rejected because it incurs concurrency overhead, query cancellation edge cases, launcher flicker, and violates the KISS principle.
- **Static Host Debounce at 300ms**: The previous default. Rejected because it introduced perceptible lag when actively typing search keywords.
- **Static Host Debounce at 200ms**: Selected because it provides snappy launcher feedback while reliably throttling intermediate keystroke network calls.
