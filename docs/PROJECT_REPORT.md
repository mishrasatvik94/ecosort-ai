# Project Report: EcoSort AI

## 1. Title
EcoSort AI - AI-Powered Waste Identification, Segregation & Disposal Assistant

## 2. Abstract
EcoSort AI is a multimodal AI decision-support prototype built to aid individuals in responsible waste disposal. By combining image classification, a Retrieval-Augmented Generation (RAG) knowledge base, and Large Language Models (LLMs), the system provides grounded, safe, and item-specific recycling guidance.

## 3. Background & 4. Problem Statement
Many municipalities have complex and constantly changing rules for waste disposal. This leads to "wish-cycling" (recycling items hoping they are recyclable) which contaminates recycling streams and damages sorting machinery.

## 5. SDG Mapping
- **Primary**: SDG 12 – Responsible Consumption and Production.
- **Secondary**: SDG 11 – Sustainable Cities and Communities, SDG 13 – Climate Action.

## 6. Target Users
Households, students, and environmentally conscious individuals lacking access to quick, localized disposal knowledge.

## 7. Design Thinking Process
Refer to `DESIGN_THINKING.md` for empathy mapping, ideation, and prototyping methodology.

## 8. Proposed Solution & 9. System Architecture
EcoSort AI provides a simple UI to upload images. It classifies the item, retrieves specific rules from a local JSON database via TF-IDF search, and synthesizes a recommendation using an LLM. 
*(See diagrams/system_architecture.png)*

## 10. AI Components & 11. RAG Workflow
- **Vision**: Mock layer for MVP (designed to be replaced with a HuggingFace pipeline).
- **RAG**: Scikit-learn TF-IDF matching over a JSON dataset.
- **LLM**: OpenAI-compatible client (or local Mock LLM).

## 12. Prototype Implementation
Implemented in Python using Streamlit for local desktop usage.

## 13. Responsible AI
Safety keyword validation, strict confidence thresholding (<0.50 rejected), and Human-in-the-Loop confirmations are core architectural pillars. Refer to `RESPONSIBLE_AI.md`.

## 14. Testing Methodology
Tested manually and via Pytest for classification confidence logic, RAG retrieval accuracy, and safety validation blocks. Refer to `TEST_PLAN.md`.

## 15. Expected Impact
Reduced contamination in local recycling streams and better awareness of e-waste hazards. *(Metrics to be validated with user testing).*

## 16. Limitations
Currently uses a mock vision layer and a small prototype dataset.

## 17. Future Scope
Integration with real municipal databases, mobile app deployment, and real vision model integration.

## 18. Conclusion
EcoSort AI successfully demonstrates the feasibility of combining RAG and LLMs to solve the localized knowledge problem in waste management.
