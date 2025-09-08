from pydantic import BaseModel, Field
from src.agents.schemas import ResearcherState
from typing import Optional
class WriterState(ResearcherState):
    draft_email: str = Field(default="", description="Drafted personalized email")
    email_template: Optional[str] = Field(default=None, description="The email template with placeholders")
