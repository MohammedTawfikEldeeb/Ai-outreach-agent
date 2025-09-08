from pydantic import BaseModel, Field

class ResearcherState(BaseModel):
    lead: dict = Field(..., description="Lead information from LinkedIn")
    research_summary: str = Field(default="", description="LLM summarized insights about the lead and company")
    raw_search_results: str = Field(default="", description="Raw Tavily search results for debugging")
