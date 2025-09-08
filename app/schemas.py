# app/schemas.py

from pydantic import BaseModel
from typing import List, Optional

class CampaignResult(BaseModel):
    id: int
    first_name: Optional[str] = None
    company_name: Optional[str] = None
    generated_email: Optional[str] = None
    status: str
    sim_opened: Optional[bool] = None
    sim_clicked: Optional[bool] = None
    sim_replied: Optional[bool] = None

class Kpis(BaseModel):
    total_processed: int
    successful_emails: int
    success_rate_percent: float
    open_rate_percent: float
    click_through_rate_percent: float
    reply_rate_percent: float