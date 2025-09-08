# 🤖 AI Outreach Agent: Autonomous Email Personalization

An end-to-end system that automates the entire cold outreach process, from lead research to crafting highly personalized emails, powered by a multi-agent LLM architecture built with LangGraph.

> **Note:** This is a demonstration/test project showcasing the capabilities of AI-powered outreach automation. All results and engagement metrics are simulated for demonstration purposes only. No actual outreach campaigns were conducted.

---

### ✨ The Problem: Scaling Personalized Outreach is Hard

Sales and business development teams waste countless hours manually researching leads and writing personalized emails. This process is:
* **Time-Consuming:** Hours spent per day on repetitive tasks.
* **Inconsistent:** Email quality varies from one person to another.
* **Hard to Scale:** It's nearly impossible to reach hundreds of leads with genuine personalization.

### 💡 The Solution: An Autonomous Agentic Workflow

This project implements a sophisticated multi-agent system built with **LangGraph** (`src/agents/graph.py`) that orchestrates a seamless workflow between specialized agents:

1.  **🔎 Research Agent (`researcher_agent.py`):** Takes a raw LinkedIn profile and uses the Tavily API to enrich it with key, actionable insights.
2.  **✍️ Writer Agent (`writer_agent.py`):** Uses the research from the first agent and a Gemini model to craft a unique, personalized email draft.
3.  **📧 Emailer Agent (`emailer_agent.py`):** Polishes the draft into a final, ready-to-send format, ensuring a professional tone and a clear call-to-action.

The entire process is managed as a directed acyclic graph (DAG), ensuring reliability and clear data flow between agents, with state managed by Pydantic schemas (`src/agents/schemas/`). All agent interactions are traced and monitored using **LangSmith** for performance optimization and debugging.

### 🎯 Project Goals

* Demonstrate proficiency in building complex AI agent systems
* Showcase skills in LLM orchestration and prompt engineering
* Implement a production-ready architecture with proper monitoring
* Simulate real-world campaign results stored in SQLite for analysis

---

### 🚀 Key Features

* **Autonomous Research & Writing:** From a CSV of leads to a database of ready-to-send emails with zero manual intervention.
* **Deep Personalization:** Emails are not just templates; they are crafted based on specific insights about each lead.
* **Campaign Simulation & Analytics:** Includes a comprehensive simulation layer that models engagement metrics (Open Rate, Reply Rate) and stores all results in an SQLite database for analysis.
* **Agent Performance Tracking:** Integrated with LangSmith for detailed monitoring and tracing of agent behaviors and performance.
* **API-First Design:** All results and KPIs are exposed via a robust **FastAPI** backend (`app/main.py`), ready for any frontend application.
* **Production-Ready:** The entire application is containerized with **Docker**, ensuring consistency and ease of deployment.
* **Configurable:** Campaign settings and templates are managed via external JSON files (`src/configs/`), making the system adaptable.

---

### 🏗️ System Architecture

The system follows a modern, decoupled architecture, separating the data processing pipeline from the data serving layer.


### 📊 Data Collection & Simulation Results

**Data Collection:** Lead data was collected using Phantombuster, a powerful data scraping tool that extracts professional information from LinkedIn profiles. The raw data contains comprehensive information about engineering professionals including their job titles, companies, locations, and career histories.

**Data Processing:** The raw LinkedIn data (`data/raw/linkedin_leads.csv`) was processed and cleaned to extract relevant information for the outreach campaign. Processed leads are stored in (`data/processed/linkedin_leads_processed.csv`) for use in the AI outreach pipeline.

**Simulation Results:** All simulation results are stored in an SQLite database (`data/campaign.db`) for easy analysis and visualization. The database contains:

* **Generated Emails:** Fully personalized email content for each lead
* **Engagement Metrics:** Simulated open rates, reply rates, and conversion data
* **Processing Times:** Performance metrics for each stage of the pipeline
* **Lead Insights:** Research data collected for each lead

To access the simulation results:
```bash
# Run the pipeline to generate results
python run_pipeline.py

# Results are stored in data/campaign.db
# You can query the database directly with any SQLite client
```

Sample database schema:
* `leads` table: Lead information and generated emails
* `engagement_metrics` table: Simulated engagement data
* `processing_logs` table: Performance metrics

To visualize the results, you can use the included Streamlit dashboard:
```bash
streamlit run dashboard/streamlit_app.py
```

### 🤖 AI Outreach Agent - Campaign Dashboard

### 📊 Key Performance Indicators (KPIs)

| Metric                        | Value                 | Description                                    |
| ----------------------------- | --------------------- | ---------------------------------------------- |
| **Total Leads Processed** | 38                    | Number of leads successfully processed         |
| **Success Rate** | `100.0%`              | Percentage of leads processed without errors   |
| **Simulated Open Rate** | `52.63%`              | Simulated percentage of leads who opened the email|
| **Simulated Reply Rate** | `5.26%`               | Simulated percentage of leads who replied      |
| **Avg. Turnaround Time** | `4.12 sec/lead`       | Average time from lead input to final email    |

*(Note: Engagement metrics are realistically simulated to showcase potential campaign outcomes.)*


### 🛠️ Tech Stack

* **Orchestration:** LangChain, LangGraph
* **LLMs:** Google Gemini API
* **Web Research:** Tavily API
* **Agent Monitoring:** LangSmith
* **Backend:** FastAPI, Pydantic
* **Data Handling:** Pandas, SQLite
* **Tooling & Environment:** UV, Docker, Docker Compose

---

### 🚀 How to Run

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/Ai-outreach-agent.git](https://github.com/your-username/Ai-outreach-agent.git)
    cd Ai-outreach-agent
    ```

2.  **Set Up Environment with UV:**
    ```bash
    # Install uv if you haven't already
    pip install uv

    # Create and sync the virtual environment using pyproject.toml and requirements.txt
    uv venv
    uv pip sync -r requirements.txt
    ```

3.  **Configure API Keys:**
    Add your `GOOGLE_API_KEY` and `TAVILY_API_KEY` to the `src/config.py` file.
    
    *(Note: For demonstration purposes, you can use placeholder values as no actual API calls are made in this simulation)*

4.  **Run the Full Pipeline:**
    These scripts populate and enrich the `data/campaign.db` database.
    ```bash
    # Step 1: Generate emails and save to database
    python run_pipeline.py

    # Step 2: Simulate engagement metrics
    python run_simulation.py
    ```

5.  **LangSmith Monitoring:**
    All agent interactions are traced using LangSmith. To view traces:
    * Set up your LangSmith API key in `src/config.py`
    * Access traces at [https://smith.langchain.com](https://smith.langchain.com)
    
    *(Note: For demonstration purposes, tracing works with placeholder API keys)*

6.  **Run the API Server:**
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will be available for testing at `http://127.0.0.1:8000/docs`.