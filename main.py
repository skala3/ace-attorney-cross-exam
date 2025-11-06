#!/usr/bin/env python3
"""
Main entry point for the AI-Powered Ace Attorney Cross-Examination System.

This is an interactive game where you cross-examine an AI witness to find
contradictions in their testimony using evidence from the case.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from case_data import create_sample_case
from llm_manager import LLMManager
from game_engine import GameEngine


def main():
    """Main function to run the game."""
    print("\n" + "=" * 60)
    print(" AI-POWERED ACE ATTORNEY CROSS-EXAMINATION")
    print("=" * 60)
    print("\nWelcome! You are a defense attorney.")
    print("Your goal: Find the contradiction in the witness's testimony")
    print("to prove your client's innocence.\n")
    print("HOW TO PLAY:")
    print("- PRESS: Ask the witness questions to gather information")
    print("- PRESENT: Present evidence that contradicts a statement")
    print("- You have 5 health. Wrong objections cost 1 health.\n")

    input("Press ENTER to begin...")

    # Initialize game components
    print("\nInitializing game...")
    case = create_sample_case()
    llm_manager = LLMManager()

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
