from typing import List
from ollama import chat, ChatResponse, Message
import time
from .logging import query_logger
_system_message = {
    "role": "system",
    "content": """You are an intelligent assistant. You have access to a vast knowledge base and a retrieval system that provides relevant information from reliable sources. Use this information to generate clear, accurate, and concise responses.  

### Instructions:
1. Combine retrieved knowledge with your understanding to answer the question comprehensively.
2. Clearly cite the sources of retrieved information, if applicable.
3. Address ambiguities by asking clarifying questions before generating a response.
4. Maintain a professional and user-friendly tone throughout.
""",
}


def _message_generator(
    history: List[Message], context: str, query: str
) -> List[Message]:
    messages: List[Message] = [_system_message]
    
    for item in history:
        messages.append(item)
    messages.append(
        {
            "role": "user",
            "content": f"""###Task:
Generate a concise answer to for the Query below based on Context.
**Context:**
```txt
{context}
```
**Query:** 
{query}
Output:""",
        }
    )
    return messages


def generate_answer(query: str, context: str, history: List[Message]):
    # Connect to LLM API (e.g., OpenAI) and generate answer
    startTime= time.time()
    response: ChatResponse = chat(
        model="qwen2.5:0.5b-instruct-fp16",
        messages=_message_generator(history=history, context=context, query=query),
    )
    answer = response["message"]["content"]
    endTime = time.time()
    query_logger(history=history, query=query,answer=answer, context=context, duration=endTime-startTime)
    return 
