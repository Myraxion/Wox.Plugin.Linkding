# AGENTS.md

Operating manual and technical guidelines for AI agents working in this repository.

## Overview

A [Wox](https://github.com/Wox-launcher/Wox) launcher integration for searching, saving, and managing bookmarks from a self-hosted [Linkding](https://github.com/sissbruecker/linkding) service.

- **Plugin Architecture**: Single-file Python SDK plugin (`Wox.Plugin.Linkding.py`) with zero third-party runtime dependencies. Standard library only (`urllib.request`, `json`, `re`, `asyncio`). See `docs/adr/0001-single-file-python-plugin.md`.
- **Interaction Model**: Smart input pattern recognition routing (`^https?://` for bookmark creation, `#` for tag browsing/filtering, plain text for bookmark search). See `docs/adr/0002-smart-input-recognition.md`.
- **Domain Language**: Always consult `CONTEXT.md` before introducing or modifying domain concepts.

## Fast Feedback Loops

Run these commands to verify changes before and after edits:

```bash
# Run full test suite
python -m unittest discover -s tests -p "test_*.py"

# Run single test class or method
python -m unittest tests.test_plugin.TestTagBrowsingAndSearch
python -m unittest tests.test_plugin.TestTagBrowsingAndSearch.test_tag_browsing_prefix_filtering

# Run static type checking
python -m mypy Wox.Plugin.Linkding.py tests/test_plugin.py
```

## Architecture & Code Standards

- **Single Source of Truth**: Metadata header (JSON in comments), setting definitions, i18n dictionaries, and runtime logic all reside in `Wox.Plugin.Linkding.py`.
- **Standard Library Only**: Do not add runtime dependencies in requirements or pip packages. The plugin runs in Wox's embedded Python runtime.
- **KISS Principle**: Implement clean, maintainable logic without speculative generalizations or unnecessary defensive branches.
- **Internationalization (i18n)**: All user-facing strings must use `i18n:<key>` references backed by both `en_US` and `zh_CN` dictionaries in the plugin header.

## Testing Guidelines & Seams

- **Public Interface Seams**: Tests verify observable behavior through the public launcher interface (`plugin.query(ctx, query)`) and action execution (`action.action(ctx, action_ctx)`).
- **External Boundary Mocking**: Mock only external HTTP calls at `urllib.request.urlopen`. Do not mock internal helper methods.
- **Test Invariants**:
  - Valid queries return correct `Result` list structure, SVG icons, and action definitions.
  - In-memory tag cache enforces 300-second TTL and lazily refreshes.
  - Settings changes invalidate caches and update plugin state.
  - Network and HTTP errors map to user-friendly translated error results.

## Agent Skills

### Issue Tracker

GitHub Issues via `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage Labels

Canonical five-role triage labels (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain Docs

Single-context (`CONTEXT.md` + `docs/adr/` at repo root). See `docs/agents/domain.md`.
