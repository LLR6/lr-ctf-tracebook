import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ANSI = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")
PROMPT = re.compile(r"^\s*(?:\[[^\n\]]+\]\s*)?(?:\$|#|>>>|PS [^>]+>)\s+(.+)$")
FLAG = re.compile(r"(?i)\b(?:flag|ctf|htb|picoctf)\{[^}\n]{1,200}\}")
SECRETS = re.compile(r"(?i)\b((?:authorization\s*:\s*bearer|password|token|api[_-]?key)\s*[:= ]\s*)\S+")
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----")


def clean(raw: str, keep_flags: bool = False) -> str:
    raw = ANSI.sub("", raw.replace("\r\n", "\n"))
    raw = PRIVATE_KEY.sub("[REDACTED PRIVATE KEY]", raw)
    raw = SECRETS.sub(r"\1[REDACTED]", raw)
    if not keep_flags:
        raw = FLAG.sub("[REDACTED FLAG]", raw)
    return raw


def extract(raw: str, keep_flags: bool = False) -> dict:
    sanitized = clean(raw, keep_flags)
    entries = []
    current = None
    for number, line in enumerate(sanitized.splitlines(), 1):
        match = PROMPT.match(line)
        if match:
            if current:
                entries.append(current)
            current = {"line": number, "command": match.group(1), "output": []}
        elif current:
            current["output"].append(line)
    if current:
        entries.append(current)
    for item in entries:
        item["output"] = "\n".join(item["output"]).strip()[:3000]
    return {"schema": "lr-ctf-tracebook/v1", "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "entries": entries, "unassigned_lines": len(sanitized.splitlines()) - sum(1 + len(x["output"].splitlines()) for x in entries)}


def render(title: str, record: dict) -> str:
    out = [f"# {title}", "", "> 自动生成的证据草稿。请人工补上题目来源、授权范围、思路与失败尝试；不要直接公开未经核查的内容。", "", "## 元数据", "", f"- 原始记录 SHA-256：`{record['source_sha256']}`", "- 分类：待填写", "- 环境 / 版本：待填写", "", "## 操作与观察", ""]
    for i, entry in enumerate(record["entries"], 1):
        out += [f"### {i}. 源文件 L{entry['line']}", "", "命令：", "", "```text", entry["command"].replace("```", "'''"), "```", "", "观察：", "", "```text", (entry["output"] or "（无记录）").replace("```", "'''"), "```", "", "为什么这样做 / 结论：待人工填写", ""]
    out += ["## 复现检查", "", "- [ ] 核对命令、环境及输出", "- [ ] 删除目标地址、账号、密钥和 flag 等不宜公开内容", "- [ ] 补充每一步的推理和失败路线", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="把授权 CTF 终端记录整理为可核查的复盘草稿")
    parser.add_argument("transcript", help="文本记录路径；- 表示 stdin")
    parser.add_argument("--title", default="CTF 复盘草稿")
    parser.add_argument("--format", choices=("md", "json"), default="md")
    parser.add_argument("--keep-flags", action="store_true", help="默认遮盖 flag；显式开启才保留")
    args = parser.parse_args(argv)
    try:
        raw = sys.stdin.read() if args.transcript == "-" else Path(args.transcript).read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        parser.error(str(exc))
    record = extract(raw, args.keep_flags)
    print(json.dumps(record, ensure_ascii=False, indent=2) if args.format == "json" else render(args.title, record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
