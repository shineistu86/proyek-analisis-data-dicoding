import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

# 1. Menyiapkan Data
day_df = pd.read_csv("main_data.csv")
hour_df = pd.read_csv("hour_data.csv")

# Memastikan kolom dteday bertipe datetime
day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

# 2. Membuat Komponen Filter di Sidebar
min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("data:image/png;base64,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")
    st.markdown("## Bike Sharing Dashboard")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data
main_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date)) &
    (day_df["dteday"] <= pd.to_datetime(end_date))
]

main_hour_df = hour_df[
    (hour_df["dteday"] >= pd.to_datetime(start_date)) &
    (hour_df["dteday"] <= pd.to_datetime(end_date))
]

# 3. Dashboard
st.header('Bike Sharing Dashboard')

# Metrik utama
st.subheader('Daily Sharing Metrics')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = main_df["cnt"].sum()
    st.metric("Total Rides", value=f"{total_orders:,}")

with col2:
    total_registered = main_df["registered"].sum()
    st.metric("Registered Users", value=f"{total_registered:,}")

with col3:
    total_casual = main_df["casual"].sum()
    st.metric("Casual Users", value=f"{total_casual:,}")

st.markdown("---")


# Visualisasi 1

st.subheader("Pengaruh Musim & Cuaca Terhadap Penyewaan")

fig1, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

# Plot 1: Season
sns.barplot(
    x="season",
    y="cnt",
    data=main_df,
    palette="viridis",
    errorbar=None,
    ax=ax1[0]
)
ax1[0].set_title("Rata-rata Penyewaan Berdasarkan Musim", fontsize=15)
ax1[0].set_xlabel("Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)")
ax1[0].set_ylabel("Rata-rata Penyewaan")

# Plot 2: Weather
sns.barplot(
    x="weathersit",
    y="cnt",
    data=main_df,
    palette="coolwarm",
    errorbar=None,
    ax=ax1[1]
)
ax1[1].set_title("Rata-rata Penyewaan Berdasarkan Kondisi Cuaca", fontsize=15)
ax1[1].set_xlabel("Cuaca (1: Cerah, 2: Mendung, 3: Hujan/Salju)")
ax1[1].set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig1)

# Visualisasi 2

st.subheader("Tren Penyewaan Sepeda per Jam (Hari Kerja vs Libur)")

fig2, ax2 = plt.subplots(figsize=(14, 6))

sns.lineplot(
    x="hr",
    y="cnt",
    hue="workingday",
    data=main_hour_df,
    palette=["#FF6F61", "#4169E1"],
    linewidth=2.5,
    errorbar=None,
    ax=ax2
)

ax2.set_title("Tren Penyewaan: Hari Kerja vs Libur", fontsize=18)
ax2.set_xlabel("Jam (00:00 - 23:00)")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_xticks(range(0, 24))
ax2.legend(title="Kategori Hari", labels=["Hari Libur", "Hari Kerja"])
ax2.grid(True, alpha=0.3)

st.pyplot(fig2)

# Visualisasi 3

st.subheader("Analisis Lanjutan: Pengaruh Kategori Suhu (Clustering)")

fig3, ax3 = plt.subplots(figsize=(10, 5))

# Membuat kategori suhu jika belum ada
if "temp_category" not in main_df.columns:
    def classify_temp(temp):
        if temp < 0.33:
            return "Dingin"
        elif temp < 0.66:
            return "Sejuk"
        else:
            return "Panas"

    main_df["temp_category"] = main_df["temp"].apply(classify_temp)

sns.barplot(
    x="temp_category",
    y="cnt",
    data=main_df,
    palette="YlOrRd",
    order=["Dingin", "Sejuk", "Panas"],
    errorbar=None,
    ax=ax3
)

ax3.set_title("Rata-rata Penyewaan Berdasarkan Suhu", fontsize=15)
ax3.set_xlabel("Kategori Suhu")
ax3.set_ylabel("Rata-rata Penyewaan")

st.pyplot(fig3)