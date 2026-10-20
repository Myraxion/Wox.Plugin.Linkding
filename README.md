# Wox.Plugin.Linkding

<p align="center">
  <img src="https://raw.githubusercontent.com/sissbruecker/linkding/master/assets/logo.png" width="128" height="128" alt="Linkding Logo" />
</p>

<p align="center">
  <strong>A <a href="https://github.com/Wox-launcher/Wox">Wox</a> launcher plugin for searching, saving, and managing bookmarks from a self-hosted <a href="https://github.com/sissbruecker/linkding">Linkding</a> service.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Wox-v2.4.2+-5856e0.svg" alt="Min Wox Version" />
  <img src="https://img.shields.io/badge/Runtime-Python%203-blue.svg" alt="Python Runtime" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License" />
</p>

<p align="center">
  English | <a href="README_zh.md">简体中文</a>
</p>

---

## 📖 Introduction

**Wox.Plugin.Linkding** is a single-file Python SDK plugin that allows you to quickly search, smartly save, and navigate tags in your self-hosted Linkding bookmark service directly through Wox.

---

## ✨ Features

- 🔍 **Instant Bookmark Search**
  - Type `ld <keyword>` to perform full-text search across bookmark titles, descriptions, and URLs.
- 🖼️ **Website Favicons**
  - Bookmarks use the favicon saved by Linkding in search results, tag-filtered results, selection previews, and duplicate checks.
  - Results appear immediately with the Linkding icon; favicons load in the background and replace it in place. Missing icons, download errors, and non-image responses keep the Linkding icon.
  - Successful downloads and failures are cached in memory for 300 seconds. Changing the Linkding URL or API token clears this cache.
  - Image decoding is handled by Wox; downloaded but corrupt image files may still show Wox's generic placeholder.
- ⚡ **Multi-Action Interaction**
  - **Default Action (Enter)**: Open the bookmark directly in your default browser.
  - **Copy Link**: Copy the bookmark URL to the system clipboard in one click.
  - **Open in Linkding**: Quickly jump to the corresponding search page in Linkding's Web UI.
- 🏷️ **Interactive Tag Browsing & Filtering**
  - Type `ld #` to list all tags; type `ld #<prefix>` (e.g., `ld #dev`) for real-time, case-insensitive prefix filtering.
  - Built-in in-memory tag cache with a 300-second TTL and lazy refresh for a smooth browsing experience.
  - Press Enter on any tag to automatically autocomplete your query to `ld #<tag> ` (with trailing space), instantly listing all bookmarks under that tag.
- ➕ **Smart Bookmark Creation & Duplicate Detection**
  - **Smart pattern recognition**: typing or pasting a URL directly (e.g., `ld https://...` or `ld woxlauncher.com`) automatically switches to bookmark creation mode without needing any subcommands. Unprefixed URLs (e.g., copied from browser address bars) are automatically normalized with protocol completion (`http://` for localhost/127.0.0.1, `https://` for other domains and IPs).
  - Automatically calls Linkding's `/check` endpoint to verify if the URL is already saved, showing a warning indicator to prevent duplicates.
  - Quick tag assignment: `ld woxlauncher.com #tech #dev` automatically extracts space-separated `#tag`s and applies them to the bookmark.
  - Triggers Linkding server-side auto-scraping for title and description.
- 📌 **Selection Query Support**
  - Select text or URLs in any browser or application and press the Wox Selection hotkey (e.g., `Win+Alt+Space`) to instantly interact with Linkding: recognized URLs trigger bookmark duplicate checking and saving, while plain text triggers bookmark search.
  - A fixed “Linkding Bookmarks” entry appears immediately while the search runs, then updates its status and read-only preview in place. Press Enter to expand using your configured trigger keyword (default: `ld <keyword>`) and select a bookmark in Wox; even a single match expands first. Early Enter reuses the pending search. With no matches, Enter lets you edit the search terms. `Ctrl+J` offers Linkding web search as a secondary action.
- 🌐 **Bilingual Support (i18n)**
  - Built-in English and Simplified Chinese localization; automatically adjusts to Wox system language preferences.
- 🛡️ **Declarative Settings Validation**
  - Uses Wox declarative `QueryRequirements`. On first launch without a server URL or API token configured, Wox prompts you directly to fill in settings, preventing silent runtime failures.

---

## 🛠️ Installation & Configuration

### 1. Obtain Linkding API Token

1. Log in to your Linkding web interface.
2. Navigate to **Settings** -> locate the **REST API** section.
3. Copy the generated **API Token**.

### 2. Configure Plugin in Wox

1. Open Wox, type `ld`, or open Wox Settings and find the **Linkding** plugin.
2. Configure the following fields:
   - **Linkding URL**: Base URL of your Linkding instance (e.g., `https://linkding.example.com`, without trailing slash).
   - **API Token**: The REST API Token copied in the previous step.
   - **Max Results**: Maximum number of search results to display (default: `10`).

---

## 💡 Usage Guide

| Scenario | Example Input | Description |
| :--- | :--- | :--- |
| **Basic Search** | `ld python` | Search bookmarks containing "python", displaying title, URL, and associated tags |
| **Browse All Tags** | `ld #` | List all available tags |
| **Filter Tags by Prefix** | `ld #dev` | Filter tags starting with "dev", press Enter to autocomplete `ld #dev ` |
| **Filter Bookmarks by Tag** | `ld #dev ` | Show all bookmarks containing the `dev` tag |
| **Tag + Keyword Search** | `ld #dev fastapi` | Search for bookmarks tagged `dev` that also match "fastapi" |
| **Quick Add Bookmark** | `ld https://news.ycombinator.com` | Check if URL exists, press Enter to quickly save |
| **Add Bookmark with Tags** | `ld https://github.com #dev #git` | Save bookmark and automatically attach `dev` and `git` tags |

---

## 🧑‍💻 Development & Testing

This project uses standard Python `unittest` and `mypy` for quality assurance.

### Set Up the Development Environment

Wox supplies `wox_plugin` when running the plugin. For local imports, editor completion, and tests, install the SDK and type checker in a virtual environment (Python 3.12 recommended):

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\Activate.ps1
```

On macOS/Linux, use `.venv/bin/python` and `source .venv/bin/activate` instead. In VS Code, select the project's `.venv` through **Python: Select Interpreter** if an interpreter was already selected. Reload the editor window if the missing-import diagnostic persists.

### Run Full Test Suite

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### Run Type Checking

```bash
python -m mypy Wox.Plugin.Linkding.py tests/test_plugin.py
```

---

## 📂 Project Structure & Architecture Decisions

- `Wox.Plugin.Linkding.py`: Single-file plugin containing metadata, settings definitions, i18n dictionaries, and business logic.
- `tests/test_plugin.py`: Comprehensive behavior-driven unit tests mocking Wox runtime and Linkding HTTP responses.
- [CONTEXT.md](CONTEXT.md): Core domain concepts and ubiquitous terminology.
- [docs/adr/0001-single-file-python-plugin.md](docs/adr/0001-single-file-python-plugin.md): ADR on adopting a single-file Python SDK architecture.
- [docs/adr/0002-smart-input-recognition.md](docs/adr/0002-smart-input-recognition.md): ADR on smart input pattern recognition over explicit subcommands.

---

## 🙏 Acknowledgements

- [Linkding](https://github.com/sissbruecker/linkding) is created by [Sascha Ißbrücker](https://github.com/sissbruecker) and licensed under the MIT License.
- Built for the [Wox](https://github.com/Wox-launcher/Wox) launcher ecosystem.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
