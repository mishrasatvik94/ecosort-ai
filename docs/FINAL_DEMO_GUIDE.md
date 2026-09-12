# Final Demo Guide (3-Minute Presentation)

## A. How to start the prototype
Open your terminal in VS Code, ensure your virtual environment is active, and run the Streamlit app.

## B. Exact command
```bash
streamlit run app/main.py
```

---

## C. Demo Case 1 — Banana Peel
- **IMAGE TO USE**: `banana.jpg`
- **ACTION**: Upload the image.
- **EXPECTED OUTPUT**: High Confidence > 0.80. RAG pulls Organic rules.
- **AI FEATURE DEMONSTRATED**: Standard Vision-to-RAG-to-LLM pipeline.
- **WHAT I SHOULD SAY**: "Here we upload a banana peel. The vision model predicts 'Organic' with high confidence. The RAG system retrieves local composting guidelines, and our AI formulates a clear disposal recommendation."

---

## D. Demo Case 2 — Plastic Bottle
- **IMAGE TO USE**: `bottle.jpg`
- **ACTION**: Upload the image.
- **EXPECTED OUTPUT**: High Confidence > 0.80. RAG pulls Plastic rules.
- **AI FEATURE DEMONSTRATED**: Accurate categorization and handling instructions.
- **WHAT I SHOULD SAY**: "For a plastic bottle, the AI not only tells us to recycle it, but the RAG guidelines specifically remind us to empty all liquids first, preventing contamination."

---

## E. Demo Case 3 — E-Waste
- **IMAGE TO USE**: `mobile.jpg`
- **ACTION**: Upload the image.
- **EXPECTED OUTPUT**: High Confidence > 0.80. RAG pulls E-Waste rules.
- **AI FEATURE DEMONSTRATED**: Data privacy awareness in disposal.
- **WHAT I SHOULD SAY**: "E-waste is critical. When I upload a mobile phone, the AI specifically advises me to factory reset the device for data privacy before taking it to a certified drop-off."

---

## F. Demo Case 4 — Battery
- **IMAGE TO USE**: `battery.jpg`
- **ACTION**: Upload the image.
- **EXPECTED OUTPUT**: High Confidence. RAG pulls Hazardous safety warnings.
- **AI FEATURE DEMONSTRATED**: Responsible AI safety guardrails.
- **WHAT I SHOULD SAY**: "Lithium batteries cause fires in recycling trucks. Notice how our RAG system pulls a strict safety warning, and the AI highlights that it should NEVER go in the regular trash."

---

## G. Demo Case 5 — Low Confidence / Unknown
- **IMAGE TO USE**: `unknown.jpg`
- **ACTION**: Upload the image.
- **EXPECTED OUTPUT**: Confidence < 0.50. Error message forces manual dropdown.
- **AI FEATURE DEMONSTRATED**: Human-in-the-Loop & Anti-Hallucination.
- **WHAT I SHOULD SAY**: "If the AI is unsure, like with this ambiguous item, it admits low confidence and stops. It asks the user to manually select the category. It refuses to hallucinate a rule if it doesn't know what the item is. This is Responsible AI in practice."
