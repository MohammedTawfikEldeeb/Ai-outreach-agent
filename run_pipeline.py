# run_pipeline.py

import sqlite3
import time
import pandas as pd
from pathlib import Path
from tqdm import tqdm

from src.agents.graph import OutreachGraph

DB_PATH = Path(__file__).parent / "data" / "campaign.db"
LEADS_CSV_PATH = Path(__file__).parent / "data" / "processed" / "linkedin_leads_processed.csv"

def setup_database():
  
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emails_campaign (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        company_name TEXT,
        linkedin_url TEXT,
        generated_email TEXT,
        status TEXT,
        error_message TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def main():
    
    setup_database()
    
    print("Loading leads from CSV...")
    leads_df = pd.read_csv(LEADS_CSV_PATH)
    leads = leads_df.to_dict(orient="records")

    print(f"Found {len(leads)} leads. Initializing outreach graph...")
    outreach_graph = OutreachGraph()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Running pipeline on all leads...")
    for lead in tqdm(leads, desc="Processing Leads"):
        try:
            result_state = outreach_graph.run(lead)
            final_email = result_state.get("final_email", "")

            cursor.execute("""
            INSERT INTO emails_campaign (first_name, last_name, company_name, linkedin_url, generated_email, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                lead.get("firstName"),
                lead.get("lastName"),
                lead.get("companyName"),
                lead.get("linkedinUrl"),
                final_email,
                "success"
            ))
        except Exception as e:
            print(f"\nError processing lead {lead.get('firstName')}: {e}")
            cursor.execute("""
            INSERT INTO emails_campaign (first_name, company_name, status, error_message)
            VALUES (?, ?, ?, ?)
            """, (lead.get("firstName"), lead.get("companyName"), "failed", str(e)))
        
        conn.commit()

    conn.close()
    print(f"\nPipeline finished. Results saved to {DB_PATH}")

if __name__ == "__main__":
    main()