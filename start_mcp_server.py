#!/usr/bin/env python3
"""
MCP Server Startup Script

This script provides a convenient way to start the File Converter MCP server
with proper configuration and error handling.
"""

import sys
import os
import logging
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def setup_logging():
    """Setup logging configuration for the MCP server"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Set MCP specific logging
    mcp_logger = logging.getLogger("mcp")
    mcp_logger.setLevel(logging.INFO)
    
    return logging.getLogger("file_converter_mcp")

def check_dependencies():
    """Check if all required dependencies are available"""
    try:
        import mcp
        import docx2pdf
        import pdf2docx
        from PIL import Image
        import pandas
        import pdfkit
        import markdown
        print("✓ All dependencies are available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: python -m pip install -e .")
        return False

def main():
    """Main entry point for the MCP server"""
    print("Starting File Converter MCP Server...")
    
    # Setup logging
    logger = setup_logging()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    try:
        # Import and run the MCP server
        from file_converter_server import mcp
        
        print("✓ MCP server initialized successfully")
        print("✓ Available tools:")
        print("  - docx2pdf: Convert Word documents to PDF")
        print("  - pdf2docx: Convert PDF to Word documents")
        print("  - convert_image: Convert between image formats")
        print("  - excel2csv: Convert Excel files to CSV")
        print("  - html2pdf: Convert HTML/Markdown to PDF")
        print("  - convert_file: Generic file conversion")
        print("  - convert_content: Convert from base64 content")
        print("\nStarting server...")
        
        # Run the MCP server
        mcp.run()
        
    except KeyboardInterrupt:
        print("\n✓ Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 