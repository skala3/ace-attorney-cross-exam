"""
LLM Manager for Ace Attorney cross-examination system.
Handles all interactions with the OpenAI API for generating testimonies,
responses, and validating contradictions.
"""

import os
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv

from case_data import CaseData, Testimony, Contradiction, Evidence


class LLMManager:
    """Manages LLM interactions for witness testimonies and contradiction detection."""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the LLM manager.

        Args:
            api_key: OpenAI API key. If None, loads from environment.
            model: OpenAI model to use (default: gpt-4o-mini)
        """
        load_dotenv()
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_testimony(self, case: CaseData) -> Testimony:
        """
        Generate a witness testimony with embedded contradictions.

        Args:
            case: The case data to generate testimony for

        Returns:
            Testimony object with statements and contradictions
        """
        prompt = f"""You are a detective testifying in court about a murder case.

CASE DETAILS:
- Crime: {case.crime}
- Victim: {case.victim}
- Defendant: {case.defendant}
- Case: {case.description}

AVAILABLE EVIDENCE:
{case.get_evidence_summary()}

CRITICAL INSTRUCTION:
Generate a testimony of exactly 4-5 statements. One statement MUST contain this contradiction:
- Statement should claim that "{case.defendant} delivered coffee to the victim at 8:15 AM"
- This contradicts the security log which shows they arrived at 9:00 AM

The testimony should sound professional and confident, but contain this timing error.

Format your response as a JSON object:
{{
    "statements": ["statement 1", "statement 2", ...],
    "contradicting_statement_index": <index of the statement with the error>
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a witness in an Ace Attorney-style court case. Generate realistic testimonies.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

        import json

        result = json.loads(response.choices[0].message.content)
        statements = result["statements"]
        contradicting_index = result.get("contradicting_statement_index", 2)

        return Testimony(
            witness_name=case.witness_name,
            statements=statements,
            contradictions=[
                Contradiction(
                    statement_id=contradicting_index,
                    evidence_id=case.correct_solution.evidence_id,
                    explanation=case.correct_solution.explanation,
                )
            ],
            context=case.case_facts,
        )

    def validate_objection(
        self,
        testimony: Testimony,
        statement_index: int,
        evidence: Evidence,
        player_argument: str,
    ) -> tuple[bool, str]:
        """
        Validate if the player's objection is correct.

        Args:
            testimony: The current testimony
            statement_index: Which statement the player is objecting to
            evidence: The evidence the player is presenting
            player_argument: The player's explanation of the contradiction

        Returns:
            Tuple of (is_valid, explanation)
        """
        statement = testimony.get_statement(statement_index)
        if not statement:
            return False, "Invalid statement index."

        # Check if this matches a known contradiction
        for contradiction in testimony.contradictions:
            if (
                contradiction.statement_id == statement_index
                and contradiction.evidence_id == evidence.id
            ):
                return True, f"CORRECT! {contradiction.explanation}"

        # Use LLM to evaluate if there might be a valid but unexpected contradiction
        prompt = f"""Evaluate if this objection in a court case is valid:

WITNESS STATEMENT:
"{statement}"

PRESENTED EVIDENCE:
{evidence}

PLAYER'S ARGUMENT:
"{player_argument}"

Determine if the evidence legitimately contradicts the statement based on the player's reasoning.

Respond in JSON format:
{{
    "is_valid": true/false,
    "explanation": "brief explanation of why this is/isn't a valid contradiction"
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a judge evaluating logical contradictions in a court case.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )

        import json

        result = json.loads(response.choices[0].message.content)
        return result["is_valid"], result["explanation"]

    def generate_witness_response(
        self, testimony: Testimony, player_question: str
    ) -> str:
        """
        Generate the witness's response to a player question.

        Args:
            testimony: Current testimony
            player_question: Question asked by the player

        Returns:
            Witness response string
        """
        context = f"""You are {testimony.witness_name} being cross-examined in court.

YOUR TESTIMONY:
{chr(10).join(f"{i+1}. {s}" for i, s in enumerate(testimony.statements))}

BACKGROUND CONTEXT (for staying in character):
{testimony.context}

The defense attorney just asked you: "{player_question}"

Respond naturally as the witness. Be defensive if the question challenges your testimony,
or cooperative if it's a clarifying question. Keep responses concise (2-3 sentences).
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a witness being cross-examined. Stay in character.",
                },
                {"role": "user", "content": context},
            ],
            temperature=0.8,
        )

        return response.choices[0].message.content.strip()
