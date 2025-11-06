#!/usr/bin/env python3
"""
Enhanced main entry point for AI-Powered Ace Attorney (LOCAL LLM VERSION).
Supports multiple test cases with difficulty selection.
"""

import sys
import os
import argparse

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from case_library import get_all_cases, get_case_by_index
from llm_manager_local import LocalLLMManager, get_available_models
from game_engine import GameEngine


def list_cases():
    """Display all available cases."""
    cases = get_all_cases()
    print("\n" + "=" * 60)
    print("AVAILABLE CASES")
    print("=" * 60)
    for i, case in enumerate(cases):
        print(f"\nCase {i+1}: {case.title}")
        print(f"  Crime: {case.crime}")
        print(f"  Defendant: {case.defendant}")
        print(f"  Evidence: {len(case.evidence_list)} items")
    print("\n" + "=" * 60)


def main():
    """Main function to run the game with local LLMs."""
    parser = argparse.ArgumentParser(description="Ace Attorney with Local LLMs")
    parser.add_argument(
        "--model",
        type=str,
        default="microsoft/phi-2",
        help="HuggingFace model ID to use (default: microsoft/phi-2)",
    )
    parser.add_argument(
        "--case",
        type=int,
        default=1,
        help="Case number to play (1-4, default: 1)",
    )
    parser.add_argument(
        "--list-models", action="store_true", help="List recommended models"
    )
    parser.add_argument(
        "--list-cases", action="store_true", help="List available cases"
    )
    args = parser.parse_args()

    if args.list_models:
        print("\nRecommended Models:")
        print("\nSMALL (6-8GB VRAM):")
        for model in get_available_models()["small"]:
            print(f"  - {model}")
        print("\nMEDIUM (14-16GB VRAM):")
        for model in get_available_models()["medium"]:
            print(f"  - {model}")
        print("\nLARGE (140GB+ VRAM, multi-GPU):")
        for model in get_available_models()["large"]:
            print(f"  - {model}")
        print(
            "\nUsage: python main_local_enhanced.py --model meta-llama/Llama-3.1-8B-Instruct\n"
        )
        return

    if args.list_cases:
        list_cases()
        print("\nUsage: python main_local_enhanced.py --case 2\n")
        return

    print("\n" + "=" * 60)
    print(" AI-POWERED ACE ATTORNEY (LOCAL LLM VERSION)")
    print("=" * 60)
    print(f"\nUsing model: {args.model}")
    print("No API keys required - runs entirely on your GPU!\n")

    # Load the selected case
    case = get_case_by_index(args.case - 1)
    print(f"Selected Case: {case.title}")
    print(f"Defendant: {case.defendant}")
    print(f"Crime: {case.crime}\n")

    print("Welcome! You are a defense attorney.")
    print("Your goal: Find the contradiction in the witness's testimony")
    print("to prove your client's innocence.\n")
    print("HOW TO PLAY:")
    print("- PRESS: Ask the witness questions to gather information")
    print("- PRESENT: Present evidence that contradicts a statement")
    print("- You have 5 health. Wrong objections cost 1 health.\n")

    input("Press ENTER to begin...")

    # Initialize game components
    print("\nInitializing game...")

    print(f"Loading LLM: {args.model}")
    print("(This may take a minute on first run...)")
    llm_manager = LocalLLMManager(model_name=args.model)

    # Create and run game
    game = GameEngine(case, llm_manager)

    try:
        game.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
