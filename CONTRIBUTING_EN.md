# Contributing Guidelines

Thank you for considering contributing to the File Converter MCP Server project! Here are some guidelines to help you get started.

## Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/wowyuarm/file-converter-mcp.git
   cd file-converter-mcp
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Unix/Mac
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Development Workflow

1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make changes and test:
   ```bash
   # Run the server in development mode
   mcp dev file_converter_server.py
   ```

3. Commit your changes:
   ```bash
   git add .
   git commit -m "Describe your changes"
   ```

4. Push to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```

5. Create a Pull Request

## Code Standards

- Follow PEP 8 coding standards
- Add appropriate documentation for new features
- Ensure code passes all tests

## Adding New Conversion Tools

If you want to add a new file conversion tool, follow these steps:

1. Add a new conversion function in `file_converter_server.py`
2. Register the tool using the `@mcp.tool` decorator
3. Ensure the function returns properly formatted JSON responses
4. Update the tool documentation in README.md and README_CN.md

## Reporting Issues

If you find any issues, please report them in GitHub Issues and provide the following information:

- Detailed description of the issue
- Steps to reproduce
- Expected behavior and actual behavior
- Environment information (OS, Python version, etc.)

Thank you again for your contribution! 