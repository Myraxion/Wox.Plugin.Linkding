# Wox.Plugin.Linkding

<p align="center">
  <img src="https://raw.githubusercontent.com/sissbruecker/linkding/master/assets/logo.png" width="128" height="128" alt="Linkding Logo" />
</p>

<p align="center">
  <strong>专为 <a href="https://github.com/Wox-launcher/Wox">Wox</a> 启动器打造的 <a href="https://github.com/sissbruecker/linkding">Linkding</a> 自建书签服务集成插件</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Wox-v2.4.2+-5856e0.svg" alt="Min Wox Version" />
  <img src="https://img.shields.io/badge/Runtime-Python%203-blue.svg" alt="Python Runtime" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License" />
</p>

<p align="center">
  <a href="README.md">English</a> | 简体中文
</p>

---

## 📖 简介

**Wox.Plugin.Linkding** 是一个单文件 Python SDK 插件，让你可以通过 Wox 在自建的 Linkding 书签服务中实现快速检索、智能收藏与标签导航。

---

## ✨ 核心特性

- 🔍 **即时书签搜索**
  - 输入 `ld <关键字>` 即可全文检索书签的标题、描述与网址。
- 🏷️ **标签浏览与检索**
  - 输入 `ld #` 列出所有标签；输入 `ld #<前缀>`（如 `ld #dev`）实时进行不区分大小写的前缀过滤。
- ➕ **智能收藏**
  - 直接输入或粘贴 URL（如 `ld https://...` 或 `ld woxlauncher.com`）自动进入添加模式。
  - 支持快捷追加标签：`ld woxlauncher.com #tech #dev` 自动提取空格分隔的 `#tag` 并为书签打标。
- 📌 **支持 Selection Query 选区查询**
  - 选中文本或链接，按下 Wox 选区查询快捷键与本插件联动：识别为网址则展示查重与快捷保存，普通文本则直接在 Linkding 中搜索。

---

## 🛠️ 安装与配置

### 1. 获取 Linkding API Token

1. 登录你的 Linkding 网页控制台。
2. 进入 **Settings** -> 找到 **REST API** 区域。
3. 复制生成的 **API Token**。

### 2. 在 Wox 中配置插件

1. 呼出 Wox，输入 `ld` 或进入 Wox 设置页面找到 **Linkding** 插件。
2. 填写以下配置项：
   - **Linkding URL**：Linkding 服务基础地址（例如 `https://linkding.example.com`，末尾不需要斜杠）。
   - **API Token**：刚才复制的 REST API Token。
   - **Max Results**：搜索结果最大展示数（默认：`10`）。

---

## 💡 使用指南

| 操作场景 | 输入示例 | 说明 |
| :--- | :--- | :--- |
| **基础搜索** | `ld python` | 搜索包含 "python" 的书签，展示标题、网址与关联标签 |
| **浏览全部标签** | `ld #` | 展示所有可用标签 |
| **前缀筛选标签** | `ld #dev` | 过滤以 "dev" 开头的标签，选中回车自动填充  |
| **标签 + 关键字搜索**| `ld #dev fastapi` | 检索带有 `dev` 标签且包含 "fastapi" 的书签 |
| **快速添加书签** | `ld https://news.ycombinator.com` | 检测是否已存在，按回车快速添加 |
| **带标签添加书签** | `ld https://github.com #dev #git` | 添加书签并自动绑定 `dev` 和 `git` 两个标签 |

---

## 🧑‍💻 开发与测试

本项目使用标准 Python `unittest` 与 `mypy` 进行质量保证。

### 配置开发环境

Wox 在运行插件时提供 `wox_plugin`。本地导入、编辑器补全和测试需要在虚拟环境中安装 SDK 与类型检查工具（推荐 Python 3.12）：

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements-dev.txt
.venv\Scripts\Activate.ps1
```

macOS/Linux 对应使用 `.venv/bin/python` 和 `source .venv/bin/activate`。如果 VS Code 已选择过其他解释器，请通过 **Python: Select Interpreter** 切换到本项目的 `.venv`；若仍显示缺失导入诊断，重新加载编辑器窗口。

### 运行全量测试套件

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### 运行类型检查

```bash
python -m mypy Wox.Plugin.Linkding.py tests/test_plugin.py
```

---

## 🙏 鸣谢与致谢

- [Linkding](https://github.com/sissbruecker/linkding) 由 [Sascha Ißbrücker](https://github.com/sissbruecker) 创建并遵循 MIT 协议开源。
- 感谢 [Wox](https://github.com/Wox-launcher/Wox) 启动器生态。

---

## 📄 开源许可证

本项目遵循 [MIT License](LICENSE)。
