import re
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

class ScamDetector:
    
    # Rule-based patterns
    SCAM_KEYWORDS = {
        'english': [
            'guaranteed profit', 'send money first', 'urgent', 'limited stock',
            'visa guarantee', 'earn lakh', 'pay now', 'lottery prize',
            'work from home earn', 'double your money', 'easy money',
            'no risk', '100% guaranteed', 'limited offer', 'act now'
        ],
        'bangla': [
            'নিশ্চিত লাভ', 'টাকা পাঠান', 'জরুরি', 'গ্যারান্টি',
            'লাখ আয়', 'অবিশ্বাস্য অফার', 'এখনই', 'ভিসা নিশ্চিত'
        ],
        'banglish': [
            'takar guarantee', 'taka pathao', 'lakh income', 'visa confirm',
            'easy taka', 'profit nishchit', 'joldi koro', 'aj e'
        ]
    }
    
    PAYMENT_KEYWORDS = {
        'bkash': ['bkash', 'বিকাশ', 'bikash'],
        'rocket': ['rocket', 'রকেট'],
        'bank': ['bank', 'ব্যাংক', 'transfer']
    }
    
    URGENCY_KEYWORDS = [
        'urgent', 'today only', 'limited time', 'hurry', 'last chance',
        'আজই', 'জরুরি', 'শেষ সুযোগ', 'joldi', 'aj e', 'akhon'
    ]
    
    OVERPROMISE_KEYWORDS = [
        'guaranteed', 'easy money', 'no risk', 'লাখ', 'lakh',
        'crore', 'কোটি', 'nishchit', 'guarantee', '100%'
    ]
    
    def detect_language(self, text):
        """Detect if text is English, Bangla, or Banglish"""
        bangla_chars = len(re.findall(r'[\u0980-\u09FF]', text))
        english_chars = len(re.findall(r'[a-zA-Z]', text))
        
        if bangla_chars > english_chars:
            return 'bangla'
        elif english_chars > 0 and bangla_chars > 0:
            return 'banglish'
        return 'english'
    
    def detect_payment_method(self, text):
        """Detect mentioned payment methods"""
        text_lower = text.lower()
        for method, keywords in self.PAYMENT_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return method
        return 'none'
    
    def rule_based_check(self, text):
        """Rule-based scam detection"""
        text_lower = text.lower()
        red_flags = []
        
        # Check scam keywords
        for lang, keywords in self.SCAM_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    red_flags.append(f"Suspicious keyword: '{keyword}'")
        
        # Check urgency
        for keyword in self.URGENCY_KEYWORDS:
            if keyword.lower() in text_lower:
                red_flags.append(f"Urgency pressure: '{keyword}'")
                break
        
        # Check overpromise
        for keyword in self.OVERPROMISE_KEYWORDS:
            if keyword.lower() in text_lower:
                red_flags.append(f"Overpromise detected: '{keyword}'")
                break
        
        # Check payment before service
        payment_method = self.detect_payment_method(text)
        if payment_method != 'none':
            if any(word in text_lower for word in ['first', 'আগে', 'age', 'now', 'akhon']):
                red_flags.append(f"Payment requested upfront via {payment_method}")
        
        return red_flags
    
    def ai_analysis(self, text):
        """AI-powered analysis using GPT"""
        try:
            prompt = f"""You are CheckBhai, a scam detection expert for Bangladesh. Analyze this message for scam indicators:

"{text}"

Provide:
1. Risk Level (Low/Medium/High)
2. Risk Score (0-100)
3. Detailed analysis in Bangla and English (2-3 sentences)
4. Specific red flags

Format as JSON: {{"risk_level": "...", "risk_score": X, "analysis": "...", "red_flags": [...]}}"""

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a scam detection expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content
            # Parse JSON response
            import json
            return json.loads(result)
        except:
            # Fallback if AI fails
            return {
                "risk_level": "medium",
                "risk_score": 50,
                "analysis": "Unable to complete AI analysis. Rule-based check performed.",
                "red_flags": []
            }
    
    def analyze(self, text):
        """Complete scam analysis pipeline"""
        language = self.detect_language(text)
        payment_method = self.detect_payment_method(text)
        rule_flags = self.rule_based_check(text)
        
        # If many rule flags, high risk immediately
        if len(rule_flags) >= 3:
            return {
                "risk_level": "high",
                "risk_score": 85,
                "red_flags": rule_flags,
                "ai_analysis": "Multiple scam indicators detected. Be extremely cautious!",
                "language": language,
                "payment_method_mentioned": payment_method,
                "rule_based_flags": rule_flags
            }
        
        # Get AI analysis
        ai_result = self.ai_analysis(text)
        
        # Combine results
        all_flags = rule_flags + ai_result.get("red_flags", [])
        final_score = max(len(rule_flags) * 20, ai_result.get("risk_score", 50))
        
        if final_score >= 70:
            risk_level = "high"
        elif final_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            "risk_level": risk_level,
            "risk_score": min(final_score, 100),
            "red_flags": list(set(all_flags)),
            "ai_analysis": ai_result.get("analysis", "Analysis complete."),
            "language": language,
            "payment_method_mentioned": payment_method,
            "rule_based_flags": rule_flags
        }
