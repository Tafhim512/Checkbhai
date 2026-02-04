
import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Protocol
from openai import AsyncOpenAI

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIService")

class AIProvider(Protocol):
    async def analyze_text(self, text: str) -> Optional[Dict]:
        ...
    
    @property
    def name(self) -> str:
        ...

class OpenAIProvider:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self._name = "OpenAI"

    @property
    def name(self) -> str:
        return self._name

    async def analyze_text(self, text: str) -> Optional[Dict]:
        prompt = f"""
        Analyze the following message for potential scam indicators.
        Output high-quality analysis in JSON format:
        {{
            "is_scam": boolean,
            "explanation_en": "Reason why it's a scam or legit (English)",
            "explanation_bn": "Reason why it's a scam or legit (Bangla)",
            "scam_probability": float (0-1),
            "red_flags": ["list of indicators observed"]
        }}
        Message: "{text}"
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a senior security analyst specializing in Bangladeshi fraud patterns."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                timeout=15.0
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"OpenAI analysis failed: {e}")
            return None

class GroqProvider:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        self._name = "Groq"

    @property
    def name(self) -> str:
        return self._name

    async def analyze_text(self, text: str) -> Optional[Dict]:
        prompt = f"""
        Analyze the following message for potential scam indicators.
        Output high-quality analysis in JSON format:
        {{
            "is_scam": boolean,
            "explanation_en": "Reason why it's a scam or legit (English)",
            "explanation_bn": "Reason why it's a scam or legit (Bangla)",
            "scam_probability": float (0-1),
            "red_flags": ["list of indicators observed"]
        }}
        Message: "{text}"
        """
        try:
            # Groq doesn't always support response_format="json_object" depending on model,
            # but llama-3.3-70b-versatile and 3.1-70b usually do.
            response = await self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a senior security analyst specializing in Bangladeshi fraud patterns. Always output raw JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                timeout=15.0
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"Groq analysis failed: {e}")
            return None

class AIService:
    def __init__(self):
        self.providers: List[AIProvider] = []
        
        # Initialize providers based on ENV
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and not openai_key.startswith("your-"):
            self.providers.append(OpenAIProvider(openai_key))
            logger.info("OpenAI provider initialized.")
            
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and not groq_key.startswith("your-"):
            self.providers.append(GroqProvider(groq_key))
            logger.info("Groq provider initialized.")
            
        if not self.providers:
            logger.warning("No AI providers initialized. Falling back to rules engine only.")

    async def analyze_message(self, text: str) -> Dict:
        """
        Tries providers in order. Falls back to next if one fails.
        """
        for provider in self.providers:
            logger.info(f"Attempting analysis with {provider.name}...")
            result = await provider.analyze_text(text)
            if result:
                result["provider"] = provider.name
                return result
        
        # Absolute fallback if all providers fail or are missing
        return {
            "is_scam": False, # Neutral
            "prediction": "Unknown",
            "confidence": 0.0,
            "explanation_en": "Deep AI analysis unavailable. Using basic patterns.",
            "explanation_bn": "ডিপ এআই বিশ্লেষণ পাওয়া যায়নি। বেসিক প্যাটার্ন ব্যবহার করা হচ্ছে।",
            "red_flags": [],
            "provider": "None"
        }

# Global singleton
_ai_service = None

def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
