import json
from openai import OpenAI
from app.ai.prompts import SYSTEM_PROMPT
from app.safety.validation import validate_response
from app.utils.logger import get_logger

logger = get_logger(__name__)

class AIAssistant:
    def __init__(self, api_key: str, base_url: str, model_name: str):
        self.api_key = api_key
        self.model_name = model_name
        self.use_mock = not bool(api_key)
        
        if not self.use_mock:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            logger.warning("No OPENAI_API_KEY provided. Using Mock LLM.")

    def generate_recommendation(self, item_name: str, category: str, confidence: float, rag_context: list) -> str:
        
        context_str = json.dumps(rag_context, indent=2) if rag_context else "No specific guidance found in the knowledge base."
        
        user_prompt = f"""
Detected Item: {item_name}
Predicted Category: {category}
Confidence: {confidence:.2f}

Retrieved Disposal Information:
{context_str}
"""

        if self.use_mock:
            return self._mock_generation(item_name, category, confidence, rag_context)

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.0
            )
            llm_text = response.choices[0].message.content.strip()
            
            if not validate_response(llm_text):
                logger.error("Safety validation failed for LLM response.")
                return "Error: The generated response failed safety validation."
            
            return llm_text
        except Exception as e:
            logger.error(f"LLM API Error: {str(e)}")
            return f"Error: AI API unavailable. ({str(e)})"

    def _mock_generation(self, item_name: str, category: str, confidence: float, rag_context: list) -> str:
        """
        A fallback mock generation method if no API key is provided.
        """
        if not rag_context:
            action = "I don't have enough verified information to provide a definitive disposal recommendation."
            why = "No matched rules found in the local database."
            safety = "Handle with generic caution."
            info = "Insufficient info"
        else:
            best_match = rag_context[0]
            action = best_match.get("disposal_guidance", "Check local municipal guidelines.")
            why = best_match.get("handling", "General best practice.")
            safety = best_match.get("safety_warning", "Handle with care.")
            info = best_match.get("source", "No specific guidance found")
            
        if confidence < 0.5:
            action = "I don't have enough verified information to provide a definitive disposal recommendation."
            why = "Cannot recommend action due to very low confidence."
            info = "Insufficient info"

        response = f"""Detected Item: {item_name}
Category: {category}
Confidence: {confidence:.2f}
Recommended Action: {action}
Why: {why}
Safety Note: {safety}
Information Basis: {info}"""
        
        if not validate_response(response):
            return "Error: The generated response failed safety validation."
            
        return response
