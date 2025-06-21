# Dependency Management Guide

## Project Dependencies

This project uses the following main dependencies:

- `mcp[cli]` - MCP (Model Context Protocol) server framework
- `docx2pdf` - Word document to PDF conversion
- `pdf2docx` - PDF to Word document conversion
- `pillow` - Image processing library
- `pandas` - Data processing library
- `pdfkit` - HTML to PDF conversion
- `markdown` - Markdown processing

## Package Managers

The project supports two package managers:

### 1. uv (Recommended)

The project uses `uv` as the primary package manager with configuration files:
- `pyproject.toml` - Project configuration and dependency declarations
- `uv.lock` - Lock file to ensure dependency version consistency

Install dependencies:
```bash
# Install uv
pip install uv

# Sync dependencies
uv sync

# Run the project
uv run python file_converter_server.py
```

### 2. pip

You can also use traditional pip installation:

```bash
# Install project dependencies
pip install -e .

# Run the project
python file_converter_server.py
```

## Dependency Testing

Run the dependency test script:
```bash
python test_dependencies.py
```

## Common Issues

### 1. ModuleNotFoundError: No module named 'pillow'

**Cause**: Pillow package not correctly installed or incorrect import method

**Solution**:
- Ensure correct import method: `from PIL import Image`
- Reinstall dependencies: `pip install -e .` or `uv sync`
- Check if `"pillow"` is included in `pyproject.toml` dependencies

### 2. GitHub Workflows Failure

**Cause**: Dependency installation issues in CI/CD environment

**Solution**:
- The project provides two Workflows configurations:
  - `.github/workflows/python-test.yml` - Using uv
  - `.github/workflows/python-test-pip.yml` - Using pip
- Ensure all dependencies are correctly declared in `pyproject.toml`

### 3. System-level Dependencies

Some packages may require system-level dependencies:

- `pdfkit` requires `wkhtmltopdf`
- `docx2pdf` requires Microsoft Word on Windows
- `docx2pdf` requires Pages or LibreOffice on macOS

## Development Environment Setup

1. Clone the project
2. Install uv: `pip install uv`
3. Sync dependencies: `uv sync`
4. Run tests: `uv run python test_dependencies.py`
5. Start server: `uv run python file_converter_server.py`

## Updating Dependencies

```bash
# Using uv
uv add <package_name>
uv sync

# Using pip
pip install <package_name>
pip freeze > requirements.txt  # if needed
``` 