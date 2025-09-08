from src.agents.schemas import EmailerState
from langchain_google_genai import ChatGoogleGenerativeAI
from src import config

class EmailerAgent:
    def __init__(self , model = "gemini-1.5-flash" , temperature = 0):
        self.llm = ChatGoogleGenerativeAI(
            model = model,
            temperature = temperature,
            google_api_key = config.GOOGLE_API_KEY,
        )

    def _email_node(self , state: EmailerState):
        """
        Node to generate the final email output
        """
        lead = state.lead
        filled_template = state.filled_template 
        product_context = "SaaS platform for AI model deployment"

        prompt = f"""
        You are a professional B2B copywriter.

        You have a filled email template and the following lead information:

        Lead Info:
        - Name: {lead.get('firstName')} {lead.get('lastName')}
        - Job Title: {lead.get('linkedinJobTitle')}
        - Company: {lead.get('companyName')}
        - Location: {lead.get('location')}

        Filled Template:
        {filled_template} # <-- استخدم المتغير الصحيح هنا

        Product/Service we offer: {product_context}

        Your task:
        1. Rewrite the draft from the filled template into a polished, concise, and persuasive cold email.
        2. Make it professional but friendly, optionally including 1-2 emojis.
        3. Include a clear subject line relevant to the lead.
        4. Ensure a strong call-to-action at the end.
        5. Keep it under 150 words.

        Output the final email as ready-to-send text including Subject, greeting, body, and closing.
        """
        
        final_email_text = self.llm.invoke(prompt).content

        state.final_email = final_email_text
        return state

