# Evaluation Matrix

| Test ID | Input | Expected Behaviour | Actual Result | Status | Evidence Screenshot |
|---|---|---|---|---|---|
| E01 | `banana.jpg` | Predicts Organic, retrieves compost rules | | | |
| E02 | `bottle.jpg` | Predicts Plastic, retrieves recycle rules | | | |
| E03 | `glass.jpg` | Predicts Glass, retrieves glass handling rules | | | |
| E04 | `mobile.jpg` | Predicts E-Waste, retrieves safety and reset rules | | | |
| E05 | `battery.jpg` | Predicts E-Waste, warns about fire risks | | | |
| E06 | `unknown.jpg` | Low confidence (<50%), halts and prompts human | | | |
| E07 | Invalid image file | Streamlit catches upload error | | | |
| E08 | Unsupported file (.txt) | File uploader rejects format | | | |
| E09 | Medium confidence (0.50 - 0.79) | Prompts for human "Yes/No" validation | | | |
| E10 | Missing RAG information | LLM says "I don't have enough verified information..." | | | |
| E11 | LLM API unavailable | Fails gracefully to Mock Generator | | | |
| E12 | Unsafe generated output | Caught by safety keyword validator | | | |
