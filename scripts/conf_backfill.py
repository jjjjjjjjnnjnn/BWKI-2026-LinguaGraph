"""P2 conf backfill: re-run only the -1 (resumed, conf unknown) pages per book.
GPU dml. Run once; merges into existing manifests.
Usage: python scripts/conf_backfill.py
"""
import glob
import json
import subprocess
import sys
from pathlib import Path

PDF_FOR = {
    "zh_huaxue_xb1": "data/textbook/cn_mirror/zh_化学选必1_化学反应原理.pdf",
    "zh_huaxue_xb2": "data/textbook/cn_mirror/zh_化学选必2_物质结构与性质.pdf",
    "zh_huaxue_xb3": "data/textbook/cn_mirror/zh_化学选必3_有机化学基础.pdf",
    "zh_wuli_bx3": "data/textbook/cn_mirror/zh_物理必修3_普通高中教科书.pdf",
    "zh_wuli_xb1": "data/textbook/cn_mirror/zh_物理选必1_普通高中教科书.pdf",
    "zh_wuli_xb2": "data/textbook/cn_mirror/zh_物理选必2_普通高中教科书.pdf",
    "zh_wuli_xb3": "data/textbook/cn_mirror/zh_物理选必3_普通高中教科书.pdf",
}
SKILL = r"C:\Users\rongj\.config\opencode\skills\pdf-reading\scripts\pdf_extract.py"


def main() -> None:
    for prefix, pdf in PDF_FOR.items():
        mf = Path(f"data/textbook/pages/{prefix}/{prefix}_manifest_ocr.json")
        d = json.loads(mf.read_text(encoding="utf-8"))
        miss = [str(p["page"]) for p in d["pages"]
                if p.get("mean_conf", 0) == -1.0]
        if not miss:
            print(f"{prefix}: nothing missing")
            continue
        print(f"{prefix}: backfilling {len(miss)} pages", flush=True)
        r = subprocess.run(
            [sys.executable, SKILL, pdf, "--out",
             f"data/textbook/pages/{prefix}", "--prefix", prefix,
             "--force-tier", "scan", "--dpi", "150", "--device", "dml",
             "--pages", ",".join(miss)],
            capture_output=True, text=True)
        print(r.stdout[-500:] if r.stdout else "")
        if r.returncode != 0:
            print(f"FAILED {prefix}:\n{r.stderr[-2000:]}")
            return
    print("backfill done")


if __name__ == "__main__":
    main()
