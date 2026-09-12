import base64
import zlib
import urllib.request
import os

def generate_kroki_url(diagram: str) -> str:
    compressed = zlib.compress(diagram.encode('utf-8'), 9)
    b64 = base64.urlsafe_b64encode(compressed).decode('utf-8')
    return f"https://kroki.io/mermaid/png/{b64}"

def save_diagram(diagram: str, filename: str):
    url = generate_kroki_url(diagram)
    print(f"Fetching diagram for {filename}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        print(f"Successfully saved {filename}")
    except Exception as e:
        print(f"Failed to save {filename}: {e}")

system_architecture = """
graph TD
    A[User] -->|Uploads Image| B[Streamlit UI]
    B --> C[Vision Layer]
    C -->|Item & Category| D[RAG Retriever]
    D -->|Queries| E[(JSON Knowledge Base)]
    E -->|Rules| D
    D -->|Context| F[AI Assistant]
    F -->|Raw Response| G[Safety Validator]
    G -->|Clean Recommendation| B
"""

ai_workflow = """
flowchart TD
    A[Image] --> B[Preprocess]
    B --> C[Mock Vision Classifier]
    C -->|Output| D{Confidence Score}
    D -->|>= 0.80| E[Accept Prediction]
    D -->|0.50 - 0.79| F[Prompt User Confirmation]
    D -->|< 0.50| G[Reject & Prompt Manual Selection]
    F -->|Confirmed| E
    F -->|Rejected| G
    G --> H[User Selects Category]
    H --> E
    E --> I[TF-IDF RAG Search]
    I --> J[LLM Generation]
"""

user_flow = """
sequenceDiagram
    participant U as User
    participant UI as Streamlit UI
    participant AI as EcoSort AI
    
    U->>UI: Uploads Waste Image
    UI->>AI: Send Image for Classification
    AI-->>UI: Returns Category & Confidence
    
    alt Confidence >= 0.8
        UI->>U: Displays High Confidence Result
    else Confidence Medium
        UI->>U: Asks for Confirmation
        U->>UI: Clicks Yes/No
    else Confidence Low
        UI->>U: Asks for Manual Selection
        U->>UI: Selects Category
    end
    
    UI->>AI: Request Disposal Guidelines
    AI-->>UI: Generates RAG-Grounded Recommendation
    UI->>U: Displays Recommendation & Safety Note
"""

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    diagrams_dir = os.path.join(base_dir, "diagrams")
    
    save_diagram(system_architecture, os.path.join(diagrams_dir, "system_architecture.png"))
    save_diagram(ai_workflow, os.path.join(diagrams_dir, "ai_workflow.png"))
    save_diagram(user_flow, os.path.join(diagrams_dir, "user_flow.png"))
