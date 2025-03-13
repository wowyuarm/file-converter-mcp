"""
File Converter MCP Server

This MCP server provides multiple file conversion tools for AI Agents to use.
It supports various file format conversions such as:
- DOCX to PDF
- PDF to DOCX
- Image format conversions
- And more

The server is built using the Model Context Protocol (MCP) Python SDK.
"""

from mcp.server.fastmcp import FastMCP, Context
import os
import base64
from pathlib import Path
import tempfile
import mimetypes
import json

# Initialize MCP server
mcp = FastMCP("File Converter")

# Helper functions
def validate_file_exists(file_path: str, expected_extension: str = None) -> bool:
    """
    Validate that a file exists and optionally check its extension.
    """
    path = Path(file_path)
    if not path.exists():
        raise ValueError(f"File not found: {file_path}")
    
    if expected_extension and not file_path.lower().endswith(expected_extension.lower()):
        raise ValueError(f"File must have {expected_extension} extension, got: {file_path}")
    
    return True

def get_base64_encoded_file(file_path: str) -> str:
    """
    Read a file and return its base64 encoded content.
    """
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

def format_error_response(error_msg: str) -> dict:
    """
    Format error message as a proper JSON response.
    """
    return {
        "success": False,
        "error": str(error_msg)
    }

def format_success_response(data: str) -> dict:
    """
    Format successful response as a proper JSON response.
    """
    return {
        "success": True,
        "data": data
    }

# DOCX to PDF conversion tool
@mcp.tool("docx2pdf")
def convert_docx_to_pdf(input_file: str) -> dict:
    """
    Convert a DOCX file to PDF format.
    
    Args:
        input_file: Path to the DOCX file to convert.
        
    Returns:
        Dictionary containing success status and either base64 encoded PDF or error message.
    """
    try:
        # Validate input file
        validate_file_exists(input_file, ".docx")
        
        # Generate output file path
        output_file = os.path.splitext(input_file)[0] + ".pdf"
        
        # Import here to avoid dependency if not needed
        from docx2pdf import convert
        
        # Perform conversion
        convert(input_file, output_file)
        
        # Return base64 encoded PDF
        return format_success_response(get_base64_encoded_file(output_file))
    
    except Exception as e:
        return format_error_response(f"Error converting DOCX to PDF: {str(e)}")

# PDF to DOCX conversion tool
@mcp.tool("pdf2docx")
def convert_pdf_to_docx(input_file: str) -> dict:
    """
    Convert a PDF file to DOCX format.
    
    Args:
        input_file: Path to the PDF file to convert.
        
    Returns:
        Dictionary containing success status and either base64 encoded DOCX or error message.
    """
    try:
        # Validate input file
        validate_file_exists(input_file, ".pdf")
        
        # Generate output file path
        output_file = os.path.splitext(input_file)[0] + ".docx"
        
        # Import pdf2docx here to avoid dependency if not needed
        from pdf2docx import Converter
        
        # Perform conversion
        cv = Converter(input_file)
        cv.convert(output_file)
        cv.close()
        
        # Return base64 encoded DOCX
        return format_success_response(get_base64_encoded_file(output_file))
    
    except Exception as e:
        return format_error_response(f"Error converting PDF to DOCX: {str(e)}")

# Image format conversion tool
@mcp.tool("convert_image")
def convert_image(input_file: str, output_format: str) -> dict:
    """
    Convert an image file to another format.
    
    Args:
        input_file: Path to the image file to convert.
        output_format: Target format (e.g., "png", "jpg", "webp").
        
    Returns:
        Dictionary containing success status and either base64 encoded image or error message.
    """
    try:
        # Validate input file exists
        validate_file_exists(input_file)
        
        # Check if output format is valid
        valid_formats = ["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff"]
        if output_format.lower() not in valid_formats:
            raise ValueError(f"Unsupported output format: {output_format}. Supported formats: {', '.join(valid_formats)}")
        
        # Generate output file path
        output_file = os.path.splitext(input_file)[0] + "." + output_format.lower()
        
        # Import PIL here to avoid dependency if not needed
        from PIL import Image
        
        # Perform conversion
        img = Image.open(input_file)
        img.save(output_file)
        
        # Return base64 encoded image
        return format_success_response(get_base64_encoded_file(output_file))
    
    except Exception as e:
        return format_error_response(f"Error converting image: {str(e)}")

# Excel to CSV conversion tool
@mcp.tool("excel2csv")
def convert_excel_to_csv(input_file: str) -> dict:
    """
    Convert an Excel file (XLS/XLSX) to CSV format.
    
    Args:
        input_file: Path to the Excel file to convert.
        
    Returns:
        Dictionary containing success status and either base64 encoded CSV or error message.
    """
    try:
        # Validate input file
        if not input_file.lower().endswith(('.xls', '.xlsx')):
            raise ValueError(f"File must be an Excel file (.xls or .xlsx), got: {input_file}")
        validate_file_exists(input_file)
        
        # Generate output file path
        output_file = os.path.splitext(input_file)[0] + ".csv"
        
        # Import pandas here to avoid dependency if not needed
        import pandas as pd
        
        # Perform conversion
        df = pd.read_excel(input_file)
        df.to_csv(output_file, index=False)
        
        # Return base64 encoded CSV
        return format_success_response(get_base64_encoded_file(output_file))
    
    except Exception as e:
        return format_error_response(f"Error converting Excel to CSV: {str(e)}")

# HTML to PDF conversion tool
@mcp.tool("html2pdf")
def convert_html_to_pdf(input_file: str) -> dict:
    """
    Convert an HTML file to PDF format.
    
    Args:
        input_file: Path to the HTML file to convert.
        
    Returns:
        Dictionary containing success status and either base64 encoded PDF or error message.
    """
    try:
        # Validate input file
        validate_file_exists(input_file, ".html")
        
        # Generate output file path
        output_file = os.path.splitext(input_file)[0] + ".pdf"
        
        # Import here to avoid dependency if not needed
        import pdfkit
        
        # Perform conversion
        pdfkit.from_file(input_file, output_file)
        
        # Return base64 encoded PDF
        return format_success_response(get_base64_encoded_file(output_file))
    
    except Exception as e:
        return format_error_response(f"Error converting HTML to PDF: {str(e)}")

# Generic file conversion tool using file paths
@mcp.tool("convert_file")
def convert_file(input_file: str, input_format: str, output_format: str, ctx: Context = None) -> dict:
    """
    Generic file conversion tool that attempts to convert between various formats.
    
    Args:
        input_file: Path to the file to convert.
        input_format: Source format (e.g., "docx", "pdf").
        output_format: Target format (e.g., "pdf", "docx").
        ctx: Optional context object for progress reporting.
        
    Returns:
        Dictionary containing success status and either base64 encoded file or error message.
    """
    try:
        # Log progress if context is provided
        if ctx:
            ctx.info(f"Converting {input_file} from {input_format} to {output_format}")
        
        # Validate input file exists
        validate_file_exists(input_file)
        
        # Define conversion mapping: {(source_format, target_format): conversion_function}
        conversion_map = {
            ("docx", "pdf"): convert_docx_to_pdf,
            ("pdf", "docx"): convert_pdf_to_docx,
            # Additional format conversions can be added here
        }
        
        # Look up the appropriate conversion function
        conversion_key = (input_format.lower(), output_format.lower())
        if conversion_key in conversion_map:
            conversion_func = conversion_map[conversion_key]
            return conversion_func(input_file)
        else:
            # For image conversions
            if input_format.lower() in ["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff"]:
                return convert_image(input_file, output_format)
            
            raise ValueError(f"Unsupported conversion: {input_format} to {output_format}")
    
    except Exception as e:
        return format_error_response(f"Error converting file: {str(e)}")

if __name__ == "__main__":
    mcp.run() 