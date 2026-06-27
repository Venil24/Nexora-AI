"""
backend/run.py
Application entry point. Start the Flask development server.
Usage: python backend/run.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("FLASK_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True") == "True"

    print("=" * 50)
    print("  Nexora-AI Backend Server")
    print(f"  Running on: http://localhost:{port}")
    print(f"  Debug mode: {debug}")
    print("=" * 50)

    app.run(host="0.0.0.0", port=port, debug=debug)
