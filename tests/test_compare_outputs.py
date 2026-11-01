"""scripts/compare_outputs.py 的自测：时间戳不算差异，内容变化必须报出来。"""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
import zipfile
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import compare_outputs  # noqa: E402

CORE = ('<cp:coreProperties><dcterms:created xsi:type="dcterms:W3CDTF">{t}</dcterms:created>'
        '<dcterms:modified xsi:type="dcterms:W3CDTF">{t}</dcterms:modified></cp:coreProperties>')


def docx(path: Path, body: str, stamp: str, zip_time=(2026, 1, 1, 0, 0, 0)) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in (("word/document.xml", f"<w:document><w:t>{body}</w:t></w:document>"),
                           ("docProps/core.xml", CORE.format(t=stamp)),
                           ("docProps/app.xml", f"<Properties><TotalTime>{stamp[-2:]}</TotalTime></Properties>")):
            archive.writestr(zipfile.ZipInfo(name, zip_time), data)


def quiet(*args: str) -> int:
    with redirect_stdout(io.StringIO()):
        return compare_outputs.main(list(args))


class CompareOutputsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_timestamps_are_ignored(self) -> None:
        docx(self.root / "a/x.docx", "正文", "2026-11-01T00:00:01Z")
        docx(self.root / "b/x.docx", "正文", "2026-11-02T08:30:59Z", zip_time=(2027, 5, 5, 5, 5, 4))
        (self.root / "a/p.html").write_bytes(b"<p>1</p>\r\n")
        (self.root / "b/p.html").write_bytes(b"<p>1</p>\n")
        self.assertEqual(compare_outputs.diff_dirs(self.root / "a", self.root / "b"), [])

    def test_part_change_is_reported_with_part_name(self) -> None:
        docx(self.root / "a/x.docx", "正文", "2026-11-01T00:00:01Z")
        docx(self.root / "b/x.docx", "正文改", "2026-11-01T00:00:01Z")
        report = compare_outputs.diff_dirs(self.root / "a", self.root / "b")
        self.assertIn("不同：x.docx::word/document.xml", report)
        self.assertTrue(any("正文改" in line for line in report))

    def test_missing_and_extra_files(self) -> None:
        (self.root / "a").mkdir()
        (self.root / "b").mkdir()
        (self.root / "a/old.json").write_text("{}", "utf-8")
        (self.root / "b/new.json").write_text("{}", "utf-8")
        self.assertEqual(compare_outputs.diff_dirs(self.root / "a", self.root / "b"),
                         ["多出：new.json", "缺少：old.json"])

    def test_snapshot_and_check_round_trip(self) -> None:
        docx(self.root / "out/x.docx", "正文", "2026-11-01T00:00:01Z")
        manifest = self.root / "manifest.json"
        self.assertEqual(quiet("snapshot", str(self.root / "out"), "-o", str(manifest)), 0)
        self.assertEqual(quiet("check", str(self.root / "out"), str(manifest)), 0)
        docx(self.root / "out/x.docx", "正文改", "2026-11-01T00:00:01Z")
        self.assertEqual(quiet("check", str(self.root / "out"), str(manifest)), 1)


if __name__ == "__main__":
    unittest.main()
