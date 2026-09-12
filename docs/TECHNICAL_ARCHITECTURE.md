# Technical Architecture

## 1. System Overview
EcoSort AI is a local Python/Streamlit prototype combining a simulated vision layer, a local RAG engine, and an LLM to provide waste disposal guidance.

## 2. Component Architecture
- **Frontend**: Streamlit UI (`app/main.py`)
- **Backend Core**: Python 3.13
- **Data Store**: Local JSON files (`data/*.json`)

## 3. Data Flow
1. User uploads image.
2. Image is preprocessed and passed to the classifier.
3. Classifier outputs Category and Confidence.
4. Confidence dictates workflow (Auto -> RAG, Medium -> Human Confirm, Low -> Human Manual).
5. RAG queries JSON DB.
6. LLM synthesizes response based on retrieved rules.
7. Safety validator checks final string.

## 4. Vision Layer
Currently simulated. Preprocesses image for sizing, but relies on a deterministic mapping script.

## 5. Classification Layer
`PrototypeDemonstrationClassifier` maps filenames to categories and confidence scores to ensure reliable demos.

## 6. RAG Layer
`Retriever` class tokenizes the query and documents, calculating token intersection (Jaccard-like similarity) to retrieve the top matching rule.

## 7. LLM Layer
`AIAssistant` class calls the OpenAI API (if configured) using a strict system prompt. If no API key is provided, it safely falls back to `_mock_generation`.

## 8. Safety Layer
`validate_response` checks the generated string against a blocklist of dangerous keywords (e.g., "burn", "drink").

## 9. Human Feedback
Handled via Streamlit session state (`st.session_state.step`). Freezes execution to await user UI button clicks.

## 10. Error Handling
Streamlit `try/except` blocks gracefully catch image processing errors. The LLM is forced to output "Insufficient info" if RAG fails.

## 11. Security
No PII is stored. `.env` is gitignored.

## 12. Privacy
Images are only processed in memory and immediately discarded.

## 13. Limitations
- Vision model is a demo placeholder.
- RAG uses simple keyword matching, not semantic vector embeddings.
- DB is small.

## 14. Future Architecture
Replace Vision Mock with HuggingFace ResNet. Replace JSON with Pinecone/ChromaDB. Wrap in a FastAPI backend and React Native frontend.
