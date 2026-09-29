# Trace Model

CTF Tracebook 只整理已经存在的终端记录，不执行命令，也不自动“补全”解题思路。

## Command taxonomy

v2 为每个识别到的命令增加一个轻量类别：

- `inspection`：file / checksec / readelf / objdump / strings / nm / ldd
- `debugging`：gdb / lldb / pwndbg / gef
- `script`：Python / Ruby / Node / Perl
- `build`：gcc / clang / make / cmake
- `network`：curl / wget / nc / socat / ssh
- `shell`：其他命令

这个分类只用于复盘结构，不代表命令意图。

## Outcome heuristic

每一步还会标记：

- `no-output`
- `observed`
- `error-like`

`error-like` 只是根据 error / failed / traceback 等词做的启发式判断。它不是命令退出码，也不能证明操作失败。

## Session summary

JSON v2 增加：

- command count；
- category counts；
- error-like step count。

这样可以快速看出一次会话主要是在信息收集、调试、写脚本还是反复处理错误。

## Evidence rules

Tracebook 保留：

- 源文本 SHA-256；
- 命令所在原始行号；
- 命令输出；
- flag / token / password / private key 的默认遮盖。

公开 writeup 前仍应人工检查地址、账号、未公开题目内容和比赛规则。

## Why not auto-write reasoning?

终端记录能证明“做了什么、看到了什么”，却不能可靠证明“当时为什么这样做”。

因此“为什么这样做 / 结论”故意保留给解题者填写，避免工具替人编造推理。
