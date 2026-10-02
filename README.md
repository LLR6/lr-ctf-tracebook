# CTF Tracebook

### 题解写不出来？先把终端里的证据留住。

把已有终端文本整理成 Markdown / JSON 复盘草稿：命令、观察、源行号、输入哈希和去敏统计一起保留。适合比赛结束后整理 write-up、回看失败尝试和分享可核查的操作记录。

[快速体验](#30-秒试玩) · [实跑案例](docs/DEMO.md) · [完整输出](examples/showcase/output.json) · [反馈问题](https://github.com/LLR6/lr-ctf-tracebook/issues)

| 你的场景 | 可以先试什么 |
| --- | --- |
| 操作很多，忘了每步做过什么 | 提取命令和对应输出，保留源行号 |
| 准备公开终端记录 | 查看 flag / 口令 / 私钥去敏统计，再人工复核 |
| 想继续补充完整题解 | 在草稿中补上自己的推理和失败原因 |

<p align="center"><img src="./docs/media/social-preview.svg" alt="CTF Tracebook — Turn terminal traces into a writeup" width="100%"></p>
<p align="center"><img src="./docs/media/cli-demo.gif" alt="真实示例：终端记录转换为可核查的复盘草稿" width="100%"></p>
<p align="center"><sub>示例来自仓库自带的 session.txt；画面为便于阅读的节选。</sub></p>
<p align="center"><strong>打完一道题，让复盘从证据开始，而不是从记忆开始。</strong></p>
<p align="center">纯文本终端记录 → 带源行号的 Markdown / JSON 草稿；默认遮盖 flag 与常见口令。</p>
<p align="center"><a href="#30-秒看懂">30 秒看懂</a> · <a href="#5-分钟开始">5 分钟开始</a> · <a href="#能力与边界">能力与边界</a></p>
<p align="center"><img alt="Test" src="https://github.com/LLR6/lr-ctf-tracebook/actions/workflows/test.yml/badge.svg"> <img alt="Python 3.10+" src="https://img.shields.io/badge/python-3.10%2B-blue"> <img alt="MIT" src="https://img.shields.io/badge/license-MIT-green"> </p>

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


## 实跑结果与使用案例

本次运行提取 **3 条命令**：2 条 inspection、1 条 script；遮盖 **1 个 flag**，`unassigned_lines` 为 0。输出保留 L1 / L3 / L5 和原始文本 SHA-256。类别与 outcome 是整理标签，不代表真实进程退出码。

[查看运行过程与读结果的方法](docs/DEMO.md) · [查看未经改写的 JSON 输出](examples/showcase/output.json)

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

<details>
<summary>工程文档与兼容性</summary>

[Architecture](./docs/ARCHITECTURE.md) · [Benchmarks](./docs/BENCHMARKS.md) · [Trace model](./docs/TRACE_MODEL.md) · [Threat model](./docs/THREAT_MODEL.md) · [Roadmap](./docs/ROADMAP.md) · [Compatibility](./docs/COMPATIBILITY.md) · [Releasing](./docs/RELEASING.md) · [Support](./SUPPORT.md)
 · [Change risk](./docs/CHANGE_RISK.md) · [Failure modes](./docs/FAILURE_MODES.md)

[贡献说明](CONTRIBUTING.md) · [版本记录](CHANGELOG.md) · [输出格式](schemas)

</details>
