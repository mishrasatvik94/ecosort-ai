# Test Plan

## Unit Tests (Automated via Pytest)
- `test_classifier.py`: Validates that "banana.jpg" yields > 0.80 confidence, and "unknown.jpg" yields < 0.50.
- `test_rag.py`: Validates that querying "banana" returns the correct organic disposal rule, and garbage text returns empty lists.
- `test_outputs.py`: Validates that the safety keyword filter successfully blocks dangerous phrases like "burn it".

## Manual UI Testing Scenarios
1. **Valid Image**: Upload `banana.jpg`. Expectation: High confidence, direct generation of compost advice.
2. **Ambiguous Image**: Upload `blurry.jpg`. Expectation: Low confidence (<0.50), system forces manual dropdown selection.
3. **E-waste**: Upload `battery.jpg`. Expectation: Retrieves e-waste safety guidelines, correctly advises against throwing in trash.
4. **Hazardous**: Upload `bleach.jpg`. Expectation: Safe handling instructions retrieved.
5. **AI API Unavailable**: Run without `.env`. Expectation: System gracefully uses Mock LLM and still functions.
6. **User Correction**: Upload an item that scores 0.70. Expectation: System asks "Is this correct?". Click 'No', select manually, verify correct RAG rules are loaded for the manual selection.

*[INSERT ACTUAL MANUAL TESTING RESULTS HERE AFTER DEPLOYMENT]*
