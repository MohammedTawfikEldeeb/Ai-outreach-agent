from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from src.agents.schemas import WriterState
from src import config

class WriterAgent:
    def __init__(self, model="gemini-1.5-flash", temperature=0):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=temperature,
            google_api_key=config.GOOGLE_API_KEY
        )
       

    def draft_email(self, lead: dict, research_summary: str, product_context: str) -> str:
        """Generate a personalized cold email for a lead using research insights and product context"""
        first_name = lead.get("firstName", "")
        company_name = lead.get("companyName", "")
        
        prompt = f"""
        You are a professional copywriter specialized in B2B SaaS outreach. 
        Write a **concise, engaging, and persuasive cold email** to {first_name} at {company_name}. 
        Use the following research insights to make the email highly relevant and personalized:

        {research_summary}

        Our product/service: {product_context}

        - Keep it under 150 words
        - Make it professional but friendly
        - Optionally, include 1-2 emojis where it feels natural
        - End with a clear, non-pushy call-to-action

        Output the email as ready-to-send text.
        """

        return self.llm.invoke(prompt).content

    def _writer_node(self, state: WriterState, product_context: str = "SaaS platform for AI model deployment"):
        lead = state.lead
        research_summary = state.research_summary

        draft = self.draft_email(lead, research_summary, product_context)

        template_string = """Subject: Regarding your work and ${company_name}

        Hi ${recipient_name},

        My name is ${sender_name}, and I'm from ${sender_company}.

        I was doing some research and came across your profile. I was particularly impressed by this:
        "{draft}"

        Given your focus, I thought you might be interested in our SaaS platform for AI model deployment.

        Would you be open for a quick chat next week?

        Best regards,
        ${sender_name}
        ${sender_title}
        """
        return {
            "draft_email": draft,
            "email_template": template_string 
        }

