# Safety keywords that could indicate dangerous advice
DANGEROUS_KEYWORDS = [
    "burn it",
    "drink",
    "eat",
    "mix with bleach",
    "throw in the ocean",
    "flush down the toilet"
]

def validate_response(response_text: str) -> bool:
    """
    Validates if the LLM response contains obviously dangerous instructions.
    Returns True if safe, False if potentially dangerous.
    """
    lower_text = response_text.lower()
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in lower_text:
            return False
    return True
