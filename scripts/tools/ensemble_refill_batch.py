#!/usr/bin/env python3
"""Parallel ensemble refill batch runner.

Usage:
  python scripts/tools/ensemble_refill_batch.py --jobs "m1:depth:n1,m2:breadth:n2" [--workers 5] [--timeout 300]

Parent (unicode-safe, in-process) pre-picks smallest-first missing targets with
globally distinct bases (no shared stage file). Workers run
ensemble_refill_one.py --no-manifest as subprocesses (isolated, no sys.argv
race). Parent updates each _manifest.json single-threaded (no lost updates).
Stops scheduling new work on 403/quota signature. Key ONLY from env.
Exit 0 = all filed; 2 = partial (some failed/absent, details in output).
"""
import concurrent.futures
import json
import os
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DRIVER = os.path.join(BASE_DIR, "scripts", "tools", "ensemble_refill_one.py")


def tsize(base):
    p = os.path.join(BASE_DIR, "data", "textbook", base + ".txt")
    return os.path.getsize(p) if os.path.exists(p) else 10 ** 12


def pick(model, mode, n, used_bases):
    depth = json.load(open(os.path.join(BASE_DIR, "research", "ensemble_v2",
                                        "depth24.json"), encoding="utf-8"))["depth24"]
    exp = {"%s.r%d.json" % (b, i) for b in depth for i in (1, 2, 3)}
    ddir = os.path.join(BASE_DIR, "research", "ensemble_v2", model)
    disk = {f for f in os.listdir(ddir) if f.endswith(".json") and f != "_manifest.json"}
    m = json.load(open(os.path.join(ddir, "_manifest.json"), encoding="utf-8"))
    if mode == "depth":
        dnr = set(m.get("do_not_retry", [])) if (m := json.load(open(os.path.join(ddir, "_manifest.json"), encoding="utf-8"))) else set()
        pool = sorted((exp - disk - dnr), key=lambda f: (tsize(f[:-8] if f[-8:-6] == ".r" else f), f))
    else:
        pool = sorted([f for f in m.get("missing", []) if f not in exp and f not in disk],
                      key=lambda f: (tsize(f[:-8] if f[-8:-6] == ".r" else f), f))
    out = []
    for f in pool:
        b = f[:-8] if f[-8:-6] == ".r" else f
        if b in used_bases:
            continue
        used_bases.add(b)
        out.append((model, b, f))
        if len(out) >= n:
            break
    return out


def log(s, flush=True):
    try:
        print(s, flush=flush)
    except UnicodeEncodeError:
        print(s.encode("ascii", "backslashreplace").decode("ascii"), flush=flush)


def run_one(model, base, target, timeout):
    env = dict(os.environ)
    try:
        r = subprocess.run([sys.executable, "-B", DRIVER, "--model", model,
                            "--base", base, "--target", target,
                            "--no-manifest", "--timeout", str(timeout)],
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout + 90, cwd=BASE_DIR)
        out = (r.stdout or "") + (r.stderr or "")
    except subprocess.TimeoutExpired:
        return (model, target, "timeout", "")
    filed_ok = (r.returncode == 0 and "FILED" in out)
    quota = ("403" in out or "AllocationQuota" in out or "FreeTierOnly" in out)
    return (model, target, "filed" if filed_ok else ("quota" if quota else "fail"), out[-400:])


def update_manifests(filed):
    by_model = {}
    for model, target in filed:
        by_model.setdefault(model, []).append(target)
    for model, targets in by_model.items():
        mf_p = os.path.join(BASE_DIR, "research", "ensemble_v2", model, "_manifest.json")
        m = json.load(open(mf_p, encoding="utf-8"))
        for t in targets:
            if t not in m.get("done", []):
                m.setdefault("done", []).append(t)
            m["missing"] = [x for x in m.get("missing", []) if x != t]
            m["failed"] = [x for x in m.get("failed", []) if x != t]
        json.dump(m, open(mf_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main():
    args = sys.argv[1:]
    if "--help" in args or "-h" in args:
        print('Usage: ensemble_refill_batch.py --jobs "model:depth|breadth:n,..." [--workers 5] [--timeout 300]')
        print("  Pre-picks smallest-first missing targets (distinct bases); workers run")
        print("  ensemble_refill_one.py --no-manifest; parent updates manifests. Key from env.")
        return 0
    jobs = args[args.index("--jobs") + 1]
    workers = int(args[args.index("--workers") + 1]) if "--workers" in args else 5
    timeout = int(args[args.index("--timeout") + 1]) if "--timeout" in args else 300
    used = set()
    queue = []
    for spec in jobs.split(","):
        model, mode, n = spec.split(":")
        queue.extend(pick(model.strip(), mode.strip(), int(n), used))
    log("QUEUED %d distinct-bases" % len(queue), flush=True)
    if not queue:
        return 2
    filed, failed, quota_hit = [], [], False
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(run_one, mo, ba, ta, timeout): (mo, ta)
                for mo, ba, ta in queue}
        for fut in concurrent.futures.as_completed(futs):
            mo, ta = futs[fut]
            try:
                m2, t2, status, tail = fut.result()
            except Exception as e:
                status, tail = "fail", repr(e)[:200]
            if status == "filed":
                filed.append((m2, t2))
                log("FILED %s/%s" % (m2, t2), flush=True)
            elif status == "quota":
                quota_hit = True
                failed.append((m2, t2, "quota"))
                log("QUOTA_HIT %s/%s STOP-SCHEDULING" % (m2, t2), flush=True)
            else:
                failed.append((m2, t2, tail[-120:]))
                log("FAIL %s/%s %s" % (m2, t2, tail[-120:]), flush=True)
    update_manifests(filed)
    log("BATCH_DONE filed=%d failed=%d quota=%s" % (len(filed), len(failed), quota_hit))
    return 0 if not failed else 2


if __name__ == "__main__":
    sys.exit(main())
