from langgraph.graph import StateGraph, START, END
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from src.agents.schemas import ResearcherState
import pandas as pd
from src import config

class ResearchAgent:
    def __init__(self, model="gemini-1.5-flash", temperature=0):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=config.GOOGLE_API_KEY,
        )
        self.tavily_tool = TavilySearch(max_results=3, api_key=config.TAVILY_API_KEY)
        

  
    def fetch_company_info(self, company_name: str) -> str:
        """Fetch company info using Tavily API for the given company name"""
        if not company_name:
            return "No company name provided."
        results = self.tavily_tool.invoke(f"{company_name} company profile")
        return str(results)


    def summarize_insights(self, lead: dict, raw_results: str, product_context: str) -> str:
        """Summarize top 3 actionable insights for personalized cold email"""
        first_name = lead.get("firstName", "")
        last_name = lead.get("lastName", "")
        job_title = lead.get("linkedinJobTitle", "")
        company_name = lead.get("companyName", "")

        prompt = f"""
        You are a professional market researcher. 
        Lead info:

        - Name: {first_name} {last_name}
        - Job Title: {job_title}
        - Company: {company_name}
        - Location: {lead.get('location')}
        - Company Info: {raw_results}

        Product/Service we offer: {product_context}

        Summarize the top 3 actionable insights to write a personalized cold email that highlights the product benefits for this lead.
        """
        return self.llm.invoke(prompt).content

    def _research_node(self, state: ResearcherState, product_context: str = "SaaS platform for AI model deployment"):
        lead = state.lead
        company_name = lead.get("companyName", "")

        raw_results = self.fetch_company_info(company_name)
        summary = self.summarize_insights(lead, raw_results, product_context)

        return ResearcherState(
            lead=lead,
            research_summary=summary,
            raw_search_results=raw_results
        )


