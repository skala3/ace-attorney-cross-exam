#!/usr/bin/env python3
"""
Simple test to verify the local LLM setup works.
"""

import sys
sys.path.insert(0, "src")

print("=" * 60)
print("TESTING LOCAL LLM SETUP")
print("=" * 60)

print("\n1. Checking imports...")
try:
    import torch
    print(f"   [OK] PyTorch {torch.__version__}")
    print(f"   [OK] CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"   [OK] GPU: {torch.cuda.get_device_name(0)}")
        print(f"   [OK] GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
except ImportError as e:
    print(f"   [X] PyTorch import failed: {e}")
    sys.exit(1)

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("   [OK] Transformers imported")
except ImportError as e:
    print(f"   [X] Transformers import failed: {e}")
    sys.exit(1)

try:
    from case_data import create_sample_case
    from llm_manager_local import LocalLLMManager
    print("   [OK] Game modules imported")
except ImportError as e:
    print(f"   [X] Game modules failed: {e}")
    sys.exit(1)

print("\n2. Loading test model...")
print("   (Using microsoft/phi-2 - fully open, no auth required)")

try:
    # Use Phi-2 for testing (fully open, no HuggingFace auth needed)
    llm = LocalLLMManager(
        model_name="microsoft/phi-2",
        max_new_tokens=50
    )
    print("   [OK] Model loaded successfully!")
except Exception as e:
    print(f"   [X] Model loading failed: {e}")
    print("\n   Note: First run downloads the model (~2.7GB)")
    sys.exit(1)

print("\n3. Testing testimony generation...")
try:
    case = create_sample_case()
    testimony = llm.generate_testimony(case)
    print(f"   [OK] Generated {len(testimony.statements)} statements")
    print(f"   [OK] Testimony preview: {testimony.statements[0][:60]}...")
except Exception as e:
    print(f"   [X] Generation failed: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("SUCCESS! System is ready to play")
print("=" * 60)
print("\nRun the full game with:")
print("  python3 main_local.py --model meta-llama/Llama-3.2-3B-Instruct")
print()
