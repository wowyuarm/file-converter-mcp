# File Converter MCP Server

[![Python Tests](https://github.com/yourusername/file-converter-mcp/actions/workflows/python-test.yml/badge.svg)](https://github.com/yourusername/file-converter-mcp/actions/workflows/python-test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

This MCP server provides multiple file conversion tools for converting various document and image formats. This project is built using the [Model Context Protocol (MCP)](https://modelcontextprotocol.io) and is designed to serve AI agents that need file conversion capabilities.

## Overview

The File Converter MCP Server is designed to:

- Convert between multiple file formats using specialized conversion tools
- Provide a simple interface for AI agents to invoke the conversion process via the MCP protocol
- Return the converted files as Base64 encoded strings

## Features

- **MCP Server Integration**: Built using the MCP Python SDK (FastMCP) for standardized communication
- **Multiple Conversion Tools**: Specialized tools for various conversion tasks:
  - **DOCX to PDF**: Convert Microsoft Word documents to PDF
  - **PDF to DOCX**: Convert PDF documents to Microsoft Word format
  - **Image Format Conversion**: Convert between various image formats (JPG, PNG, WebP, etc.)
  - **Excel to CSV**: Convert Excel spreadsheets to CSV format
  - **HTML to PDF**: Convert HTML files to PDF format
  - **Generic Conversion**: A versatile tool that attempts to handle various format conversions
- **Extensible Architecture**: Easily extendable to support additional file format conversions
- **Error Handling**: Comprehensive error validation and reporting

## Technologies

- Python 3.x
- [Model Context Protocol (MCP) Python SDK](https://pypi.org/project/mcp/)
- Various conversion libraries:
  - [docx2pdf](https://pypi.org/project/docx2pdf/) - for DOCX to PDF conversion
  - [pdf2docx](https://pypi.org/project/pdf2docx/) - for PDF to DOCX conversion
  - [Pillow](https://pypi.org/project/Pillow/) - for image format conversions
  - [pandas](https://pypi.org/project/pandas/) - for Excel to CSV conversion
  - [pdfkit](https://pypi.org/project/pdfkit/) - for HTML to PDF conversion

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/file-converter-mcp.git
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
   pip install mcp docx2pdf pdf2docx pillow pandas pdfkit
   ```

   Alternatively, if you are using [uv](https://docs.astral.sh/uv/):

   ```bash
   uv add "mcp[cli]" docx2pdf pdf2docx pillow pandas pdfkit
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

#### docx2pdf
Command: `docx2pdf`
- **Input**: Path to a .docx file
- **Output**: Base64 encoded string of the converted PDF file

#### pdf2docx
Command: `pdf2docx`
- **Input**: Path to a PDF file
- **Output**: Base64 encoded string of the converted DOCX file

#### convert_image
Command: `convert_image`
- **Input**: 
  - Path to an image file
  - Target format (e.g., "png", "jpg", "webp")
- **Output**: Base64 encoded string of the converted image

#### excel2csv
Command: `excel2csv`
- **Input**: Path to an Excel file (.xls or .xlsx)
- **Output**: Base64 encoded string of the converted CSV file

#### html2pdf
Command: `html2pdf`
- **Input**: Path to an HTML file
- **Output**: Base64 encoded string of the converted PDF file

#### convert_file (Generic Converter)
Command: `convert_file`
- **Input**: 
  - Path to the input file
  - Source format (e.g., "docx", "pdf")
  - Target format (e.g., "pdf", "docx")
- **Output**: Base64 encoded string of the converted file

## Error Handling

- Each tool validates that the provided file exists and has the correct extension
- Detailed error messages are returned in case of any conversion failures
- The server gracefully handles exceptions and returns informative error messages

## Contributing

Contributions are welcome! If you'd like to contribute, please follow the guidelines in [CONTRIBUTING.md](CONTRIBUTING.md) (中文版: [贡献指南](CONTRIBUTING.md), English: [Contributing Guidelines](CONTRIBUTING_EN.md)).

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

## GitHub Repository

Visit the GitHub repository at: https://github.com/yourusername/file-converter-mcp 