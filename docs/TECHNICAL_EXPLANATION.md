# 60-Second Technical Explanation

"So, the AI works in a continuous pipeline. First, the user uploads an image. That image goes to our classifier, which detects the item and outputs a specific waste category along with a confidence score. 

If the confidence is high, we proceed. If it's low, the system halts and asks the human to manually verify it—this is our human-in-the-loop safety measure. 

Once we have a verified category and item name, we use a RAG system—Retrieval-Augmented Generation. We take the item name and search our local knowledge base to pull the exact, verified disposal rules for that specific item. 

Finally, we send both the item name and the retrieved rules to our Large Language Model. The LLM is strictly prompted to only use the retrieved context to generate a friendly, easy-to-read disposal recommendation. Before the user sees it, a final safety script checks the output for dangerous keywords to make sure it's totally safe to display."
