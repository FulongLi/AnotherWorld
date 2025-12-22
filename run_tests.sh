#!/bin/bash
# Linux/Mac shell script to run all tests

echo "========================================"
echo "Running All Tests"
echo "========================================"
echo ""

echo "[1/5] Running basic test..."
python test_run.py
if [ $? -ne 0 ]; then
    echo "Basic test failed!"
    exit 1
fi
echo ""

echo "[2/5] Running architecture demo..."
python examples/architecture_demo.py
if [ $? -ne 0 ]; then
    echo "Architecture demo failed!"
    exit 1
fi
echo ""

echo "[3/5] Running China model demo..."
python examples/china_demo.py
if [ $? -ne 0 ]; then
    echo "China demo failed!"
    exit 1
fi
echo ""

echo "[4/5] Running family policy demo..."
python examples/family_policy_demo.py
if [ $? -ne 0 ]; then
    echo "Family policy demo failed!"
    exit 1
fi
echo ""

echo "[5/5] Running Pareto principle demo..."
python examples/pareto_demo.py
if [ $? -ne 0 ]; then
    echo "Pareto demo failed!"
    exit 1
fi
echo ""

echo "========================================"
echo "All tests completed successfully!"
echo "========================================"

