# 文件转换 MCP 服务器

该 MCP 服务器提供多种文件转换工具，用于转换各种文档和图像格式。该项目基于 [Model Context Protocol（MCP）](https://modelcontextprotocol.io) 构建，旨在为需要文件转换功能的 AI 代理提供服务。

## 概述

文件转换 MCP 服务器的设计目标是：

- 通过专门的转换工具实现多种文件格式之间的转换
- 为 AI 代理通过 MCP 协议调用转换过程提供简洁的接口
- 以 Base64 编码字符串的形式返回转换后的文件

## 功能特点

- **MCP 服务器集成**：使用 MCP Python SDK（FastMCP）构建，实现标准化通信
- **多种转换工具**：针对各种转换任务的专用工具：
  - **DOCX 转 PDF**：将 Microsoft Word 文档转换为 PDF
  - **PDF 转 DOCX**：将 PDF 文档转换为 Microsoft Word 格式
  - **图像格式转换**：在各种图像格式之间转换（JPG、PNG、WebP 等）
  - **Excel 转 CSV**：将 Excel 电子表格转换为 CSV 格式
  - **HTML 转 PDF**：将 HTML 文件转换为 PDF 格式
  - **通用转换**：一个多功能工具，可处理各种格式转换
- **可扩展架构**：易于扩展，以支持更多的文件格式转换
- **错误处理**：全面的错误验证和报告机制

## 技术架构

- Python 3.x
- [Model Context Protocol（MCP）Python SDK](https://pypi.org/project/mcp/)
- 各种转换库：
  - [docx2pdf](https://pypi.org/project/docx2pdf/) - 用于 DOCX 转 PDF
  - [pdf2docx](https://pypi.org/project/pdf2docx/) - 用于 PDF 转 DOCX
  - [Pillow](https://pypi.org/project/Pillow/) - 用于图像格式转换
  - [pandas](https://pypi.org/project/pandas/) - 用于 Excel 转 CSV
  - [pdfkit](https://pypi.org/project/pdfkit/) - 用于 HTML 转 PDF

## 安装指南

1. **克隆代码仓库**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **创建虚拟环境（推荐）**

   ```bash
   python -m venv venv
   source venv/bin/activate      # Unix系统下
   venv\Scripts\activate         # Windows系统下
   ```

3. **安装依赖**

   使用 pip 安装所需包：

   ```bash
   pip install mcp docx2pdf pdf2docx pillow pandas pdfkit
   ```

   或者，如果使用 [uv](https://docs.astral.sh/uv/)：

   ```bash
   uv add "mcp[cli]" docx2pdf pdf2docx pillow pandas pdfkit
   ```

   注意：某些转换库可能有额外的系统依赖。请查阅它们的文档了解详情。

## 使用方法

### 开发模式运行服务器

测试服务器，运行以下命令：

```bash
mcp dev file_converter_server.py
```

### 安装到 Claude Desktop

可选择将服务器安装到 Claude Desktop：

```bash
mcp install file_converter_server.py --name "File Converter"
```

### API / 工具

该 MCP 服务器暴露以下工具：

#### docx2pdf
命令：`docx2pdf`
- **输入**：.docx 文件路径
- **输出**：转换后的 PDF 文件，以 Base64 编码字符串形式返回

#### pdf2docx
命令：`pdf2docx`
- **输入**：PDF 文件路径
- **输出**：转换后的 DOCX 文件，以 Base64 编码字符串形式返回

#### convert_image
命令：`convert_image`
- **输入**：
  - 图像文件路径
  - 目标格式（例如 "png"、"jpg"、"webp"）
- **输出**：转换后的图像文件，以 Base64 编码字符串形式返回

#### excel2csv
命令：`excel2csv`
- **输入**：Excel 文件路径（.xls 或 .xlsx）
- **输出**：转换后的 CSV 文件，以 Base64 编码字符串形式返回

#### html2pdf
命令：`html2pdf`
- **输入**：HTML 文件路径
- **输出**：转换后的 PDF 文件，以 Base64 编码字符串形式返回

#### convert_file（通用转换器）
命令：`convert_file`
- **输入**：
  - 输入文件路径
  - 源格式（例如 "docx"、"pdf"）
  - 目标格式（例如 "pdf"、"docx"）
- **输出**：转换后的文件，以 Base64 编码字符串形式返回

## 错误处理

- 每个工具都会验证所提供的文件是否存在并具有正确的扩展名
- 若转换过程中发生错误，将返回详细的错误信息
- 服务器优雅地处理异常并返回信息丰富的错误消息

## 贡献指南

欢迎贡献代码！请遵循以下步骤参与项目：

- Fork 本仓库
- 创建新分支，实现功能或修复 Bug
- 编写清晰、简洁且注释明确的代码
- 提交 Pull Request 前确保所有测试通过
- 若改动影响使用方式或 API，请更新本 README 文档

## 许可证

本项目采用 MIT 许可证发布，详见 [LICENSE](LICENSE) 文件。 