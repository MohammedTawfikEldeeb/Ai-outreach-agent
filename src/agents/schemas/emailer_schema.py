from pydantic import BaseModel , Field
from typing import Optional , Dict
from src.agents.schemas import WriterState

class EmailerState(WriterState):
    filled_template: Optional[str] = Field(default=None, description="Email template after filling placeholders")
    final_email: Optional[str] = Field(None, description="The final email to send")
    sender_profile: Optional[Dict] = Field(default=None, description="Synthetic or real sender profile")
