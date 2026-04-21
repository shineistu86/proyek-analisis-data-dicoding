import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='darkgrid')

PRIMARY_COLOR = "#3B82F6"
SECONDARY_COLOR = "#10B981"
ACCENT_COLOR = "#F59E0B"
DANGER_COLOR = "#EF4444"

season_palette = {
    "Spring": "#22C55E",
    "Summer": "#F59E0B",
    "Fall": "#D97706",
    "Winter": "#3B82F6"
}

weather_palette = {
    "Cerah": "#60A5FA",
    "Mendung": "#94A3B8",
    "Hujan/Salju": "#1E3A8A"
}

temp_palette = {
    "Dingin": "#1D4ED8",
    "Sejuk": "#10B981",
    "Panas": "#EF4444"
}

day_df = pd.read_csv("main_data.csv")
hour_df = pd.read_csv("hour_data.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
weather_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan/Salju"}

day_df["season_label"] = day_df["season"].map(season_mapping)
day_df["weather_label"] = day_df["weathersit"].map(weather_mapping)

hour_df['day_type'] = hour_df['workingday'].map({
    1: 'Hari Kerja',
    0: 'Hari Libur'
})

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.markdown("## Filter Data")
    st.caption("Sesuaikan tampilan data sesuai kebutuhan analisis")

    start_date, end_date = st.date_input(
        "Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    selected_season = st.multiselect(
        "Musim",
        options=sorted(day_df["season_label"].dropna().unique()),
        default=sorted(day_df["season_label"].dropna().unique())
    )

    selected_weather = st.multiselect(
        "Cuaca",
        options=day_df["weather_label"].dropna().unique(),
        default=day_df["weather_label"].dropna().unique()
    )

main_df = day_df[
    (day_df["dteday"] >= pd.to_datetime(start_date)) &
    (day_df["dteday"] <= pd.to_datetime(end_date)) &
    (day_df["season_label"].isin(selected_season)) &
    (day_df["weather_label"].isin(selected_weather))
].copy()

main_hour_df = hour_df[
    (hour_df["dteday"] >= pd.to_datetime(start_date)) &
    (hour_df["dteday"] <= pd.to_datetime(end_date))
].copy()

if main_df.empty:
    st.warning("Tidak ada data pada filter yang dipilih.")
    st.stop()

st.title("Bike Sharing Analytics Dashboard")
st.caption("Analisis perilaku pengguna untuk mengoptimalkan distribusi sepeda berdasarkan musim, cuaca, dan waktu.")

st.divider()

st.subheader("Overview Kinerja Penyewaan")

col1, col2, col3 = st.columns(3)

with col1:
    total = main_df['cnt'].sum()
    st.metric("Total Rides", f"{total:,}")
    st.caption("Total penyewaan dalam periode terpilih")

with col2:
    reg = main_df['registered'].sum()
    st.metric("Registered Users", f"{reg:,}")
    st.caption("Pengguna tetap mendominasi")

with col3:
    casual = main_df['casual'].sum()
    st.metric("Casual Users", f"{casual:,}")
    st.caption("Cenderung fluktuatif")

st.divider()

st.subheader("Pengaruh Musim & Cuaca")

fig1, ax1 = plt.subplots(1, 2, figsize=(16, 6))

sns.barplot(
    x="season_label",
    y="cnt",
    hue="season_label",
    data=main_df,
    palette=season_palette,
    order=["Spring", "Summer", "Fall", "Winter"],
    errorbar=None,
    legend=False,
    dodge=False,
    ax=ax1[0]
)

ax1[0].set_title("Rata-rata Penyewaan Berdasarkan Musim")
ax1[0].set_xlabel("")
ax1[0].set_ylabel("Rata-rata")

sns.barplot(
    x="weather_label",
    y="cnt",
    hue="weather_label",
    data=main_df,
    palette=weather_palette,
    errorbar=None,
    legend=False,
    dodge=False,
    ax=ax1[1]
)

ax1[1].set_title("Rata-rata Penyewaan Berdasarkan Cuaca")
ax1[1].set_xlabel("")
ax1[1].set_ylabel("")

st.pyplot(fig1)

st.info(
    "Musim Fall secara konsisten menghasilkan demand tertinggi, menjadikannya periode krusial untuk optimasi distribusi. "
    "Sebaliknya, kondisi hujan atau salju menurunkan penggunaan secara signifikan sehingga perlu strategi mitigasi."
)

st.divider()

st.subheader("Pola Penggunaan Harian")

fig2, ax2 = plt.subplots(figsize=(14, 6))

sns.lineplot(
    x="hr",
    y="cnt",
    hue="day_type",
    data=main_hour_df,
    palette=[PRIMARY_COLOR, DANGER_COLOR],
    linewidth=2.5,
    errorbar=None,
    ax=ax2
)

ax2.set_title("Hari Kerja vs Hari Libur")
ax2.set_xlabel("Jam")
ax2.set_ylabel("Rata-rata Penyewaan")
ax2.set_xticks(range(0, 24))
ax2.grid(True, alpha=0.3)

st.pyplot(fig2)

st.info(
    "Pola komuter terlihat jelas pada hari kerja dengan lonjakan di pagi dan sore hari. "
    "Ini menunjukkan kebutuhan distribusi sepeda yang sinkron dengan mobilitas kerja."
)

st.divider()

st.subheader("Pengaruh Suhu")

def classify_temp(temp):
    if temp < 0.33:
        return "Dingin"
    elif temp < 0.66:
        return "Sejuk"
    else:
        return "Panas"

main_df["temp_category"] = main_df["temp"].apply(classify_temp)

fig3, ax3 = plt.subplots(figsize=(10, 5))

sns.barplot(
    x="temp_category",
    y="cnt",
    hue="temp_category",
    data=main_df,
    palette=temp_palette,
    order=["Dingin", "Sejuk", "Panas"],
    errorbar=None,
    legend=False,
    dodge=False,
    ax=ax3
)

ax3.set_title("Rata-rata Penyewaan Berdasarkan Suhu")
ax3.set_xlabel("")
ax3.set_ylabel("Rata-rata")

st.pyplot(fig3)

st.success(
    "Suhu sejuk menjadi kondisi paling optimal. Distribusi sepeda sebaiknya difokuskan pada kondisi ini untuk memaksimalkan utilisasi."
)

st.divider()

st.subheader("Rekomendasi")

st.markdown("""
- Tingkatkan distribusi sepeda saat **Summer & Fall**  
- Fokuskan operasional pada jam sibuk (07–09 & 17–19) di hari kerja  
- Optimalkan penempatan di area rekreasi saat akhir pekan  
- Jadwalkan maintenance saat demand rendah (Spring / cuaca buruk)  
""")
