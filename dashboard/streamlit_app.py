
import streamlit as st
import pandas as pd
import requests

API_BASE_URL = "http://127.0.0.1:8000" 

st.set_page_config(layout="wide")
st.title("🤖 AI Outreach Agent - Campaign Dashboard")


st.header("Key Performance Indicators (KPIs)")

try:
    response_kpis = requests.get(f"{API_BASE_URL}/campaign/kpis")
    response_kpis.raise_for_status() 
    kpis = response_kpis.json()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Leads Processed", kpis['total_processed'])
    col2.metric("Success Rate", f"{kpis['success_rate_percent']}%")
    col3.metric("Simulated Open Rate", f"{kpis['open_rate_percent']}%")
    col4.metric("Simulated Reply Rate", f"{kpis['reply_rate_percent']}%")

except requests.exceptions.RequestException as e:
    st.error(f"Could not connect to the API. Make sure the FastAPI server is running. Error: {e}")
    st.stop()

st.divider()


st.header(" Campaign Results")

try:
    response_results = requests.get(f"{API_BASE_URL}/campaign/results")
    response_results.raise_for_status()
    results_data = response_results.json()
    
    df = pd.DataFrame(results_data)
    

    st.dataframe(df, use_container_width=True, column_config={
        "id": st.column_config.NumberColumn("ID"),
        "sim_opened": st.column_config.CheckboxColumn("Opened?"),
        "sim_clicked": st.column_config.CheckboxColumn("Clicked?"),
        "sim_replied": st.column_config.CheckboxColumn("Replied?")
    })

except requests.exceptions.RequestException as e:
    st.error(f"Could not fetch campaign results from the API. Error: {e}")