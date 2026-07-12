import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Sales Forecasting Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 End-to-End Sales Forecasting & Demand Intelligence System")

st.markdown("""
This dashboard provides:
- Sales Overview
- Forecast Explorer
- Anomaly Detection
- Product Demand Segmentation
""")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("train.csv")

    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        dayfirst=True
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        dayfirst=True
    )

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month_name()

    return df


df = load_data()

# ----------------------------
# Sidebar
# ----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "Sales Overview",
        "Forecast Explorer",
        "Anomaly Detection",
        "Product Segmentation"
    ]
)

# ----------------------------
# Sales Overview
# ----------------------------
if page == "Sales Overview":

    st.header("Sales Overview Dashboard")

    total_sales = df["Sales"].sum()
    total_orders = df["Order ID"].nunique()
    total_customers = df["Customer ID"].nunique()

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Sales", f"${total_sales:,.0f}")
    c2.metric("Total Orders", total_orders)
    c3.metric("Total Customers", total_customers)

    yearly = df.groupby("Year")["Sales"].sum().reset_index()

    fig = px.line(
        yearly,
        x="Year",
        y="Sales",
        markers=True,
        title="Yearly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    category = df.groupby("Category")["Sales"].sum().reset_index()

    fig2 = px.bar(
        category,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category"
    )

    st.plotly_chart(fig2, use_container_width=True)
    # ----------------------------
# Forecast Explorer
# ----------------------------
if page == "Forecast Explorer":

    st.header("Forecast Explorer")

    yearly = df.groupby("Year")["Sales"].sum().reset_index()

    fig = px.line(
        yearly,
        x="Year",
        y="Sales",
        markers=True,
        title="Yearly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.success("Sales show an overall increasing trend over the years.")

# ----------------------------
# Anomaly Detection
# ----------------------------
if page == "Anomaly Detection":

    st.header("Anomaly Detection")

    fig = px.box(
        df,
        y="Sales",
        title="Sales Outlier Detection"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("Extreme values in the boxplot may represent unusual sales transactions.")
    # ----------------------------
# Product Segmentation
# ----------------------------
if page == "Product Segmentation":

    st.header("Product Demand Segmentation")

    category_sales = (
        df.groupby("Sub-Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_sales,
        x="Sub-Category",
        y="Sales",
        color="Sales",
        title="Sales by Product Sub-Category"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Business Insight")

    st.write("""
- High sales products should be stocked more frequently.
- Medium sales products require balanced inventory.
- Low sales products should be stocked carefully to reduce inventory costs.
- Product demand segmentation helps improve inventory planning.
""")

# ----------------------------
# Footer
# ----------------------------
st.sidebar.success("✅ Dashboard Ready")