import os

# Set PORT to 8000 if not set
port_str = os.getenv("PORT", "8000")
os.environ["PORT"] = port_str

try:
    port = int(port_str)
    if not (0 <= port <= 65535):
        raise ValueError
except ValueError:
    print(f"Invalid PORT: {port_str}. Must be integer between 0 and 65535.")
    exit(1)

import uvicorn
uvicorn.run("app.main:app", host="0.0.0.0", port=port)
