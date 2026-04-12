from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.openai_service import get_openai_service, OpenAIService
from app.services.lms_service import get_lms_client, LMSClient

router = APIRouter()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    response: str

@router.post("/general", response_model=ChatResponse)
async def general_chat(
    request: ChatRequest, 
    openai_service: OpenAIService = Depends(get_openai_service),
    lms_client: LMSClient = Depends(get_lms_client)
):
    try:
        messages = [m.model_dump() for m in request.messages]
        # General bot consumes EVERYTHING: LMS Data + Internal KB
        response_text = await openai_service.chat(messages, bot_type="general", lms_client=lms_client)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/course", response_model=ChatResponse)
async def course_chat(
    request: ChatRequest, 
    openai_service: OpenAIService = Depends(get_openai_service),
    lms_client: LMSClient = Depends(get_lms_client)
):
    try:
        messages = [m.model_dump() for m in request.messages]
        # Course bot consumes ONLY LMS Course data
        response_text = await openai_service.chat(messages, bot_type="course", lms_client=lms_client)
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
