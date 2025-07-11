# CivicGPT+ — Multimodal Civic Engagement & AI Pipeline

CivicGPT+ is a research-grade AI/ML pipeline project built to analyze, predict, and visualize public sentiment, civic trends, and community risks using real-world multimodal data.

> 🔧 Built and deployed using open-source tools + Azure Free Tier cloud services.

---

## Project Goals

- Aggregate and unify civic data from news, social media, and government sources.
- Perform real-time sentiment analysis and classify emerging civic issues.
- Use LLMs + RAG (Retrieval-Augmented Generation) to answer civic questions.
- Predict trends like public engagement or potential risks.
- Serve insights via APIs and dashboards for policymakers and citizens.

---

## Tech Stack Overview

| Layer | Toolset |
|-------|---------|
| **Ingestion & Scheduling** | Apache Airflow, RSS Feeds, Twitter API, Azure Blob |
| **Processing** | Databricks (Community Edition), PySpark |
| **Modeling** | Hugging Face Transformers, scikit-learn, XGBoost, MLflow |
| **RAG System** | OpenAI Embeddings, LangChain, Pinecone / pgvector |
| **API Layer** | FastAPI, GraphQL (Strawberry) |
| **Dashboard** | Dash or Streamlit, Plotly, Mapbox |
| **MLOps** | Docker, GitHub Actions, Prometheus, Grafana |
| **Security** | Pydantic, Azure Key Vault, CORS, Rate Limiting |
| **Cloud Services** | Azure App Service, Azure Blob Storage, Azure PostgreSQL |

---

## Real-World Application Areas

- Civic planning & outreach
- Sentiment-based public policy design
- City service improvement via citizen feedback
- Automated analysis of open government data



## 💻 Running the Project

### 🟢 First-Time Initialization (One-Time Setup)

Run this only once after cloning or resetting your project:

```bash
# Start Airflow, Postgres, Scheduler, and Webserver in background
docker-compose up -d

# Initialize the Airflow metadata database
docker-compose run airflow-webserver airflow db init

# Create Airflow admin user
docker-compose run airflow-webserver airflow users create \
  --username admin \
  --password admin \
  --firstname Civic \
  --lastname GPT \
  --role Admin \
  --email civicgpt@example.com
```

Once initialized, open your browser and go to:

```
http://localhost:8080
```

Use the following credentials to log in:

- **Username:** `admin`
- **Password:** `admin`

---

### 🛑 Stop All Services

To gracefully shut down all running containers:

```bash
docker-compose down
```

---

### 🔁 Resume Project After Shutdown

To bring everything back up after a stop:

```bash
docker-compose up -d
```

Once containers are running, revisit:

```
http://localhost:8080
```

Your DAGs and environment will pick up from where they left off.
