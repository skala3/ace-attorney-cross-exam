"""
Local LLM Manager for Ace Attorney cross-examination system.
Uses HuggingFace transformers for local GPU inference.
No API keys required!
"""

import json
import torch
from typing import List, Optional, Tuple
from transformers import AutoTokenizer, AutoModelForCausalLM

from case_data import CaseData, Testimony, Contradiction, Evidence


class LocalLLMManager:
    """Manages local LLM interactions using HuggingFace transformers."""

    def __init__(
        self,
        model_name: str = "meta-llama/Llama-3.2-3B-Instruct",
        device: str = "auto",
        max_new_tokens: int = 512,
    ):
        """
        Initialize the local LLM manager.

        Args:
            model_name: HuggingFace model ID
            device: Device to run on ('cuda', 'cpu', or 'auto')
            max_new_tokens: Maximum tokens to generate
        """
        print(f"Loading model: {model_name}")
        print("This may take a few minutes on first run...")

        self.model_name = model_name
        self.max_new_tokens = max_new_tokens

        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float16,
            device_map=device,
        )

        print(f"Model loaded successfully on {self.model.device}")

    def _generate(self, messages: list, temperature: float = 0.7) -> str:
        """
        Generate text from messages using the local model.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        # Format messages using chat template (with fallback for models without templates)
        try:
            prompt = self.tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        except Exception:
            # Fallback: simple prompt formatting for models without chat templates
            prompt = ""
            for msg in messages:
                if msg["role"] == "system":
                    prompt += f"System: {msg['content']}\n\n"
                elif msg["role"] == "user":
                    prompt += f"User: {msg['content']}\n\n"
                elif msg["role"] == "assistant":
                    prompt += f"Assistant: {msg['content']}\n\n"
            prompt += "Assistant: "

        # Tokenize
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        # Decode
        generated_text = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].shape[1] :], skip_special_tokens=True
        )

        return generated_text.strip()

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

Respond ONLY with a JSON object in this exact format:
{{
    "statements": ["statement 1", "statement 2", "statement 3", "statement 4"],
    "contradicting_statement_index": 1
}}

Do not include any other text, just the JSON."""

        messages = [
            {
                "role": "system",
                "content": "You are a witness in a court case. Generate realistic testimonies in JSON format.",
            },
            {"role": "user", "content": prompt},
        ]

        response = self._generate(messages, temperature=0.7)

        # Try to extract JSON from response
        try:
            # Find JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)
            else:
                # Fallback if no JSON found
                result = self._create_fallback_testimony()
        except json.JSONDecodeError:
            print("Warning: Failed to parse JSON, using fallback testimony")
            result = self._create_fallback_testimony()

        statements = result.get("statements", [])
        contradicting_index = result.get("contradicting_statement_index", 1)

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

    def _create_fallback_testimony(self) -> dict:
        """Create a fallback testimony if JSON parsing fails."""
        return {
            "statements": [
                "I arrived at the crime scene at 9:00 AM as part of my routine patrol.",
                "I witnessed the defendant, Secretary Smith, delivering coffee to the victim at 8:15 AM that morning.",
                "The victim appeared to be in good health when I saw them earlier.",
                "I discovered the victim's body at approximately 9:30 AM.",
                "The coffee cup on the desk tested positive for poison.",
            ],
            "contradicting_statement_index": 1,
        }

    def validate_objection(
        self,
        testimony: Testimony,
        statement_index: int,
        evidence: Evidence,
        player_argument: str,
    ) -> Tuple[bool, str]:
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

        # Check if this matches the known contradiction
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

Respond ONLY with JSON in this format:
{{
    "is_valid": true or false,
    "explanation": "brief explanation"
}}"""

        messages = [
            {
                "role": "system",
                "content": "You are a judge evaluating logical contradictions in a court case. Respond only with JSON.",
            },
            {"role": "user", "content": prompt},
        ]

        response = self._generate(messages, temperature=0.3)

        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end > start:
                json_str = response[start:end]
                result = json.loads(json_str)
                return result.get("is_valid", False), result.get(
                    "explanation", "Unable to evaluate."
                )
        except:
            pass

        return False, "The evidence does not clearly contradict this statement."

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

The defense attorney just asked you: "{player_question}"

Respond naturally as the witness in 2-3 sentences. Be defensive if challenged, cooperative if clarifying."""

        messages = [
            {
                "role": "system",
                "content": "You are a witness being cross-examined. Stay in character. Be brief.",
            },
            {"role": "user", "content": context},
        ]

        return self._generate(messages, temperature=0.8)


# Convenience function for easier model loading
def get_available_models():
    """Return a list of recommended models for different hardware."""
    return {
        "small": [
            "meta-llama/Llama-3.2-3B-Instruct",  # ~6GB VRAM
            "microsoft/Phi-3-mini-4k-instruct",  # ~8GB VRAM
        ],
        "medium": [
            "meta-llama/Llama-3.1-8B-Instruct",  # ~16GB VRAM
            "mistralai/Mistral-7B-Instruct-v0.3",  # ~14GB VRAM
        ],
        "large": [
            "meta-llama/Llama-3.1-70B-Instruct",  # ~140GB VRAM (needs multi-GPU)
            "Qwen/Qwen2.5-72B-Instruct",  # ~144GB VRAM (needs multi-GPU)
        ],
    }
