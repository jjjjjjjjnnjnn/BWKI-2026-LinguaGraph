#!/usr/bin/env python3
"""Which rendered links vanished in pipeline rebuild (read-only)."""
import io
import json

old = json.load(io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\merged_bak\\visualization_data.json", encoding="utf-8"))["links"]
new = json.load(io.open("data/math_extractions/merged/visualization_data.json", encoding="utf-8"))["links"]
o = io.open("C:\\Users\\rongj\\AppData\\Local\\Temp\\opencode\\visdiff.txt", "w", encoding="utf-8")


def key(e):
    return (e.get("source"), e.get("target"))


so = {key(e) for e in old}
sn = {key(e) for e in new}
o.write("old=%d new=%d\nvanished:\n" % (len(old), len(new)))
for k in sorted(so - sn):
    o.write(repr(k) + "\n")
o.write("appeared:\n")
for k in sorted(sn - so):
    o.write(repr(k) + "\n")
o.close()
print("old=%d new=%d vanished=%d appeared=%d" % (len(old), len(new), len(so - sn), len(sn - so)))
