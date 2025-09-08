# app/main.py

import sqlite3
from fastapi import FastAPI, HTTPException
from pathlib import Path
from typing import List
from . import schemas


DB_PATH = Path(__file__).parent.parent / "data" / "campaign.db"
app = FastAPI(title="AI Outreach Agent API")

def get_db_connection():
    """ينشئ اتصالًا بقاعدة البيانات."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # هذا يجعل النتائج تعمل مثل الـ dictionaries
    return conn

@app.get("/campaign/results", response_model=List[schemas.CampaignResult])
def get_campaign_results():
    """يجلب كل نتائج الحملة من قاعدة البيانات."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # تأكد من أن أسماء الأعمدة هنا تطابق الأعمدة في قاعدة البيانات والـ schema
        cursor.execute("""
            SELECT id, first_name, company_name, generated_email, 
                   status, sim_opened, sim_clicked, sim_replied 
            FROM emails_campaign
        """)
        rows = cursor.fetchall()
        conn.close()

        # ✅ الخطوة الأهم: تحويل كل صف إلى dictionary بشكل صريح
        results = [dict(row) for row in rows]
        
        return results

    except Exception as e:
        # هذا السطر سيساعد في طباعة الخطأ في الـ terminal الخاص بالـ API
        print(f"An error occurred in /campaign/results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/campaign/kpis", response_model=schemas.Kpis)
def get_campaign_kpis():
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # حساب المؤشرات
        total_processed = cursor.execute("SELECT COUNT(id) FROM emails_campaign").fetchone()[0]
        successful_emails = cursor.execute("SELECT COUNT(id) FROM emails_campaign WHERE status = 'success'").fetchone()[0]
        opened = cursor.execute("SELECT COUNT(id) FROM emails_campaign WHERE sim_opened = 1").fetchone()[0]
        clicked = cursor.execute("SELECT COUNT(id) FROM emails_campaign WHERE sim_clicked = 1").fetchone()[0]
        replied = cursor.execute("SELECT COUNT(id) FROM emails_campaign WHERE sim_replied = 1").fetchone()[0]
        
        conn.close()

      
        success_rate = (successful_emails / total_processed * 100) if total_processed > 0 else 0
        open_rate = (opened / successful_emails * 100) if successful_emails > 0 else 0
        ctr = (clicked / opened * 100) if opened > 0 else 0
        reply_rate = (replied / successful_emails * 100) if successful_emails > 0 else 0

        return {
            "total_processed": total_processed,
            "successful_emails": successful_emails,
            "success_rate_percent": round(success_rate, 2),
            "open_rate_percent": round(open_rate, 2),
            "click_through_rate_percent": round(ctr, 2),
            "reply_rate_percent": round(reply_rate, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))