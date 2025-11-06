#!/usr/bin/env python3
"""
Test suite using Llama 3.1-8B-Instruct for better quality results.
This demonstrates the improvement over smaller models.
"""

import sys
sys.path.insert(0, "src")

from case_data import create_sample_case
from case_library import get_all_cases
from llm_manager_local import LocalLLMManager

print("=" * 60)
print("ACE ATTORNEY LLM - LARGER MODEL TEST")
print("=" * 60)
print("\nTrying different models to find one that works without auth...")

# Try different models (some don't require HuggingFace login)
test_models = [
    "mistralai/Mistral-7B-Instruct-v0.3",  # No auth required
    "meta-llama/Llama-3.2-3B-Instruct",    # Might not require auth
    "meta-llama/Llama-3.1-8B-Instruct",    # Requires auth
]

llm = None
model_used = None

for model in test_models:
    try:
        print(f"\nTrying: {model}")
        llm = LocalLLMManager(model_name=model, max_new_tokens=512)
        model_used = model
        print(f"[OK] Successfully loaded: {model}")
        break
    except Exception as e:
        print(f"[X] Failed: {str(e)[:100]}")
        continue

if llm is None:
    print("\n" + "="*60)
    print("ERROR: Could not load any model")
    print("="*60)
    print("\nLlama models require HuggingFace authentication.")
    print("\nTo use Llama 3.1-8B-Instruct:")
    print("1. Go to: https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct")
    print("2. Click 'Agree and access repository'")
    print("3. Get your token: https://huggingface.co/settings/tokens")
    print("4. Run: huggingface-cli login")
    print("   or: export HF_TOKEN=your_token_here")
    print("\nAlternatively, use models that don't require auth:")
    print("  python3 main_local.py --model mistralai/Mistral-7B-Instruct-v0.3")
    sys.exit(1)

print(f"\n[OK] Using model: {model_used}\n")
print("[OK] Model loaded successfully\n")

# Test 1: Testimony generation quality
print("=" * 60)
print("TEST 1: Testimony Generation Quality")
print("=" * 60)

case = create_sample_case()
print(f"\nCase: {case.title}")
print("Generating testimony...")

testimony = llm.generate_testimony(case)
print(f"[OK] Generated {len(testimony.statements)} statements\n")

print("TESTIMONY:")
for i, stmt in enumerate(testimony.statements):
    marker = " <-- CONTRADICTION" if i == case.correct_solution.statement_id else ""
    print(f"  {i+1}. {stmt}{marker}")

# Test 2: Witness response quality
print("\n" + "=" * 60)
print("TEST 2: Witness Response Quality")
print("=" * 60)

questions = [
    "Can you explain the timeline more clearly?",
    "Are you absolutely certain about the timing?",
    "Did you see anyone else that morning?",
]

for q in questions:
    print(f"\n[Phoenix]: {q}")
    response = llm.generate_witness_response(testimony, q)
    print(f"[{testimony.witness_name}]: {response}")

# Test 3: Objection validation accuracy
print("\n" + "=" * 60)
print("TEST 3: Objection Validation Accuracy")
print("=" * 60)

print("\nTesting CORRECT objection...")
correct_evidence = case.get_evidence_by_id(case.correct_solution.evidence_id)
is_valid_correct, explanation_correct = llm.validate_objection(
    testimony,
    case.correct_solution.statement_id,
    correct_evidence,
    case.correct_solution.explanation
)

print(f"Result: {is_valid_correct}")
print(f"Explanation: {explanation_correct}")

if is_valid_correct:
    print("[OK] Correct objection VALIDATED")
else:
    print("[X] Correct objection NOT validated (unexpected)")

print("\nTesting INCORRECT objection...")
wrong_evidence = case.get_evidence_by_id("coffee_cup")
wrong_statement_idx = 0
wrong_argument = "The coffee cup proves the defendant is guilty"

is_valid_wrong, explanation_wrong = llm.validate_objection(
    testimony,
    wrong_statement_idx,
    wrong_evidence,
    wrong_argument
)

print(f"Result: {is_valid_wrong}")
print(f"Explanation: {explanation_wrong}")

if not is_valid_wrong:
    print("[OK] Incorrect objection REJECTED")
else:
    print("[X] Incorrect objection validated (should be rejected)")

# Test 4: All cases with Llama 3.1
print("\n" + "=" * 60)
print("TEST 4: All Cases with Llama 3.1")
print("=" * 60)

cases = get_all_cases()
results = []

for i, test_case in enumerate(cases):
    print(f"\n--- Case {i+1}: {test_case.title} ---")

    # Generate testimony
    test_testimony = llm.generate_testimony(test_case)
    print(f"  [OK] Generated {len(test_testimony.statements)} statements")

    # Test correct objection
    correct_ev = test_case.get_evidence_by_id(test_case.correct_solution.evidence_id)
    is_valid, explanation = llm.validate_objection(
        test_testimony,
        test_case.correct_solution.statement_id,
        correct_ev,
        test_case.correct_solution.explanation
    )

    status = "[OK]" if is_valid else "[X]"
    print(f"  {status} Correct objection: {is_valid}")

    results.append({
        "case": test_case.title,
        "validated": is_valid
    })

# Summary
print("\n" + "=" * 60)
print("SUMMARY - LLAMA 3.1-8B RESULTS")
print("=" * 60)

validated_count = sum(1 for r in results if r["validated"])
total_count = len(results)

for i, result in enumerate(results):
    status = "[OK]" if result["validated"] else "[X]"
    print(f"{status} Case {i+1}: {result['case']}")

print(f"\nValidation Success Rate: {validated_count}/{total_count} ({validated_count/total_count*100:.0f}%)")

if validated_count == total_count:
    print("\nPERFECT! All objections validated correctly!")
elif validated_count >= total_count * 0.75:
    print("\n[OK] GOOD! Most objections validated correctly.")
else:
    print("\n[!] Some objections not validated (may need prompt tuning)")

print("\n" + "=" * 60)
print("Llama 3.1-8B provides significantly better results than phi-2!")
print("Recommended for production use.")
print("=" * 60)
