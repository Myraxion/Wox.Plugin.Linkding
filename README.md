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
- ⚡ **Multi-Action Interaction**
  - **Default Action (Enter)**: Open the bookmark directly in your default browser.
  - **Copy Link**: Copy the bookmark URL to the system clipboard in one click.
  - **Open in Linkding**: Quickly jump to the corresponding search page in Linkding's Web UI.
- 🏷️ **Interactive Tag Browsing & Filtering**
  - Type `ld #` to list all tags; type `ld #<prefix>` (e.g., `ld #dev`) for real-time, case-insensitive prefix filtering.
  - Built-in in-memory tag cache with a 300-second TTL and lazy refresh for a smooth browsing experience.
  - Press Enter on any tag to automatically autocomplete your query to `ld #<tag> ` (with trailing space), instantly listing all bookmarks under that tag.
- ➕ **Smart Bookmark Creation & Duplicate Detection**
  - **Smart pattern recognition**: typing or pasting a URL directly (e.g., `ld https://...`) automatically switches to bookmark creation mode without needing any subcommands.
  - Automatically calls Linkding's `/check` endpoint to verify if the URL is already saved, showing a warning indicator to prevent duplicates.
  - Quick tag assignment: `ld https://example.com #tech #dev` automatically extracts space-separated `#tag`s and applies them to the bookmark.
  - Triggers Linkding server-side auto-scraping for title and description.
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
