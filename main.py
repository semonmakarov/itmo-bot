# main.py
from fastapi import FastAPI, Response
from pydantic import BaseModel
from utils.llm_handler import process_query_async
import json
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class RequestData(BaseModel):
    query: str
    id: int

def parse_options(question: str) -> bool:
    """Определяет наличие вариантов ответа в вопросе"""
    return any(line.strip() and line[0].isdigit() for line in question.split('\n')[1:])

@app.post("/api/request")
async def handle_request(request_data: RequestData) -> Response:
    """Обработчик запросов с улучшенной обработкой ошибок"""
    try:
        has_options = parse_options(request_data.query)
        
        # Асинхронная обработка запроса
        llm_response = await process_query_async(
            query=request_data.query,
            query_id=request_data.id,
            has_options=has_options
        )
        
        return Response(
            content=json.dumps(llm_response, ensure_ascii=False),
            media_type="application/json; charset=utf-8"
        )
        
    except Exception as e:
        logger.error(f"Error processing request {request_data.id}: {str(e)}")
        return Response(
            content=json.dumps({
                "id": request_data.id,
                "answer": None,
                "reasoning": f"Error processing request: {str(e)}",
                "sources": []
            }, ensure_ascii=False),
            media_type="application/json; charset=utf-8",
            status_code=500
        )
