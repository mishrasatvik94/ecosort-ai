# Presentation Talk Track

**SLIDE 1 (Title):**
"Hi everyone, my name is [Your Name], and for my 1M1B final project, I built EcoSort AI—an AI-powered waste identification and disposal assistant."

**SLIDE 2 (Problem):**
"I chose this problem because recycling is incredibly confusing. We all want to do the right thing, but municipal rules change all the time. This confusion leads to 'wish-cycling,' which actually contaminates entire recycling batches."

**SLIDE 3 (Target Users):**
"Our target user is the everyday eco-conscious household. When someone is holding a greasy pizza box or a broken toy, they won't spend 10 minutes reading a PDF on a city website. They need instant answers at the moment of disposal."

**SLIDE 4 (SDG 12):**
"This directly addresses SDG 12: Responsible Consumption and Production. Better sorting means less contamination, more efficient recycling, and safer handling of hazardous materials."

**SLIDE 5 (How Might We):**
"So the question was: How might we provide instant, accurate, and localized disposal guidance right when the user needs it?"

**SLIDE 6 (Solution):**
"The answer is EcoSort AI. It's a prototype that lets you snap a picture of an item, and it instantly identifies it, retrieves the specific local rules, and explains exactly how to throw it away safely."

**SLIDE 7 (Architecture):**
"Technically, it uses a three-part pipeline. A vision classifier identifies the object. But vision models don't know local laws—so I implemented a Retrieval-Augmented Generation (RAG) system to pull local rules from a database, and an LLM to explain them clearly."

**SLIDE 8 (RAG Workflow):**
"RAG is critical here. It prevents the AI from hallucinating or giving generic advice. It forces the AI to base its answer *only* on verified local database entries."

**SLIDE 9 (Screenshots):**
"Here is the prototype in action. You can see it identifying a plastic bottle and providing verified recycling instructions."

**SLIDE 10 (Responsible AI):**
"Because this involves physical waste, Responsible AI is a priority. I implemented a Human-in-the-Loop system. If the AI is uncertain about an item, it halts and asks the human to verify. It never guesses. It also has a safety filter to prevent dangerous advice, like telling someone to throw a lithium battery in the regular trash."

**SLIDE 11 (Testing):**
"The codebase is fully unit-tested, and I conducted initial manual user testing. [Insert specific testing insight here, e.g., 'Users loved how fast the RAG system pulled the exact safety rule for e-waste.']"

**SLIDE 12 (Impact):**
"While this is just a prototype, the expected impact of a deployed version is a measurable drop in household contamination rates and a massive decrease in sanitation worker hazards from improperly discarded batteries."

**SLIDE 13 (Limitations):**
"To be fully transparent, this is a student prototype. For this demo, I am using a deterministic vision mock to ensure it runs reliably on my laptop. The RAG database is also currently limited to a small proof-of-concept dataset."

**SLIDE 14 (Future Scope):**
"In the future, I plan to move this to a mobile app, train a waste-specific edge vision model, and integrate a geolocation API to automatically fetch live rules from any city. Thank you!"
