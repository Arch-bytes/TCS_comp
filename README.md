# Deepfake Interview Alert Tool (Enterprise Prototype)

Professional AI prototype for spotting interview impersonation risk using synthetic data and modular NLP/Rule logic.

## Architecture

- **`services/config.py`**: Centralized configuration for weights, thresholds, and behavioral flags.
- **`services/nlp_match.py`**: Modular NLP engine for TF-IDF similarity and skill coverage.
- **`services/rules.py`**: Heuristic rules for canned phrases, answer depth, and behavioral observations.
- **`services/scoring.py`**: High-level risk assessment coordinator.
- **`data/synthetic_candidates.py`**: Demo dataset including the "Jordan Smith" (CAN-007) mismatch case.
- **`app/main.py`**: Glassmorphic NiceGUI dashboard for interactive review.

## Key Features

- **Risk Scoring (0-100)**: Multi-factor aggregation of text alignment and behavioral anomalies.
- **Anomaly Detection**: Identifies lip-sync errors, prompting detection, eye-contact issues, and AI assistant phrasing.
- **Requirement-Specific Cases**: Demonstrates the Python/ML mismatch pattern from the Cyber Defense problem statement.
- **Testable**: Comprehensive unit test suite in `tests/`.

## Setup & Run

1. **Environment**: Python 3.11+
2. **Install**: `pip install -r requirements.txt`
3. **Run App**: `python -m app.main`
4. **Run Tests**: `python -m unittest discover tests`

## Demo Script

1. **Clean Case (CAN-001)**: Shows low risk with strong alignment.
2. **Skill Mismatch (CAN-007)**: Profile says "Python/ML", but answer is generic. Shows high risk.
3. **AI Detected (CAN-004)**: Shows high risk due to "As an AI language model" phrasing.
4. **Behavioral Flags (CAN-005)**: Shows risk increase due to lip-sync and audio sync issues.