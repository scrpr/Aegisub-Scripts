from pydantic import BaseModel
from typing import List

class Line(BaseModel):
    speaker: str
    text: str
    id: int

class LinesModel(BaseModel):
    context: str
    keywords: str
    lines: List[Line]