# This file will define your AI response models (Pydantic)
from pydantic import BaseModel

class AiResponse(BaseModel):
    answer: str
