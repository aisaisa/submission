import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime as dtm
from babel.numbers import format_currency
sns.set(style='dark')
# Function untuk menyiapkan dataframe
def orders_df(df):
    count_order_df = df.groupby("purchase_time").total.sum().sort_values(ascending=False).reset_index()
    count_order_df.rename(columns={
        "purchase_time": "order_date",
        "total": "order_count"
    }, inplace=True)
    return count_order_df

def best_seller_df(df):
    best_seller_category_df = df.groupby("product_category").total.sum().sort_values(ascending=False).reset_index()
    return best_seller_category_df

# Load cleaned data
countOrder_df = pd.read_csv("count_order.csv")
countOrder_df.sort_values(by="total", inplace=True)
countOrder_df.reset_index(inplace=True)

bestSeller_df = pd.read_csv("best_seller_category.csv")
bestSeller_df.sort_values(by="total", inplace=True)
bestSeller_df.reset_index(inplace=True)

# Mengubah tipe data
countOrder_df['purchase_time'] = pd.to_datetime(countOrder_df['purchase_time'])

# Filter data
min_date = countOrder_df['purchase_time'].min()
max_date = countOrder_df['purchase_time'].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    g1, g2, g3 = st.columns([0.5,2,0.5])
    with g1:
        st.write(" ")
    with g3:
        st.write(" ")
    with g2:
        st.image("https://github.com/aisaisa/bangkitAcademy/raw/main/assets/logozilla.png", width=150)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        format="YYYY/MM/DD",
        value=[min_date, max_date]
    )

# Menyiapkan dataframe
count_order = orders_df(countOrder_df)
best_seller = best_seller_df(bestSeller_df)

# Membuat tampilan dashboard
st.header('E-Commerce Collection Dashboard :sparkles:')
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    total_orders = count_order.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    timestamp =  (end_date - start_date).days
    st.metric("Time depth in days", value=timestamp)

count_order_plot = count_order[(count_order["order_date"] >= str(start_date)) & 
                (count_order["order_date"] <= str(end_date))]

fig, ax = plt.subplots(figsize=(16, 8))
ax.scatter(
    count_order_plot["order_date"],
    count_order_plot["order_count"],
    marker='o', 
    linewidth=2,
    color="#0046AF"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Product performance
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#0046AF", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="total", y="product_category", data=best_seller.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="total", y="product_category", data=best_seller.sort_values(by="total", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)