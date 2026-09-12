import pytest
from app.safety.validation import validate_response

def test_valid_response():
    response = "Please dispose of this in the recycling bin."
    assert validate_response(response) is True

def test_dangerous_response():
    response = "If you don't want it, you should burn it in the backyard."
    assert validate_response(response) is False

def test_dangerous_response_mix():
    response = "Mix with bleach to clean it first."
    assert validate_response(response) is False
