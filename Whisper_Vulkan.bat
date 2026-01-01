@echo off
setlocal
title Whisper - TTS - Vulkan

:: --- CONFIGURATION ---
set "CURRENT_DIR=%~dp0"
set "EXE=%CURRENT_DIR%whisper-server.exe"
set "MODEL=%CURRENT_DIR%models\ggml-large-v3-turbo-q5_0.bin"

:: Corrected the VAD model filename below to match your downloaded file
set "VAD_MODEL=%CURRENT_DIR%models\ggml-silero-v6.2.0.bin"

set PORT=8383
set HOST=0.0.0.0

echo Starting Whisper Server (Vulkan)...
echo Endpoint Hardcoded to: /v1/audio/transcriptions
echo Language Forced: English
echo VAD Enabled: Yes

:: Check if VAD model exists
if not exist "%VAD_MODEL%" (
    echo [ERROR] VAD model not found at: %VAD_MODEL%
    echo Please check the filename in the models folder.
    pause
    exit /b
)

"%EXE%" -m "%MODEL%" ^
    --host %HOST% ^
    --port %PORT% ^
    --convert ^
    --language en ^
    --vad ^
    --vad-model "%VAD_MODEL%"

pause