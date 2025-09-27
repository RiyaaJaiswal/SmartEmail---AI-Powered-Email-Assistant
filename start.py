#!/usr/bin/env python3
"""
SmartEmail - AI-Powered Email Assistant
Windows-friendly startup script for cloud deployment
"""

import os
import sys
from app import create_interface

def main():
    """Main function to start the SmartEmail application"""
    try:
        # Create the Gradio interface
        interface = create_interface()
        
        # Get port from environment (Render sets this automatically)
        port = int(os.environ.get("PORT", 7860))
        
        print(f"Starting SmartEmail on port {port}")
        
        # Launch the application
        interface.launch(
            server_name="0.0.0.0",  # Allow external connections
            server_port=port,
            share=False,
            show_error=True
        )
        
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

