# EcoSort AI - 1M1B AI for Sustainability Prototype

EcoSort AI is a **student prototype** demonstrating an AI-assisted waste identification and disposal guidance workflow, developed for the 1M1B AI for Sustainability Virtual Internship.

## What is this?
This project is a fully functional Next.js web application. It demonstrates how Vision Models, Retrieval-Augmented Generation (RAG), and Large Language Models (LLMs) can be combined to solve the problem of household recycling contamination ("wish-cycling"). 

> [!IMPORTANT]
> **Prototype Status:** This is NOT a production-ready application. It is a web-based demonstration designed to show the end-to-end AI workflow.

## Implemented Features
- **Modern Web UI**: Built with Next.js and Tailwind CSS for a responsive, mobile-friendly experience.
- **RAG Engine**: Locally searches a curated JSON database (`data/disposal_rules.json`) using token overlap to ground the LLM in verified local rules.
- **LLM Synthesis**: Uses an OpenAI-compatible API to generate natural language explanations via Next.js API Routes. Includes a seamless deterministic fallback generator if no API key is provided.
- **Safety Validation**: Blocks dangerous keywords from being output.
- **Human-in-the-Loop**: The UI pauses and asks the user to confirm low-confidence AI predictions, forcing manual selection if confidence is too low.

## Honest AI Disclosure (Demonstration Components)
- **Prototype Demonstration Classifier**: To ensure 100% reliable public demonstrations without heavy GPU inference costs, the Vision Classifier currently uses a deterministic filename mapping heuristic. **This is a simulation of a computer vision model, not actual pixel analysis.**
- **Demo Mode UI**: The UI explicitly displays debug data, RAG tracing, and verification statuses so evaluators can see the underlying data flow.

## Requirements for a Real Production Model
To upgrade this from a prototype to a real-world application, the following would be required:
1. **Computer Vision**: Integrating a real PyTorch/TensorFlow model trained on a massive waste dataset (e.g., TrashNet).
2. **Vector Database**: Replacing the local JSON token matcher with a true semantic vector database (e.g., Pinecone) using dense embeddings.

---

## Running Locally

### 1. Navigate to the Web Directory
```bash
cd web
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Environment Variables (Optional)
If you want to use the real OpenAI LLM instead of the local mock fallback, create a `.env.local` file inside the `web/` folder:
```
OPENAI_API_KEY=your_secret_key_here
```
*Never commit this file to GitHub.*

### 4. Start the Development Server
```bash
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## Deployment
See `docs/DEPLOYMENT.md` for step-by-step instructions on deploying this Next.js app to Vercel or Firebase.
