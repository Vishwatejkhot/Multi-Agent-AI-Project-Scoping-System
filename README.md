# 🚀 Multi-Agent AI Project Scoping System

An AI-powered multi-agent system that converts startup ideas into:

-   Structured MVP scope\
-   Recommended tech stack\
-   Risk analysis\
-   Engineering complexity scoring\
-   Timeline estimation\
-   Country-adjusted cost estimation\
-   Real-time currency conversion\
-   Investor-ready branded PDF reports

------------------------------------------------------------------------

## 🧠 What This Project Demonstrates

This is not just a chatbot.

It demonstrates:

-   Multi-agent orchestration
-   Retrieval-Augmented Generation (RAG)
-   Tool augmentation
-   Structured JSON validation (Pydantic)
-   Financial modeling logic
-   Country-based cost adjustments
-   Real-time FX conversion
-   White-label PDF generation
-   Production-style architecture

------------------------------------------------------------------------

## 📦 Features

### Multi-Agent Pipeline

1.  Clarification Agent\
2.  MVP Agent\
3.  Tech Stack Agent\
4.  Risk Agent\
5.  Complexity Estimator (tool)\
6.  Timeline Calculator (tool)\
7.  Cost Estimator (country-aware)\
8.  Investor Report Agent

------------------------------------------------------------------------

## 🌍 International Ready

-   Development cost adjusted per country
-   Real-time currency conversion
-   Dynamic branding support
-   Logo upload (PNG/JPG)
-   Custom accent color

------------------------------------------------------------------------

## 📄 Investor-Grade PDF Includes

-   Cover page
-   Centered logo
-   Watermark background
-   Structured overview table
-   Timeline bar chart
-   Cost breakdown chart
-   Risk breakdown
-   Investor readiness score
-   Page numbers

------------------------------------------------------------------------

## 🏗 Architecture Overview

User Idea\
↓\
RAG Retrieval\
↓\
Clarification Agent\
↓\
MVP Agent\
↓\
Tech Stack Agent\
↓\
Risk Agent\
↓\
Tool Layer\
(Complexity → Timeline → Country-Based Cost)\
↓\
Investor Report Agent\
↓\
Branded PDF Export

------------------------------------------------------------------------

## 🛠 Tech Stack

-   Python\
-   Streamlit\
-   LangChain\
-   Groq (LLM)\
-   FAISS\
-   Sentence Transformers\
-   Pydantic\
-   ReportLab\
-   Requests\
-   dotenv

------------------------------------------------------------------------

## 🚀 How To Run

### 1️⃣ Clone Repository

``` bash
git clone <your-repo-url>
cd project_scoping_assistant
```

### 2️⃣ Create Virtual Environment

Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

Mac / Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4️⃣ Add Groq API Key

Create a `.env` file:

    GROQ_API_KEY=your_api_key_here

### 5️⃣ Build Vector Store

``` bash
python rag/build_vectorstore.py
```

### 6️⃣ Run App

``` bash
streamlit run app.py
```

Open: http://localhost:8501

------------------------------------------------------------------------

## 💡 Why This Project Matters

Founders often:

-   Build without defined scope
-   Underestimate cost
-   Ignore risk
-   Overbuild MVP
-   Misjudge timeline

This system solves that using:

-   AI reasoning
-   Engineering judgment
-   Deterministic cost modeling
-   Investor-ready reporting

------------------------------------------------------------------------

## 🔥 Future Improvements

-   Async multi-agent execution
-   LangGraph state machine
-   Persistent project storage
-   Authentication & multi-user SaaS
-   Deployment (AWS / Render / Railway)
-   Risk heatmap visualization
-   Gantt timeline chart
-   Cost breakdown by phase

------------------------------------------------------------------------

## 📜 License

MIT License
