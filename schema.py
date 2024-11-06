# schema.py
from pydantic import BaseModel
from typing import Optional

class TransactionBase(BaseModel):
    type: str
    amount: float
    description: Optional[str] = None

    class Config:
        orm_mode = True
