#!/bin/bash
# Run all test suites for Ace Attorney LLM system

echo "========================================================"
echo "ACE ATTORNEY LLM - COMPLETE TEST SUITE"
echo "========================================================"
echo ""
echo "This will run 4 test suites:"
echo "  1. Basic setup test (30s)"
echo "  2. Gameplay test (1-2 min)"
echo "  3. Comprehensive test (2-3 min)"
echo "  4. All cases test (2-3 min)"
echo ""
echo "Total time: ~5-8 minutes"
echo ""
read -p "Press ENTER to start..."

TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Basic setup
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 1/4: Basic Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 test_simple.py; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[OK] TEST 1 PASSED"
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[X] TEST 1 FAILED"
fi

# Test 2: Gameplay
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 2/4: Core Gameplay"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 test_gameplay.py; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[OK] TEST 2 PASSED"
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[X] TEST 2 FAILED"
fi

# Test 3: Comprehensive
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 3/4: Comprehensive Suite"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 test_comprehensive.py; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[OK] TEST 3 PASSED"
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[X] TEST 3 FAILED"
fi

# Test 4: All cases
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "TEST 4/4: All Cases"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if python3 test_all_cases.py; then
    TESTS_PASSED=$((TESTS_PASSED + 1))
    echo "[OK] TEST 4 PASSED"
else
    TESTS_FAILED=$((TESTS_FAILED + 1))
    echo "[X] TEST 4 FAILED"
fi

# Final summary
echo ""
echo "========================================================"
echo "FINAL TEST RESULTS"
echo "========================================================"
echo "Tests Passed: $TESTS_PASSED/4"
echo "Tests Failed: $TESTS_FAILED/4"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo "ALL TESTS PASSED!"
    echo "System is ready for production use!"
    echo ""
    echo "To play the game:"
    echo "  python3 main_local.py --model meta-llama/Llama-3.1-8B-Instruct"
    exit 0
else
    echo "[!]  Some tests failed. Review output above."
    exit 1
fi
