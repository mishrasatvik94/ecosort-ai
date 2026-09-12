import os
import json
import subprocess

def check_files():
    required = [
        "README.md", "requirements.txt", ".env.example", ".gitignore",
        "app/main.py", "app/config.py", "app/vision/preprocessing.py",
        "app/vision/classifier.py", "app/rag/knowledge_base.py",
        "app/rag/retriever.py", "app/ai/prompts.py", "app/ai/assistant.py",
        "app/safety/validation.py", "data/waste_categories.json",
        "data/disposal_rules.json", "docs/PRD.md", "docs/PROJECT_REPORT.md",
        "docs/DESIGN_THINKING.md", "docs/AI_WORKFLOW.md", "docs/RESPONSIBLE_AI.md",
        "docs/TEST_PLAN.md", "docs/DEMO_SCRIPT.md",
        "presentation/EcoSort_AI_Final_Presentation.md"
    ]
    all_exist = True
    for f in required:
        if not os.path.exists(f):
            print(f"MISSING FILE: {f}")
            all_exist = False
    return all_exist

def check_json_and_categories():
    try:
        with open("data/waste_categories.json", "r") as f:
            cats = json.load(f)
        with open("data/disposal_rules.json", "r") as f:
            rules = json.load(f)
            
        required_cats = [
            "Organic", "Paper", "Plastic", "Glass", "Metal", 
            "E-Waste", "Hazardous", "Sanitary", "Recyclable Mixed Material", "Other/Unknown"
        ]
        cat_names = [c["name"] for c in cats]
        for rc in required_cats:
            if rc not in cat_names:
                print(f"MISSING CATEGORY: {rc}")
                return False, False
        return True, True
    except Exception as e:
        print(f"JSON ERROR: {e}")
        return False, False

def check_security():
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "sk-" in content or "your_api_key_here" not in content:
                print("WARNING: .env file might contain real secrets!")
                # For local verification it's ok if .env exists, but we warn.
    
    with open(".env.example", "r") as f:
        content = f.read()
        if "sk-" in content:
            print("SECURITY ERROR: .env.example contains a secret key!")
            return False
            
    # Check if .env is in .gitignore
    with open(".gitignore", "r") as f:
        if ".env" not in f.read():
            print("SECURITY ERROR: .env not in .gitignore")
            return False
            
    return True

def check_tests():
    try:
        result = subprocess.run(["python", "-m", "pytest", "tests/", "--collect-only"], capture_output=True, text=True)
        if result.returncode != 0:
            print("TEST ERROR: Tests could not be discovered or failed to compile.")
            print(result.stdout, result.stderr)
            return False
        return True
    except Exception as e:
        print(f"TEST DISCOVERY ERROR: {e}")
        return False

def main():
    print("EcoSort AI Verification")
    print("=======================\n")
    
    files_ok = check_files()
    print(f"[{'PASS' if files_ok else 'FAIL'}] Project structure")
    
    json_ok, cat_ok = check_json_and_categories()
    print(f"[{'PASS' if json_ok else 'FAIL'}] JSON validation")
    print(f"[{'PASS' if cat_ok else 'FAIL'}] Required categories exist")
    
    sec_ok = check_security()
    print(f"[{'PASS' if sec_ok else 'FAIL'}] Security checks")
    
    tests_ok = check_tests()
    print(f"[{'PASS' if tests_ok else 'FAIL'}] Tests discovery")
    
    all_ok = files_ok and json_ok and cat_ok and sec_ok and tests_ok
    print(f"\nFinal Status: {'READY' if all_ok else 'NOT READY'}")

if __name__ == '__main__':
    main()
