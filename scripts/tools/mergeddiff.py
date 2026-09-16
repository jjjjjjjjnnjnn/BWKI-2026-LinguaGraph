#!/usr/bin/env python3
"""Diff rebuilt merged relations vs frozen backup (read-only)."""
import io
import json

old = json.load(io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\merged_bak\\aligned_data.json", encoding="utf-8"))["relations"]
new = json.load(io.open("data/math_extractions/merged/aligned_data.json", encoding="utf-8"))["relations"]


def key(r):
    return (r.get("source"), r.get("target"), r.get("type"))


so, sn = {key(r) for r in old}, {key(r) for r in new}
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\mergeddiff.txt", "w", encoding="utf-8")
o.write("old=%d new=%d\n" % (len(old), len(new)))
o.write("--- vanished (in old, not new) ---\n")
for k in sorted(so - sn):
    o.write(repr(k) + "\n")
o.write("--- appeared (in new, not old) ---\n")
for k in sorted(sn - so):
    o.write(repr(k) + "\n")
o.close()
print("old=%d new=%d vanished=%d appeared=%d" % (len(old), len(new), len(so - sn), len(sn - so)))
