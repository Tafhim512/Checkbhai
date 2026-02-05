import os
import json
import httpx
import logging
from typing import Dict, List, Optional, Protocol

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIService")

class GrokProvider:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self._name = "Grok"

    @property
    def name(self) -> str:
        return self._name

    async def analyze_text(self, text: str) -> Optional[str]:
        """
        Custom Grok API implementation.
        Format: {"message": "<user prompt>"}
        Returns: Raw text response from Grok
        """
        prompt = f"Analyze this message for scams and explain the indicators found. Language: English and Bangla. Message: {text}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "message": prompt
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.api_url,
                    json=payload,
                    headers=headers
                )
                
                if response.status_code == 200:
                    # Return only the response from Grok as text
                    # Support both raw text, {"message": "..."}, and {"response": "..."}
                    try:
                        res_data = response.json()
                        if isinstance(res_data, str):
                            return res_data
                        if isinstance(res_data, dict):
                            return (res_data.get("message") or 
                                    res_data.get("response") or 
                                    res_data.get("text") or 
                                    str(res_data))
                        return str(res_data)
                    except:
                        # If not JSON, return raw text as requested
                        return response.text
                else:
                    logger.error(f"Grok API error {response.status_code}: {response.text}")
                    return None
        except Exception as e:
            logger.error(f"Grok request failed: {e}")
            return None

class AIService:
    def __init__(self):
        self.provider: Optional[GrokProvider] = None
        
        # Load specific environment variables for Grok
        # Official API URL requested by user
        grok_url = os.getenv("GROK_API_URL", "https://api.grok.openai.com/v1")
        # Official API Key provided by user (via ENV)
        grok_key = os.getenv("GROK_API_KEY")
        
        logger.info(f"ENV Status: GROK_API_KEY present: {bool(grok_key)}")
        
        if grok_key and grok_url:
            self.provider = GrokProvider(grok_url, grok_key)
            logger.info(f"✓ Official Grok provider initialized at {grok_url}")
        else:
            logger.warning("⚠ GROK_API_KEY or GROK_API_URL missing. Using fallback templates.")

    async def analyze_message(self, text: str) -> Dict:
        """
        Uses Grok to generate an explanation only.
        """
        if not self.provider:
            return self._get_fallback_response()

        logger.info(f"Attempting analysis with {self.provider.name}...")
        result_text = await self.provider.analyze_text(text)
        
        if result_text:
            return {
                "explanation_en": result_text,
                "provider": self.provider.name,
                "red_flags": [] # Rules engine will handle flags
            }
        
        return self._get_fallback_response()

    def _get_fallback_response(self) -> Dict:
        return {
            "is_scam": False,
            "prediction": "Unknown",
            "confidence": 0.0,
            "explanation_en": None, # Will trigger template fallback in check.py
            "explanation_bn": None,
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
