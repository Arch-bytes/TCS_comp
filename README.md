# Deepfake Interview Alert Tool

Offline hackathon prototype for spotting interview impersonation risk using synthetic data only.

## What it does

- NiceGUI app with one input flow and one results flow.
- Local TF-IDF + cosine similarity scoring from `scikit-learn`.
- Deterministic rules for canned phrases, short answers, and manual observation notes.
- Advisory-only output with the required disclaimer always shown.

## Run it

1. Create or activate a Python 3.11 environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the app with `python -m app.main`.

## Demo script

1. Load the clean synthetic case and show a low score with visible reasons.
2. Load the mismatch case and show a higher score with reasons.
3. Load the suspicious-flag case and point to the manual observation notes.
4. Close by saying the scoring contract can later swap to a database, stronger embeddings, and access control without changing the API shape.

## Descoped for the 1-hour build

- No database or ORM.
- No auth or user accounts.
- No network/API calls.
- No real biometric, audio, or video processing.

## Safety note

This score supports interviewer review and does not make a hiring decision.