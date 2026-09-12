import json
import os
from typing import List, Dict

class KnowledgeBase:
    def __init__(self, categories_path: str, rules_path: str):
        self.categories_path = categories_path
        self.rules_path = rules_path
        self.categories = self._load_json(self.categories_path)
        self.rules = self._load_json(self.rules_path)

    def _load_json(self, path: str) -> List[Dict]:
        if not os.path.exists(path):
            return []
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_all_rules(self) -> List[Dict]:
        return self.rules

    def get_categories(self) -> List[Dict]:
        return self.categories

    def get_category_names(self) -> List[str]:
        return [c["name"] for c in self.categories]
