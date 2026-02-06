import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, '.')

from app.services.ai_service import get_ai_service

async def test_grok_integration():
    print("Testing Official Grok Integration...")
    
    # Manually set env vars for testing
    # Manually set env vars for testing (Simulated)
    # NOTE: Ensure these are set in your real environment, do not commit real keys!
    if not os.environ.get("GROK_API_KEY"):
        print("⚠️ Warning: GROK_API_KEY not found in env. Test may fail.")
    
    ai_service = get_ai_service()
    
    test_message = "Congratulations! You have won 1,000,000 BDT. Click here to claim: http://scam.link"
    
    print(f"-> Analyzing message: {test_message}")
    result = await ai_service.analyze_message(test_message)
    
    print("\n--- Grok Response ---")
    print(f"Provider: {result.get('provider')}")
    print(f"Explanation: {result.get('explanation_en')}")
    print("----------------------\n")
    
    if result.get('provider') == "Grok" and result.get('explanation_en'):
        print("✅ PASS: Grok integration works!")
    else:
        print("❌ FAIL: Grok integration failed or fell back to templates.")

if __name__ == "__main__":
    asyncio.run(test_grok_integration())
