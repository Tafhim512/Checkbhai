import asyncio
import httpx
import sys
import os

# Add parent directory to path
sys.path.insert(0, '.')

BASE_URL = "http://localhost:8000"

async def test_anon_history():
    print("Testing Anonymous History Flow...")
    
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # 1. Perform a message check as guest
        # We'll simulate a fingerprint via User-Agent and IP (actually localhost)
        headers = {"User-Agent": "Verification-Bot/1.0"}
        msg = {"message": "Looking for a job? Pay 500 TK fee to start working today!"}
        
        print(f"-> Sending message check as guest...")
        res = await client.post("/check/message", json=msg, headers=headers)
        if res.status_code != 200:
            print(f"❌ Check failed: {res.text}")
            return
        
        print(f"✓ Message checked. Risk: {res.json()['risk_level']}")
        
        # 2. Retrieve history as same guest
        print(f"-> Retrieving history...")
        res = await client.get("/history/", headers=headers)
        if res.status_code != 200:
            print(f"❌ History retrieval failed: {res.text}")
            return
            
        history = res.json()
        print(f"✓ Found {len(history)} items in history")
        
        if len(history) > 0:
            print(f"✅ PASS: Anonymous history successfully retrieved via fingerprint.")
        else:
            print(f"❌ FAIL: History empty for anonymous user.")

async def test_admin_flow():
    print("\nTesting Admin Report Flow...")
    # NOTE: This assumes an admin exists or we use internal logic
    # We will just verify the endpoint exists and returns 401/403 for now if unauth
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        res = await client.get("/admin/reports")
        if res.status_code in [401, 403]:
            print("✅ PASS: Admin endpoint is protected.")
        else:
            print(f"⚠️ Warning: Admin endpoint returned {res.status_code}")

if __name__ == "__main__":
    try:
        asyncio.run(test_anon_history())
        asyncio.run(test_admin_flow())
    except Exception as e:
        print(f"Connection Error: {e}. Is the backend running?")
