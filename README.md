# 🇨🇳 China2Market AI
### AI-Powered Import Export Supply Chain Analytics Platform

Built for Maharashtra-based importers sourcing from Chinese suppliers.

## Problem Statement
Track products from China → Import → Store → Maharashtra Distribution → Profit

## Modules
| Module | Description |
|--------|-------------|
| Product Management | Catalog with import/sell pricing |
| Sales Analytics | Revenue, profit, city-wise breakdown |
| Inventory Alerts | Low stock, dead stock, overstock |
| Demand Forecasting | ML-based next-month prediction |
| Supplier Analysis | Delay tracking, damage rates, ratings |

## Tech Stack
- **Language**: Python 3.12
- **Dashboard**: Streamlit
- **ML**: Scikit-learn
- **Charts**: Plotly
- **Data**: Pandas + CSV / MySQL

## Setup
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Dataset
- 4,000 orders | 2023–2024
- 6 Maharashtra cities
- 6 product categories
- 4 Chinese suppliers

## Folder Structure
```
China2MarketAI/
├── data/           ← sales_data.csv
├── models/         ← ML model files
├── dashboard/      ← Streamlit page modules
├── database/       ← DB schema & connection
├── notebooks/      ← EDA Jupyter notebooks
├── screenshots/    ← UI previews
├── app.py          ← Main Streamlit app
├── requirements.txt
└── README.md
```

## Developed By
[Your Name] | TY Project | 2024
