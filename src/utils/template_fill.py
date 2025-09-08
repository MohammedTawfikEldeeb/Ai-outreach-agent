# src/utils/template_fill.py
from string import Template
from typing import Dict

def fill_email_template(draft_text: str, sender_profile: Dict[str, str], recipient_name: str) -> str:
 
    template = Template(draft_text)
    safe_map = {
        "recipient_name": recipient_name or "",
        "sender_name": sender_profile.get("sender_name", ""),
        "sender_title": sender_profile.get("sender_title", ""),
        "sender_company": sender_profile.get("sender_company", ""),
        "sender_website": sender_profile.get("sender_website", ""),
        "sender_email": sender_profile.get("sender_email", "")
    }
    return template.safe_substitute(safe_map)
