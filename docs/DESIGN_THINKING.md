# Design Thinking Process

## 1. Empathize
**Initial Observations (Hypothesis)**: 
People frequently hesitate at recycling bins, unsure if an item (like a greasy pizza box) is recyclable, compostable, or trash.

**Proposed User Interview Questions**:
- Tell me about the last time you weren't sure how to throw something away.
- How do you currently find out where an item belongs?
- How much time are you willing to spend figuring out waste disposal?

## 2. Define
**Problem Statement**: 
Everyday consumers want to dispose of waste correctly but struggle due to confusing or inaccessible local guidelines, leading to contaminated recycling streams.

**How Might We (HMW)**: 
How might we provide instant, accurate, and hyper-local disposal guidance for everyday items right at the moment of disposal?

## 3. Ideate
**Alternative Ideas Considered**:
- A smart trash can with built-in sensors (too expensive, hardware-dependent).
- A purely text-based chatbot (too much friction for the user to type descriptions).
- **Selected Idea (EcoSort AI)**: An image-based application that identifies the item visually and retrieves rules immediately.

## 4. Prototype
We built EcoSort AI as a Streamlit application, prioritizing the end-to-end AI workflow over UI polish.
**Assumptions**: We assume users will be willing to snap a picture. We assume the knowledge base can be scaled to cover local municipal differences.

## 5. Test
**Testing Plan**:
- Observe 5 users attempting to sort 5 items (banana peel, battery, plastic bottle, pizza box, ambiguous item).
- Measure success rate and time taken.
- Gather feedback on the Human-in-the-Loop interaction.

*[INSERT ACTUAL USER TEST RESULTS]* -> (To be validated)
