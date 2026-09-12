# Screenshot Checklist

To complete your 1M1B presentation, capture the following screenshots while running `streamlit run app/main.py`.

## 1. Application home/input screen
- **What should be visible**: The empty Streamlit UI with the title "EcoSort AI" and the file upload box.
- **Belongs to Slide**: 9 (Prototype Screenshots)

## 2. Image uploaded
- **What should be visible**: An image (e.g., banana peel) successfully uploaded and displayed in the UI.
- **Belongs to Slide**: 9 (Prototype Screenshots)

## 3. Classification result & 4. Confidence score
- **What should be visible**: The green success box saying "High Confidence Prediction: Organic (0.92)".
- **Belongs to Slide**: 9 (Prototype Screenshots)

## 5. Retrieved RAG information
- **What should be visible**: The expanded "Debug / Demo Data" sidebar on the left showing the retrieved JSON knowledge base record.
- **Belongs to Slide**: 8 (RAG Workflow)

## 6. Final AI recommendation
- **What should be visible**: The main text area displaying the final LLM-generated recommendation with "Recommended Action", "Why", and "Safety Note".
- **Belongs to Slide**: 9 (Prototype Screenshots)

## 7. Hazardous/e-waste safety response
- **What should be visible**: The output from the `battery.jpg` test, specifically showing the Safety Note about fire risks.
- **Belongs to Slide**: 10 (Responsible AI)

## 8. Low-confidence response & 9. Human correction
- **What should be visible**: The red error box for `unknown.jpg` ("Low Confidence. The AI is uncertain.") and the manual dropdown box asking the user to select the category.
- **Belongs to Slide**: 10 (Responsible AI)

## 10. Test/verification output
- **What should be visible**: Your VS Code terminal showing the green `[PASS]` output from `python scripts/verify_project.py` and `pytest tests/`.
- **Belongs to Slide**: 11 (Testing)
