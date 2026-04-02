# This file represents Note data (can be saved to DB)
from pydantic import BaseModel

class Note(BaseModel):
    title: str
    content: str
