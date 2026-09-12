import streamlit as st
import sys
import os
import re

# Ensure the app directory is in the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import (
    OPENAI_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME, 
    CONFIDENCE_THRESHOLD, CONFIDENCE_LOW_THRESHOLD,
    WASTE_CATEGORIES_FILE, DISPOSAL_RULES_FILE
)
from app.vision.preprocessing import preprocess_image
from app.vision.classifier import PrototypeDemonstrationClassifier
from app.rag.knowledge_base import KnowledgeBase
from app.rag.retriever import Retriever
from app.ai.assistant import AIAssistant
from app.utils.logger import get_logger

logger = get_logger(__name__)

st.set_page_config(page_title="EcoSort AI", page_icon="♻️", layout="wide")

@st.cache_resource
def load_systems():
    kb = KnowledgeBase(WASTE_CATEGORIES_FILE, DISPOSAL_RULES_FILE)
    retriever = Retriever(kb)
    classifier = PrototypeDemonstrationClassifier(kb.get_category_names())
    assistant = AIAssistant(OPENAI_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME)
    return kb, retriever, classifier, assistant

kb, retriever, classifier, assistant = load_systems()

# ----------------- SIDEBAR STATUS PANEL -----------------
with st.sidebar:
    st.info("⚠️ **Prototype Demo Mode** — Result generated using predefined demonstration mapping.")
    st.header("⚙️ Model Status Panel")
    st.markdown("""
    - **Vision Engine**: Prototype Demonstration Classifier
    - **Classification Mode**: Deterministic Filename Mapping
    - **RAG Engine**: Local TF-IDF / Keyword Retrieval
    - **Generative AI**: OpenAI-compatible LLM / Fallback Mock
    - **Safety Layer**: Keyword-based validation
    - **Human-in-the-loop**: Enabled
    """)
    
    with st.expander("🚨 Prototype Limitations"):
        st.markdown("""
        - **Vision**: Uses deterministic mapping, not real image pixel analysis. A waste-specific trained model would be required for production deployment.
        - **Knowledge Base**: Limited coverage prototype database.
        - **Local Rules**: Does not fetch live zip-code specific rules.
        - **Deployment**: Not for production or public field use.
        """)

# ----------------- MAIN UI -----------------
st.title("♻️ EcoSort AI")
st.subheader("AI-Powered Waste Identification & Disposal Assistant")

if not OPENAI_API_KEY:
    st.info("ℹ️ Running in Local Mock LLM Mode (No OpenAI API Key found).")

# Initialize session state for multi-step interaction
if "step" not in st.session_state:
    st.session_state.step = "upload"
    st.session_state.predicted_category = None
    st.session_state.confidence = 0.0
    st.session_state.filename = ""

uploaded_file = st.file_uploader("Upload an image of the waste item", type=["jpg", "jpeg", "png"])

if uploaded_file is not None and st.session_state.step == "upload":
    try:
        # 1. Preprocess
        image = preprocess_image(uploaded_file.read())
        
        # 2. Classify
        cat, conf = classifier.predict(image, uploaded_file.name)
        st.session_state.predicted_category = cat
        st.session_state.confidence = conf
        st.session_state.filename = uploaded_file.name
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image, caption="Uploaded Image", use_container_width=True)
            
        with col2:
            # 3. Determine next step based on confidence
            if conf >= CONFIDENCE_THRESHOLD:
                st.success(f"**High Confidence AI Prediction**: {cat} ({conf:.2f})")
                st.session_state.step = "generate"
                st.rerun()
                
            elif conf >= CONFIDENCE_LOW_THRESHOLD:
                st.warning(f"**Moderate Confidence AI Prediction**: {cat} ({conf:.2f})")
                st.session_state.step = "confirm"
                st.rerun()
                
            else:
                st.error(f"**Low Confidence**: {conf:.2f}. The AI is uncertain.")
                st.session_state.step = "manual_selection"
                st.rerun()
                
    except Exception as e:
        st.error(f"Error processing image: {e}")

# Step: Confirm prediction
if st.session_state.step == "confirm":
    st.write(f"The AI thinks this is **{st.session_state.predicted_category}**.")
    st.write("Was this classification correct?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Yes, proceed"):
            st.session_state.step = "generate"
            st.rerun()
    with col2:
        if st.button("❌ No, let me correct it"):
            st.session_state.step = "manual_selection"
            st.rerun()

# Step: Manual selection
if st.session_state.step == "manual_selection":
    st.error("⚠️ AI confidence was too low. Falling back to human validation.")
    st.write("Please manually select the correct category:")
    selected_cat = st.selectbox("Category", kb.get_category_names())
    if st.button("Confirm Selection"):
        st.session_state.predicted_category = selected_cat
        st.session_state.confidence = 1.0 # User verified
        st.session_state.step = "generate"
        st.rerun()

# Step: Generate Response
if st.session_state.step == "generate":
    cat = st.session_state.predicted_category
    conf = st.session_state.confidence
    item_name = st.session_state.filename.split(".")[0].replace("_", " ").title()
    
    with st.spinner("Retrieving guidelines..."):
        # 4. RAG Retrieval
        query = f"{item_name} {cat}"
        retrieved_info = retriever.search(query, top_k=2)
        
        # 5. AI Generation
        response = assistant.generate_recommendation(item_name, cat, conf, retrieved_info)
        
    st.markdown("---")
    
    if cat in ["E-Waste", "Hazardous"]:
        st.error("🛑 **WARNING: Special handling may be required. Follow verified local disposal guidance.**")
        
    # Split response into sections if possible (for mock display mostly, or we just format raw)
    st.markdown("### 📋 Final Analysis & Recommendation")
    
    st.markdown(f"**🤖 AI PREDICTION:** {item_name} -> {cat}")
    st.markdown(f"**📊 CONFIDENCE:** {conf:.2f}")
    
    if retrieved_info:
        st.markdown(f"**✅ VERIFIED INFORMATION:** Retrieved from '{retrieved_info[0].get('source', 'Unknown')}' (Status: {retrieved_info[0].get('verification', 'Needs local/official verification')})")
    else:
        st.markdown("**⚠️ VERIFIED INFORMATION:** No specific guidelines found in knowledge base.")
        
    st.markdown("---")
    st.markdown("**💡 RECOMMENDATION & SAFETY NOTE:**")
    st.info(response)
    
    # Debug / Demo RAG Evidence Sidebar
    with st.sidebar:
        st.markdown("---")
        st.header("🔍 RAG Evidence Trace")
        st.markdown(f"1. **User Input**: Image uploaded (`{st.session_state.filename}`)")
        st.markdown(f"2. **Detected Item**: `{item_name}`")
        st.markdown(f"3. **Predicted Category**: `{cat}`")
        st.markdown(f"4. **Retrieval Query**: `{query}`")
        
        st.subheader("5. Top Retrieved Knowledge")
        if retrieved_info:
            for idx, r in enumerate(retrieved_info):
                st.markdown(f"**Source**: {r.get('source')}\n\n**Guidance**: {r.get('disposal_guidance')}")
        else:
            st.text("No records retrieved.")
            
        st.subheader("6. LLM Generation")
        with st.expander("Show Raw Output"):
            st.text(response)
    
    if st.button("Start Over"):
        st.session_state.step = "upload"
        st.session_state.predicted_category = None
        st.session_state.confidence = 0.0
        st.session_state.filename = ""
        st.rerun()
