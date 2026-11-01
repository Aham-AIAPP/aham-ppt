#!/usr/bin/env python3
"""产出比对：判断两次生成的样张是否相同，列出不同的文件和部件。

用法：
  python compare_outputs.py snapshot 目录 -o 清单.json   记录目录里每份样张的校验值
  python compare_outputs.py check 目录 清单.json          重新计算并与清单比对，不同时返回 1
  python compare_outputs.py diff 目录A 目录B              直接比对两个目录，不同时返回 1 并打印差异

比对规则：
- Word、Excel、PowerPoint 按压缩包里的部件逐个比对。压缩包时间戳不参与比对；
  docProps/core.xml 里的创建、修改时间和 docProps/app.xml 里的编辑总时长先去掉再比。
- PDF 用 pdftoppm 按 72 dpi 转成逐页图片再比对像素，没有 pdftoppm 时比对去掉日期和 ID 后的字节。
- 网页、JSON、Markdown、SVG 等文本按字节比对，换行统一为 LF。
- 其他文件按字节比对。

只用标准库，可以复制到任何仓库使用。
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

OFFICE = {".docx", ".xlsx", ".pptx", ".docm", ".xlsm", ".dotx", ".potx"}
TEXT = {".html", ".htm", ".json", ".md", ".svg", ".txt", ".css", ".js", ".mjs", ".xml", ".csv", ".yaml", ".yml"}
IGNORED_NAMES = {".DS_Store"}

_CORE_TIMES = re.compile(rb"<dcterms:(created|modified)[^>]*>[^<]*</dcterms:\1>")
_APP_TOTAL = re.compile(rb"<TotalTime>[^<]*</TotalTime>")
_PDF_VOLATILE = re.compile(rb"/(CreationDate|ModDate)\s*\([^)]*\)|/ID\s*\[[^\]]*\]")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_part(name: str, data: bytes) -> bytes:
    if name == "docProps/core.xml":
        return _CORE_TIMES.sub(b"", data)
    if name == "docProps/app.xml":
        return _APP_TOTAL.sub(b"", data)
    return data


def office_parts(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        return {info.filename: normalize_part(info.filename, archive.read(info.filename))
                for info in archive.infolist() if not info.is_dir()}


def pdf_pages(path: Path) -> dict[str, bytes]:
    if shutil.which("pdftoppm"):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["pdftoppm", "-r", "72", "-png", str(path), f"{tmp}/p"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return {f"page-{i + 1}": png.read_bytes()
                    for i, png in enumerate(sorted(Path(tmp).glob("p-*.png"), key=lambda p: int(p.stem.split("-")[-1])))}
    return {"bytes": _PDF_VOLATILE.sub(b"", path.read_bytes())}


def file_parts(path: Path) -> dict[str, bytes]:
    suffix = path.suffix.lower()
    if suffix in OFFICE:
        return office_parts(path)
    if suffix == ".pdf":
        return pdf_pages(path)
    data = path.read_bytes()
    if suffix in TEXT:
        data = data.replace(b"\r\n", b"\n")
    return {"": data}


def iter_files(root: Path, exclude: tuple[str, ...] = ()) -> list[Path]:
    files = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_file() and path.name not in IGNORED_NAMES and not any(re.search(p, rel) for p in exclude):
            files.append(path)
    return files


def snapshot(root: Path, exclude: tuple[str, ...] = ()) -> dict[str, dict[str, str]]:
    return {path.relative_to(root).as_posix(): {part: _sha(data) for part, data in sorted(file_parts(path).items())}
            for path in iter_files(root, exclude)}


def compare(old: dict[str, dict[str, str]], new: dict[str, dict[str, str]]) -> list[str]:
    lines = []
    for name in sorted(set(old) | set(new)):
        if name not in new:
            lines.append(f"缺少：{name}")
        elif name not in old:
            lines.append(f"多出：{name}")
        elif old[name] != new[name]:
            parts = sorted(p for p in set(old[name]) | set(new[name]) if old[name].get(p) != new[name].get(p))
            label = "、".join(p or "全文" for p in parts)
            lines.append(f"不同：{name}（{label}）")
    return lines


def _text_diff(a: bytes, b: bytes, label: str, limit: int) -> list[str]:
    def lines(data: bytes) -> list[str]:
        text = data.decode("utf-8", "replace")
        if text.lstrip().startswith("<"):
            text = re.sub(r">\s*<", ">\n<", text)
        return text.splitlines()
    out = list(difflib.unified_diff(lines(a), lines(b), f"改前/{label}", f"改后/{label}", n=1, lineterm=""))
    return out[:limit] + ([f"……还有 {len(out) - limit} 行差异"] if len(out) > limit else [])


def diff_dirs(a: Path, b: Path, exclude: tuple[str, ...] = (), limit: int = 40) -> list[str]:
    names_a = {p.relative_to(a).as_posix() for p in iter_files(a, exclude)}
    names_b = {p.relative_to(b).as_posix() for p in iter_files(b, exclude)}
    report = []
    for name in sorted(names_a | names_b):
        if name not in names_b:
            report.append(f"缺少：{name}")
            continue
        if name not in names_a:
            report.append(f"多出：{name}")
            continue
        pa, pb = file_parts(a / name), file_parts(b / name)
        for part in sorted(set(pa) | set(pb)):
            if pa.get(part) == pb.get(part):
                continue
            label = f"{name}::{part}" if part else name
            report.append(f"不同：{label}")
            if part.startswith("page-") or Path(part or name).suffix.lower() in {".png", ".jpg", ".jpeg", ".emf", ".bin"}:
                continue
            report.extend("  " + line for line in _text_diff(pa.get(part, b""), pb.get(part, b""), label, limit))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--exclude", action="append", default=[], help="不参与比对的相对路径（正则），可重复")
    sub = parser.add_subparsers(dest="command", required=True)
    s = sub.add_parser("snapshot")
    s.add_argument("root", type=Path)
    s.add_argument("-o", "--output", type=Path, required=True)
    c = sub.add_parser("check")
    c.add_argument("root", type=Path)
    c.add_argument("manifest", type=Path)
    d = sub.add_parser("diff")
    d.add_argument("a", type=Path)
    d.add_argument("b", type=Path)
    d.add_argument("--limit", type=int, default=40)
    args = parser.parse_args(argv)
    exclude = tuple(args.exclude)

    if args.command == "snapshot":
        data = snapshot(args.root, exclude)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(data, ensure_ascii=False, indent=1, sort_keys=True) + "\n", "utf-8")
        print(f"已记录 {len(data)} 份样张：{args.output}")
        return 0
    if args.command == "check":
        problems = compare(json.loads(args.manifest.read_text("utf-8")), snapshot(args.root, exclude))
    else:
        problems = diff_dirs(args.a, args.b, exclude, args.limit)
    if problems:
        print("\n".join(problems))
        return 1
    print("样张一致")
    return 0


if __name__ == "__main__":
    sys.exit(main())
