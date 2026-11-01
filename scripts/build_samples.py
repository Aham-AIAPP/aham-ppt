#!/usr/bin/env python3
"""生成基准样张：用 demo/build.js 的五页示例走一遍完整流程，把每一步的产出写进同一个目录。

用法：
  python scripts/build_samples.py 输出目录 [--repo 仓库根目录] [--check]

  --repo   用哪一份仓库的引擎生成，默认是本脚本所在的仓库。CI 用它给 PR 的基础分支生成对照样张。
  --check  生成后按 CONTRIBUTING.md 的约定检查：check_slides.js 为 0 个 ERROR、0 个 WARNING，
           check_deck.py 为 0 个 ERROR。不满足时返回 1。

输出目录里的样张：
  deck/deck.json、deck/slides/*.html   demo/build.js 写出的网页幻灯片
  preview.html                          preview.js 合成的预览页
  check_slides.md                       check_slides.js 的报告
  png/01.png …                          check_slides.js --png 的逐页截图
  demo.pptx                             html2pptx.js 导出的 PPTX
  check_deck.md                         check_deck.py 用示例配置检查 PPTX 的报告

本脚本只按顺序调用仓库现有的命令，不改它们的参数含义。导出和截图依赖浏览器排版，
同一台机器上两次生成应当一致，换机器或换浏览器版本后不保证一致，所以仓库里不存校验值清单，
改用 scripts/compare_outputs.py diff 比对同一台机器上改前、改后的两份样张。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
SUMMARY = re.compile(r"ERROR (\d+) 条　WARNING (\d+) 条")


def run(cmd: list[str], cwd: Path | None = None, ok: tuple[int, ...] = (0,)) -> subprocess.CompletedProcess:
    """运行一条命令；退出码不在 ok 里时打印输出并中止。"""
    print("$", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8")
    if proc.returncode not in ok:
        sys.stdout.write(proc.stdout)
        sys.stderr.write(proc.stderr)
        raise SystemExit(f"命令失败，退出码 {proc.returncode}：{' '.join(cmd)}")
    if proc.stderr.strip():
        sys.stderr.write(proc.stderr)
    return proc


def build(out: Path, repo: Path) -> dict[str, int]:
    engine = repo / "assets" / "html2pptx"
    tools = repo / "assets" / "tools"
    deck = out / "deck"

    run(["node", str(engine / "demo" / "build.js"), str(deck)])
    run(["node", str(engine / "preview.js"), str(deck), str(out / "preview.html")])

    # check_slides.js 有 ERROR 时退出码为 1，这是检查结论，不是生成失败；退出码 2 才是程序出错
    proc = run(["node", str(engine / "check_slides.js"), str(deck), "--png", str(out / "png")], ok=(0, 1))
    (out / "check_slides.md").write_text(proc.stdout, "utf-8")
    m = SUMMARY.search(proc.stdout)
    if not m:
        raise SystemExit("check_slides.js 的报告里找不到 ERROR、WARNING 计数")
    slides_err, slides_warn = int(m.group(1)), int(m.group(2))

    run(["node", str(engine / "html2pptx.js"), str(deck), str(out / "demo.pptx")])

    # 在输出目录里用相对路径运行，报告第一行的文件名在任何目录下都相同，两份样张才能逐字比对
    run([sys.executable, str(tools / "check_deck.py"), "demo.pptx",
         "--config", str(tools / "check_deck.example.json"), "--out", "check_deck.md"],
        cwd=out, ok=(0, 1))
    m = SUMMARY.search((out / "check_deck.md").read_text("utf-8"))
    if not m:
        raise SystemExit("check_deck.py 的报告里找不到 ERROR、WARNING 计数")
    return {"slides_error": slides_err, "slides_warning": slides_warn,
            "deck_error": int(m.group(1)), "deck_warning": int(m.group(2))}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out", type=Path, help="输出目录，必须不存在或为空")
    parser.add_argument("--repo", type=Path, default=HERE, help="用哪一份仓库的引擎生成，默认是本仓库")
    parser.add_argument("--check", action="store_true", help="检查结果不为 0 时返回 1")
    args = parser.parse_args(argv)

    out, repo = args.out.resolve(), args.repo.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"输出目录不为空：{out}")
    out.mkdir(parents=True, exist_ok=True)

    counts = build(out, repo)
    files = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file())
    print(f"已生成 {len(files)} 份样张：{out}")
    print(f"check_slides.js：ERROR {counts['slides_error']}　WARNING {counts['slides_warning']}")
    print(f"check_deck.py：ERROR {counts['deck_error']}　WARNING {counts['deck_warning']}")

    if args.check and (counts["slides_error"] or counts["slides_warning"] or counts["deck_error"]):
        print("检查未通过：check_slides.js 应为 0 个 ERROR、0 个 WARNING，check_deck.py 应为 0 个 ERROR。")
        print((out / "check_slides.md").read_text("utf-8"))
        print((out / "check_deck.md").read_text("utf-8"))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
