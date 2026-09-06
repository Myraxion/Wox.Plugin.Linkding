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
- ⚡ **多动作交互支持**
  - **默认动作（回车）**：在系统默认浏览器中直接打开书签。
  - **复制链接**：一键将书签 URL 拷贝至系统剪贴板。
  - **在 Linkding 中打开**：快速跳转至 Linkding Web 端对应的搜索页面。
- 🏷️ **交互式标签浏览与检索（Tag Browsing）**
  - 输入 `ld #` 列出所有标签；输入 `ld #<前缀>`（如 `ld #dev`）实时进行不区分大小写的前缀过滤。
  - 内置标签内存缓存与 300 秒 TTL 惰性刷新机制，浏览体验如丝般顺滑。
  - 选中标签回车自动将输入更新为 `ld #<tag> `（附带末尾空格），立即展示该标签下的所有书签。
- ➕ **智能收藏与重复检测（Smart Bookmark Creation）**
  - **智能模式识别**，直接输入或粘贴 URL（如 `ld https://...`）自动进入添加模式，无需记忆或输入任何子命令。
  - 自动调用 Linkding `/check` 接口检测是否已收藏；若已收藏则展示预警提示，防止重复添加。
  - 支持快捷追加标签：`ld https://example.com #tech #dev` 自动提取空格分隔的 `#tag` 并为书签打标。
  - 触发 Linkding 服务端自动刮削（Scrape）网页标题和描述。
- 🌐 **双语支持（i18n）**
  - 内置中英双语国际化，根据 Wox 系统偏好自动切换显示。
- 🛡️ **声明式配置检验**
  - 采用 Wox 声明式 `QueryRequirements`，首次使用时若未配置服务端地址或 Token，Wox 会直接提示填写，防止运行时静默失败。

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
| **前缀筛选标签** | `ld #dev` | 过滤以 "dev" 开头的标签，回车自动填充 `ld #dev ` |
| **按标签过滤书签** | `ld #dev ` | 展示所有包含 `dev` 标签的书签 |
| **标签 + 关键字搜索**| `ld #dev fastapi` | 检索带有 `dev` 标签且包含 "fastapi" 的书签 |
| **快速添加书签** | `ld https://news.ycombinator.com` | 检测是否已存在，按回车快速添加 |
| **带标签添加书签** | `ld https://github.com #dev #git` | 添加书签并自动绑定 `dev` 和 `git` 两个标签 |

---

## 🧑‍💻 开发与测试

本项目使用标准 Python `unittest` 与 `mypy` 进行质量保证。

### 运行全量测试套件

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

### 运行类型检查

```bash
python -m mypy Wox.Plugin.Linkding.py tests/test_plugin.py
```

---

## 📂 项目结构与架构决策

- `Wox.Plugin.Linkding.py`: 包含插件元数据、配置声明、国际化与完整业务逻辑的单文件插件。
- `tests/test_plugin.py`: 完整的行为驱动单元测试，模拟 Wox 运行环境与 Linkding HTTP 响应。
- [CONTEXT.md](CONTEXT.md): 项目核心领域概念与专用术语表。
- [docs/adr/0001-single-file-python-plugin.md](docs/adr/0001-single-file-python-plugin.md): 采用单文件 Python SDK 架构决策。
- [docs/adr/0002-smart-input-recognition.md](docs/adr/0002-smart-input-recognition.md): 采用智能输入模式识别替代显式子命令决策。

---

## 📄 开源许可证

本项目遵循 [MIT License](LICENSE)。
