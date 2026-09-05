# Use Single-File Python SDK Plugin Architecture

We decided to build this plugin as a single-file Python SDK plugin (`Wox.Plugin.Linkding.py`) rather than a packaged multi-file `.wox` extension or a process-per-query script plugin. The linkding REST API only requires HTTP communication, which is fully covered by Python's standard library (`urllib.request` and `json`), eliminating the need for third-party dependencies while benefiting from Wox 2.4.2+ in-process execution, instant file-save reloading, and minimal maintenance overhead.

## Considered Options

- **Packaged Node.js / Python SDK plugin (`.wox`)**: Allowed external dependencies and multi-file architecture, but added build steps, packaging tooling, and slower development iteration cycles.
- **Script plugin (process-per-query)**: Stateless and short-lived, but lacked persistent memory caching for tags, had higher process startup latency per keystroke, and provided limited Public API integration.
- **Single-file Python SDK plugin**: Chosen for zero-dependency portability, access to the full Public API, memory-cached tags, and instant reload on file save.
