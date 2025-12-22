# Anthropic兼容API配置指南

本文档提供了在中国AI服务中使用Anthropic兼容模式的详细配置指南。

## 快速开始

### 1. 安装依赖

```bash
pip install -q -U langchain-anthropic langchain langgraph rich python-dotenv
```

⚠️ **注意**：虽然安装的是Anthropic客户端库，但中国AI服务实际上使用的是OpenAI函数格式的兼容层。

### 2. 环境变量配置

在项目根目录创建 `.env` 文件，包含以下配置：

```bash
# Anthropic兼容API配置
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic  # MiniMax
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

## 支持的服务提供商

### MiniMax

```bash
ANTHROPIC_BASE_URL=https://api.minimaxi.com/anthropic
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

### DeepSeek

```bash
ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

## 重要注意事项

⚠️ **端点区别**：Anthropic兼容端点与OpenAI兼容端点不同！

| 服务提供商 | OpenAI兼容端点 | Anthropic兼容端点 |
|-----------|----------------|------------------|
| MiniMax | `https://api.minimax.chat/v1` | `https://api.minimaxi.com/anthropic` |
| DeepSeek | `https://api.deepseek.com/v1` | `https://api.deepseek.com/anthropic` |

## 推荐的模型

### 轻量级模型（快速，适合开发测试）
- `claude-3-haiku-20240307`

### 高质量模型（适合生产环境）
- `claude-3-5-sonnet-20241022`

## 使用示例

```python
from langchain_anthropic import ChatAnthropic
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatAnthropic(
    model=os.environ.get("ANTHROPIC_MODEL", "claude-3-haiku-20240307"),
    anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
    base_url=os.environ.get("ANTHROPIC_BASE_URL"),
    temperature=0.2
)

# 使用OpenAI函数格式的结构化输出（兼容中国AI服务）
llm_with_structure = llm.with_structured_output({
    "type": "object",
    "properties": {
        "answer": {"type": "string", "description": "答案"},
        "confidence": {"type": "number", "description": "置信度"}
    },
    "title": "response",
    "description": "AI回复和置信度",
    "required": ["answer", "confidence"]
})

response = llm_with_structure.invoke("请介绍一下人工智能")
print(response)  # 直接得到结构化数据，无需JSON解析
```

⚠️ **重要说明**：中国AI服务的Anthropic兼容模式实际上使用的是OpenAI函数格式，需要包含 `title` 和 `description` 字段。

## 优势

1. **优雅的结构化输出**：自动返回结构化数据，无需手动解析JSON
2. **更好的类型安全**：自动验证返回数据格式
3. **代码更简洁**：减少错误处理代码
4. **更好的错误处理**：提供清晰的错误信息
5. **广泛兼容**：支持多种中国AI服务

## 常见问题

### Q: 为什么需要不同的端点？
A: Anthropic兼容模式需要专门的端点来处理结构化输出功能。这些端点与中国AI服务的标准OpenAI兼容端点不同。

### Q: 可以使用哪些模型？
A: 推荐使用Anthropic的模型名称，如`claude-3-haiku-20240307`或`claude-3-5-sonnet-20241022`。

### Q: API密钥可以通用吗？
A: 是的，通常您可以使用相同的API密钥，但需要确保在正确的端点上使用。

### Q: 中国AI服务真的支持Anthropic格式吗？
A: 虽然中国AI服务提供了Anthropic兼容的端点，但实际上它们使用的是OpenAI函数格式。这意味着您需要在结构化输出定义中包含 `title` 和 `description` 字段。

### Q: 为什么要使用这种混合方式？
A: 这种方式结合了Anthropic客户端库的便利性和OpenAI函数格式的兼容性，是在中国AI服务上实现优雅结构化输出的最佳实践。