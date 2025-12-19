"""
AI-Powered Expense Categorization
Uses NLP to automatically categorize expenses from descriptions
"""

import re
import pickle
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Indian-specific expense categories
CATEGORIES = [
    "Groceries",
    "Dining",
    "Transport",
    "Housing",
    "Entertainment",
    "Healthcare",
    "Shopping",
    "Education",
    "Utilities",
    "Insurance",
    "Investment",
    "Other"
]

# Keywords mapping for Indian context
INDIAN_KEYWORDS = {
    "Groceries": [
        "dmart", "bigbazaar", "reliance fresh", "more", "supermarket", "grocery",
        "vegetables", "fruits", "milk", "bread", "rice", "dal", "sabzi",
        "kirana", "ration", "provisions"
    ],
    "Dining": [
        "swiggy", "zomato", "restaurant", "cafe", "dhaba", "hotel", "food",
        "lunch", "dinner", "breakfast", "pizza", "burger", "biryani",
        "dominos", "kfc", "mcdonalds", "subway", "haldiram", "bikanervala"
    ],
    "Transport": [
        "uber", "ola", "rapido", "metro", "bus", "train", "auto", "rickshaw",
        "petrol", "diesel", "fuel", "cng", "parking", "toll", "fastag",
        "irctc", "flight", "taxi", "cab"
    ],
    "Housing": [
        "rent", "maintenance", "society", "housing", "apartment", "flat",
        "electricity", "water", "gas", "cylinder", "lpg", "repair",
        "furniture", "home", "paint"
    ],
    "Entertainment": [
        "movie", "pvr", "inox", "netflix", "amazon prime", "hotstar", "spotify",
        "concert", "show", "bookmyshow", "game", "fun", "party", "club"
    ],
    "Healthcare": [
        "doctor", "hospital", "clinic", "medicine", "pharmacy", "apollo",
        "medlife", "1mg", "netmeds", "health", "treatment", "checkup",
        "lab", "test", "insurance", "medical"
    ],
    "Shopping": [
        "amazon", "flipkart", "myntra", "ajio", "meesho", "shopping",
        "clothes", "shoes", "mall", "store", "online", "order",
        "fashion", "accessories", "gadget"
    ],
    "Education": [
        "fees", "tuition", "course", "udemy", "coursera", "book", "study",
        "school", "college", "university", "coaching", "exam", "education"
    ],
    "Utilities": [
        "electricity bill", "water bill", "phone bill", "internet", "wifi",
        "broadband", "jio", "airtel", "vodafone", "bsnl", "recharge",
        "mobile", "postpaid", "prepaid"
    ],
    "Insurance": [
        "lic", "insurance", "premium", "policy", "health insurance",
        "car insurance", "life insurance", "term insurance"
    ],
    "Investment": [
        "mutual fund", "sip", "stock", "shares", "zerodha", "groww",
        "upstox", "investment", "fd", "fixed deposit", "ppf", "nps"
    ]
}


class ExpenseCategorizer:
    """ML-based expense categorizer for Indian context"""
    
    def __init__(self, model_path: str = None):
        self.model_path = model_path or "ml/models/expense_categorizer.pkl"
        self.pipeline = None
        self.is_trained = False
        
        # Load model if exists
        if Path(self.model_path).exists():
            self.load_model()
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess expense description"""
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def _keyword_match(self, text: str) -> str:
        """Rule-based categorization using keywords"""
        text_lower = text.lower()
        
        scores = {}
        for category, keywords in INDIAN_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[category] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return "Other"
    
    def predict(self, description: str) -> Tuple[str, float]:
        """
        Predict category for expense description
        
        Returns:
            (category, confidence)
        """
        # First try keyword matching (fast and accurate for known patterns)
        keyword_category = self._keyword_match(description)
        
        # If ML model is available, use it for better accuracy
        if self.is_trained and self.pipeline:
            processed = self._preprocess_text(description)
            
            try:
                category = self.pipeline.predict([processed])[0]
                probabilities = self.pipeline.predict_proba([processed])[0]
                confidence = max(probabilities)
                
                # If keyword match and ML agree, high confidence
                if keyword_category == category:
                    return category, min(confidence + 0.1, 1.0)
                
                # If ML is confident, use it
                if confidence > 0.6:
                    return category, confidence
                
                # Otherwise use keyword match
                return keyword_category, 0.5
            except Exception as e:
                print(f"ML prediction failed: {e}")
                return keyword_category, 0.5
        
        # Fallback to keyword matching
        return keyword_category, 0.5 if keyword_category != "Other" else 0.2
    
    def predict_batch(self, descriptions: List[str]) -> List[Tuple[str, float]]:
        """Predict categories for multiple descriptions"""
        return [self.predict(desc) for desc in descriptions]
    
    def train(self, training_data: List[Tuple[str, str]]):
        """
        Train the model on labeled data
        
        Args:
            training_data: List of (description, category) tuples
        """
        if len(training_data) < 10:
            print("Not enough training data. Using keyword-based categorization.")
            return
        
        descriptions, categories = zip(*training_data)
        
        # Preprocess
        descriptions = [self._preprocess_text(desc) for desc in descriptions]
        
        # Create pipeline
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=500, ngram_range=(1, 2))),
            ('classifier', MultinomialNB(alpha=0.1))
        ])
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            descriptions, categories, test_size=0.2, random_state=42
        )
        
        # Train
        self.pipeline.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluate
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model trained! Accuracy: {accuracy:.2%}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        # Save model
        self.save_model()
    
    def save_model(self):
        """Save trained model to disk"""
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'pipeline': self.pipeline,
                'is_trained': self.is_trained
            }, f)
        
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk"""
        try:
            with open(self.model_path, 'rb') as f:
                data = pickle.load(f)
                self.pipeline = data['pipeline']
                self.is_trained = data['is_trained']
            
            print(f"Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.is_trained = False


# Example usage and sample training data
SAMPLE_TRAINING_DATA = [
    ("Paid 500 to Swiggy for dinner", "Dining"),
    ("DMart grocery shopping 2500", "Groceries"),
    ("Uber ride to airport 850", "Transport"),
    ("Netflix subscription 199", "Entertainment"),
    ("Electricity bill payment 1200", "Utilities"),
    ("Apollo pharmacy medicines 450", "Healthcare"),
    ("Myntra shoes purchase 1999", "Shopping"),
    ("Metro card recharge 200", "Transport"),
    ("Dominos pizza order 699", "Dining"),
    ("Rent payment 15000", "Housing"),
    ("Zerodha brokerage 20", "Investment"),
    ("Phone recharge Jio 299", "Utilities"),
    ("BookMyShow movie tickets 600", "Entertainment"),
    ("Vegetables from local market 300", "Groceries"),
    ("OLA auto rickshaw 60", "Transport"),
    ("LIC premium payment 5000", "Insurance"),
    ("Udemy course purchase 399", "Education"),
    ("Haldiram snacks 250", "Groceries"),
    ("Petrol pump fill 2000", "Transport"),
    ("Amazon Prime renewal 1499", "Entertainment"),
]


if __name__ == "__main__":
    # Demo
    categorizer = ExpenseCategorizer()
    
    # Train with sample data
    categorizer.train(SAMPLE_TRAINING_DATA)
    
    # Test predictions
    test_cases = [
        "Spent 1200 on groceries at BigBazaar",
        "Zomato food delivery 450",
        "Metro ticket to Connaught Place",
        "Doctor consultation fee 800",
        "Flipkart shopping 3500",
    ]
    
    print("\n" + "="*50)
    print("Testing Predictions:")
    print("="*50)
    
    for desc in test_cases:
        category, confidence = categorizer.predict(desc)
        print(f"\nDescription: {desc}")
        print(f"Category: {category} (confidence: {confidence:.2%})")
