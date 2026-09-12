import pytest
from app.vision.classifier import PrototypeDemonstrationClassifier

@pytest.fixture
def classifier():
    categories = ["Organic", "Plastic", "E-Waste", "Paper", "Hazardous", "Sanitary", "Glass", "Metal", "Other/Unknown"]
    return PrototypeDemonstrationClassifier(categories)

def test_classifier_banana(classifier):
    cat, conf = classifier.predict(None, filename="banana.jpg")
    assert cat == "Organic"
    assert conf > 0.80

def test_classifier_unknown(classifier):
    cat, conf = classifier.predict(None, filename="unknown.jpg")
    assert cat == "Other/Unknown"
    assert conf < 0.50

def test_classifier_blurry(classifier):
    cat, conf = classifier.predict(None, filename="blurry.jpg")
    assert conf < 0.80
