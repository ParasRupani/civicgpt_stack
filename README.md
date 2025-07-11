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