"""Detached sequential supervisor for local LM Studio P1 collection (v2).

Direct Popen (no cmd wrapper): supervisor owns worker handles, can
poll/kill/relaunch. Stall = log unchanged for 12 min -> kill + relaunch
(max 3 per tag). Queue: phi -> qwen05 -> gemma -> [sauerkraut + hymt] ->
qwen3 -> qwen35. ONE wave at a time (parallel inside B only).
Log: p1local/supervisor.log
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(r'C:\Users\rongj\Desktop\学校\BWKI-2026-备战')
LDIR = Path(r'C:\Users\rongj\AppData\Local\Temp\opencode\p1local')
LMS = r'C:\Users\rongj\.lmstudio\bin\lms.exe'
SLOG = LDIR / 'supervisor.log'
API = 'http://127.0.0.1:1234/v1'
STALL_S = 720
MAX_RELAUNCH = 3

QUEUE = [
    (('phi-4-mini-instruct',), ('phi',)),
    (('qwen2.5-0.5b-instruct',), ('qwen05',)),
    (('gemma-3-270m-it',), ('gemma',)),
    (('llama-3-sauerkrautlm-8b-instruct', 'hy-mt2-1.8b'), ('sauerkraut', 'hymt')),
    (('qwen/qwen3-8b',), ('qwen3',)),
    (('qwen/qwen3.5-9b',), ('qwen35',)),
]


def log(msg):
    line = time.strftime('%H:%M:%S') + ' ' + msg
    print(line, flush=True)
    with open(SLOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def loaded_ids():
    try:
        d = json.load(urllib.request.urlopen(API + '/models', timeout=15))
        return [m['id'] for m in d.get('data', [])]
    except Exception:
        return []


def lms(args):
    r = subprocess.run([LMS] + args, capture_output=True, text=True, timeout=600)
    return r.returncode


def finished(tag):
    p = LDIR / ('j-' + tag + '.log')
    if not p.exists():
        return False
    t = p.read_text(encoding='utf-8', errors='replace')
    return ('Done:' in t) or ('ABORT ' in t)


def launch(api_id, tag):
    import os
    env = dict(os.environ)
    env['LMSTUDIO_API_KEY'] = 'not-needed'
    env['LDS_ABORT_AFTER'] = '3'
    env['LDS_SLEEP_SECS'] = '3'
    fh = open(LDIR / ('j-' + tag + '.log'), 'a', encoding='utf-8')
    proc = subprocess.Popen(
        [sys.executable, 'scripts/lds_c_llm_subject.py', '--model', api_id,
         '--provider', 'lmstudio', '--api-url', API, '--api-key-env',
         'LMSTUDIO_API_KEY', '--probes', 'P1', '--k', '10'],
        cwd=str(ROOT), env=env, stdout=fh, stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    return proc, fh


def main():
    log('supervisor-v2 start')
    for keys, tags in QUEUE:
        for k in keys:
            log('load ' + k + ' rc=' + str(lms(['load', k, '--yes'])))
        time.sleep(8)
        ids = loaded_ids()
        log('served: ' + str(ids))
        workers = {}
        for key, tag in zip(keys, tags):
            api_id = key if key in ids else (ids[-1] if ids else key)
            if finished(tag):
                log(tag + ' already finished, skip')
                continue
            proc, fh = launch(api_id, tag)
            workers[tag] = {'proc': proc, 'fh': fh, 'api': api_id, 'relaunches': 0}
            log('launched ' + tag + ' pid=' + str(proc.pid))
        while True:
            time.sleep(60)
            pending = [t for t in tags if not finished(t)]
            if not pending:
                break
            for t in pending:
                w = workers.get(t)
                if w is None:
                    continue
                alive = w['proc'].poll() is None
                try:
                    mtime = (LDIR / ('j-' + t + '.log')).stat().st_mtime
                except OSError:
                    mtime = 0
                stalled = (time.time() - mtime) > STALL_S
                if (not alive and not finished(t)) or stalled:
                    if w['relaunches'] >= MAX_RELAUNCH:
                        log(t + ' relaunch budget spent, moving on')
                        try:
                            w['proc'].kill()
                        except Exception:
                            pass
                        workers.pop(t)
                        continue
                    try:
                        w['proc'].kill()
                    except Exception:
                        pass
                    w['fh'].close()
                    proc, fh = launch(w['api'], t)
                    w.update({'proc': proc, 'fh': fh, 'relaunches': w['relaunches'] + 1})
                    log('relaunched ' + t + ' (stall/death) pid=' + str(proc.pid))
        for t in tags:
            w = workers.get(t)
            if w:
                try:
                    w['fh'].close()
                except Exception:
                    pass
            log(t + ' finished')
        for k in keys:
            lms(['unload', k])
    log('ALL WAVES COMPLETE')


if __name__ == '__main__':
    main()
