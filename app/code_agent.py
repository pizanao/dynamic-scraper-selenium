from selenium.webdriver.common.by import By

class CodeAgent:
    # Selector adaptation loop: tries semantic selectors and reports winners.
    def __init__(self):
        self.candidates = {
            "card": [".product-card", "[data-role='product-card']", "article"],
            "title": [".title", "[data-field='title']", "h2", "a"],
            "category": [".category", "[data-field='category']", "[data-category]"],
            "price": [".price", "[data-field='price']", "[data-price]"],
            "rating": [".rating", "[data-field='rating']", "[data-rating]"]
        }
        self.report = {}

    def find_many(self, root, field):
        for selector in self.candidates[field]:
            els = root.find_elements(By.CSS_SELECTOR, selector)
            if els:
                self.report[f"{field}_selector"] = selector
                return els
        return []

    def find_first(self, root, field):
        found = self.find_many(root, field)
        return found[0] if found else None

    @staticmethod
    def money(v: str) -> float:
        return float(v.replace('$', '').replace(',', '').strip())

    @staticmethod
    def rating(v: str) -> float:
        return float(v.replace('★', '').strip())
