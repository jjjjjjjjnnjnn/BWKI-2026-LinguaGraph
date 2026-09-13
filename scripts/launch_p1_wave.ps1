# P1 wave launcher (detached): 5 channels x resume-safe P1 collection.
# Run detached: Start-Process powershell -Args '-File scripts/launch_p1_wave.ps1' -WindowStyle Hidden
$R = 'C:\Users\rongj\Desktop\学校\BWKI-2026-备战'
$L = 'C:\Users\rongj\AppData\Local\Temp\opencode\p1wave'
New-Item -ItemType Directory -Path $L -Force | Out-Null
$env:OPENCODE_CALL_TIMEOUT = '180'
$env:LDS_ABORT_AFTER = '3'

function Launch($name, $log, $cmd) {
    Start-Process -FilePath 'python' -ArgumentList $cmd -WorkingDirectory $R `
        -RedirectStandardOutput "$L/$log" -RedirectStandardError "$L/${name}.err" `
        -WindowStyle Hidden
}

$env:LDS_SLEEP_SECS = '2'
Launch 'j1' 'j1-spark.log' @('scripts/lds_c_opencode_run_subject.py','--model','opencode-go/muse-spark-1.3-contributor','--provider','opencode-go','--probes','P1','--k','10')
Start-Sleep -Seconds 20
Launch 'j2' 'j2-grok.log' @('scripts/lds_c_opencode_run_subject.py','--model','opencode-go/grok-4.6','--provider','opencode-go','--probes','P1','--k','10')

$env:LDS_SLEEP_SECS = '3'
Launch 'j3' 'j3-qwenmax.log' @('scripts/lds_c_llm_subject.py','--model','qwen-max','--provider','dashscope','--api-url','https://dashscope.aliyuncs.com/compatible-mode/v1','--api-key-env','DASHSCOPE_API_KEY','--probes','P1','--k','10')

$env:LDS_SLEEP_SECS = '5'
$or = @('scripts/lds_c_llm_subject.py','--api-url','https://openrouter.ai/api/v1','--api-key-env','OPENROUTER_API_KEY','--probes','P1','--k','10')
# sequential OR chain in one detached process (shared daily quota)
$chain = '$m=@(@(\"openrouter\",\"nvidia/nemotron-3-ultra-550b-a55b:free\"),@(\"\",\"nvidia/nemotron-3-nano-30b-a3b:free\"),@(\"\",\"poolside/laguna-s-2.1:free\"),@(\"\",\"cohere/north-mini-code:free\"),@(\"\",\"inclusionai/ling-3.0-tiny:free\"));foreach($x in $m){if($x[0]-eq\"\"){python scripts/lds_c_llm_subject.py --model $x[1] --api-url https://openrouter.ai/api/v1 --api-key-env OPENROUTER_API_KEY --probes P1 --k 10}else{python scripts/lds_c_llm_subject.py --model $x[1] --provider $x[0] --api-url https://openrouter.ai/api/v1 --api-key-env OPENROUTER_API_KEY --probes P1 --k 10}}'
Start-Process -FilePath 'powershell' -ArgumentList @('-NoProfile','-Command',$chain) -WorkingDirectory $R `
    -RedirectStandardOutput "$L/j4-openrouter.log" -RedirectStandardError "$L/j4.err" -WindowStyle Hidden

$env:LDS_SLEEP_SECS = '90'
Launch 'j5' 'j5-mistral.log' @('scripts/lds_c_llm_subject.py','--model','mistral-medium-latest','--api-url','https://api.mistral.ai/v1','--api-key-env','MISTRAL_API_KEY','--probes','P1','--k','10')
