from typing import Literal

from pydantic import BaseModel, Field


class TicketTriage(BaseModel):
    category: Literal["billing", "technical", "account", "general"]
    urgency: Literal["low", "medium", "high"]
    summary: str = Field(min_length=8, max_length=180)
    next_action: str = Field(min_length=8, max_length=180)
