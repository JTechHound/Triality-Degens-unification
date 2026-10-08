#!/usr/bin/env bash
# ================================================================================
# TRIALITY CORE PRE-COMPILE VALIDATION CHECK GATEWAY
# Module: Continuous Integration Automated Build Halt Engine (Local Commit Guard)
# [REPAIRED 2026-10-08] Source transmission fused several line breaks; restored.
# ================================================================================
# Define text-formatting escape parameters for the CI console log output
COLOR_CYAN='\033[0;36m'
COLOR_GREEN='\033[0;32m'
COLOR_RED='\033[0;31m'
COLOR_RESET='\033[0m'

echo -e "${COLOR_CYAN}[CI PRE-COMPILE INITIALIZED]: Executing Triality Matrix Validation Gateway...${COLOR_RESET}"
# Step 1: Check for the presence of the runtime environment
if ! command -v python3 &> /dev/null; then
    echo -e "${COLOR_RED}[CRITICAL GATE FAILURE]: python3 environment could not be resolved in path system.${COLOR_RESET}"
    exit 1
fi
# Step 2: Dynamically discover and execute the automated validator test modules
# We force Python to use bufferless stream output to capture real-time logs
python3 -u -m unittest discover -s . -p "*validator*.py"
TEST_GATE_RESULT=$?
# Step 3: Evaluate test runner exit codes to lock build gate constraints
if [ $TEST_GATE_RESULT -eq 0 ]; then
    echo -e "${COLOR_GREEN}[BUILD SUCCESS]: All structural dimensions and sign-invariants cleared. Proceeding to compilation core.${COLOR_RESET}"
    exit 0
else
    echo -e "${COLOR_RED}[CRITICAL BUILD ERROR]: Parameter validation tests failed. Matrix dimensions or sign vectors are broken.${COLOR_RESET}"
    echo -e "${COLOR_RED}[COMPILE PAUSED]: Blocking downward pipeline compilation execution until invariants are mathematically reconciled.${COLOR_RESET}"
    exit 1
fi
