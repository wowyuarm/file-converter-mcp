# Based on official Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libmagic1 \
        wkhtmltopdf \
        libreoffice \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install uv
RUN uv sync

# Expose port (if running a web service)
EXPOSE 8000

# Startup command (customize as needed)
CMD ["uvicorn", "file_converter_server:app", "--host", "0.0.0.0", "--port", "8000"] 