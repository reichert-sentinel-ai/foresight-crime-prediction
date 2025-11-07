@echo off
REM Install recharts and start frontend server
cd /d "C:\Users\reich\Projects\HEDIS-MA-Top-12-w-HEI-Prep\project\repo-foresight\frontend"
echo Installing recharts...
"C:\Program Files\nodejs\npm.cmd" install recharts
echo.
echo Checking installation...
if exist "node_modules\recharts" (
    echo ✅ recharts installed successfully!
    echo.
    echo Starting frontend server...
    "C:\Program Files\nodejs\npm.cmd" run dev
) else (
    echo ❌ Installation failed. Please check errors above.
    pause
)

