# 更新日志

## [1.1.0] - 2025-12-22

### 新增
- 通用化API配置，支持多个OpenAI兼容的中国AI服务提供商
- 支持DeepSeek、通义千问等更多AI模型

### 改进
- 将环境变量从`MINIMAX_*`改为通用的`OPENAI_*`格式
- 更新`.env.example`文件，提供多种AI服务配置示例
- 优化README文档，包含详细的配置说明

### 修复
- 替换所有notebook中的ChatNebius引用为ChatOpenAI
- 统一使用OpenAI兼容接口

### 配置变更
```bash
# 之前
MINIMAX_API_KEY=...
MINIMAX_BASE_URL=...
MINIMAX_MODEL=...

# 现在
OPENAI_API_KEY=...
OPENAI_BASE_URL=...
OPENAI_MODEL=...
```

### 支持的AI服务
- MiniMax: `MiniMax-M2`
- DeepSeek: `deepseek-chat`
- 通义千问: `qwen-turbo`
- 其他OpenAI兼容服务
