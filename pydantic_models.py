from pydantic import BaseModel

class Note(BaseModel):
    name: str
    description: str
    created_by:str
    priority: int
