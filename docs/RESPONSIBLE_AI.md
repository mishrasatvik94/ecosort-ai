# Responsible AI Guidelines

## 1. Accuracy Limitations
The system explicitly states that it provides decision support, not authoritative regulatory advice. The Vision layer is a mock prototype.

## 2. Bias
The prototype dataset currently reflects generalized Western municipal guidelines and may not accurately reflect rural or developing nations' recycling capabilities.

## 3. Hallucination Prevention
The LLM is highly constrained by the System Prompt to only use the provided RAG context and to output "Insufficient info" if the RAG context is empty.

## 4. Privacy
No user images or location data are stored or logged persistently.

## 5. Transparency
AI predictions are clearly labelled with their confidence scores.

## 6. Human-in-the-Loop
The system enforces human confirmation for any prediction below 80% confidence.

## 7. Safety
A post-processing keyword filter (`validation.py`) acts as a safeguard against dangerous generated instructions (e.g., advising burning of hazardous waste).

## 8. Data Provenance
Data in `disposal_rules.json` is labelled as "Prototype Example Data" with a `last_verified` timestamp.
