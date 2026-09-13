# Slow-drip scheduler for rate-limited channels (e.g. mistral official 429).
# Runs the subject script with --limit 2 per wave so ABORT_AFTER=3 never
# false-fires on 429s; sleeps 10 min between waves; stops at 30 good units.
# Detached: Start-Process cmd.exe /c <thisfile> -WindowStyle Hidden
set LDS_ABORT_AFTER=3
set LDS_SLEEP_SECS=600
:loop
python scripts/lds_c_llm_subject.py --model mistral-medium-latest --api-url https://api.mistral.ai/v1 --api-key-env MISTRAL_API_KEY --probes P1 --k 10 --limit 2 >> C:\Users\rongj\AppData\Local\Temp\opencode\p1wave\j5-mistral-drip.log 2>&1
python -c "import sys;sys.path.insert(0,'scripts');from lds_c_llm_subject import collect_good_units;from pathlib import Path;g=collect_good_units(Path('data/lds_c/llm_subject'),'llm_subject_mistral-medium-latest');print('good=',len(g));sys.exit(0 if len(g)>=30 else 1)"
if %errorlevel%==0 goto done
timeout /t 600 /nobreak >nul
goto loop
:done
echo DRIP-COMPLETE >> C:\Users\rongj\AppData\Local\Temp\opencode\p1wave\j5-mistral-drip.log
