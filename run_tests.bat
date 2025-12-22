@echo off
REM Windows batch script to run all tests
echo ========================================
echo Running All Tests
echo ========================================
echo.

echo [1/5] Running basic test...
python test_run.py
if errorlevel 1 (
    echo Basic test failed!
    pause
    exit /b 1
)
echo.

echo [2/5] Running architecture demo...
python examples/architecture_demo.py
if errorlevel 1 (
    echo Architecture demo failed!
    pause
    exit /b 1
)
echo.

echo [3/5] Running China model demo...
python examples/china_demo.py
if errorlevel 1 (
    echo China demo failed!
    pause
    exit /b 1
)
echo.

echo [4/5] Running family policy demo...
python examples/family_policy_demo.py
if errorlevel 1 (
    echo Family policy demo failed!
    pause
    exit /b 1
)
echo.

echo [5/5] Running Pareto principle demo...
python examples/pareto_demo.py
if errorlevel 1 (
    echo Pareto demo failed!
    pause
    exit /b 1
)
echo.

echo ========================================
echo All tests completed successfully!
echo ========================================
pause

