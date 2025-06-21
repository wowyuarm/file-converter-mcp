# File Converter MCP Server

[简体中文](README_CN.md) | English

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

This MCP server provides multiple file conversion tools for converting various document and image formats. This project is built using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) and is designed to serve AI agents that need file conversion capabilities.

## Features

  - **DOCX to PDF**: Convert Microsoft Word documents to PDF
  - **PDF to DOCX**: Convert PDF documents to Microsoft Word format
  - **Image Format Conversion**: Convert between various image formats (JPG, PNG, WebP, etc.)
  - **Excel to CSV**: Convert Excel spreadsheets to CSV format
  - **HTML to PDF**: Convert HTML files to PDF format
  - **Markdown to PDF**: Convert Markdown documents to PDF with proper styling
  - **Generic Conversion**: A versatile tool that attempts to handle various format conversions

## Technologies

- Python 3.10+
- [Model Context Protocol (MCP) Python SDK](https://pypi.org/project/mcp/)
- Various conversion libraries:
  - [docx2pdf](https://pypi.org/project/docx2pdf/) - for DOCX to PDF conversion
  - [pdf2docx](https://pypi.org/project/pdf2docx/) - for PDF to DOCX conversion
  - [Pillow](https://pypi.org/project/Pillow/) - for image format conversions
  - [pandas](https://pypi.org/project/pandas/) - for Excel to CSV conversion
  - [pdfkit](https://pypi.org/project/pdfkit/) - for HTML to PDF conversion
  - [markdown](https://pypi.org/project/markdown/) - for Markdown to HTML conversion

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/wowyuarm/file-converter-mcp.git
   cd file-converter-mcp
   ```

2. **Create a Virtual Environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Unix-based systems
   venv\Scripts\activate         # On Windows
   ```

3. **Install Dependencies**

   Install the required packages using pip:

   ```bash
   pip install mcp docx2pdf pdf2docx pillow pandas pdfkit markdown
   ```

   Alternatively, if you are using [uv](https://docs.astral.sh/uv/):

   ```bash
   uv add "mcp[cli]" docx2pdf pdf2docx pillow pandas pdfkit markdown
   ```

   Note: Some conversion libraries may have additional system dependencies. Please check their documentation for details.

## Usage

### Running the Server in Development Mode

To test the server, run:

```bash
mcp dev file_converter_server.py
```

### Installing for Claude Desktop

Optionally, you can install the server on Claude Desktop with:

```bash
mcp install file_converter_server.py --name "File Converter"
```

### API / Tools

The MCP server exposes the following tools:

#### Path-Based Tools (Also Support Content Input)

##### docx2pdf
Command: `docx2pdf`
- **Input Option 1**: Path to a .docx file
  ```
  input_file: path/to/document.docx
  ```
- **Input Option 2**: Base64 encoded content of the DOCX file
  ```
  file_content_base64: [base64 encoded string]
  ```
- **Output**: Base64 encoded string of the converted PDF file

##### pdf2docx
Command: `pdf2docx`
- **Input Option 1**: Path to a PDF file
  ```
  input_file: path/to/document.pdf
  ```
- **Input Option 2**: Base64 encoded content of the PDF file
  ```
  file_content_base64: [base64 encoded string]
  ```
- **Output**: Base64 encoded string of the converted DOCX file

##### convert_image
Command: `convert_image`
- **Input Option 1**: 
  ```
  input_file: path/to/image.png
  output_format: jpg
  ```
- **Input Option 2**:
  ```
  file_content_base64: [base64 encoded string]
  input_format: png
  output_format: jpg
  ```
- **Output**: Base64 encoded string of the converted image

##### excel2csv
Command: `excel2csv`
- **Input**: Path to an Excel file (.xls or .xlsx)
- **Output**: Base64 encoded string of the converted CSV file

##### html2pdf
Command: `html2pdf`
- **Input**: Path to an HTML or Markdown file (.html, .md, .markdown)
- **Output**: Base64 encoded string of the converted PDF file

##### convert_file (Generic Converter)
Command: `convert_file`
- **Input Option 1**: 
  ```
  input_file: path/to/file.docx
  input_format: docx
  output_format: pdf
  ```
- **Input Option 2**:
  ```
  file_content_base64: [base64 encoded string]
  input_format: docx
  output_format: pdf
  ```
- **Output**: Base64 encoded string of the converted file

#### Content-Based Tools (Legacy)

These are maintained for backward compatibility. All main tools now support content-based input directly.

##### convert_content (Generic Content Converter)
Command: `convert_content`
- **Input**:
  - Base64 encoded content of the input file
  - Source format (e.g., "docx", "pdf", "md")
  - Target format (e.g., "pdf", "docx")
- **Output**: Base64 encoded string of the converted file

##### docx2pdf_content
Command: `docx2pdf_content`
- **Input**: Base64 encoded content of the DOCX file
- **Output**: Base64 encoded string of the converted PDF file

##### pdf2docx_content
Command: `pdf2docx_content`
- **Input**: Base64 encoded content of the PDF file
- **Output**: Base64 encoded string of the converted DOCX file

##### markdown2pdf_content
Command: `markdown2pdf_content`
- **Input**: Base64 encoded content of the Markdown file
- **Output**: Base64 encoded string of the converted PDF file

## File Handling

The server includes robust file path handling that:
- Uses a multi-stage search strategy to find files
- Searches for uploaded files in common locations (temp directories, current directory)
- Tries multiple filename variations (case-insensitive, with/without extensions)
- Provides detailed logs to help troubleshoot file location issues
- Works seamlessly with files uploaded via Claude chat interface
- Supports relative and absolute file paths
- Automatically detects file formats when possible

### Dual-Mode Input

All conversion tools now support two methods of input:

1. **Path-Based Conversion** (traditional approach)
   ```
   @File Converter
   docx2pdf
   input_file: file.docx
   ```

2. **Content-Based Conversion** (works even when path lookup fails)
   ```
   @File Converter
   docx2pdf
   file_content_base64: [base64 encoded string]
   ```

This dual-mode approach provides maximum flexibility and reliability:
- When in doubt, use content-based input for guaranteed processing
- All intermediate files are created with unique names in temporary directories
- Temporary files are automatically cleaned up after processing

### Handling Claude-Specific File Uploads

When using with Claude, if a file upload fails to be found:

1. Try using the original filename with a preceding path:
   ```
   @File Converter
   docx2pdf
   input_file: /tmp/file.docx
   ```

2. If that fails, obtain the file content directly from Claude:
   ```
   @File Converter
   docx2pdf
   file_content_base64: [base64 content obtained from Claude]
   ```

## Error Handling

- Each tool validates file existence using multiple search strategies
- Detailed error messages are returned in a structured JSON format: `{"success": false, "error": "error message"}`
- Successful conversions return: `{"success": true, "data": "base64 encoded file content"}`
- The server includes comprehensive logging for troubleshooting
- The server gracefully handles exceptions and returns informative error messages

## Contributing

Contributions are welcome! If you'd like to contribute, please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md) (中文版: [贡献指南](CONTRIBUTING.md), English: [Contributing Guidelines](CONTRIBUTING_EN.md)).

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## GitHub Repository

Visit the GitHub repository at: https://github.com/wowyuarm/file-converter-mcp

## MCP Server Configuration

This project can be used as a Model Context Protocol (MCP) server, providing file conversion tools to AI agents.

### Quick Start

1. **Install dependencies:**
   ```bash
   python -m pip install -e .
   ```

2. **Start the MCP server:**
   ```bash
   python start_mcp_server.py
   ```

3. **Configure your MCP client** (e.g., Claude Desktop, Cursor) with the following configuration:

   **Recommended configuration** (`cursor-mcp.config.json`):
   ```json
   {
     "mcpServers": {
       "file-converter": {
         "command": "python",
         "args": ["file_converter_server.py"],
         "cwd": "."
       }
     }
   }
   ```

   **Alternative configuration** (`mcp.config.json`):
   ```json
   {
     "mcpServers": {
       "file-converter": {
         "command": "python",
         "args": ["file_converter_server.py"],
         "cwd": "."
       }
     }
   }
   ```

### Important Notes

- **stdio mode is recommended** - This is the most reliable way to connect MCP servers
- **Use `cursor-mcp.config.json`** for the simplest configuration
- **Make sure the server is running** before connecting from Cursor

### Available Tools

The MCP server provides the following tools:

- **`docx2pdf`**: Convert Word documents to PDF
- **`pdf2docx`**: Convert PDF to Word documents  
- **`convert_image`**: Convert between image formats (PNG, JPG, WEBP, etc.)
- **`excel2csv`**: Convert Excel files to CSV
- **`html2pdf`**: Convert HTML/Markdown to PDF
- **`convert_file`**: Generic file conversion between supported formats
- **`convert_content`**: Convert files from base64 content

### Usage Examples

Once configured, you can use the tools in your AI agent:

```
Convert this Word document to PDF: [upload file]
Convert this image from PNG to JPG: [upload file]
Convert this Excel file to CSV: [upload file]
``` 