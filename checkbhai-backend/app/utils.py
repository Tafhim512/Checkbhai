import hashlib
from fastapi import Request

def get_fingerprint(request: Request) -> str:
    """
    Generate a simple SHA256 fingerprint based on IP and User-Agent.
    This allows anonymous users to see their recent history.
    """
    ip = request.client.host if request.client else "unknown"
    ua = request.headers.get("user-agent", "unknown")
    
    raw = f"{ip}|{ua}"
    return hashlib.sha256(raw.encode()).hexdigest()
