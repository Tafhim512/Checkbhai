"""
CheckBhai Rules Engine - Pattern-based risk detection
Detects suspicious patterns across English, Bangla, and Banglish
"""

import re
from typing import List, Tuple

class RulesEngine:
    """Rule-based risk detection engine"""
    
    # Pressure keywords in multiple languages
    URGENCY_KEYWORDS = {
        'english': ['urgent', 'immediately', 'now', 'today', 'hurry', 'limited', 'last chance', 
                   'expire', 'within 24 hours', 'only', 'slots left', 'stock left'],
        'bangla': ['taratari', 'ajo', 'ekhoni', 'ekhon', 'shesh', 'limited'],
        'bangla_unicode': ['তাড়াতাড়ি', 'আজ', 'এখনই', 'এখন', 'শেষ', 'দ্রুত']
    }
    
    # Payment request keywords
    PAYMENT_KEYWORDS = {
        'english': ['pay', 'send money', 'bkash', 'rocket', 'nagad', 'bank transfer', 
                   'advance', 'fee', 'taka pathao', 'payment'],
        'bangla': ['taka', 'pathao', 'bkash', 'rocket', 'advance', 'fee', 'taka den'],
        'bangla_unicode': ['টাকা', 'পাঠাও', 'বিকাশ', 'রকেট', 'নগদ', 'ফি']
    }
    
    # Unrealistic promise keywords
    OVERPROMISE_KEYWORDS = {
        'english': ['guarantee', '100%', 'guaranteed', 'confirm', 'sure', 'certain', 
                   'no risk', 'risk free', 'easy money'],
        'bangla': ['guarantee', 'confirm', 'nischit', 'pakka', 'guarantee'],
        'bangla_unicode': ['গ্যারান্টি', 'নিশ্চিত', 'পাক্কা', 'কনফার্ম']
    }
    
    # Suspicious patterns
    SUSPICIOUS_PATTERNS = {
        'too_good_prices': r'\b(only|matro|মাত্র)\s*(\d+)\s*(taka|টাকা|BDT)',
        'percentage': r'(\d+)%',
        'large_numbers': r'(\d+)\s*(lakh|লাখ|thousand|হাজার)',
        'job_fees': r'(registration|visa|processing)\s*(fee|ফি)',
        'personal_info_request': r'(PIN|password|OTP|পাসওয়ার্ড|পিন)'
    }
    
    def __init__(self):
        self.red_flags = []
    
    def check_message(self, text: str) -> Tuple[List[str], int]:
        """
        Analyze message for suspicious patterns
        Returns: (red_flags, risk_score)
        """
        self.red_flags = []
        risk_score = 0
        text_lower = text.lower()
        
        # Check for pressure tactics
        if self._contains_keywords(text_lower, self.URGENCY_KEYWORDS):
            self.red_flags.append("⚠️ Uses pressure tactics or artificial urgency")
            risk_score += 25
        
        # Check for payment requests
        if self._contains_keywords(text_lower, self.PAYMENT_KEYWORDS):
            self.red_flags.append("💰 Requests advance or direct payment")
            risk_score += 30
        
        # Check for unrealistic promises
        if self._contains_keywords(text_lower, self.OVERPROMISE_KEYWORDS):
            self.red_flags.append("🎯 Makes unrealistic guarantees")
            risk_score += 25
        
        # Check for sensitive info phishing
        if re.search(self.SUSPICIOUS_PATTERNS['personal_info_request'], text, re.IGNORECASE):
            self.red_flags.append("🔐 Requests sensitive personal information (PIN/OTP)")
            risk_score += 60
        
        # Check for job/visa fees
        if re.search(self.SUSPICIOUS_PATTERNS['job_fees'], text, re.IGNORECASE):
            self.red_flags.append("📋 Charges fees for job or visa services")
            risk_score += 40
        
        # Check for suspiciously low prices
        price_match = re.search(self.SUSPICIOUS_PATTERNS['too_good_prices'], text, re.IGNORECASE)
        if price_match:
            try:
                amount = int(price_match.group(2))
                if amount < 20000 and any(word in text_lower for word in ['iphone', 'macbook', 'laptop', 'gold', 'স্বর্ণ']):
                    self.red_flags.append("💸 Suspiciously low price for premium items")
                    risk_score += 30
            except:
                pass
        
        # Check for high percentage returns
        percent_match = re.search(self.SUSPICIOUS_PATTERNS['percentage'], text)
        if percent_match:
            try:
                percentage = int(percent_match.group(1))
                if percentage > 50:
                    self.red_flags.append("📈 Promises unrealistic returns")
                    risk_score += 30
            except:
                pass
        
        # Check for prize/lottery patterns
        if any(word in text_lower for word in ['lottery', 'লটারি', 'prize', 'won', 'jitechen', 'জিতেছেন']):
            if any(word in text_lower for word in ['fee', 'claim', 'ফি', 'processing']):
                self.red_flags.append("🎰 Unsolicited prize claim requiring fees")
                risk_score += 50
        
        # Cap risk score at 100
        risk_score = min(risk_score, 100)
        
        return self.red_flags, risk_score
    
    def _contains_keywords(self, text: str, keyword_dict: dict) -> bool:
        """Check if text contains any keywords from the dictionary"""
        for lang, keywords in keyword_dict.items():
            if any(keyword in text for keyword in keywords):
                return True
        return False
    
    def get_risk_level(self, risk_score: int) -> str:
        """Convert risk score to risk level"""
        if risk_score >= 60:
            return "High"
        elif risk_score >= 30:
            return "Medium"
        else:
            return "Low"
    
    def generate_explanation(self, text: str, risk_level: str, red_flags: List[str], ai_confidence: float = None) -> str:
        """Generate evidence-based explanation in English"""
        if risk_level == "High":
            explanation = "⚠️ **High Risk Pattern Detected.** This message matches multiple patterns often associated with suspicious activity. "
        elif risk_level == "Medium":
            explanation = "⚡ **Potential Risk.** This message contains some suspicious elements. "
        else:
            explanation = "✅ **Low Risk.** This message does not show obvious suspicious patterns. "
        
        if red_flags:
            explanation += f"Identified flags: {', '.join(red_flags)}. "
        
        if risk_level in ["High", "Medium"]:
            explanation += "Always verify the sender's identity through official channels before sharing money or personal data."
        
        return explanation

    def generate_explanation_bn(self, text: str, risk_level: str, red_flags: List[str]) -> str:
        """Generate evidence-based explanation in Bangla"""
        if risk_level == "High":
            explanation = "⚠️ **উচ্চ ঝুঁকি সনাক্ত করা হয়েছে!** এই বার্তাটিতে সন্দেহজনক কার্যক্রমের একাধিক লক্ষণ পাওয়া গেছে। "
        elif risk_level == "Medium":
            explanation = "⚡ **ঝুঁকি থাকতে পারে।** এই বার্তাটিতে কিছু সন্দেহজনক উপাদান রয়েছে। "
        else:
            explanation = "✅ **ঝুঁকি কম মনে হচ্ছে।** এই বার্তায় বড় কোনো সন্দেহজনক লক্ষণ পাওয়া যায়নি। "
        
        if risk_level in ["High", "Medium"]:
            explanation += "টাকা বা ব্যক্তিগত তথ্য শেয়ার করার আগে সর্বদা অফিশিয়াল মাধ্যমে পরিচয় যাচাই করুন।"
        
        return explanation
