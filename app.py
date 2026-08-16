"""
China2Market AI — Main Streamlit Application
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="China2Market AI",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Load Data ──────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/sales_data.csv", parse_dates=["Order_Date", "Delivery_Date"])
    df["Revenue"] = df["Selling_Price"] * df["Quantity_Sold"]
    return df

df = load_data()

# ── Sidebar Filters ────────────────────────────────────────
st.sidebar.image("https://flagcdn.com/cn.svg", width=60)
st.sidebar.title("China2Market AI")
st.sidebar.markdown("---")

year_filter = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
city_filter = st.sidebar.multiselect("City", sorted(df["City"].unique()), default=sorted(df["City"].unique()))
product_filter = st.sidebar.multiselect("Product", sorted(df["Product_Name"].unique()), default=sorted(df["Product_Name"].unique()))

df_f = df[df["Year"].isin(year_filter) & df["City"].isin(city_filter) & df["Product_Name"].isin(product_filter)]

# ── Page Header ────────────────────────────────────────────
st.title("🇨🇳 China2Market AI Dashboard")
st.markdown("**Import → Store → Maharashtra Distribution → Profit Tracker**")
st.markdown("---")

# ── KPI Row ────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Orders",    f"{len(df_f):,}")
k2.metric("Total Revenue",   f"₹{df_f['Revenue'].sum():,.0f}")
k3.metric("Total Profit",    f"₹{df_f['Profit'].sum():,.0f}")
k4.metric("Avg Delay (Days)",f"{df_f['Shipment_Delay_Days'].mean():.1f}")
k5.metric("Damaged Orders",  f"{df_f['Damaged_Goods'].sum():,}")

st.markdown("---")

# ── Charts Row 1 ───────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Top Products by Revenue")
    prod_rev = df_f.groupby("Product_Name")["Revenue"].sum().sort_values(ascending=False)
    fig = px.bar(prod_rev, x=prod_rev.values, y=prod_rev.index, orientation='h',
                 color=prod_rev.values, color_continuous_scale="Reds",
                 labels={"x":"Revenue (₹)", "y":""})
    fig.update_layout(showlegend=False, coloraxis_showscale=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🗺️ City-wise Sales Distribution")
    city_rev = df_f.groupby("City")["Revenue"].sum().reset_index()
    fig = px.pie(city_rev, values="Revenue", names="City",
                 color_discrete_sequence=px.colors.qualitative.Set3)
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

# ── Charts Row 2 ───────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("📈 Monthly Revenue Trend")
    monthly = df_f.groupby(["Year","Month"])["Revenue"].sum().reset_index()
    monthly["Period"] = monthly["Year"].astype(str) + "-" + monthly["Month"].astype(str).str.zfill(2)
    monthly = monthly.sort_values("Period")
    fig = px.line(monthly, x="Period", y="Revenue", markers=True,
                  color_discrete_sequence=["#FF4B4B"])
    fig.update_layout(height=350, xaxis_tickangle=45)
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.subheader("🚢 Supplier Delay Analysis")
    sup_delay = df_f.groupby("Supplier").agg(
        Avg_Delay=("Shipment_Delay_Days","mean"),
        Damage_Count=("Damaged_Goods","sum"),
        Total_Orders=("Order_ID","count")
    ).reset_index()
    sup_delay["Damage_Rate_%"] = (sup_delay["Damage_Count"] / sup_delay["Total_Orders"] * 100).round(2)
    fig = px.scatter(sup_delay, x="Avg_Delay", y="Damage_Rate_%", size="Total_Orders",
                     text="Supplier", color="Supplier",
                     labels={"Avg_Delay":"Avg Delay (Days)","Damage_Rate_%":"Damage Rate %"})
    fig.update_traces(textposition="top center")
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ── Inventory Alerts ───────────────────────────────────────
st.markdown("---")
st.subheader("🚨 Inventory Alerts")

# Simulate stock levels from sales velocity
stock_sim = df_f.groupby("Product_Name")["Quantity_Sold"].sum().reset_index()
stock_sim.columns = ["Product", "Units_Sold"]
stock_sim["Stock_Remaining"] = (stock_sim["Units_Sold"] * 0.08).astype(int)  # ~8% remaining sim

low_stock  = stock_sim[stock_sim["Stock_Remaining"] < 50]
dead_stock = stock_sim[stock_sim["Units_Sold"] < stock_sim["Units_Sold"].quantile(0.2)]

a1, a2 = st.columns(2)
with a1:
    st.error(f"🔴 Low Stock Products ({len(low_stock)})")
    if len(low_stock) > 0:
        st.dataframe(low_stock, use_container_width=True, hide_index=True)
    else:
        st.success("All products adequately stocked")

with a2:
    st.warning(f"⚠️ Slow Moving / Dead Stock ({len(dead_stock)})")
    st.dataframe(dead_stock[["Product","Units_Sold"]].rename(columns={"Units_Sold":"Units_Sold_2yr"}),
                 use_container_width=True, hide_index=True)

# ── Raw Data ───────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Sales Data"):
    st.dataframe(df_f.head(100), use_container_width=True)
    st.download_button("⬇️ Download Filtered CSV", df_f.to_csv(index=False), "filtered_sales.csv")

st.markdown("---")
st.caption("China2Market AI | TY Project 2024 | Built with Streamlit + Plotly")
