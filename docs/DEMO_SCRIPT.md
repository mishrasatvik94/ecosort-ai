# Demo Script (2-3 Minutes)

**1. Introduce Problem (0:00 - 0:30)**
"Hello, for my final project I built EcoSort AI. Recycling rules are confusing, which leads to contamination. I wanted to build an AI assistant that identifies waste and gives you instant, localized rules."

**2. High Confidence Path (0:30 - 1:00)**
"Let's upload an image of a banana peel (upload banana.jpg). The vision model classifies this as Organic with high confidence. The RAG system pulls the compost rules, and the LLM formats it nicely for the user."

**3. Safety & E-Waste (1:00 - 1:30)**
"Now let's upload a lithium battery (upload battery.jpg). It correctly identifies it as E-Waste. Notice the safety note retrieved by RAG—it warns about fire risks and tells the user not to throw it in the normal trash."

**4. Human-in-the-Loop & Uncertainty (1:30 - 2:00)**
"If I upload something blurry (upload blurry.jpg), the AI has low confidence. Instead of hallucinating, it forces the user to manually select the category, keeping the human in control. This follows Responsible AI principles."

**5. Impact & Conclusion (2:00 - 2:30)**
"By reducing wish-cycling, this prototype directly supports SDG 12: Responsible Consumption and Production. Thank you."
