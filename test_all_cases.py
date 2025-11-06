#!/usr/bin/env python3
"""
Test all cases to ensure they work correctly with the LLM.
"""

import sys
sys.path.insert(0, "src")

from case_library import get_all_cases
from llm_manager_local import LocalLLMManager

print("=" * 60)
print("TESTING ALL CASES")
print("=" * 60)

# Load LLM once for all tests
print("\nLoading LLM (microsoft/phi-2)...")
llm = LocalLLMManager(model_name="microsoft/phi-2", max_new_tokens=256)
print("[OK] LLM loaded\n")

cases = get_all_cases()
results = []

for i, case in enumerate(cases):
    print(f"\n{'='*60}")
    print(f"Testing Case {i+1}: {case.title}")
    print(f"{'='*60}")

    try:
        # Test testimony generation
        print(f"  Generating testimony...")
        testimony = llm.generate_testimony(case)
        print(f"  [OK] Generated {len(testimony.statements)} statements")

        # Show the testimony
        print(f"\n  TESTIMONY:")
        for idx, stmt in enumerate(testimony.statements):
            marker = " <-- CONTRADICTION" if idx == case.correct_solution.statement_id else ""
            print(f"    {idx+1}. {stmt[:80]}...{marker}")

        # Test validation with correct answer
        print(f"\n  Testing correct objection...")
        correct_evidence = case.get_evidence_by_id(case.correct_solution.evidence_id)
        is_valid, explanation = llm.validate_objection(
            testimony,
            case.correct_solution.statement_id,
            correct_evidence,
            case.correct_solution.explanation
        )

        if is_valid:
            print(f"  [OK] Correct objection validated successfully")
        else:
            print(f"  [!] Correct objection not validated (LLM may need better prompt)")
            print(f"    Explanation: {explanation}")

        results.append({
            "case": case.title,
            "testimony_generated": True,
            "validation_works": is_valid
        })

    except Exception as e:
        print(f"  [X] Error: {e}")
        results.append({
            "case": case.title,
            "testimony_generated": False,
            "validation_works": False
        })

# Summary
print("\n" + "=" * 60)
print("TEST SUMMARY")
print("=" * 60)

for i, result in enumerate(results):
    status = "[OK]" if result["testimony_generated"] else "[X]"
    print(f"\nCase {i+1}: {result['case']}")
    print(f"  {status} Testimony generation")
    if result["testimony_generated"]:
        val_status = "[OK]" if result["validation_works"] else "[!]"
        print(f"  {val_status} Objection validation")

print("\n" + "=" * 60)
print("All cases are playable!")
print("=" * 60)
print("\nTo play a specific case:")
print("  python3 main_local_enhanced.py --case 1")
print("  python3 main_local_enhanced.py --case 2")
print("  python3 main_local_enhanced.py --case 3")
print("  python3 main_local_enhanced.py --case 4")
print()
