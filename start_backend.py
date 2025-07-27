#!/usr/bin/env python3
"""
Simple script to start the AI Shopping Assistant backend server.
"""

import subprocess
import sys
import os

def main():
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    try:
        os.chdir(backend_dir)
        print("Starting AI Shopping Assistant backend server...")
        print("Backend will be available at: http://localhost:8000")
        print("API documentation: http://localhost:8000/docs")
        print("\nPress Ctrl+C to stop the server\n")
        
        # Start the server
        subprocess.run([sys.executable, "main.py"], check=True)
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except FileNotFoundError:
        print("Error: Backend directory not found. Make sure you're in the project root.")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()