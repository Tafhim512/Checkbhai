
import os
import json
import asyncio
import logging
from typing import Dict, List, Optional, Protocol
import httpx # Use httpx for direct API calls if needed, or openai SDK

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIService")

class AIProvider(Protocol):
    async def analyze_text(self, text: str) -> Optional[Dict]:
        ...
    
    @property
    def name(self) -> str:
        ...

class GrokProvider:
    """
    Official xAI Grok Provider
    """
    def __init__(self, api_key: str, api_url: str = "https://api.grok.openai.com/v1"):
        self.api_key = api_key
        self.api_url = api_url
        self._name = "Grok (xAI)"

    @property
    def name(self) -> str:
        return self._name

    async def analyze_text(self, text: str) -> Optional[Dict]:
        prompt = f"""
        Analyze the following message for potential scam indicators.
        Output high-quality analysis in JSON format:
        {{
            "explanation_en": "Clear explanation of why this is a scam or safe (English)",
            "explanation_bn": "Clear explanation of why this is a scam or safe (Bangla)",
            "red_flags": ["list of indicators observed"]
        }}
        Message: "{text}"
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Grok Beta API payload structure (OpenAI compatible)
        payload = {
            "model": "grok-beta", 
            "messages": [
                {"role": "system", "content": "You are a senior security analyst specializing in Bangladeshi fraud patterns. Output raw JSON."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions", # Adjust based on actual base URL usage
                    json=payload,
                    headers=headers
                )
                
                if response.status_code != 200:
                    logger.error(f"Grok API Error {response.status_code}: {response.text}")
                    return None
                    
                data = response.json()
                content = data['choices'][0]['message']['content']
                
                # Strip markdown blocks if present
                if "```json" in content:
                    content = content.replace("```json", "").replace("```", "")
                
                return json.loads(content)

        except Exception as e:
            logger.error(f"Grok analysis failed: {e}")
            return None

class AIService:
    def __init__(self):
        self.provider: Optional[AIProvider] = None
        
        # Load Grok Configuration
        grok_key = os.getenv("GROK_API_KEY")
        grok_url = os.getenv("GROK_API_URL", "https://api.x.ai/v1")
        
        if grok_key:
            self.provider = GrokProvider(grok_key, grok_url)
            logger.info("✓ Grok provider initialized")
        else:
            logger.warning("⚠ GROK_API_KEY not found. AI features disabled.")

    async def analyze_message(self, text: str) -> Dict:
        """
        Analyzes message using Grok.
        """
        if not self.provider:
            return self._get_fallback_response()

        logger.info(f"Attempting analysis with {self.provider.name}...")
        result_text = await self.provider.analyze_text(text)
        
        if result_text:
            return {
                "explanation_en": result_text.get("explanation_en"),
                "explanation_bn": result_text.get("explanation_bn"),
                "provider": self.provider.name,
                "red_flags": result_text.get("red_flags", [])
            }
        
        return self._get_fallback_response()

    def _get_fallback_response(self):
        return {
            "explanation_en": "Analysis completed using pattern matching (AI unavailable).",
            "explanation_bn": "প্যাটার্ন ম্যাচিং ব্যবহার করে বিশ্লেষণ সম্পন্ন হয়েছে (AI অফলাইন)।",
            "provider": "None",
            "red_flags": []
        }

_ai_service = None

def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
