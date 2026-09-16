#!/usr/bin/env python3
"""Single-shot ensemble refill: extract one base, audit, file into ensemble_v2.

Usage:
  python scripts/tools/ensemble_refill_one.py --model <id> --base <basename> --target <file.rN.json> [--timeout S]

Pipeline: run bailian_reextract via runpy (unicode-safe) -> audit parsed
(15-40 concepts / 10-30 relations / refs resolve / no placeholders) ->
copy to research/ensemble_v2/<model>/<target> (skip if exists) ->
update _manifest.json (done+ / missing- / failed-).
Exit 0 = filed; 1 = usage; 2 = target exists (skip, no call); 3 = call error;
4 = audit fail (exploration only, not filed).
Key ONLY from env BAILIAN_API_KEY / BAILIAN_MAX_TOKENS / BAILIAN_BASE.
"""
import json
import os
import shutil
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def audit(parsed):
    cs = parsed["extracted_concepts"]
    rs = parsed.get("extracted_relations", [])
    assert isinstance(cs, list) and 15 <= len(cs) <= 40, "concepts=%d" % len(cs)
    assert isinstance(rs, list) and 10 <= len(rs) <= 30, "relations=%d" % len(rs)
    names = {c.get("name", "") for c in cs if isinstance(c, dict)}
    assert not any(v in ("...", "..", "") for v in names), "placeholder"
    for c in cs:
        blob = (c.get("name", "") or "") + "".join(c.get("aliases", []) or [])
        assert "?" not in blob and "\ufffd" not in blob, "mojibake"
    for r in rs:
        assert r.get("source") in names and r.get("target") in names, "dangling"


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print("usage: ensemble_refill_one.py --model ID [--base B | --depth-idx I | --auto-depth | --auto-breadth] [--target F | --run N] [--timeout S] [--no-manifest] [--help]")
        print("  Extracts one base via bailian_reextract, audits (15-40 concepts/10-30 relations/refs/no-mojibake),")
        print("  files into research/ensemble_v2/<model>/ and updates _manifest.json. Key from env.")
        return 0
    if "--model" not in args or (("--base" not in args and "--depth-idx" not in args and "--auto-depth" not in args and "--auto-breadth" not in args) or ("--target" not in args and "--run" not in args and "--auto-depth" not in args and "--auto-breadth" not in args)):
        print("usage: ensemble_refill_one.py --model ID [--base B | --depth-idx I | --auto-depth | --auto-breadth] [--target F | --run N] [--timeout S]")
        return 1
    model = args[args.index("--model") + 1]
    if "--auto-depth" in args or "--auto-breadth" in args:
        depth = json.load(open(os.path.join(BASE_DIR, "research", "ensemble_v2",
                                            "depth24.json"), encoding="utf-8"))["depth24"]
        exp = {"%s.r%d.json" % (b, i) for b in depth for i in (1, 2, 3)}
        ddir = os.path.join(BASE_DIR, "research", "ensemble_v2", model)
        disk = {f for f in os.listdir(ddir) if f.endswith(".json") and f != "_manifest.json"}

        def tsize(fn):
            b = fn[:-8] if fn[-8:-6] == ".r" else fn
            p = os.path.join(BASE_DIR, "data", "textbook", b + ".txt")
            return os.path.getsize(p) if os.path.exists(p) else 10 ** 12

        if "--auto-depth" in args:
            m0 = json.load(open(os.path.join(ddir, "_manifest.json"), encoding="utf-8"))
            dnr = set(m0.get("do_not_retry", []))
            pool = sorted((exp - disk - dnr), key=lambda f: (tsize(f), f))
        else:
            m0 = json.load(open(os.path.join(ddir, "_manifest.json"), encoding="utf-8"))
            pool = sorted([f for f in m0.get("missing", [])
                           if f not in exp and f not in disk], key=lambda f: (tsize(f), f))
        if not pool:
            print("AUTO_POOL_EMPTY")
            return 2
        target = pool[0]
        base = target[:-8] if target[-8:-6] == ".r" else target
        print("AUTO_PICK %s" % target)
    elif "--depth-idx" in args:
        di = int(args[args.index("--depth-idx") + 1])
        depth = json.load(open(os.path.join(BASE_DIR, "research", "ensemble_v2",
                                            "depth24.json"), encoding="utf-8"))["depth24"]
        base = depth[di]
    else:
        base = args[args.index("--base") + 1]
    timeout = int(args[args.index("--timeout") + 1]) if "--timeout" in args else 300
    if "--auto-depth" not in args and "--auto-breadth" not in args:
        if "--run" in args:
            target = "%s.r%s.json" % (base, args[args.index("--run") + 1])
        else:
            target = args[args.index("--target") + 1]

    dst = os.path.join(BASE_DIR, "research", "ensemble_v2", model, target)
    if os.path.exists(dst):
        print("SKIP target exists: %s" % target)
        return 2
    txt = os.path.join(BASE_DIR, "data", "textbook", base + ".txt")
    if not os.path.exists(txt):
        print("SOURCE_TXT_MISSING: %s" % base)
        return 3

    import runpy
    sys.argv = ["bailian_reextract.py", base, "--model", model, "--timeout", str(timeout)]
    stage = os.path.join(BASE_DIR, "research", "bailian_audit", base + ".bailian.json")
    before = os.path.getmtime(stage) if os.path.exists(stage) else -1.0
    call_ok = True
    try:
        runpy.run_path(os.path.join(BASE_DIR, "scripts", "tools", "bailian_reextract.py"),
                       run_name="__main__")
    except SystemExit as e:
        if e.code != 0 and e.code is not None:
            print("CALL_DONE exit=%s" % e.code)
            call_ok = False
    except Exception as e:
        print("CALL_DONE exception %s" % e)
        call_ok = False
    if not call_ok:
        print("CALL_FAILED -> refuse to file (stale stage guard)")
        return 3
    try:
        after = os.path.getmtime(stage)
    except Exception:
        after = -1.0
    if after <= before:
        print("STAGE_NOT_FRESH -> refuse to file")
        return 3

    stage = os.path.join(BASE_DIR, "research", "bailian_audit", base + ".bailian.json")
    try:
        d = json.load(open(stage, encoding="utf-8"))
    except Exception as e:
        print("STAGE_READ_FAIL %s" % e)
        return 3
    if d.get("model") != model:
        print("STAGE_MODEL_MISMATCH %s vs %s" % (d.get("model"), model))
        return 3
    try:
        audit(d.get("parsed") or {})
    except Exception as e:
        print("AUDIT_FAIL %s -> exploration only, not filed" % e)
        return 4
    shutil.copyfile(stage, dst)
    if "--no-manifest" not in args:
        mf_p = os.path.join(BASE_DIR, "research", "ensemble_v2", model, "_manifest.json")
        m = json.load(open(mf_p, encoding="utf-8"))
        if target not in m.get("done", []):
            m.setdefault("done", []).append(target)
        m["missing"] = [x for x in m.get("missing", []) if x != target]
        m["failed"] = [x for x in m.get("failed", []) if x != target]
        json.dump(m, open(mf_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        print("NO_MANIFEST_SKIP")
    p = d["parsed"]
    print("FILED %s/%s c=%d r=%d" % (model, target, len(p["extracted_concepts"]),
                                     len(p.get("extracted_relations", []))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
