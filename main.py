from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from yt_chatbot.backend import chatbot_with_memory, update_retriever_for_url

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    input: str
    url: str

current_video_url = None

@app.post("/chat")
async def chat(request: ChatRequest):
    global current_video_url
    try:
        if request.url != current_video_url:
            update_retriever_for_url(request.url)
            current_video_url = request.url

        response = chatbot_with_memory.invoke(
            {"input": request.input},
            config={"configurable": {"session_id": "chrome_user_1"}}
        )
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)