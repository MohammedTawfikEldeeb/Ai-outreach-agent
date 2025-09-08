from src.agents.researcher_agent import ResearchAgent
from src.agents.writer_agent import WriterAgent
from src.agents.emailer_agent import EmailerAgent
from src.agents.schemas import WriterState
from src.agents.schemas import EmailerState
from langgraph.graph import StateGraph, START, END
import pandas as pd
from pathlib import Path
from src.configs.sender_profile import SENDER_PROFILE
from src.utils.template_fill import fill_email_template


class OutreachGraph:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.writer_agent = WriterAgent()
        self.email_agent = EmailerAgent()
        self.graph = self._build_graph()

    def _build_graph(self):
        graph = StateGraph(EmailerState)
        
     
        graph.add_node("researcher", self._research_node)
        graph.add_node("writer", self._writer_node)
        graph.add_node("template_filler", self._template_filler_node) 
        graph.add_node("emailer", self._email_node)
        
        graph.add_edge(START, "researcher")
        graph.add_edge("researcher", "writer")
        graph.add_edge("writer", "template_filler") 
        graph.add_edge("template_filler", "emailer") 
        graph.add_edge("emailer", END)
        
        return graph.compile()

    def _research_node(self, state: EmailerState):
        return self.research_agent._research_node(state)

    def _writer_node(self, state: EmailerState):
        return self.writer_agent._writer_node(state)
    
    def _template_filler_node(self, state: EmailerState):
        
        sender_profile = SENDER_PROFILE
        recipient_name = state.lead.get("firstName") or state.lead.get("fullName") or ""
        if state.email_template is None:
            raise ValueError("Email template is not set in the state.")
        filled = fill_email_template(state.email_template, sender_profile, recipient_name)

       
        state.filled_template = filled
        state.sender_profile = sender_profile
        return state

    
    def _email_node(self, state: EmailerState):
        return self.email_agent._email_node(state)

    def run(self, lead: dict):
        state = EmailerState(lead=lead)
        return self.graph.invoke(state)

# ---------------- Test ----------------
if __name__ == "__main__":
    project_root = Path(__file__).parent.parent.parent
    DATA_PATH = project_root / "data" / "processed"
    leads_df = pd.read_csv(DATA_PATH / "linkedin_leads_processed.csv")
    sample_lead = leads_df.iloc[0].to_dict()

    outreach_graph = OutreachGraph()
    result = outreach_graph.run(sample_lead)