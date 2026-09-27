from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.rag_agent import ParkingRAGAgent

app = FastAPI(title="Parking Chatbot Stage 1", version="1.0")
agent = ParkingRAGAgent()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response_text = agent.generate_response(request.message)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)