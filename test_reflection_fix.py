#!/usr/bin/env python3
"""测试反思架构修复后的工作流"""

import os
import sys
import json
from typing import List, TypedDict, Optional
from dotenv import load_dotenv

# OpenAI兼容接口和LangChain组件
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

# 用于美观的打印输出
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

# --- API密钥设置 ---
load_dotenv()

class ReflectionState(TypedDict):
    """表示我们反思图的状态。"""
    user_request: str
    draft: Optional[dict]
    critique: Optional[dict]
    refined_code: Optional[dict]

def generator_node(state):
    """生成代码的初始草稿。"""
    print("--- 1. 生成初始草稿 ---")
    # 使用兼容OpenAI API的JSON schema格式
    generator_llm = llm.with_structured_output({
        "type": "json_schema",
        "json_schema": {
            "name": "draft_code",
            "schema": {
                "type": "object",
                "properties": {
                    "code": {"type": "string", "description": "生成的用于解决用户请求的Python代码。"},
                    "explanation": {"type": "string", "description": "代码工作原理的简要说明。"}
                },
                "required": ["code", "explanation"],
                "additionalProperties": False
            }
        }
    })

    prompt = f"""你是一位Python专家程序员。编写一个Python函数来解决以下请求。
    提供一个简单、清晰的实现和说明。

    请求：{state['user_request']}

    请以JSON格式返回，包含code和explanation两个字段。"""

    draft = generator_llm.invoke(prompt)
    return {"draft": draft.content}

def critic_node(state):
    """批判生成的代码是否有错误和效率问题。"""
    print("--- 2. 批判草稿 ---")
    # 使用兼容OpenAI API的JSON schema格式
    critic_llm = llm.with_structured_output({
        "type": "json_schema",
        "json_schema": {
            "name": "critique",
            "schema": {
                "type": "object",
                "properties": {
                    "has_errors": {"type": "boolean", "description": "代码是否有潜在的错误或逻辑错误？"},
                    "is_efficient": {"type": "boolean", "description": "代码是否以高效和最优的方式编写？"},
                    "suggested_improvements": {"type": "array", "items": {"type": "string"}, "description": "改进代码的具体、可操作的建议。"},
                    "critique_summary": {"type": "string", "description": "批判的摘要。"}
                },
                "required": ["has_errors", "is_efficient", "suggested_improvements", "critique_summary"],
                "additionalProperties": False
            }
        }
    })

    code_to_critique = state['draft']['code']

    prompt = f"""你是一位专业的代码审查员和高级Python开发人员。你的任务是对以下代码进行彻底的批判。

    分析代码的以下方面：
    1.  **错误和缺陷：** 是否有任何潜在的运行时错误、逻辑缺陷或未处理的边缘情况？
    2.  **效率和最佳实践：** 这是解决问题的最有效方式吗？它是否遵循标准的Python约定（PEP 8）？

    提供结构化的批判和具体、可操作的建议。

    要审查的代码：
    ```python
    {code_to_critique}
    ```

    请以JSON格式返回，包含has_errors、is_efficient、suggested_improvements和critique_summary字段。"""

    critique = critic_llm.invoke(prompt)
    return {"critique": critique.content}

def refiner_node(state):
    """基于批判完善代码。"""
    print("--- 3. 完善代码 ---")
    # 使用兼容OpenAI API的JSON schema格式
    refiner_llm = llm.with_structured_output({
        "type": "json_schema",
        "json_schema": {
            "name": "refined_code",
            "schema": {
                "type": "object",
                "properties": {
                    "refined_code": {"type": "string", "description": "最终改进的Python代码。"},
                    "refinement_summary": {"type": "string", "description": "基于批判所做更改的摘要。"}
                },
                "required": ["refined_code", "refinement_summary"],
                "additionalProperties": False
            }
        }
    })

    draft_code = state['draft']['code']
    critique_suggestions = json.dumps(state['critique'], indent=2)

    prompt = f"""你是一位Python专家程序员，负责基于批判完善一段代码。

    你的目标是重写原始代码，实现批判中的所有建议改进。

    **原始代码：**
    ```python
    {draft_code}
    ```

    **批判和建议：**
    {critique_suggestions}

    请提供最终完善的代码和你所做更改的摘要。

    请以JSON格式返回，包含refined_code和refinement_summary字段。"""

    refined_code = refiner_llm.invoke(prompt)
    return {"refined_code": refined_code.content}

def main():
    """测试反思架构工作流"""

    # 检查API密钥
    if not os.environ.get("OPENAI_API_KEY"):
        print("❌ 错误：未找到OPENAI_API_KEY。请检查.env文件。")
        sys.exit(1)

    # 初始化LLM
    global llm
    llm = ChatOpenAI(
        model=os.environ.get("OPENAI_MODEL", "deepseek-chat"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.deepseek.com/v1"),
        api_key=os.environ.get("OPENAI_API_KEY"),
        temperature=0.2
    )

    print("✅ LLM初始化成功")

    # 构建图
    graph_builder = StateGraph(ReflectionState)
    graph_builder.add_node("generator", generator_node)
    graph_builder.add_node("critic", critic_node)
    graph_builder.add_node("refiner", refiner_node)
    graph_builder.set_entry_point("generator")
    graph_builder.add_edge("generator", "critic")
    graph_builder.add_edge("critic", "refiner")
    graph_builder.add_edge("refiner", END)

    reflection_app = graph_builder.compile()

    print("✅ 反思图编译成功")

    # 测试请求
    user_request = "编写一个Python函数来查找第n个斐波那契数。"
    initial_input = {"user_request": user_request}

    print(f"\n🚀 启动反思工作流，请求：'{user_request}'\n")

    try:
        # 运行工作流
        final_state = None
        for state_update in reflection_app.stream(initial_input, stream_mode="values"):
            final_state = state_update

        print("\n✅ 反思工作流完成！")

        # 检查结果
        if final_state and 'draft' in final_state and 'critique' in final_state and 'refined_code' in final_state:
            print("\n--- 初始草稿 ---")
            print(f"说明：{final_state['draft']['explanation']}")
            print(f"代码：\n{final_state['draft']['code']}")

            print("\n--- 批判 ---")
            print(f"摘要：{final_state['critique']['critique_summary']}")
            print("建议改进：")
            for improvement in final_state['critique']['suggested_improvements']:
                print(f"  - {improvement}")

            print("\n--- 最终完善代码 ---")
            print(f"完善摘要：{final_state['refined_code']['refinement_summary']}")
            print(f"代码：\n{final_state['refined_code']['refined_code']}")

            print("\n🎉 测试成功！反思架构工作流运行正常。")
            return True
        else:
            print("❌ 错误：final_state不完整")
            return False

    except Exception as e:
        print(f"❌ 错误：{str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)