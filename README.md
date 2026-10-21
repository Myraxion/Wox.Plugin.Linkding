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
- 🏷️ **Tag Browsing & Filtering**
  - Type `ld #` to list all tags; type `ld #<prefix>` (e.g., `ld #dev`) for real-time, case-insensitive prefix filtering.
- ➕ **Smart Bookmark Creation**
  - Type or paste a URL directly (e.g., `ld https://...` or `ld woxlauncher.com`) to automatically switch to bookmark creation mode.
  - Quick tag assignment: `ld woxlauncher.com #tech #dev` automatically extracts space-separated `#tag`s and applies them to the bookmark.
- 📌 **Selection Query Support**
  - Select text or a URL and press the Wox Selection hotkey to interact with Linkding: recognized URLs trigger duplicate checking and quick saving, while plain text triggers bookmark search.

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
| **Filter Tags by Prefix** | `ld #dev` | Filter tags starting with "dev"; select a tag and press Enter to autocomplete |
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

## 🙏 Acknowledgements

- [Linkding](https://github.com/sissbruecker/linkding) is created by [Sascha Ißbrücker](https://github.com/sissbruecker) and licensed under the MIT License.
- Built for the [Wox](https://github.com/Wox-launcher/Wox) launcher ecosystem.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
