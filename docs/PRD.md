# Product Requirements Document (PRD)
**Project Name**: EcoSort AI

## 1. Product Overview
EcoSort AI is a multimodal AI decision-support prototype that helps users identify waste items from images and provides grounded disposal recommendations.

## 2. Problem
Improper waste segregation leads to recycling contamination, environmental hazards, and reduced efficiency in waste management systems. Most individuals want to recycle but lack immediate, item-specific guidance.

## 3. Goals & Non-goals
**Goal**: Build a functional local prototype demonstrating an end-to-end AI workflow (Vision -> RAG -> LLM -> Validation) for waste segregation.
**Non-goal**: Do not build a production-ready mobile app or website. Do not build a heavily resourced custom computer vision model. Do not invent disposal regulations.

## 4. Target Users
- **Primary Persona**: Eco-conscious households (Hypothesis).
- **Secondary Persona**: Students learning about recycling (Hypothesis).

## 5. Functional Requirements
1. The user must be able to upload an image.
2. The system must classify the image into one of 10 predefined categories.
3. The system must retrieve disposal rules from a local JSON knowledge base based on the classification.
4. The system must use an LLM (or mock) to format the response into a clear, grounded recommendation.
5. The system must prompt for human confirmation if confidence is between 50% and 79%.
6. The system must reject predictions below 50% confidence.

## 6. Acceptance Criteria
- Uploading a "banana.jpg" successfully shows "Organic" and compost instructions.
- Uploading an "unknown.jpg" triggers the uncertainty workflow.
- Dangerous advice is caught by the safety validator.
- The app runs locally via `streamlit run`.

## 7. Risks & Dependencies
- **Risk**: API failures. **Mitigation**: Mock LLM fallback implemented.
- **Risk**: Hallucinations. **Mitigation**: RAG implementation with strict system prompts.
