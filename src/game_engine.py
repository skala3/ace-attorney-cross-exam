"""
Game engine for Ace Attorney cross-examination system.
Manages game flow, user interaction, and victory conditions.
"""

from typing import Optional, Union
from case_data import CaseData, Testimony, Evidence

# Try to import both LLM managers, use whichever is available
try:
    from llm_manager import LLMManager
except ImportError:
    LLMManager = None

try:
    from llm_manager_local import LocalLLMManager
except ImportError:
    LocalLLMManager = None


class GameEngine:
    """Main game engine for cross-examination gameplay."""

    def __init__(self, case: CaseData, llm_manager):
        """
        Initialize the game engine.

        Args:
            case: The case data to play
            llm_manager: LLM manager for AI interactions
        """
        self.case = case
        self.llm = llm_manager
        self.testimony: Optional[Testimony] = None
        self.health = 5  # Player health (mistakes allowed)
        self.game_won = False

    def start_game(self):
        """Start the game by generating the initial testimony."""
        print("=" * 60)
        print(f"CASE: {self.case.title}")
        print("=" * 60)
        print(f"\n{self.case.description}\n")
        print(f"Victim: {self.case.victim}")
        print(f"Defendant: {self.case.defendant}")
        print(f"Crime: {self.case.crime}\n")

        print("Generating witness testimony...")
        self.testimony = self.llm.generate_testimony(self.case)

        print(f"\n{self.testimony.witness_name} takes the stand.\n")
        self.display_testimony()

    def display_testimony(self):
        """Display the current testimony."""
        if not self.testimony:
            return

        print("\n--- TESTIMONY ---")
        for i, statement in enumerate(self.testimony.statements):
            print(f"{i + 1}. {statement}")
        print("-" * 60)

    def display_evidence(self):
        """Display available evidence."""
        print("\n--- EVIDENCE COURT RECORD ---")
        for evidence in self.case.evidence_list:
            print(f"  [{evidence.id}] {evidence.name}")
            print(f"      {evidence.description}")
        print("-" * 60)

    def display_health(self):
        """Display current health/penalty status."""
        filled = "*" * self.health
        empty = "-" * (5 - self.health)
        print(f"\nHealth: [{filled}{empty}] ({self.health}/5)")

    def take_turn(self):
        """Execute one turn of gameplay."""
        if not self.testimony:
            print("Error: No testimony loaded")
            return False

        self.display_health()
        print("\nWhat would you like to do?")
        print("1. Press (ask a question)")
        print("2. Present (present evidence against a statement)")
        print("3. Review testimony")
        print("4. Check evidence")
        print("5. Give up")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            self.handle_press()
        elif choice == "2":
            self.handle_present()
        elif choice == "3":
            self.display_testimony()
        elif choice == "4":
            self.display_evidence()
        elif choice == "5":
            print("\nYou gave up. Game over.")
            return False
        else:
            print("Invalid choice. Try again.")

        return self.health > 0 and not self.game_won

    def handle_press(self):
        """Handle the player pressing the witness with a question."""
        question = input("\nWhat do you want to ask the witness? ")

        if not question.strip():
            print("You need to ask a question!")
            return

        print(f"\n[Phoenix]: {question}")
        print("\nWitness is thinking...")

        response = self.llm.generate_witness_response(self.testimony, question)
        print(f"\n[{self.testimony.witness_name}]: {response}\n")

    def handle_present(self):
        """Handle the player presenting evidence."""
        self.display_testimony()
        print("\nWhich statement do you want to challenge?")

        try:
            statement_num = int(input("Statement number: ").strip())
            statement_index = statement_num - 1

            if statement_index < 0 or statement_index >= len(self.testimony.statements):
                print("Invalid statement number!")
                return
        except ValueError:
            print("Please enter a valid number!")
            return

        self.display_evidence()
        evidence_id = input("\nWhich evidence do you want to present? [id]: ").strip()

        evidence = self.case.get_evidence_by_id(evidence_id)
        if not evidence:
            print(f"Evidence '{evidence_id}' not found!")
            return

        argument = input(
            "\nExplain the contradiction (what's wrong with this statement?): "
        ).strip()

        if not argument:
            print("You need to explain the contradiction!")
            return

        print("\nJudge is deliberating...")

        is_valid, explanation = self.llm.validate_objection(
            self.testimony, statement_index, evidence, argument
        )

        if is_valid:
            print("\n" + "=" * 60)
            print("OBJECTION SUSTAINED!")
            print("=" * 60)
            print(f"\n{explanation}\n")
            print("YOU WIN! The contradiction has been exposed!")
            print(f"The real killer was not {self.case.defendant}!")
            self.game_won = True
        else:
            self.health -= 1
            print("\n" + "=" * 60)
            print("OBJECTION OVERRULED!")
            print("=" * 60)
            print(f"\n{explanation}\n")

            if self.health > 0:
                print(f"Penalty! Health remaining: {self.health}/5")
            else:
                print("You've run out of health. Game over.")
                print(f"\nThe defendant, {self.case.defendant}, was found guilty.")
                print("(But they were actually innocent!)")

    def play(self):
        """Main game loop."""
        self.start_game()

        while self.health > 0 and not self.game_won:
            if not self.take_turn():
                break

        print("\n" + "=" * 60)
        if self.game_won:
            print("CONGRATULATIONS! Case solved!")
        else:
            print("GAME OVER")
        print("=" * 60)
