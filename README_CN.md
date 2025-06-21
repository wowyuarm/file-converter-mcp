# 文件转换 MCP 服务器

简体中文 | [English](README.md)

该 MCP 服务器提供多种文件转换工具，用于转换各种文档和图像格式。该项目基于 [Model Context Protocol（MCP）](https://modelcontextprotocol.io) 构建，旨在为需要文件转换功能的 AI 代理提供服务。

## 功能

  - **DOCX 转 PDF**：将 Microsoft Word 文档转换为 PDF
  - **PDF 转 DOCX**：将 PDF 文档转换为 Microsoft Word 格式
  - **图像格式转换**：在各种图像格式之间转换（JPG、PNG、WebP 等）
  - **Excel 转 CSV**：将 Excel 电子表格转换为 CSV 格式
  - **HTML 转 PDF**：将 HTML 文件转换为 PDF 格式
  - **Markdown 转 PDF**：将 Markdown 文档转换为 PDF，并应用适当的样式
  - **通用转换**：一个多功能工具，可处理各种格式转换

## 技术架构

- Python 3.10+
- [Model Context Protocol（MCP）Python SDK](https://pypi.org/project/mcp/)
- 各种转换库：
  - [docx2pdf](https://pypi.org/project/docx2pdf/) - 用于 DOCX 转 PDF
  - [pdf2docx](https://pypi.org/project/pdf2docx/) - 用于 PDF 转 DOCX
  - [Pillow](https://pypi.org/project/Pillow/) - 用于图像格式转换
  - [pandas](https://pypi.org/project/pandas/) - 用于 Excel 转 CSV
  - [pdfkit](https://pypi.org/project/pdfkit/) - 用于 HTML 转 PDF
  - [markdown](https://pypi.org/project/markdown/) - 用于 Markdown 转 HTML

## 安装指南

1. **克隆代码仓库**

   ```bash
   git clone https://github.com/wowyuarm/file-converter-mcp.git
   cd file-converter-mcp
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
   pip install mcp docx2pdf pdf2docx pillow pandas pdfkit markdown
   ```

   或者，如果使用 [uv](https://docs.astral.sh/uv/)：

   ```bash
   uv add "mcp[cli]" docx2pdf pdf2docx pillow pandas pdfkit markdown
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

#### 基于路径的工具

##### docx2pdf
命令：`docx2pdf`
- **输入**：.docx 文件路径
- **输出**：转换后的 PDF 文件，以 Base64 编码字符串形式返回

##### pdf2docx
命令：`pdf2docx`
- **输入**：PDF 文件路径
- **输出**：转换后的 DOCX 文件，以 Base64 编码字符串形式返回

##### convert_image
命令：`convert_image`
- **输入**：
  - 图像文件路径
  - 目标格式（例如 "png"、"jpg"、"webp"）
- **输出**：转换后的图像文件，以 Base64 编码字符串形式返回

##### excel2csv
命令：`excel2csv`
- **输入**：Excel 文件路径（.xls 或 .xlsx）
- **输出**：转换后的 CSV 文件，以 Base64 编码字符串形式返回

##### html2pdf
命令：`html2pdf`
- **输入**：HTML 或 Markdown 文件路径（.html、.md、.markdown）
- **输出**：转换后的 PDF 文件，以 Base64 编码字符串形式返回

##### convert_file（通用转换器）
命令：`convert_file`
- **输入**：
  - 输入文件路径
  - 源格式（例如 "docx"、"pdf"、"md"）
  - 目标格式（例如 "pdf"、"docx"）
- **输出**：转换后的文件，以 Base64 编码字符串形式返回

#### 基于内容的工具

##### convert_content（通用内容转换器）
命令：`convert_content`
- **输入**：
  - 输入文件的 Base64 编码内容
  - 源格式（例如 "docx"、"pdf"、"md"）
  - 目标格式（例如 "pdf"、"docx"）
- **输出**：转换后的文件，以 Base64 编码字符串形式返回

##### docx2pdf_content
命令：`docx2pdf_content`
- **输入**：DOCX 文件的 Base64 编码内容
- **输出**：转换后的 PDF 文件，以 Base64 编码字符串形式返回

##### pdf2docx_content
命令：`pdf2docx_content`
- **输入**：PDF 文件的 Base64 编码内容
- **输出**：转换后的 DOCX 文件，以 Base64 编码字符串形式返回

##### markdown2pdf_content
命令：`markdown2pdf_content`
- **输入**：Markdown 文件的 Base64 编码内容
- **输出**：转换后的 PDF 文件，以 Base64 编码字符串形式返回

## 文件处理

服务器包含强大的文件路径处理功能：
- 使用多阶段搜索策略查找文件
- 在常见位置（临时目录、当前目录）搜索上传的文件
- 尝试多种文件名变体（不区分大小写，带/不带扩展名）
- 提供详细日志以帮助排查文件位置问题
- 与通过 Claude 聊天界面上传的文件无缝协作
- 支持相对和绝对文件路径
- 在可能的情况下自动检测文件格式

### 直接内容转换

如果基于路径的方法失败，您可以使用基于内容的工具：
1. 将文件转换为 base64 编码
2. 使用 `*_content` 工具之一直接从文件内容进行转换
3. 这种方式可以绕过文件路径问题，在某些环境中更可靠

## 错误处理

- 每个工具都使用多种搜索策略验证文件是否存在
- 以结构化的 JSON 格式返回详细的错误信息：`{"success": false, "error": "错误信息"}`
- 成功转换返回：`{"success": true, "data": "base64编码的文件内容"}`
- 服务器包含全面的日志记录用于故障排除
- 服务器优雅地处理异常并返回信息丰富的错误消息

## 贡献指南

欢迎贡献代码！如果您想贡献，请遵循 [CONTRIBUTING.md](CONTRIBUTING.md) 中的指南（中文版：[贡献指南](CONTRIBUTING.md)，英文版：[Contributing Guidelines](CONTRIBUTING_EN.md)）。

## 许可证

本项目采用 MIT 许可证发布，详见 [LICENSE](LICENSE) 文件。

## GitHub 仓库

访问 GitHub 仓库：https://github.com/wowyuarm/file-converter-mcp 

## MCP 服务器配置

本项目可用作模型上下文协议 (MCP) 服务器，为 AI 代理提供文件转换工具。

### 快速开始

1. **安装依赖：**
   ```bash
   python -m pip install -e .
   ```

2. **启动 MCP 服务器：**
   ```bash
   python start_mcp_server.py
   ```

3. **配置你的 MCP 客户端**（如 Claude Desktop、Cursor）使用以下配置：

   **推荐配置** (`cursor-mcp.config.json`)：
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

   **替代配置** (`mcp.config.json`)：
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

### 重要说明

- **推荐使用 stdio 模式** - 这是连接 MCP 服务器最可靠的方式
- **使用 `cursor-mcp.config.json`** 获得最简单的配置
- **在从 Cursor 连接之前确保服务器正在运行**

### 可用工具

MCP 服务器提供以下工具：

- **`docx2pdf`**：将 Word 文档转换为 PDF
- **`pdf2docx`**：将 PDF 转换为 Word 文档
- **`convert_image`**：在图像格式之间转换（PNG、JPG、WEBP 等）
- **`excel2csv`**：将 Excel 文件转换为 CSV
- **`html2pdf`**：将 HTML/Markdown 转换为 PDF
- **`convert_file`**：在支持的格式之间进行通用文件转换
- **`convert_content`**：从 base64 内容转换文件

### 使用示例

配置完成后，你可以在 AI 代理中使用这些工具：

```
将此 Word 文档转换为 PDF：[上传文件]
将此图像从 PNG 转换为 JPG：[上传文件]
将此 Excel 文件转换为 CSV：[上传文件]
``` 