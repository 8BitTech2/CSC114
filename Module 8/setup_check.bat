@echo off
echo === C2C Agent Demo Setup Check ===
echo.

echo [1/4] Checking Python...
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
    python3 --version 2>NUL
    if %ERRORLEVEL% NEQ 0 (
        echo FAILED: Python not found. Try "python3" instead of "python" in later commands, or ask IT for Python access.
        pause
        exit /b 1
    )
)
echo OK
echo.

echo [2/4] Installing required packages...
pip install --user scikit-learn requests numpy
if %ERRORLEVEL% NEQ 0 (
    echo FAILED: pip install did not complete. Lab machine may block package installs.
    echo Try running this script as Administrator, or ask IT to pre-install: scikit-learn, requests, numpy
    pause
    exit /b 1
)
echo OK
echo.

echo [3/4] Checking ANTHROPIC_API_KEY is set...
if "%ANTHROPIC_API_KEY%"=="" (
    echo WARNING: ANTHROPIC_API_KEY is not set in this terminal session.
    echo Run: set ANTHROPIC_API_KEY=sk-ant-your-key-here
    echo Then re-run this script.
) else (
    echo OK - key is set for this session
)
echo.

echo [4/4] Testing connection to Anthropic API...
python -c "import requests, os; k=os.environ.get('ANTHROPIC_API_KEY'); r=requests.post('https://api.anthropic.com/v1/messages', headers={'x-api-key':k,'anthropic-version':'2023-06-01','content-type':'application/json'}, json={'model':'claude-sonnet-4-6','max_tokens':20,'messages':[{'role':'user','content':'say OK'}]}, timeout=15); print('HTTP', r.status_code); print(r.text[:300])"
echo.

echo === Setup check complete ===
echo If step 4 printed "HTTP 200" and readable text, you are ready for the live demo.
echo If step 4 failed with a connection error, the lab network likely blocks api.anthropic.com -- use the backup plan (saved gap_report.json + dashboard).
echo If step 4 failed with HTTP 401, double-check your API key is correct.
pause
