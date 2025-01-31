from fastapi import FastAPI, Response
from pydantic import BaseModel
from utils.llm_handler import process_query
import json

app = FastAPI()

class RequestData(BaseModel):
    query: str
    id: int

def parse_options(question):
    options = []
    lines = question.split('\n')
    for line in lines[1:]:
        if line.strip() and line[0].isdigit():
            options.append(line.strip())
    return bool(options)

@app.post("/api/request")
async def handle_request(request_data: RequestData):
    try:
        has_options = parse_options(request_data.query)
        
        response_data = process_query(
            request_data.query,
            request_data.id,
            has_options
        )
        
        # Явно указываем кодировку UTF-8
        return Response(
            content=json.dumps(response_data, ensure_ascii=False),
            media_type="application/json; charset=utf-8"
        )
    
    except Exception as e:
        return Response(
            content=json.dumps({
                "id": request_data.id,
                "answer": None,
                "reasoning": f"Error processing request: {str(e)}",
                "sources": []
            }, ensure_ascii=False),
            media_type="application/json; charset=utf-8"
        )