# 🚀 RechargePlanFinder version V1

A specialized data-to-API engine built to solve "Choice Paralysis" in mobile plan selection. This project serves as a proof-of-concept for a decoupled architecture using FastAPI and PostgreSQL.

## 🎯 The Features
This Product ensures 99.9% uptime and stateless execution on cloud environments, the following constraints are currently in place:
* **Provider Scope:** Currently exclusively processing **Jio Plans**.
* **Filter Depth:** Multi-dimensional querying logic. Filtering engine processes **OTT Subscriptions**, **Price Thresholds**, **Data Quotas**, and **Validity Periods** using set-based SQL operations for sub-second response times.
* **Architecture:** Deprecated Selenium-based scraping in favor of a stateless, manual data-push architecture to eliminate environment-heavy dependencies.

## 🏗️ System Architecture
The system is built on a "Thin-Client" philosophy to ensure high-speed responses even on free-tier cloud infrastructure.

* **Backend:** FastAPI (Python) using **SQLModel** (SQLAlchemy + Pydantic) for high-performance ORM.
* **Database:** Relational PostgreSQL hosted on Render, optimized with set-based SQL queries.
* **Frontend:** Streamlit utilizing **@st.cache_data** to eliminate redundant API calls.
* **CI/CD:** Automated deployment via GitHub hooks to Render (API/DB) and Streamlit Cloud (UI).

## 🛠️ Tech Stack
* **Environment:** `uv` (Fastest Python package manager)
* **API Framework:** FastAPI 0.136.0+
* **Database:** PostgreSQL
* **ORM:** SQLModel
* **Deployment:** Render & Streamlit Community Cloud

## 🔌 API Endpoints (Documentation at /docs)
* `GET /allJioplans/` - Retrieves the full plan ecosystem.
* `GET /jioplansprices/` -Retrieves the price of each plan.
* `GET /jioplansbenefits/` - Retrieves the details of each plan.
* `GET /unique-subscriptions` - Returns a sorted list of unique OTT benefits (Set-logic).
* `GET /filter-plans-by-otts` - Dynamic filtering based on user-selected OTT pills.
* `GET /filter-plans-by-prices` - Filters plans based on minimum and maximum prices.
* `GET /filter-plans-by-validity`- Filters plans based on minimum and maximum days .
* `GET /filter-plans-by-data` - Filters plans based on minimum and maximum amount of data.

## 🚀 Installation & Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sa-Hitesh-k/BestRechargePlanFinder.git
   cd BestRechargePlanFinder

2. **Sync the environment:**
   ```bash
   uv sync

3. **Database Setup:**
Create a .env file in the root directory:

   DATABASE_URL=postgresql://user:password@localhost:5432/dbname

4. **Run the API:**

   ```bash
   uvicorn main:app --reload