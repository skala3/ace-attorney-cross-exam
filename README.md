# Ace Attorney Cross-Examination

![Ace Attorney](ace_attorney_banner.png)

An interactive witness cross-examination game powered by Large Language Models. Find contradictions in AI-generated testimonies using natural language.

## Features

- **AI-Generated Testimonies**: Dynamic witness statements with embedded contradictions
- **Natural Language**: Question witnesses and present evidence in your own words
- **4 Cases**: Murder, theft, accident, and arson scenarios
- **100% Local**: No API keys, runs on your GPU

## Quick Start

```bash
pip install torch transformers
python3 main_local.py
```

## How to Play

1. **Read** the case details and evidence
2. **Listen** to the witness testimony
3. **Press** to ask questions or **Present** evidence to expose contradictions
4. **Win** by finding the right contradiction before losing all 5 health

## Supported Models

- **Small** (~8GB VRAM): `microsoft/phi-2`, `meta-llama/Llama-3.2-3B-Instruct`
- **Medium** (~16GB VRAM): `meta-llama/Llama-3.1-8B-Instruct` (recommended)
- **Large** (~140GB+ VRAM): `meta-llama/Llama-3.1-70B-Instruct`

## Testing

```bash
python3 test_simple.py              # Quick test
python3 test_comprehensive.py       # Full suite
./run_all_tests.sh                  # All tests
```

## License

MIT License
