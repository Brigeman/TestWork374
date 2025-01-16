from pydantic import BaseModel, Field
from datetime import datetime

class TransactionCreate(BaseModel):
    transaction_id: str = Field(..., max_length=50)
    user_id: str = Field(..., max_length=50)
    amount: float
    currency: str = Field(..., max_length=10)
    timestamp: datetime