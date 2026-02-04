"""
CheckBhai AI Engine - Text classification for scam detection
Supports English, Bangla, and Banglish text
"""

import pickle
import os
import json
from typing import Tuple, Dict, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import numpy as np
from openai import AsyncOpenAI

from app.training_data import get_training_data

class AIEngine:
    """AI-powered scam detection using text classification and LLM reasoning"""
    
    def __init__(self, model_path: str = "app/models/scam_classifier.pkl"):
        self.model_path = model_path
        self.model = None
        self.is_trained = False
        self.openai_client = None
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.openai_client = AsyncOpenAI(api_key=api_key)
        
        # Try to load existing model
        if os.path.exists(model_path):
            self.load_model()
        else:
            # Train new model if none exists
            self.train_model()
    
    def train_model(self, save: bool = True):
        # ... (Existing training logic remains the same)
        print("Training CheckBhai AI model...")
        training_data = get_training_data()
        texts = [item['text'] for item in training_data]
        labels = [1 if item['label'] == 'Scam' else 0 for item in training_data]
        
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 3),
                max_features=5000,
                min_df=1,
                max_df=0.9,
                sublinear_tf=True,
                analyzer='char_wb'
            )),
            ('clf', MultinomialNB(alpha=0.1))
        ])
        
        self.model.fit(texts, labels)
        self.is_trained = True
        
        if save:
            self.save_model()
        return True

    async def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive analysis using both local model and LLM if available
        """
        # 1. Local Model Prediction
        proba = self.model.predict_proba([text])[0]
        scam_confidence = float(proba[1])
        prediction = "Scam" if scam_confidence > 0.5 else "Legit"
        
        result = {
            "prediction": prediction,
            "confidence": scam_confidence if prediction == "Scam" else float(proba[0]),
            "is_scam": prediction == "Scam",
            "explanation_en": "Basic pattern matching detected.",
            "explanation_bn": "প্রাথমিক প্যাটার্ন ম্যাচিং সনাক্ত করা হয়েছে।",
            "red_flags": []
        }
        
        # 2. LLM Reasoning (if configured)
        if self.openai_client:
            try:
                llm_result = await self._get_llm_reasoning(text)
                if llm_result:
                    result.update(llm_result)
            except Exception as e:
                print(f"LLM Reasoning failed: {e}")
        
        return result

    async def _get_llm_reasoning(self, text: str) -> Optional[Dict]:
        """Call LLM for deep reasoning and bilingual explanation"""
        prompt = f"""
        Analyze the following message for potential scam indicators.
        The message might be in English, Bangla, or Banglish (Bangla in Roman script).
        
        Message: "{text}"
        
        Output high-quality analysis in JSON format:
        {{
            "is_scam": boolean,
            "explanation_en": "Reason why it's a scam or legit (English)",
            "explanation_bn": "Reason why it's a scam or legit (Bangla)",
            "scam_probability": float (0-1),
            "red_flags": ["list of indicators observed"]
        }}
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior security analyst specializing in Bangladeshi fraud patterns."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except:
            return None

    def predict(self, text: str) -> Tuple[str, float]:
        # Legacy support for existing routers
        proba = self.model.predict_proba([text])[0]
        if proba[1] > 0.5:
            return "Scam", float(proba[1])
        return "Legit", float(proba[0])

    def analyze(self, text: str) -> Dict:
        # Synchronous wrapper for legacy support
        prediction, confidence = self.predict(text)
        return {
            "prediction": prediction,
            "confidence": float(confidence),
            "is_scam": prediction == "Scam",
            "confidence_percentage": int(confidence * 100)
        }

    def save_model(self):
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self):
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.is_trained = True
        except Exception as e:
            self.train_model()

    def retrain_with_feedback(self, new_texts: list, new_labels: list):
        training_data = get_training_data()
        all_texts = [item['text'] for item in training_data] + new_texts
        all_labels = [1 if item['label'] == 'Scam' else 0 for item in training_data] + new_labels
        self.model.fit(all_texts, all_labels)
        self.save_model()
        return True

# Global AI engine instance
ai_engine = None

def get_ai_engine():
    global ai_engine
    if ai_engine is None:
        ai_engine = AIEngine()
    return ai_engine

# Global AI engine instance
ai_engine = None

def get_ai_engine():
    """Get or create AI engine instance"""
    global ai_engine
    if ai_engine is None:
        ai_engine = AIEngine()
    return ai_engine
