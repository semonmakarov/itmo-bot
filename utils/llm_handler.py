# utils/llm_handler.py
import os
import re
import aiohttp  # Переходим на асинхронные запросы
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

# Конфигурация производительности
MAX_TOKENS_RESPONSE = 150  # Ограничение длины ответа
TIMEOUT = 12  # Сокращение таймаута

async def get_llm_response(session: aiohttp.ClientSession, query: str) -> Dict:
    try:
        payload = {
            "model": "sonar-pro-chat",
            "messages": [
                {
                    "role": "system", 
                    "content": f"""Вы эксперт по Университету ИТМО. Формат ответа:
1. Номер ответа (только цифра)
2. Краткое объяснение (максимум 2 предложения)

Пример: 
2. Санкт-Петербург - правильный ответ"""
                },
                {"role": "user", "content": query}
            ],
            "max_tokens": MAX_TOKENS_RESPONSE
        }

        async with session.post(
            "https://api.perplexity.ai/chat/completions",
            json=payload,
            timeout=TIMEOUT
        ) as response:
            
            if response.status == 200:
                result = await response.json()
                return {
                    "content": result['choices'][0]['message']['content'],
                    "sources": result.get('citations', [])[:2]  # Берем только 2 источника
                }
            return {"content": "", "sources": []}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"content": "", "sources": []}

async def process_batch(queries: List[Dict]) -> List[Dict]:
    connector = aiohttp.TCPConnector(limit_per_host=10)  # Параллельные подключения
    async with aiohttp.ClientSession(
        connector=connector,
        headers={
            "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
            "Content-Type": "application/json"
        }
    ) as session:
        tasks = [process_query(session, q) for q in queries]
        return await asyncio.gather(*tasks)

async def process_query(session: aiohttp.ClientSession, query_data: Dict) -> Dict:
    response = await get_llm_response(session, query_data["question"])
    
    # Оптимизированное извлечение ответа
    answer = re.findall(r'\b\d+', response["content"])
    return {
        "id": query_data["id"],
        "answer": int(answer[0]) if answer else None,
        "reasoning": " ".join(response["content"].split(". ")[:2]),  # Первые 2 предложения
        "sources": response["sources"]
    }

def extract_answer_number(text: str) -> int:
    match = re.search(r'\b([1-4])\b', text)
    return int(match.group(1)) if match else None
