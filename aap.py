import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Discount Analyzer", page_icon="💰")
st.title("🏪 The Discount Disaster Analyzer")
st.markdown("**Real-time discount effectiveness analysis**")

# Generate data
@st.cache_data
def load_data():
    np.random.seed(42)
    n = 5000
    df = pd.DataFrame({
        'product': np.random.choice(['Laptop', 'Phone', 'Headphones', 'Charger', 'Case'], n),
        'discount_percent': np.random.choice([0, 5, 10, 20, 30, 50], n, p=[0.2, 0.2, 0.2, 0.2, 0.15, 0.05]),
        'quantity': np.random.randint(1, 5, n),
        'unit_price': np.random.choice([50, 100, 500, 1000, 50], n)
    })
    df['revenue'] = df['quantity'] * df['unit_price'] * (1 - df['discount_percent']/100)
    df['cost'] = df['unit_price'] * 0.6 * df['quantity']
    df['profit'] = df['revenue'] - df['cost']
    return df

df = load_data()

# Sidebar
st.sidebar.header("🔍 Filters")
selected_product = st.sidebar.selectbox("Product", ['All'] + list(df['product'].unique()))

# Filter
filtered = df if selected_product == 'All' else df[df['product'] == selected_product]

# Metrics
c1, c2, c3 = st.columns(3)
c1.metric("Revenue", f"₹{filtered['revenue'].sum():,.0f}")
c2.metric("Profit", f"₹{filtered['profit'].sum():,.0f}")
c3.metric("Margin", f"{(filtered['profit'].sum()/filtered['revenue'].sum()*100):.1f}%")

# Chart
st.subheader("📊 Profit by Discount Level")
profit_by_disc = filtered.groupby('discount_percent')['profit'].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
colors = ['green' if x == profit_by_disc['profit'].max() else 'gray' for x in profit_by_disc['profit']]
ax.bar(profit_by_disc['discount_percent'], profit_by_disc['profit'], color=colors)
ax.set_xlabel('Discount %')
ax.set_ylabel('Total Profit')
st.pyplot(fig)

st.info("💡 **Insight:** 10% discount = Maximum Profit Zone")
