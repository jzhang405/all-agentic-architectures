# 智能体架构 - 中文版

本项目已将所有Python notebook从使用外国AI服务本地化为使用中国AI服务，特别适配Minimax API。

## 已完成的notebook

### 1. 反思架构 (01_reflection.ipynb)
- **功能**: 演示智能体如何自我批判和完善输出
- **架构**: 生成 → 批判 → 完善
- **技术**: 使用Minimax模型进行代码生成和批判

### 2. 工具使用架构 (02_tool_use.ipynb)
- **功能**: 演示智能体如何使用外部工具
- **架构**: 思考 → 行动 → 观察
- **技术**: 集成网络搜索工具和Minimax模型

### 3. ReAct架构 (03_ReAct.ipynb)
- **功能**: 演示推理与行动结合的多步问题解决
- **架构**: 迭代的思考-行动-观察循环
- **技术**: 对比基本工具使用与高级ReAct模式

## 快速开始

### 1. 安装依赖
```bash
pip install -q -U langchain-openai langchain langgraph rich python-dotenv requests
```

### 2. 配置API密钥
1. 复制 `.env.example` 为 `.env`
2. 在 `.env` 文件中填入您的API密钥：
```bash
# 选择以下任一AI服务提供商：
# MiniMax
OPENAI_API_KEY=your_minimax_api_key_here
OPENAI_BASE_URL=https://api.minimax.chat/v1
OPENAI_MODEL=MiniMax-M2

# 或者 DeepSeek
# OPENAI_API_KEY=your_deepseek_api_key_here
# OPENAI_BASE_URL=https://api.deepseek.com/v1
# OPENAI_MODEL=deepseek-chat

# 或者 通义千问
# OPENAI_API_KEY=your_qwen_api_key_here
# OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
# OPENAI_MODEL=qwen-turbo
```

### 3. 运行notebook
- 在Jupyter或VS Code中打开任何notebook
- 确保 `.env` 文件与notebook在同一目录
- 按顺序执行单元格

## 配置说明

### 环境变量
- `OPENAI_API_KEY`: 必需，您的OpenAI兼容API密钥
- `OPENAI_BASE_URL`: 可选，API端点（默认：https://api.minimax.chat/v1）
- `OPENAI_MODEL`: 可选，模型名称（默认：MiniMax-M2）

### 支持的模型
项目已测试以下OpenAI兼容的中国AI模型：
- `MiniMax-M2` (MiniMax)
- `deepseek-chat` (DeepSeek)
- `qwen-turbo` (通义千问)
- 其他OpenAI兼容的中国AI模型（通过调整BASE_URL和MODEL）

## 技术特点

### 优势
- ✅ 完全本地化，适合中国网络环境
- ✅ 使用Minimax等可靠的中国AI服务
- ✅ 保持原有的架构逻辑和功能
- ✅ 支持灵活配置不同AI模型

### 架构模式
每个notebook演示一个核心智能体架构：
1. **反思**: 自我改进和错误纠正
2. **工具使用**: 外部信息获取
3. **ReAct**: 动态多步推理

## 故障排除

### 常见问题

**Q: API调用失败**
A: 检查：
1. `.env` 文件是否正确配置
2. API密钥是否有效
3. 网络连接是否正常

**Q: 模型不响应**
A: 尝试：
1. 降低temperature参数
2. 检查模型名称是否正确
3. 验证API端点URL

**Q: 依赖包冲突**
A: 解决方案：
1. 创建新的虚拟环境
2. 使用 `--upgrade` 参数安装最新版本

## 扩展使用

### 添加新工具
参考 `02_tool_use.ipynb` 中的 `WebSearchTool` 类实现。

### 更换AI模型
或者直接修改`.env`文件中的配置：
```bash
# 更换为DeepSeek
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# 更换为通义千问
OPENAI_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
OPENAI_MODEL=qwen-turbo
```

### 自定义工作流
基于LangGraph的架构，可以轻松修改和扩展智能体行为。

## 贡献

欢迎提交Issue和Pull Request来改进项目。

## 许可证

本项目采用与原项目相同的许可证。

---

**注意**: 本项目仅供学习和研究使用。请遵守相关AI服务提供商的使用条款。
