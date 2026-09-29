# CTF Tracebook

<!-- LR-LAB-CHROME:START -->
<p align="center">
  <a href="https://github.com/LLR6"><img alt="LR Lab" src="https://img.shields.io/badge/LR_LAB-0x4C52-0D1117?style=for-the-badge&logo=github&logoColor=white"></a>
  <img alt="CTF TOOL" src="https://img.shields.io/badge/CTF_TOOL-06B6D4?style=for-the-badge">
</p>
<p align="center"><strong>Turn terminal traces into a writeup.</strong><br><sub>Evidence-first, redacted CTF session notes</sub></p>
<p align="center"><a href="https://github.com/LLR6/lr-ctf-tracebook/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/LLR6/lr-ctf-tracebook?style=flat-square&logo=github&label=stars"></a>
  <img alt="Last commit" src="https://img.shields.io/github/last-commit/LLR6/lr-ctf-tracebook?style=flat-square"> <img alt="Maintained" src="https://img.shields.io/badge/status-active-success?style=flat-square"></p>
<p align="center"><a href="https://github.com/LLR6">Profile</a> · <a href="https://github.com/LLR6?tab=repositories">All projects</a> · <a href="https://github.com/LLR6/lr-ctf-tracebook/issues">Issues</a></p>
<!-- LR-LAB-CHROME:END -->

<!-- LR-FAMILY-NAV:START -->
<p align="center"><a href="#30-秒试玩">30-second demo</a> · <a href="./examples">Examples</a> · <a href="./src">Source</a> · <a href="./tests">Tests</a></p>
<!-- LR-FAMILY-NAV:END -->


<p align="center"><img src="./docs/media/social-preview.svg" alt="CTF Tracebook — Turn terminal traces into a writeup" width="100%"></p>
<p align="center"><img src="./docs/media/cli-demo.gif" alt="真实示例：终端记录转换为可核查的复盘草稿" width="100%"></p>
<p align="center"><sub>示例来自仓库自带的 session.txt；画面为便于阅读的节选。</sub></p>
<p align="center"><strong>打完一道题，让复盘从证据开始，而不是从记忆开始。</strong></p>
<p align="center">纯文本终端记录 → 带源行号的 Markdown / JSON 草稿；默认遮盖 flag 与常见口令。</p>
<p align="center"><a href="#30-秒看懂">30 秒看懂</a> · <a href="#5-分钟开始">5 分钟开始</a> · <a href="#能力与边界">能力与边界</a></p>
<p align="center"><img alt="Test" src="https://github.com/LLR6/lr-ctf-tracebook/actions/workflows/test.yml/badge.svg"> <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue"> <img alt="MIT" src="https://img.shields.io/badge/license-MIT-green"> <img alt="Version 0.1.0" src="https://img.shields.io/badge/version-0.1.0-8b5cf6"></p>

## 30 秒看懂

你已经保存了终端记录，但命令、观察与推理散在一整段文本里。Tracebook 读取**已有记录**，提取常见 shell 提示符后的命令，保留对应输出和源文件行号，并给出待补充的推理栏位。

```text
终端文本 → 命令与观察 → 源行号 + SHA-256 → 去敏复盘草稿
```

## 30 秒试玩

```bash
python -m pip install -e .
ctf-tracebook examples/session.txt --title "一道 ELF 题的复盘" > writeup.md
```

示例草稿节选（来自 `examples/session.txt`）：

```text
源文件 L1: file challenge
观察: challenge: ELF 64-bit LSB executable

源文件 L3: checksec --file=challenge
观察: Full RELRO / Canary / NX / PIE

源文件 L5: python3 solve.py
观察: [REDACTED FLAG]
```

## 三个值得看的点

- **可回查**：每一步带源行号，原始记录的 SHA-256 写进草稿。
- **默认去敏**：遮盖 flag、常见 Token/口令和 PEM 私钥块；`--keep-flags` 需主动开启。
- **不替你编造推理**：每一步为何这样做，仍由解题者补充。

## 5 分钟开始

要求 Python 3.10+。输入是你自己复制或导出的**纯文本记录**。

```bash
git clone https://github.com/LLR6/lr-ctf-tracebook.git
cd lr-ctf-tracebook
python -m pip install -e .
ctf-tracebook examples/session.txt --title "一道 ELF 题的复盘" > writeup.md
ctf-tracebook examples/session.txt --format json
```

支持常见 `$`、`#`、`>>>` 和 PowerShell 提示符；实际提取情况请用自己的记录核对。输出是草稿，公开前请逐行检查目标地址、账号、密钥、未公开题目与授权范围。

## 能力与边界

不执行输入中的任何命令，不连接目标，不推断漏洞原理或“自动解题”。正则去敏无法覆盖所有敏感字段。仅用于有授权的比赛或训练复盘；任何错误归因和遗漏需要人工修订。

## 参与 / Help Wanted

欢迎提交**去敏**的提示符、换行命令或失败路线样例。下一步可做可编辑时间线、附件哈希与失败尝试分组。验证代码：`python -m unittest discover -s tests`。

作者：LLR6 · MIT License

<!-- LR-CONTENT-UPGRADE:START -->
## v0.2：把一次终端会话变成可读的结构

每个提取到的命令现在额外带两个轻量字段：

- `category`：inspection / debugging / script / build / network / shell
- `outcome`：no-output / observed / error-like

JSON v2 还增加会话摘要：

```json
{
  "commands": 6,
  "categories": {
    "inspection": 2,
    "script": 3,
    "debugging": 1
  },
  "error_like_steps": 2
}
```

这些标签只用于整理复盘，不代表命令意图，也不伪装成真实退出码。

为什么刻意不自动生成“推理过程”，见 [docs/TRACE_MODEL.md](docs/TRACE_MODEL.md)。

<!-- LR-CONTENT-UPGRADE:END -->

<!-- LR-DEEP-CONTENT:START -->
### Redaction coverage

JSON v2 现在增加 `redaction_summary`，会记录：

- ANSI 控制序列移除数；
- private key 遮盖数；
- secret/token 遮盖数；
- flag 遮盖数；
- 是否显式开启了 `--keep-flags`。

工具仍不会声称“已经自动发现所有敏感信息”，但至少能明确告诉使用者：当前已识别并处理了哪些类别、多少项。
<!-- LR-DEEP-CONTENT:END -->


<!-- LR-RELATED:START -->
### Related LR Lab projects
- [Android CI Doctor](https://github.com/LLR6/lr-android-ci-doctor) — evidence-first diagnosis for build logs.
- [NightWatch](https://github.com/LLR6/Cybersecurity-Detection-Engineering-Android-Automation-Learning-by-Building) — explainable defensive detection experiments.
- [LR-Agent](https://github.com/LLR6/LR-agent) — automation and reproducibility research.
<!-- LR-RELATED:END -->

<!-- LR-LAB-FOOTER:START -->
---
<p align="center"><sub>Part of <a href="https://github.com/LLR6">LR Lab</a> · Security × AI × Android × Automation</sub><br><sub>Build things that are useful, inspectable, and reproducible.</sub></p>
<!-- LR-LAB-FOOTER:END -->

