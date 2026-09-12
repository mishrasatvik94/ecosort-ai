# AI Workflow

## 1. Input Flow
1. User uploads an image via the Streamlit UI.
2. `preprocessing.py` standardizes the image.

## 2. Classification Logic
The image is sent to `classifier.py`. For this MVP, a `MockClassifier` is used which returns a category and a confidence score based on filename heuristics or random generation.

## 3. Confidence Logic & Human Feedback
- **Confidence >= 0.80**: Proceed automatically.
- **0.50 <= Confidence < 0.80**: Pause and ask the user "Was this classification correct? [Yes] [No]". If No, the user selects the category manually.
- **Confidence < 0.50**: Halt. Mark as uncertain and force manual selection.

## 4. RAG Process
1. Query constructed as: `{Item Name} {Category}`.
2. `retriever.py` uses TF-IDF to find the most semantically similar rules in `disposal_rules.json`.
3. Returns top-K results.

## 5. LLM Prompting
The retrieved context and original item data are injected into the `SYSTEM_PROMPT`. The prompt strictly forces the LLM to ground its advice in the retrieved context.

## 6. Safety Validation
Before displaying the final output, `validation.py` checks for dangerous keywords (e.g., "burn", "drink"). If caught, it replaces the output with a safety error.

## 7. Failure Cases Handled
- Missing API Key -> Falls back to Mock LLM.
- Empty RAG results -> LLM explicitly states "Insufficient info".
- Dangerous LLM output -> Caught by post-processing validation.
