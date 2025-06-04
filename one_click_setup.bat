@echo off
:: Install dependencies, set up autorun, and start the assistant on Windows
if not exist venv (
    python -m venv venv
)
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

:: Create a startup task to run the assistant after login
schtasks /Query /TN "SamanthaAssistant" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    schtasks /Create /SC ONLOGON /RL HIGHEST /TN "SamanthaAssistant" ^
        /TR "\"%CD%\venv\Scripts\python.exe\" \"%CD%\rag_assistant.py\"" /F
)

call venv\Scripts\python.exe rag_assistant.py
