FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir mcp[cli] docx2pdf pdf2docx pillow pandas pdfkit markdown

EXPOSE 3333

CMD ["python", "file_converter_server.py"]
