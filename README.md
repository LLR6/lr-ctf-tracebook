# CTF Tracebook 📓

> 终端打完题，复盘往往只剩命令截图。这个工具把**已有的终端文本记录**整理成带源行号的 Markdown 草稿，并默认遮盖 flag 与常见口令。

```bash
python -m pip install -e .
ctf-tracebook examples/session.txt --title "一道 ELF 题的复盘" > writeup.md
ctf-tracebook examples/session.txt --format json
```

输入是从终端复制或导出的纯文本，例如 `$ file challenge`、`# id`、`>>> print(1)`、`PS C:\\> dir`。输出包含命令、观察、原始行号与源文件 SHA-256。**不会凭空编造漏洞原理或成功步骤**，需要自己填入推理、失败路线、授权范围和环境版本。

## 隐私与边界

- 默认遮盖 `flag{...}` 等 flag、常见 token/口令赋值以及 PEM 私钥块。`--keep-flags` 仅在自己需要时使用。
- 原始记录只在本机读取，不执行任何记录中的命令、不连接目标。
- 正则脱敏不可能覆盖所有敏感信息，公开 writeup 前仍需逐行人工检查；特别留意 IP、账号和未公开题目。
- 仅用于有授权的训练或比赛记录。测试：`python -m unittest discover -s tests`。

欢迎提供去敏的不同 shell 提示符样例，特别是 Windows PowerShell 和多行命令。路线图：可编辑时间线、附件哈希、失败尝试分组。

作者：LLR6 · MIT License
