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
import glob
import logging
import sys
import time
import traceback

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("file_converter_mcp")

# Initialize MCP server
mcp = FastMCP("File Converter")

# Helper functions
def validate_file_exists(file_path: str, expected_extension: str = None) -> str:
    """
    Validate that a file exists and optionally check its extension.
    Returns the actual file path that exists.
    """
    logger.info(f"Looking for file: {file_path}")
    
    # First check if the file exists as is
    path = Path(file_path)
    if path.exists():
        logger.info(f"Found file at original path: {file_path}")
        # Check extension if needed
        if expected_extension and not file_path.lower().endswith(expected_extension.lower()):
            raise ValueError(f"File must have {expected_extension} extension, got: {file_path}")
        return file_path

    # Get the filename and possible variations
    filename = os.path.basename(file_path)
    filename_no_ext = os.path.splitext(filename)[0]
    possible_filenames = [
        filename,  # Original filename
        filename.lower(),  # Lowercase version
        filename.upper(),  # Uppercase version
    ]
    
    # If an extension is expected, add variants with that extension
    if expected_extension:
        for name in list(possible_filenames):  # Create a copy to iterate over
            name_no_ext = os.path.splitext(name)[0]
            possible_filenames.append(f"{name_no_ext}{expected_extension}")
            possible_filenames.append(f"{name_no_ext}{expected_extension.lower()}")
    
    # Add wildcard pattern for files with similar names (ignoring case)
    for name in list(possible_filenames):
        name_no_ext = os.path.splitext(name)[0]
        possible_filenames.append(f"{name_no_ext}.*")
    
    logger.info(f"Looking for file variations: {possible_filenames}")
    
    # Places to search
    search_locations = []
    
    # Current directory and subdirectories (recursive)
    search_locations.append(".")
    
    # Temp directories
    temp_dir = tempfile.gettempdir()
    search_locations.append(temp_dir)
    
    # Common upload directories
    for common_dir in ['/tmp', './uploads', '/var/tmp', '/var/upload', os.path.expanduser('~/tmp'), os.path.expanduser('~/Downloads')]:
        if os.path.exists(common_dir):
            search_locations.append(common_dir)
    
    # Claude specific upload locations (based on observation)
    claude_dirs = ['./claude_uploads', './uploads', './input', './claude_files', '/tmp/claude']
    for claude_dir in claude_dirs:
        if os.path.exists(claude_dir):
            search_locations.append(claude_dir)
    
    logger.info(f"Searching in locations: {search_locations}")
    
    # Gather all files in these locations
    all_files = []
    for location in search_locations:
        logger.info(f"Searching in: {location}")
        # First try direct match
        for name in possible_filenames:
            if "*" not in name:  # Skip wildcard patterns for direct match
                potential_path = os.path.join(location, name)
                if os.path.exists(potential_path):
                    logger.info(f"Found direct match: {potential_path}")
                    all_files.append(potential_path)
        
        # Then try recursive search with wildcard patterns
        try:
            for name in possible_filenames:
                pattern = os.path.join(location, "**", name)
                matches = glob.glob(pattern, recursive=True)
                if matches:
                    logger.info(f"Found matches for pattern {pattern}: {matches}")
                    all_files.extend(matches)
        except Exception as e:
            logger.warning(f"Error during recursive search in {location}: {str(e)}")
    
    # Log all the files found
    logger.info(f"All found files: {all_files}")
    
    # If we found matches, use the most likely one
    if all_files:
        # Prioritize exact matches
        for file in all_files:
            if os.path.basename(file) == filename:
                logger.info(f"Selected exact match: {file}")
                return file
        
        # If no exact match, use the first file found
        actual_path = all_files[0]
        logger.info(f"Selected first match: {actual_path}")
        
        # Check extension if needed
        if expected_extension and not actual_path.lower().endswith(expected_extension.lower()):
            logger.warning(f"File doesn't have expected extension {expected_extension}: {actual_path}")
            # Let's be flexible and NOT raise an error here, just log a warning
            # raise ValueError(f"File must have {expected_extension} extension, got: {actual_path}")
        
        return actual_path
    
    # Special case for Claude: try to use a simple glob in the current directory
    try:
        # This is a common pattern in Claude uploads - it adds random numbers
        last_resort_patterns = [
            f"*{filename}*",  # Anything containing the filename
            f"*{filename_no_ext}*.*",  # Anything containing the filename without extension
        ]
        
        for pattern in last_resort_patterns:
            logger.info(f"Trying last resort pattern: {pattern}")
            matches = glob.glob(pattern)
            if matches:
                logger.info(f"Found last resort matches: {matches}")
                for match in matches:
                    if os.path.isfile(match):
                        if expected_extension and not match.lower().endswith(expected_extension.lower()):
                            logger.warning(f"Last resort file doesn't have expected extension {expected_extension}: {match}")
                            # Be flexible here too
                        logger.info(f"Selected last resort file: {match}")
                        return match
    except Exception as e:
        logger.warning(f"Error during last resort search: {str(e)}")
    
    # If we reach here, we couldn't find the file
    error_msg = f"File not found: {file_path}. Searched in multiple locations with various filename patterns."
    logger.error(error_msg)
    raise ValueError(error_msg)

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
    # Ensure returning a pure dictionary without any prefix
    return {
        "success": False,
        "error": str(error_msg)
    }

def format_success_response(data: str) -> dict:
    """
    Format successful response as a proper JSON response.
    """
    # Ensure returning a pure dictionary without any prefix
    return {
        "success": True,
        "data": data
    }

# Custom JSON encoder to ensure all responses are valid JSON
class SafeJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder that safely handles various types.
    """
    def default(self, obj):
        try:
            return super().default(obj)
        except TypeError:
            # For objects that cannot be serialized, convert to string
            return str(obj)

# 修改debug_json_response函数
def debug_json_response(response):
    """
    Debug JSON response to ensure it's valid.
    """
    try:
        # 使用自定义编码器确保所有响应都是有效的JSON
        json_str = json.dumps(response, cls=SafeJSONEncoder)
        json.loads(json_str)  # 验证JSON是否有效
        logger.info(f"Valid JSON response: {json_str[:100]}...")
        return response
    except Exception as e:
        logger.error(f"Invalid JSON response: {str(e)}")
        logger.error(f"Response type: {type(response)}")
        logger.error(f"Response content: {str(response)[:100]}...")
        # 返回一个安全的错误响应
        return {"success": False, "error": "Internal server error: Invalid JSON response"}

# Enhanced JSON parsing
original_parse_json = mcp.parse_json if hasattr(mcp, 'parse_json') else None

def enhanced_parse_json(text):
    """Enhanced JSON parsing with detailed error information"""
    try:
        # Check if there's a non-JSON prefix
        if text and not text.strip().startswith('{') and not text.strip().startswith('['):
            # Try to find the start of JSON
            json_start = text.find('{')
            if json_start == -1:
                json_start = text.find('[')
            
            if json_start > 0:
                logger.warning(f"Found non-JSON prefix: '{text[:json_start]}'")
                text = text[json_start:]
                logger.info(f"Stripped prefix, new text: '{text[:100]}...'")
        
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        logger.error(f"Problematic string: '{text}'")
        logger.error(f"Position {e.pos}: {text[max(0, e.pos-10):e.pos]}[HERE>{text[e.pos:e.pos+1]}<HERE]{text[e.pos+1:min(len(text), e.pos+10)]}")
        logger.error(f"Full error: {traceback.format_exc()}")
        raise

# If mcp has parse_json attribute, replace it
if hasattr(mcp, 'parse_json'):
    mcp.parse_json = enhanced_parse_json
else:
    logger.warning("Cannot enhance JSON parsing, mcp object doesn't have parse_json attribute")

# DOCX to PDF conversion tool
@mcp.tool("docx2pdf")
def convert_docx_to_pdf(input_file: str = None, file_content_base64: str = None) -> dict:
    """
    Convert a DOCX file to PDF format. Supports both file path and direct file content input.
    
    Args:
        input_file: Path to the DOCX file to convert. Optional if providing file_content_base64.
        file_content_base64: Base64 encoded content of the DOCX file. Optional if providing input_file.
        
    Returns:
        Dictionary containing success status and either base64 encoded PDF or error message.
    """
    try:
        logger.info(f"Starting DOCX to PDF conversion")
        logger.info(f"Received parameters: input_file={input_file}, file_content_base64={'[BASE64 content]' if file_content_base64 else 'None'}")
        
        # Log more debug information
        if input_file:
            logger.info(f"Input file type: {type(input_file)}")
            logger.info(f"Input file length: {len(input_file) if isinstance(input_file, str) else 'not a string'}")
            logger.info(f"Input file first 20 chars: {input_file[:20] if isinstance(input_file, str) else 'not a string'}")
        
        # Validate that at least one input method is provided
        if input_file is None and file_content_base64 is None:
            logger.error("No input provided: both input_file and file_content_base64 are None")
            return debug_json_response(format_error_response("You must provide either input_file or file_content_base64"))
        
        # Create temporary directory for processing files
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Create a unique filename with timestamp
        temp_input_file = os.path.join(temp_dir, f"input_{int(time.time())}.docx")
        temp_output_file = os.path.join(temp_dir, f"output_{int(time.time())}.pdf")
        
        # Handle direct content mode
        if file_content_base64:
            logger.info("Using direct content mode (base64 input)")
            try:
                # Decode base64 content
                file_content = base64.b64decode(file_content_base64)
                
                # Write to temporary file
                with open(temp_input_file, "wb") as f:
                    f.write(file_content)
                logger.info(f"Successfully wrote input file from base64: {temp_input_file}")
                
                # Set actual file path to our temporary file
                actual_file_path = temp_input_file
            except Exception as e:
                logger.error(f"Failed to decode or write base64 input: {str(e)}")
                return debug_json_response(format_error_response(f"Error processing input file content: {str(e)}"))
                
        # Handle file path mode
        else:
            logger.info(f"Using file path mode with input: {input_file}")
            
            # List files in current directory for debugging
            try:
                current_files = os.listdir(".")
                logger.info(f"Files in current directory: {current_files}")
            except Exception as e:
                logger.warning(f"Error listing files in current directory: {str(e)}")
            
            # Try to locate the file
            try:
                actual_file_path = validate_file_exists(input_file, ".docx")
                logger.info(f"File validated, using path: {actual_file_path}")
            except Exception as e:
                logger.error(f"File validation error: {str(e)}")
                
                # Clean up temp directory before returning
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass
                    
                return debug_json_response(format_error_response(f"Error finding DOCX file: {str(e)}"))
        
        # Import docx2pdf here to avoid dependency if not needed
        try:
            from docx2pdf import convert
            logger.info("Successfully imported docx2pdf")
        except ImportError as e:
            logger.error(f"Failed to import docx2pdf: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response("Error importing docx2pdf library. Please ensure it's installed."))
        
        # Perform conversion
        logger.info(f"Starting conversion from {actual_file_path} to {temp_output_file}")
        try:
            convert(actual_file_path, temp_output_file)
            logger.info("Conversion completed successfully")
        except Exception as e:
            logger.error(f"Conversion error: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Error during DOCX to PDF conversion: {str(e)}"))
        
        # Verify the output file exists
        if not os.path.exists(temp_output_file):
            logger.error(f"Output file not found after conversion: {temp_output_file}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Conversion failed: Output file not found"))
        
        # Return base64 encoded PDF
        logger.info("Encoding PDF file as base64")
        try:
            encoded_data = get_base64_encoded_file(temp_output_file)
            logger.info("Successfully encoded PDF file")
            
            # Clean up temp directory
            try:
                import shutil
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory: {str(e)}")
                
            return debug_json_response(format_success_response(encoded_data))
        except Exception as e:
            logger.error(f"Error encoding PDF file: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Error reading converted PDF file: {str(e)}"))
    
    except Exception as e:
        logger.error(f"Unexpected error in convert_docx_to_pdf: {str(e)}")
        return debug_json_response(format_error_response(f"Error converting DOCX to PDF: {str(e)}"))

# PDF to DOCX conversion tool
@mcp.tool("pdf2docx")
def convert_pdf_to_docx(input_file: str = None, file_content_base64: str = None) -> dict:
    """
    Convert a PDF file to DOCX format. Supports both file path and direct file content input.
    
    Args:
        input_file: Path to the PDF file to convert. Optional if providing file_content_base64.
        file_content_base64: Base64 encoded content of the PDF file. Optional if providing input_file.
        
    Returns:
        Dictionary containing success status and either base64 encoded DOCX or error message.
    """
    try:
        logger.info(f"Starting PDF to DOCX conversion")
        
        # Validate that at least one input method is provided
        if input_file is None and file_content_base64 is None:
            logger.error("No input provided: both input_file and file_content_base64 are None")
            return debug_json_response(format_error_response("You must provide either input_file or file_content_base64"))
        
        # Create temporary directory for processing files
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Create a unique filename with timestamp
        temp_input_file = os.path.join(temp_dir, f"input_{int(time.time())}.pdf")
        temp_output_file = os.path.join(temp_dir, f"output_{int(time.time())}.docx")
        
        # Handle direct content mode
        if file_content_base64:
            logger.info("Using direct content mode (base64 input)")
            try:
                # Decode base64 content
                file_content = base64.b64decode(file_content_base64)
                
                # Write to temporary file
                with open(temp_input_file, "wb") as f:
                    f.write(file_content)
                logger.info(f"Successfully wrote input file from base64: {temp_input_file}")
                
                # Set actual file path to our temporary file
                actual_file_path = temp_input_file
            except Exception as e:
                logger.error(f"Failed to decode or write base64 input: {str(e)}")
                
                # Clean up temp directory before returning
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass
                    
                return debug_json_response(format_error_response(f"Error processing input file content: {str(e)}"))
                
        # Handle file path mode
        else:
            logger.info(f"Using file path mode with input: {input_file}")
            
            # Try to locate the file
            try:
                actual_file_path = validate_file_exists(input_file, ".pdf")
                logger.info(f"File validated, using path: {actual_file_path}")
            except Exception as e:
                logger.error(f"File validation error: {str(e)}")
                
                # Clean up temp directory before returning
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass
                    
                return debug_json_response(format_error_response(f"Error finding PDF file: {str(e)}"))
        
        # Import pdf2docx here to avoid dependency if not needed
        try:
            from pdf2docx import Converter
            logger.info("Successfully imported pdf2docx")
        except ImportError as e:
            logger.error(f"Failed to import pdf2docx: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response("Error importing pdf2docx library. Please ensure it's installed."))
        
        # Perform conversion
        logger.info(f"Starting conversion from {actual_file_path} to {temp_output_file}")
        try:
            cv = Converter(actual_file_path)
            cv.convert(temp_output_file)
            cv.close()
            logger.info("Conversion completed successfully")
        except Exception as e:
            logger.error(f"Conversion error: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Error during PDF to DOCX conversion: {str(e)}"))
        
        # Verify the output file exists
        if not os.path.exists(temp_output_file):
            logger.error(f"Output file not found after conversion: {temp_output_file}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Conversion failed: Output file not found"))
        
        # Return base64 encoded DOCX
        logger.info("Encoding DOCX file as base64")
        try:
            encoded_data = get_base64_encoded_file(temp_output_file)
            logger.info("Successfully encoded DOCX file")
            
            # Clean up temp directory
            try:
                import shutil
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory: {str(e)}")
                
            return debug_json_response(format_success_response(encoded_data))
        except Exception as e:
            logger.error(f"Error encoding DOCX file: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Error reading converted DOCX file: {str(e)}"))
    
    except Exception as e:
        logger.error(f"Unexpected error in convert_pdf_to_docx: {str(e)}")
        return debug_json_response(format_error_response(f"Error converting PDF to DOCX: {str(e)}"))

# Image format conversion tool
@mcp.tool("convert_image")
def convert_image(input_file: str = None, file_content_base64: str = None, output_format: str = None, input_format: str = None) -> dict:
    """
    Convert an image file to another format. Supports both file path and direct file content input.
    
    Args:
        input_file: Path to the image file to convert. Optional if providing file_content_base64.
        file_content_base64: Base64 encoded content of the image file. Optional if providing input_file.
        output_format: Target format (e.g., "png", "jpg", "webp").
        input_format: Source format (e.g., "png", "jpg"). Only required when using file_content_base64.
        
    Returns:
        Dictionary containing success status and either base64 encoded image or error message.
    """
    try:
        logger.info(f"Starting image conversion to {output_format}")
        
        # Validate that at least one input method is provided
        if input_file is None and file_content_base64 is None:
            logger.error("No input provided: both input_file and file_content_base64 are None")
            return debug_json_response(format_error_response("You must provide either input_file or file_content_base64"))
            
        # Check if output format is valid
        valid_formats = ["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff"]
        if not output_format or output_format.lower() not in valid_formats:
            logger.error(f"Invalid output format: {output_format}")
            return debug_json_response(format_error_response(f"Unsupported output format: {output_format}. Supported formats: {', '.join(valid_formats)}"))
        
        # Create temporary directory for processing files
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Created temporary directory: {temp_dir}")
        
        # Handle direct content mode
        if file_content_base64:
            logger.info("Using direct content mode (base64 input)")
            
            # Need input format when using content mode
            if not input_format:
                logger.error("input_format is required when using file_content_base64")
                
                # Clean up temp directory before returning
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass
                    
                return debug_json_response(format_error_response("input_format is required when using file_content_base64"))
                
            # Create a unique filename with timestamp
            temp_input_file = os.path.join(temp_dir, f"input_{int(time.time())}.{input_format.lower()}")
            temp_output_file = os.path.join(temp_dir, f"output_{int(time.time())}.{output_format.lower()}")
            
            try:
                # Decode base64 content
                file_content = base64.b64decode(file_content_base64)
                
                # Write to temporary file
                with open(temp_input_file, "wb") as f:
                    f.write(file_content)
                logger.info(f"Successfully wrote input file from base64: {temp_input_file}")
                
                # Set actual file path to our temporary file
                actual_file_path = temp_input_file
            except Exception as e:
                logger.error(f"Failed to decode or write base64 input: {str(e)}")
                
                # Clean up temp directory before returning
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass
                    
                return debug_json_response(format_error_response(f"Error processing input file content: {str(e)}"))
                
        # Handle file path mode
        else:
            logger.info(f"Using file path mode with input: {input_file}")
            
            # Try to locate the file
            try:
                actual_file_path = validate_file_exists(input_file)
                logger.info(f"File validated, using path: {actual_file_path}")
                
                # Detect input format from file extension if not explicitly provided
                if not input_format:
                    input_format = os.path.splitext(actual_file_path)[1].lstrip('.')
                    logger.info(f"Detected input format from file extension: {input_format}")
                
                # Create output file path
                temp_output_file = os.path.join(temp_dir, f"output_{int(time.time())}.{output_format.lower()}")
            except Exception as e:
                logger.error(f"File validation error: {str(e)}")
                
                # Clean up temp directory before returning
                try:
                    import shutil
                    shutil.rmtree(temp_dir)
                except:
                    pass
                    
                return debug_json_response(format_error_response(f"Error finding input image file: {str(e)}"))
        
        # Import PIL here to avoid dependency if not needed
        try:
            from PIL import Image
            logger.info("Successfully imported PIL")
        except ImportError as e:
            logger.error(f"Failed to import PIL: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response("Error importing PIL library. Please ensure pillow is installed."))
        
        # Perform conversion
        logger.info(f"Starting image conversion from {actual_file_path} to {temp_output_file}")
        try:
            img = Image.open(actual_file_path)
            
            # Handle special cases for certain formats
            if output_format.lower() in ['jpg', 'jpeg']:
                # Convert to RGB if saving as JPEG (removes alpha channel)
                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    logger.info("Converting image to RGB for JPEG output")
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)
                    img = background
            
            img.save(temp_output_file)
            logger.info("Conversion completed successfully")
        except Exception as e:
            logger.error(f"Conversion error: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Error during image conversion: {str(e)}"))
        
        # Verify the output file exists
        if not os.path.exists(temp_output_file):
            logger.error(f"Output file not found after conversion: {temp_output_file}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Conversion failed: Output file not found"))
        
        # Return base64 encoded image
        logger.info("Encoding output image as base64")
        try:
            encoded_data = get_base64_encoded_file(temp_output_file)
            logger.info("Successfully encoded output image")
            
            # Clean up temp directory
            try:
                import shutil
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary directory: {str(e)}")
                
            return debug_json_response(format_success_response(encoded_data))
        except Exception as e:
            logger.error(f"Error encoding output image: {str(e)}")
            
            # Clean up temp directory before returning
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass
                
            return debug_json_response(format_error_response(f"Error reading converted image file: {str(e)}"))
    
    except Exception as e:
        logger.error(f"Unexpected error in convert_image: {str(e)}")
        return debug_json_response(format_error_response(f"Error converting image: {str(e)}"))

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
        actual_file_path = validate_file_exists(input_file)
        
        # Generate output file path
        output_file = os.path.splitext(actual_file_path)[0] + ".csv"
        
        # Import pandas here to avoid dependency if not needed
        import pandas as pd
        
        # Perform conversion
        df = pd.read_excel(actual_file_path)
        df.to_csv(output_file, index=False)
        
        # Return base64 encoded CSV
        return debug_json_response(format_success_response(get_base64_encoded_file(output_file)))
    
    except Exception as e:
        return debug_json_response(format_error_response(f"Error converting Excel to CSV: {str(e)}"))

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
        # Validate input file - for HTML, be more flexible with extensions
        # since we might be handling Markdown files too
        actual_file_path = validate_file_exists(input_file)
        
        # Determine if this is Markdown and convert to HTML first if needed
        if actual_file_path.lower().endswith(('.md', '.markdown')):
            # Import markdown module if needed
            try:
                import markdown
                with open(actual_file_path, 'r', encoding='utf-8') as md_file:
                    md_content = md_file.read()
                
                html_content = markdown.markdown(md_content)
                
                # Create a temporary HTML file
                html_temp = os.path.splitext(actual_file_path)[0] + '.temp.html'
                with open(html_temp, 'w', encoding='utf-8') as html_file:
                    html_file.write(f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <title>Converted Markdown</title>
                        <style>
                            body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                            h1, h2, h3, h4, h5, h6 {{ color: #333; margin-top: 24px; }}
                            code {{ background-color: #f0f0f0; padding: 2px 4px; border-radius: 3px; }}
                            pre {{ background-color: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }}
                            blockquote {{ border-left: 4px solid #ddd; padding-left: 16px; margin-left: 0; }}
                            img {{ max-width: 100%; }}
                            table {{ border-collapse: collapse; width: 100%; }}
                            th, td {{ border: 1px solid #ddd; padding: 8px; }}
                            tr:nth-child(even) {{ background-color: #f2f2f2; }}
                        </style>
                    </head>
                    <body>
                        {html_content}
                    </body>
                    </html>
                    """)
                
                actual_file_path = html_temp
            except ImportError:
                raise ValueError("Markdown conversion requires the 'markdown' module. Please install it with 'pip install markdown'")
        
        # Generate output file path
        output_file = os.path.splitext(os.path.splitext(actual_file_path)[0])[0] + ".pdf"
        if actual_file_path.endswith('.temp.html'):
            output_file = os.path.splitext(os.path.splitext(actual_file_path)[0])[0] + ".pdf"
        
        # Import here to avoid dependency if not needed
        import pdfkit
        
        # Perform conversion
        pdfkit.from_file(actual_file_path, output_file)
        
        # Remove temporary file if it was created
        if actual_file_path.endswith('.temp.html'):
            try:
                os.remove(actual_file_path)
            except:
                pass
        
        # Return base64 encoded PDF
        return debug_json_response(format_success_response(get_base64_encoded_file(output_file)))
    
    except Exception as e:
        return debug_json_response(format_error_response(f"Error converting HTML to PDF: {str(e)}"))

# Generic file conversion tool using file paths
@mcp.tool("convert_file")
def convert_file(input_file: str = None, file_content_base64: str = None, input_format: str = None, output_format: str = None, ctx: Context = None) -> dict:
    """
    Generic file conversion tool that attempts to convert between various formats.
    Supports both file path and direct file content input.
    
    Args:
        input_file: Path to the file to convert. Optional if providing file_content_base64.
        file_content_base64: Base64 encoded content of the file. Optional if providing input_file.
        input_format: Source format (e.g., "docx", "pdf", "png").
        output_format: Target format (e.g., "pdf", "docx", "jpg").
        ctx: Optional context object for progress reporting.
        
    Returns:
        Dictionary containing success status and either base64 encoded file or error message.
    """
    try:
        # Log progress if context is provided
        if ctx:
            ctx.info(f"Converting from {input_format} to {output_format}")
        
        logger.info(f"Starting generic file conversion from {input_format} to {output_format}")
        
        # Validate that at least one input method is provided
        if input_file is None and file_content_base64 is None:
            logger.error("No input provided: both input_file and file_content_base64 are None")
            return debug_json_response(format_error_response("You must provide either input_file or file_content_base64"))
            
        # Check that formats are specified
        if not input_format or not output_format:
            logger.error(f"Missing format specification: input_format={input_format}, output_format={output_format}")
            return debug_json_response(format_error_response("You must specify both input_format and output_format"))
            
        # Define conversion mapping: {(source_format, target_format): conversion_function}
        conversion_map = {
            ("docx", "pdf"): convert_docx_to_pdf,
            ("pdf", "docx"): convert_pdf_to_docx,
            ("markdown", "pdf"): convert_html_to_pdf,
            ("md", "pdf"): convert_html_to_pdf,
            # Additional format conversions can be added here
        }
            
        # Look up the appropriate conversion function
        conversion_key = (input_format.lower(), output_format.lower())
        if conversion_key in conversion_map:
            # Call the specific conversion function with the correct parameters
            conversion_func = conversion_map[conversion_key]
            
            # Check if the function accepts file_content_base64 parameter (our updated ones do)
            if file_content_base64:
                return conversion_func(file_content_base64=file_content_base64)
            else:
                return conversion_func(input_file=input_file)
        else:
            # For image conversions
            if input_format.lower() in ["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff"]:
                if file_content_base64:
                    return convert_image(
                        file_content_base64=file_content_base64,
                        input_format=input_format,
                        output_format=output_format
                    )
                else:
                    return convert_image(
                        input_file=input_file,
                        output_format=output_format
                    )
            
            # If we got here, the conversion is not supported
            logger.error(f"Unsupported conversion: {input_format} to {output_format}")
            return debug_json_response(format_error_response(f"Unsupported conversion: {input_format} to {output_format}"))
    
    except Exception as e:
        logger.error(f"Unexpected error in convert_file: {str(e)}")
        return debug_json_response(format_error_response(f"Error converting file: {str(e)}"))

# Function to handle direct file content input
@mcp.tool("convert_content")
def convert_content(file_content_base64: str, input_format: str, output_format: str) -> dict:
    """
    Convert a file directly from its base64 content, without needing a file path.
    This is useful when the file path approach fails or when working with content
    directly from the chat.
    
    Args:
        file_content_base64: Base64 encoded content of the input file
        input_format: Source format (e.g., "docx", "pdf", "md")
        output_format: Target format (e.g., "pdf", "docx")
        
    Returns:
        Dictionary containing success status and either base64 encoded file or error message.
    """
    try:
        logger.info(f"Starting direct content conversion from {input_format} to {output_format}")
        
        # We can now directly use convert_file with file_content_base64
        return convert_file(
            file_content_base64=file_content_base64,
            input_format=input_format,
            output_format=output_format
        )
    
    except Exception as e:
        logger.error(f"Unexpected error in convert_content: {str(e)}")
        return debug_json_response(format_error_response(f"Error converting content: {str(e)}"))

# Direct DOCX to PDF conversion with content
@mcp.tool("docx2pdf_content")
def convert_docx_to_pdf_content(file_content_base64: str) -> dict:
    """
    Convert a DOCX file directly from its base64 content to PDF format.
    
    Args:
        file_content_base64: Base64 encoded content of the DOCX file
        
    Returns:
        Dictionary containing success status and either base64 encoded PDF or error message.
    """
    result = convert_docx_to_pdf(file_content_base64=file_content_base64)
    return debug_json_response(result)

# Direct PDF to DOCX conversion with content
@mcp.tool("pdf2docx_content")
def convert_pdf_to_docx_content(file_content_base64: str) -> dict:
    """
    Convert a PDF file directly from its base64 content to DOCX format.
    
    Args:
        file_content_base64: Base64 encoded content of the PDF file
        
    Returns:
        Dictionary containing success status and either base64 encoded DOCX or error message.
    """
    result = convert_pdf_to_docx(file_content_base64=file_content_base64)
    return debug_json_response(result)

# Direct Markdown to PDF conversion with content
@mcp.tool("markdown2pdf_content")
def convert_markdown_to_pdf_content(file_content_base64: str) -> dict:
    """
    Convert a Markdown file directly from its base64 content to PDF format.
    
    Args:
        file_content_base64: Base64 encoded content of the Markdown file
        
    Returns:
        Dictionary containing success status and either base64 encoded PDF or error message.
    """
    result = convert_file(file_content_base64=file_content_base64, input_format="md", output_format="pdf")
    return debug_json_response(result)

if __name__ == "__main__":
    mcp.run() 