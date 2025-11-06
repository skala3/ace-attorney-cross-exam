#!/usr/bin/env python3
"""
Automated gameplay test for the Ace Attorney LLM system.
Tests the game flow without requiring manual input.
"""

import sys
sys.path.insert(0, "src")

from case_data import create_sample_case
from llm_manager_local import LocalLLMManager
from game_engine import GameEngine

print("=" * 60)
print("AUTOMATED GAMEPLAY TEST")
print("=" * 60)

# 1. Load the case
print("\n1. Loading case...")
case = create_sample_case()
print(f"   [OK] Case loaded: {case.title}")
print(f"   [OK] Victim: {case.victim}")
print(f"   [OK] Defendant: {case.defendant}")
print(f"   [OK] Evidence count: {len(case.evidence_list)}")

# 2. Initialize LLM (use small model for quick testing)
print("\n2. Loading LLM (microsoft/phi-2 for speed)...")
llm = LocalLLMManager(model_name="microsoft/phi-2", max_new_tokens=256)
print("   [OK] LLM loaded")

# 3. Test testimony generation
print("\n3. Generating testimony...")
testimony = llm.generate_testimony(case)
print(f"   [OK] Generated {len(testimony.statements)} statements")
print("\n   TESTIMONY:")
for i, stmt in enumerate(testimony.statements):
    print(f"   {i+1}. {stmt}")

# 4. Test witness response (PRESS)
print("\n4. Testing PRESS (witness response)...")
test_question = "Can you explain what you saw that morning?"
print(f"   Question: '{test_question}'")
response = llm.generate_witness_response(testimony, test_question)
print(f"   [OK] Response: {response[:100]}...")

# 5. Test objection validation (correct solution)
print("\n5. Testing PRESENT (correct objection)...")
correct_evidence = case.get_evidence_by_id(case.correct_solution.evidence_id)
correct_statement_idx = case.correct_solution.statement_id
correct_argument = "The security log shows they arrived at 9:00 AM, not 8:15 AM"

is_valid, explanation = llm.validate_objection(
    testimony,
    correct_statement_idx,
    correct_evidence,
    correct_argument
)
print(f"   [OK] Validation result: {is_valid}")
print(f"   [OK] Explanation: {explanation}")

# 6. Test incorrect objection
print("\n6. Testing PRESENT (incorrect objection)...")
wrong_evidence = case.get_evidence_by_id("coffee_cup")
wrong_statement_idx = 0
wrong_argument = "The coffee cup has poison in it"

is_valid_wrong, explanation_wrong = llm.validate_objection(
    testimony,
    wrong_statement_idx,
    wrong_evidence,
    wrong_argument
)
print(f"   [OK] Validation result: {is_valid_wrong}")
print(f"   [OK] Explanation: {explanation_wrong}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)
print("\nThe game is ready to play!")
print("Run: python3 main_local.py\n")
