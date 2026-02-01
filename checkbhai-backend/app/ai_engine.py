"""
CheckBhai AI Engine - Text classification for scam detection
Supports English, Bangla, and Banglish text
"""

import pickle
import os
from typing import Tuple, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import numpy as np

from app.training_data import get_training_data

class AIEngine:
    """AI-powered scam detection using text classification"""
    
    def __init__(self, model_path: str = "app/models/scam_classifier.pkl"):
        self.model_path = model_path
        self.model = None
        self.is_trained = False
        
        # Try to load existing model
        if os.path.exists(model_path):
            self.load_model()
        else:
            # Train new model if none exists
            self.train_model()
    
    def train_model(self, save: bool = True):
        """Train the scam classification model"""
        print("Training CheckBhai AI model...")
        
        # Get training data
        training_data = get_training_data()
        
        # Extract features and labels
        texts = [item['text'] for item in training_data]
        labels = [1 if item['label'] == 'Scam' else 0 for item in training_data]
        
        # Create pipeline with TF-IDF and Multinomial Naive Bayes
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 3),  # Unigrams, bigrams, trigrams
                max_features=5000,
                min_df=1,
                max_df=0.9,
                sublinear_tf=True,
                analyzer='char_wb'  # Character n-grams work better for multilingual text
            )),
            ('clf', MultinomialNB(alpha=0.1))
        ])
        
        # Train the model
        self.model.fit(texts, labels)
        self.is_trained = True
        
        # Evaluate on training data (for demonstration)
        predictions = self.model.predict(texts)
        accuracy = np.mean(predictions == labels)
        print(f"Model trained! Training accuracy: {accuracy*100:.2f}%")
        
        # Save model
        if save:
            self.save_model()
        
        return accuracy
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict if message is scam or legit
        Returns: (prediction, confidence)
        """
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        # Get prediction probabilities
        proba = self.model.predict_proba([text])[0]
        
        # Class 0 = Legit, Class 1 = Scam
        scam_confidence = proba[1]
        legit_confidence = proba[0]
        
        if scam_confidence > 0.5:
            return "Scam", scam_confidence
        else:
            return "Legit", legit_confidence
    
    def analyze(self, text: str) -> Dict:
        """
        Comprehensive analysis of message
        Returns detailed analysis including prediction and confidence
        """
        prediction, confidence = self.predict(text)
        
        return {
            "prediction": prediction,
            "confidence": float(confidence),
            "is_scam": prediction == "Scam",
            "confidence_percentage": int(confidence * 100)
        }
    
    def save_model(self):
        """Save trained model to disk"""
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model from disk"""
        try:
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            self.is_trained = True
            print(f"Model loaded from {self.model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Training new model...")
            self.train_model()
    
    def retrain_with_feedback(self, new_texts: list, new_labels: list):
        """
        Retrain model with human feedback (human-in-the-loop)
        """
        # Get existing training data
        training_data = get_training_data()
        existing_texts = [item['text'] for item in training_data]
        existing_labels = [1 if item['label'] == 'Scam' else 0 for item in training_data]
        
        # Combine with new data
        all_texts = existing_texts + new_texts
        all_labels = existing_labels + new_labels
        
        # Retrain model
        self.model.fit(all_texts, all_labels)
        self.save_model()
        
        print(f"Model retrained with {len(new_texts)} new examples")
        
        return True

# Global AI engine instance
ai_engine = None

def get_ai_engine():
    """Get or create AI engine instance"""
    global ai_engine
    if ai_engine is None:
        ai_engine = AIEngine()
    return ai_engine
