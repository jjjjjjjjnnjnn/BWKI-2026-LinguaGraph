@echo off
REM ==========================================
REM OpenCode GO 模型批量基准测试
REM 使用前设置环境变量:
REM   set OPENCODE_KEY=sk-你的key
REM 然后运行: run_all_models.bat
REM ==========================================

if "%OPENCODE_KEY%"=="" (
    echo ERROR: 请先设置环境变量 OPENCODE_KEY
    echo   set OPENCODE_KEY=sk-你的key
    pause
    exit /b 1
)

cd /d C:\Users\rongj\Desktop\学校\BWKI-2026-备战

echo ===== 开始所有模型 N=92 基准测试 =====
echo 预计时间: 每个模型 ~20-30 分钟, 共 ~6 小时
echo.

REM ===== Batch 1 =====
echo [1/15] qwen3.7-plus...
python scripts/run_one_model_curl.py qwen3.7-plus
echo [2/15] qwen3.7-max...
python scripts/run_one_model_curl.py qwen3.7-max
echo [3/15] qwen3.6-plus...
python scripts/run_one_model_curl.py qwen3.6-plus
echo [4/15] qwen3.5-plus...
python scripts/run_one_model_curl.py qwen3.5-plus

REM ===== Batch 2 =====
echo [5/15] kimi-k2.6...
python scripts/run_one_model_curl.py kimi-k2.6
echo [6/15] kimi-k2.5...
python scripts/run_one_model_curl.py kimi-k2.5
echo [7/15] minimax-m3...
python scripts/run_one_model_curl.py minimax-m3
echo [8/15] minimax-m2.7...
python scripts/run_one_model_curl.py minimax-m2.7

REM ===== Batch 3 =====
echo [9/15] minimax-m2.5...
python scripts/run_one_model_curl.py minimax-m2.5
echo [10/15] glm-5.2...
python scripts/run_one_model_curl.py glm-5.2
echo [11/15] glm-5.1...
python scripts/run_one_model_curl.py glm-5.1
echo [12/15] glm-5...
python scripts/run_one_model_curl.py glm-5

REM ===== Batch 4 =====
echo [13/15] hy3-preview...
python scripts/run_one_model_curl.py hy3-preview
echo [14/15] mimo-v2.5-pro...
python scripts/run_one_model_curl.py mimo-v2.5-pro
echo [15/15] mimo-v2.5...
python scripts/run_one_model_curl.py mimo-v2.5

REM ===== Generate final figure =====
echo.
echo === ALL DONE. Generating Fig 5... ===
python scripts/figures/fig5_falsification.py

echo.
echo === Final Benchmark Results ===
python -c "import json,glob; R=[]; [R.append(json.load(open(f,encoding='utf-8'))) for f in sorted(glob.glob('data/model_comparison/oc_*_results.json'))]; R.sort(key=lambda x: -x['summary']['mean_f1']); print(f'{\"Rank\":4s} {\"Model\":25s} {\"F1\":8s} {\"N\":5s}'); print('-'*45); [print(f'{i+1:4d} {r[\"model\"]:25s} {r[\"summary\"][\"mean_f1\"]:.4f}  {r[\"valid\"]}/{r[\"total_items\"]}') for i,r in enumerate(R)]"

pause
