"""
Case data structures for Ace Attorney cross-examination system.
Defines the structure of a case, evidence, and testimonies.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class Evidence:
    """Represents a piece of evidence in the case."""
    id: str
    name: str
    description: str
    image_path: Optional[str] = None

    def __str__(self):
        return f"{self.name}: {self.description}"


@dataclass
class Contradiction:
    """Represents a contradiction between testimony and evidence."""
    statement_id: int  # Which statement in the testimony
    evidence_id: str   # Which evidence contradicts it
    explanation: str   # Why it's a contradiction


@dataclass
class Testimony:
    """A witness testimony with statements and hidden contradictions."""
    witness_name: str
    statements: List[str]
    contradictions: List[Contradiction]
    context: str  # Background information for generating responses

    def get_statement(self, index: int) -> Optional[str]:
        if 0 <= index < len(self.statements):
            return self.statements[index]
        return None


@dataclass
class CaseData:
    """Complete case information."""
    title: str
    description: str
    victim: str
    defendant: str
    crime: str
    evidence_list: List[Evidence]
    witness_name: str
    correct_solution: Contradiction  # The main contradiction to find
    case_facts: str  # Ground truth about what really happened

    def get_evidence_by_id(self, evidence_id: str) -> Optional[Evidence]:
        for evidence in self.evidence_list:
            if evidence.id == evidence_id:
                return evidence
        return None

    def get_evidence_summary(self) -> str:
        """Get a formatted summary of all evidence."""
        summary = "EVIDENCE:\n"
        for evidence in self.evidence_list:
            summary += f"  [{evidence.id}] {evidence}\n"
        return summary


# Example case template
def create_sample_case() -> CaseData:
    """Creates a sample murder mystery case for testing."""
    return CaseData(
        title="The Poisoned Coffee Mystery",
        description="A murder occurred at the law office. The defendant is accused of poisoning the victim's coffee.",
        victim="Victim Johnson",
        defendant="Secretary Smith",
        crime="Murder by poisoning",
        evidence_list=[
            Evidence(
                id="coffee_cup",
                name="Coffee Cup",
                description="A coffee cup found on the victim's desk. Contains traces of poison.",
            ),
            Evidence(
                id="security_log",
                name="Security Log",
                description="Building security log showing Secretary Smith entered at 9:00 AM, but the victim died at 8:30 AM.",
            ),
            Evidence(
                id="poison_bottle",
                name="Poison Bottle",
                description="Found in the defendant's desk drawer.",
            ),
            Evidence(
                id="witness_statement",
                name="Janitor's Statement",
                description="Janitor saw someone in a suit near the victim's office at 8:15 AM.",
            ),
        ],
        witness_name="Detective Williams",
        correct_solution=Contradiction(
            statement_id=2,  # The statement about timing
            evidence_id="security_log",
            explanation="The detective claims the defendant delivered coffee at 8:15 AM, but the security log shows she didn't arrive until 9:00 AM.",
        ),
        case_facts="""
        Ground Truth:
        - The real killer was actually the business partner who had access to the office keys
        - The partner entered at 8:15 AM (before security system was activated)
        - Secretary Smith arrived at 9:00 AM as usual
        - The poison bottle was planted in Smith's desk to frame her
        - The detective's testimony incorrectly states Smith delivered the coffee at 8:15 AM
        """,
    )
