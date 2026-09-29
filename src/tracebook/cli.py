import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from importlib.metadata import PackageNotFoundError, version

def package_version():
    try:
        return version("lr-ctf-tracebook")
    except PackageNotFoundError:
        return "dev"



ANSI = re.compile(r"\x1b(?:\[[0-?]*[ -/]*[@-~]|\][^\x07]*(?:\x07|\x1b\\))")
PROMPT = re.compile(r"^\s*(?:\[[^\n\]]+\]\s*)?(?:\$|#|>>>|PS [^>]+>)\s+(.+)$")
FLAG = re.compile(r"(?i)\b(?:flag|ctf|htb|picoctf)\{[^}\n]{1,200}\}")
SECRETS = re.compile(r"(?i)\b((?:authorization\s*:\s*bearer|password|token|api[_-]?key)\s*[:= ]\s*)\S+")
PRIVATE_KEY = re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----")
ERROR_HINT = re.compile(r"(?i)\b(error|failed|failure|exception|traceback|segmentation fault|permission denied|no such file)\b")


def classify_command(command: str) -> str:
    head = command.strip().split(maxsplit=1)[0].lower() if command.strip() else ""
    if head in {"file", "checksec", "readelf", "objdump", "strings", "nm", "ldd"}:
        return "inspection"
    if head in {"gdb", "lldb", "pwndbg", "gef"}:
        return "debugging"
    if head in {"python", "python3", "ruby", "node", "perl"}:
        return "script"
    if head in {"gcc", "g++", "clang", "make", "cmake"}:
        return "build"
    if head in {"curl", "wget", "nc", "ncat", "socat", "ssh"}:
        return "network"
    return "shell"


def infer_outcome(output: str) -> str:
    if not output.strip():
        return "no-output"
    return "error-like" if ERROR_HINT.search(output) else "observed"


def sanitize(raw: str, keep_flags: bool = False) -> tuple[str, dict]:
    normalized = raw.replace("\r\n", "\n")
    ansi_sequences = len(ANSI.findall(normalized))
    private_keys = len(PRIVATE_KEY.findall(normalized))
    secret_values = len(SECRETS.findall(normalized))
    flags = 0 if keep_flags else len(FLAG.findall(normalized))

    sanitized = ANSI.sub("", normalized)
    sanitized = PRIVATE_KEY.sub("[REDACTED PRIVATE KEY]", sanitized)
    sanitized = SECRETS.sub(r"\1[REDACTED]", sanitized)
    if not keep_flags:
        sanitized = FLAG.sub("[REDACTED FLAG]", sanitized)

    return sanitized, {
        "ansi_sequences_removed": ansi_sequences,
        "private_keys_redacted": private_keys,
        "secret_values_redacted": secret_values,
        "flags_redacted": flags,
        "flags_preserved": bool(keep_flags),
    }


def clean(raw: str, keep_flags: bool = False) -> str:
    return sanitize(raw, keep_flags)[0]


def extract(raw: str, keep_flags: bool = False) -> dict:
    sanitized, redaction_summary = sanitize(raw, keep_flags)
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
        item["category"] = classify_command(item["command"])
        item["outcome"] = infer_outcome(item["output"])

    category_counts = {}
    for item in entries:
        category_counts[item["category"]] = category_counts.get(item["category"], 0) + 1

    return {
        "schema": "lr-ctf-tracebook/v2",
        "source_sha256": hashlib.sha256(raw.encode()).hexdigest(),
        "summary": {
            "commands": len(entries),
            "categories": dict(sorted(category_counts.items())),
            "error_like_steps": sum(item["outcome"] == "error-like" for item in entries),
        },
        "redaction_summary": redaction_summary,
        "entries": entries,
        "unassigned_lines": len(sanitized.splitlines()) - sum(1 + len(x["output"].splitlines()) for x in entries),
    }


def render(title: str, record: dict) -> str:
    summary = record.get("summary", {})
    out = [
        f"# {title}",
        "",
        "> 自动生成的证据草稿。请人工补上题目来源、授权范围、思路与失败尝试；不要直接公开未经核查的内容。",
        "",
        "## 元数据",
        "",
        f"- 原始记录 SHA-256：`{record['source_sha256']}`",
        f"- 识别命令数：**{summary.get('commands', len(record['entries']))}**",
        f"- error-like 步骤：**{summary.get('error_like_steps', 0)}**",
        f"- 命令类别：`{json.dumps(summary.get('categories', {}), ensure_ascii=False)}`",
        f"- 默认脱敏摘要：`{json.dumps(record.get('redaction_summary', {}), ensure_ascii=False)}`",
        "- 分类：待填写",
        "- 环境 / 版本：待填写",
        "",
        "## 操作与观察",
        "",
    ]
    for i, entry in enumerate(record["entries"], 1):
        out += [
            f"### {i}. 源文件 L{entry['line']}",
            "",
            f"- category: **{entry.get('category', 'shell')}**",
            f"- outcome: **{entry.get('outcome', 'unknown')}**",
            "",
            "命令：",
            "",
            "```text",
            entry["command"].replace("```", "'''"),
            "```",
            "",
            "观察：",
            "",
            "```text",
            (entry["output"] or "（无记录）").replace("```", "'''"),
            "```",
            "",
            "为什么这样做 / 结论：待人工填写",
            "",
        ]
    out += ["## 复现检查", "", "- [ ] 核对命令、环境及输出", "- [ ] 删除目标地址、账号、密钥和 flag 等不宜公开内容", "- [ ] 补充每一步的推理和失败路线", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="把授权 CTF 终端记录整理为可核查的复盘草稿")
    parser.add_argument("--version", action="version", version=f"%(prog)s {package_version()}")
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
