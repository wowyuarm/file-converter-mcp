# 贡献指南

感谢您考虑为文件转换 MCP 服务器项目做出贡献！以下是一些指导原则，帮助您参与这个项目。

## 开发环境设置

1. 克隆仓库：
   ```bash
   git clone https://github.com/wowyuarm/file-converter-mcp.git
   cd file-converter-mcp
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Unix/Mac
   source .venv/bin/activate
   ```

3. 安装依赖：
   ```bash
   pip install -e .
   ```

## 开发流程

1. 创建新分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 进行更改并测试：
   ```bash
   # 在开发模式下运行服务器
   mcp dev file_converter_server.py
   ```

3. 提交更改：
   ```bash
   git add .
   git commit -m "描述你的更改"
   ```

4. 推送到 GitHub：
   ```bash
   git push origin feature/your-feature-name
   ```

5. 创建 Pull Request

## 代码规范

- 遵循 PEP 8 编码规范
- 为新功能添加适当的文档
- 确保代码通过所有测试

## 添加新的转换工具

如果您想添加新的文件转换工具，请遵循以下步骤：

1. 在 `file_converter_server.py` 中添加新的转换函数
2. 使用 `@mcp.tool` 装饰器注册工具
3. 确保函数返回格式正确的 JSON 响应
4. 更新 README.md 和 README_CN.md 中的工具文档

## 报告问题

如果您发现任何问题，请在 GitHub Issues 中报告，并提供以下信息：

- 问题的详细描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（操作系统、Python 版本等）

再次感谢您的贡献！ 