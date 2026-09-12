# EcoSort AI Fact Sheet

**Project:**  
EcoSort AI

**Primary SDG:**  
SDG 12 — Responsible Consumption and Production

**Secondary SDGs:**  
SDG 11 — Sustainable Cities and Communities  
SDG 13 — Climate Action

**Problem:**  
Household waste contamination is high because consumers are confused by complex, constantly changing local recycling guidelines.

**Users:**  
Eco-conscious households and individuals seeking quick, accurate disposal instructions at the moment of disposal.

**AI:**  
- **Generative AI**: OpenAI-compatible Large Language Model (with a local fallback Mock Generator).
- **Retrieval Engine**: Local Next.js API token overlap semantic search (RAG).

**Prototype:**  
A polished, mobile-responsive Next.js web application ready for public cloud deployment.

**RAG:**  
Locally queries a curated JSON knowledge base (`data/disposal_rules.json`) using token overlap to ground LLM responses in actual facts.

**Vision:**  
Prototype Demonstration Classifier (A simulated layer using deterministic filename mapping to guarantee a reliable, GPU-free presentation experience).

**Human-in-loop:**  
Enabled. The system prompts the user to verify predictions if confidence is between 50% and 79%, and halts automatically forcing manual selection if confidence is below 50%.

**Responsible AI:**  
Implemented. A keyword-based safety layer blocks dangerous outputs (e.g., advising the burning of e-waste). Confidence thresholds explicitly prevent hallucination on unknown items.

**Testing:**  
Next.js build successfully verified. 

**Real-user validation:**  
NOT YET COMPLETED

**Environmental impact:**  
EXPECTED / NOT YET MEASURED

**Production readiness:**  
NOT PRODUCTION READY (This is a student prototype).
