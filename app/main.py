from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router as chat_router

app = FastAPI(
    title="InfraCredit LMS Chatbot API",
    description="Backend API for General and Course-specific Chatbots",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, set this to the specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to InfraCredit LMS Chatbot API",
        "docs": "/docs",
        "endpoints": {
            "general_bot": "/api/chat/general",
            "course_bot": "/api/chat/course"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
