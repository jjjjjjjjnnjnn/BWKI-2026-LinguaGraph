"""Download the 7 needed PEP textbooks from the TapXWorld/ChinaTextbook mirror
(third-party copy; provenance unverified — local research use only, never committed).
Target: data/textbook/cn_mirror/ (gitignored via data/textbook/).
Usage: python scripts/fetch_cn_pep_mirror.py
"""
import urllib.request
from pathlib import Path

BASE = ("https://raw.githubusercontent.com/TapXWorld/ChinaTextbook/master/"
        "{path}")
PUB = "人教版-人民教育出版社"
OUT = Path("data/textbook/cn_mirror")
UA = {"User-Agent": "BWKI-2026-LinguaGraph research (single-file fetch)"}

JOBS = [
    # (local_name, subject_dir, remote_name)
    ("zh_物理必修3_普通高中教科书.pdf", "物理", "普通高中教科书·物理必修 第三册.pdf"),
    ("zh_物理选必1_普通高中教科书.pdf", "物理", "普通高中教科书·物理选择性必修 第一册.pdf"),
    ("zh_物理选必2_普通高中教科书.pdf", "物理", "普通高中教科书·物理选择性必修 第二册.pdf"),
    ("zh_物理选必3_普通高中教科书.pdf", "物理", "普通高中教科书·物理选择性必修 第三册.pdf"),
    ("zh_化学选必1_化学反应原理.pdf", "化学", "普通高中教科书·化学选择性必修1 化学反应原理.pdf"),
    ("zh_化学选必2_物质结构与性质.pdf", "化学", "普通高中教科书·化学选择性必修2 物质结构与性质.pdf"),
    ("zh_化学选必3_有机化学基础.pdf", "化学", "普通高中教科书·化学选择性必修3 有机化学基础.pdf"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ok = 0
    for local, sub, remote in JOBS:
        from urllib.parse import quote
        path = quote(f"高中/{sub}/{PUB}/{remote}", safe="/")
        url = BASE.format(path=path)
        dest = OUT / local
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=300) as r, open(dest, "wb") as f:
                total = 0
                while True:
                    chunk = r.read(1 << 20)
                    if not chunk:
                        break
                    f.write(chunk)
                    total += len(chunk)
            head = dest.read_bytes()[:5]
            assert head.startswith(b"%PDF"), f"not a PDF: {head!r}"
            print(f"OK {local}: {total / 1e6:.1f}MB")
            ok += 1
        except Exception as exc:  # noqa: BLE001
            print(f"FAIL {local}: {exc}")
            if dest.exists():
                dest.unlink()
    print(f"{ok}/{len(JOBS)} downloaded")


if __name__ == "__main__":
    main()
