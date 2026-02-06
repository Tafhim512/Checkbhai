import os
import json
import logging
from typing import Dict, List, Optional

# LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.runnables import RunnablePassthrough

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AIService")

# Set up LangSmith tracing - Ensure defaults are sensible
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "checkbhai-backend")

class LangChainAIService:
    """AI Service using LangChain with LangSmith tracing"""

    def __init__(self):
        self.llm = None
        self.chain = None
        self.is_available = False

        # Initialize LangChain components
        self._initialize_langchain()

    def _initialize_langchain(self):
        """Initialize LangChain components with graceful fallback"""
        try:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                logger.warning("OPENAI_API_KEY not found - AI analysis disabled")
                return

            # Initialize ChatOpenAI with LangChain
            self.llm = ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.1,  # Lower temperature for more consistent, stable results
                max_tokens=1000,
                api_key=openai_api_key
            )

            # Create prompt template for risk analysis
            # ALIGNED WITH CORE PRINCIPLES: No "scammer", "fraud", or "fake" analysis.
            prompt_template = ChatPromptTemplate.from_messages([
                ("system", """You are CheckBhai, a risk assessment assistant specializing in identifying suspicious communication patterns in Bangladesh.
Your goal is to provide evidence-based risk analysis. 

CORE RULES:
- Never use terms like "scammer", "fraud", or "guilty".
- Everything must be risk-based and evidence-based.
- Do not make absolute verdicts. Use "High Risk", "Medium Risk", or "Low Risk".
- Focus on observable "Red Flags".
- Be stable and predictable. No hallucinated predictions.

Analyze for:
- Advance payment requests (bKash, Nagad, etc.)
- Artificial urgency pressure
- Unrealistic guarantees
- Requests for sensitive personal info (OTP, PIN)
- Impersonation of officials or brands
"""),
                ("user", """Analyze this communication for potential risk indicators:

Message: "{text}"

Respond with a JSON object containing:
{{
    "is_high_risk": boolean,
    "risk_level": "Low|Medium|High",
    "confidence_score": float (0-1),
    "explanation_en": "Evidence-based explanation in English",
    "explanation_bn": "তথ্য-ভিত্তিক ব্যাখ্যা বাংলায়",
    "red_flags": ["list", "of", "observable", "indicators"],
    "category": "payment|job|investment|impersonation|other"
}}""")
            ])

            # Create chain with JSON output parser
            self.chain = prompt_template | self.llm | JsonOutputParser()
            self.is_available = True

            logger.info("✓ LangChain AI Service initialized with LangSmith tracing (Principles Aligned)")

        except Exception as e:
            logger.error(f"Failed to initialize LangChain AI Service: {e}")
            self.is_available = False

    async def analyze_message(self, text: str) -> Dict:
        """
        Analyze message using LangChain with LangSmith tracing
        """
        if not self.is_available or not self.chain:
            logger.warning("AI Service not available - returning fallback response")
            return self._get_fallback_response()

        try:
            logger.info(f"Analyzing message with LangChain: {text[:50]}...")

            # Run chain with tracing
            result = await self.chain.ainvoke({"text": text})

            # Ensure required fields are present and terminology is mapped correctly
            result.setdefault("risk_level", "Low")
            result.setdefault("confidence_score", 0.5)
            result.setdefault("explanation_en", "Analysis based on message patterns.")
            result.setdefault("explanation_bn", "বার্তার প্যাটার্ন ভিত্তিক বিশ্লেষণ।")
            result.setdefault("red_flags", [])
            result.setdefault("category", "other")
            
            # Map for backward compatibility if needed by other modules
            result["is_scam"] = result.get("risk_level") == "High"
            result["confidence"] = result.get("confidence_score", 0.5)

            logger.info(f"AI Analysis completed - Risk: {result.get('risk_level', 'Unknown')}")
            return result

        except Exception as e:
            logger.error(f"LangChain analysis failed: {e}")
            return self._get_fallback_response()

    def _get_fallback_response(self) -> Dict:
        """Fallback response when AI is unavailable"""
        return {
            "is_scam": False,
            "risk_level": "Low",
            "confidence": 0.0,
            "confidence_score": 0.0,
            "explanation_en": "AI analysis currently unavailable. Purely rule-based analysis applied.",
            "explanation_bn": "AI বিশ্লেষণ বর্তমানে অনুপলব্ধ। শুধুমাত্র নিয়ম-ভিত্তিক বিশ্লেষণ প্রয়োগ করা হয়েছে।",
            "red_flags": [],
            "category": "other",
            "provider": "fallback"
        }

    def analyze_sync(self, text: str) -> Dict:
        """Synchronous wrapper for legacy compatibility"""
        import asyncio
        import threading

        def run_in_new_loop(coro):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                return loop.run_until_complete(coro)
            finally:
                loop.close()

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Use a thread for sync call if loop is running
                from concurrent.futures import ThreadPoolExecutor
                with ThreadPoolExecutor() as executor:
                    future = executor.submit(run_in_new_loop, self.analyze_message(text))
                    return future.result()
            else:
                return loop.run_until_complete(self.analyze_message(text))
        except (RuntimeError, Exception) as e:
            # Fallback for sync
            return asyncio.run(self.analyze_message(text))

# Global singleton
_ai_service = None

def get_ai_service() -> LangChainAIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = LangChainAIService()
    return _ai_service
