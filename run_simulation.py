
import sqlite3
import random
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "campaign.db"

def add_simulation_columns(cursor):
    try:
        cursor.execute("ALTER TABLE emails_campaign ADD COLUMN sim_opened BOOLEAN")
        cursor.execute("ALTER TABLE emails_campaign ADD COLUMN sim_clicked BOOLEAN")
        cursor.execute("ALTER TABLE emails_campaign ADD COLUMN sim_replied BOOLEAN")
        print("Simulation columns added to the database.")
    except sqlite3.OperationalError:
    
        pass

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    add_simulation_columns(cursor)


    cursor.execute("SELECT id FROM emails_campaign WHERE status = 'success' AND sim_opened IS NULL")
    successful_emails = cursor.fetchall()
    
    if not successful_emails:
        print("No new emails to simulate. Run the pipeline first.")
        return

    print(f"Simulating engagement for {len(successful_emails)} new emails...")

    for email_id_tuple in successful_emails:
        email_id = email_id_tuple[0]
        
  
        opened = random.choices([True, False], weights=[0.65, 0.35], k=1)[0]
        clicked = False
        replied = False

        if opened:
        
            clicked = random.choices([True, False], weights=[0.20, 0.80], k=1)[0] # 20%
            replied = random.choices([True, False], weights=[0.08, 0.92], k=1)[0] # 8%

        cursor.execute("""
        UPDATE emails_campaign
        SET sim_opened = ?, sim_clicked = ?, sim_replied = ?
        WHERE id = ?
        """, (opened, clicked, replied, email_id))

    conn.commit()
    conn.close()
    print("Simulation complete. Database has been updated.")

if __name__ == "__main__":
    main()