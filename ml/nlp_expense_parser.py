"""
Natural Language Processing for Expense Entry
Allows users to type: "spent 500 on groceries yesterday"
Instead of filling forms
"""

import re
from datetime import datetime, timedelta
from typing import Dict, Optional
import dateparser

class NLPExpenseParser:
    """Parse natural language expense descriptions"""
    
    # Indian merchant patterns
    MERCHANTS = [
        'swiggy', 'zomato', 'uber', 'ola', 'dmart', 'bigbazaar',
        'flipkart', 'amazon', 'myntra', 'ajio', 'paytm', 'gpay',
        'phonepe', 'dominos', 'kfc', 'mcdonalds', 'apollo', 'medlife',
        'netflix', 'prime', 'hotstar', 'spotify', 'zerodha', 'groww'
    ]
    
    # Payment method keywords
    PAYMENT_METHODS = {
        'upi': ['upi', 'gpay', 'phonepe', 'paytm', 'bhim'],
        'cash': ['cash', 'paid in cash'],
        'card': ['card', 'credit card', 'debit card', 'swiped'],
        'netbanking': ['netbanking', 'net banking', 'online'],
    }
    
    def __init__(self):
        # Amount patterns
        self.amount_patterns = [
            r'(?:rs\.?|₹)\s*(\d+(?:,\d+)*(?:\.\d{2})?)',  # ₹500, Rs 500
            r'(\d+(?:,\d+)*(?:\.\d{2})?)\s*(?:rs|rupees)',  # 500 rs
            r'(?:spent|paid|cost|worth)\s+(\d+(?:,\d+)*(?:\.\d{2})?)',  # spent 500
            r'(\d+(?:,\d+)*(?:\.\d{2})?)\s+(?:for|on)',  # 500 for
        ]
        
        # Category keywords (from expense_categorizer.py)
        self.category_keywords = {
            "Groceries": ['grocery', 'groceries', 'vegetables', 'fruits', 'dmart', 'bigbazaar', 'kirana'],
            "Dining": ['food', 'lunch', 'dinner', 'breakfast', 'swiggy', 'zomato', 'restaurant', 'cafe'],
            "Transport": ['uber', 'ola', 'metro', 'bus', 'auto', 'rickshaw', 'petrol', 'fuel', 'cab'],
            "Healthcare": ['medicine', 'doctor', 'hospital', 'pharmacy', 'apollo', 'medlife'],
            "Shopping": ['shopping', 'amazon', 'flipkart', 'myntra', 'clothes', 'shoes'],
            "Entertainment": ['movie', 'netflix', 'prime', 'spotify', 'concert', 'game'],
            "Utilities": ['electricity', 'water', 'internet', 'phone', 'bill', 'recharge'],
            "Education": ['course', 'book', 'fees', 'tuition', 'udemy'],
        }
    
    def extract_amount(self, text: str) -> Optional[float]:
        """Extract amount from text"""
        text_lower = text.lower()
        
        for pattern in self.amount_patterns:
            match = re.search(pattern, text_lower)
            if match:
                amount_str = match.group(1).replace(',', '')
                try:
                    return float(amount_str)
                except ValueError:
                    continue
        
        # Fallback: find any number
        numbers = re.findall(r'\d+(?:\.\d{2})?', text)
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                pass
        
        return None
    
    def extract_category(self, text: str) -> str:
        """Extract category from text using keywords"""
        text_lower = text.lower()
        
        scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[category] = score
        
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return "Other"
    
    def extract_merchant(self, text: str) -> Optional[str]:
        """Extract merchant/vendor name"""
        text_lower = text.lower()
        
        for merchant in self.MERCHANTS:
            if merchant in text_lower:
                return merchant.title()
        
        # Try to find "at <merchant>" or "from <merchant>"
        at_match = re.search(r'(?:at|from)\s+([a-z\s]+?)(?:\s|$)', text_lower)
        if at_match:
            return at_match.group(1).strip().title()
        
        return None
    
    def extract_date(self, text: str) -> Optional[str]:
        """Extract date from text (handles 'yesterday', 'last week', etc.)"""
        text_lower = text.lower()
        
        # Relative dates
        if 'yesterday' in text_lower:
            date = datetime.now() - timedelta(days=1)
            return date.strftime('%Y-%m-%d')
        
        if 'today' in text_lower or 'just now' in text_lower:
            return datetime.now().strftime('%Y-%m-%d')
        
        # Try parsing with dateparser
        try:
            parsed = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'past'})
            if parsed:
                return parsed.strftime('%Y-%m-%d')
        except:
            pass
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def extract_payment_method(self, text: str) -> str:
        """Extract payment method"""
        text_lower = text.lower()
        
        for method, keywords in self.PAYMENT_METHODS.items():
            if any(keyword in text_lower for keyword in keywords):
                return method.upper()
        
        return "Unknown"
    
    def parse(self, text: str) -> Dict:
        """
        Parse natural language expense description
        
        Examples:
        - "spent 500 on groceries yesterday"
        - "paid ₹1200 for Swiggy dinner"
        - "uber ride 250 to airport"
        - "bought medicine from Apollo 450"
        
        Returns:
            {
                'amount': float,
                'category': str,
                'merchant': str (optional),
                'date': str (YYYY-MM-DD),
                'payment_method': str (optional),
                'original_text': str,
                'confidence': float
            }
        """
        result = {
            'original_text': text,
            'confidence': 0.0
        }
        
        # Extract components
        amount = self.extract_amount(text)
        category = self.extract_category(text)
        merchant = self.extract_merchant(text)
        date = self.extract_date(text)
        payment_method = self.extract_payment_method(text)
        
        # Populate result
        if amount:
            result['amount'] = amount
            result['confidence'] += 0.5
        
        if category and category != "Other":
            result['category'] = category
            result['confidence'] += 0.3
        else:
            result['category'] = "Other"
        
        if merchant:
            result['merchant'] = merchant
            result['confidence'] += 0.1
        
        if date:
            result['date'] = date
            result['confidence'] += 0.1
        
        if payment_method != "Unknown":
            result['payment_method'] = payment_method
        
        # Cap confidence at 1.0
        result['confidence'] = min(result['confidence'], 1.0)
        
        return result
    
    def validate(self, parsed: Dict) -> bool:
        """Check if parsing was successful"""
        return 'amount' in parsed and parsed.get('confidence', 0) > 0.5


# Demo and testing
if __name__ == "__main__":
    parser = NLPExpenseParser()
    
    test_cases = [
        "spent 500 on groceries yesterday",
        "paid ₹1200 for Swiggy dinner",
        "uber ride 250 to airport",
        "bought medicine from Apollo pharmacy 450 rupees",
        "Rs 2500 shopping at Flipkart",
        "netflix subscription 199",
        "metro recharge 200 today",
        "electricity bill 1500 paid via UPI",
        "dmart vegetables 300",
        "coffee with friends 400",
    ]
    
    print("="*60)
    print("Natural Language Expense Parser - Demo")
    print("="*60)
    
    for text in test_cases:
        print(f"\n📝 Input: \"{text}\"")
        result = parser.parse(text)
        
        print(f"   Amount: ₹{result.get('amount', 'N/A')}")
        print(f"   Category: {result.get('category', 'Unknown')}")
        print(f"   Merchant: {result.get('merchant', 'N/A')}")
        print(f"   Date: {result.get('date', 'N/A')}")
        print(f"   Payment: {result.get('payment_method', 'N/A')}")
        print(f"   Confidence: {result.get('confidence', 0):.0%}")
        print(f"   Valid: {'✅' if parser.validate(result) else '❌'}")
