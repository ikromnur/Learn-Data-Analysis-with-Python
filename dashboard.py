
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
daily_data = pd.read_csv("data_1.csv")
hourly_data = pd.read_csv("data_2.csv")

# Title and Description
st.title("Dashboard Penyewaan Sepeda")
st.write("Analisis data penyewaan sepeda berdasarkan cuaca dan musim, menggunakan data harian dan jam.")

# Sidebar options to select data granularity
data_option = st.sidebar.selectbox("Pilih Tingkat Analisis:", ["Data Harian", "Data Jam"])

# Common Filters
season_filter = st.sidebar.multiselect(
    "Filter Berdasarkan Musim:",
    options=daily_data["season"].unique(),
    default=daily_data["season"].unique()
)

weather_filter = st.sidebar.multiselect(
    "Filter Berdasarkan Cuaca:",
    options=daily_data["weathersit"].unique(),
    default=daily_data["weathersit"].unique()
)

# Apply filters
if data_option == "Data Harian":
    st.subheader("Analisis Harian")
    filtered_data = daily_data[(daily_data["season"].isin(season_filter)) & 
                               (daily_data["weathersit"].isin(weather_filter))]

    # Visualization: Pengaruh Cuaca terhadap Peminjaman Sepeda
    st.subheader("Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda (Harian)")
    weather_grouped = filtered_data.groupby("weathersit")["cnt"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.bar(weather_grouped["weathersit"], weather_grouped["cnt"], color="skyblue")
    ax.set_xlabel("Situasi Cuaca")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.set_title("Pengaruh Cuaca terhadap Jumlah Peminjaman")
    st.pyplot(fig)

    # Visualization: Peminjaman Sepeda Berdasarkan Musim
    st.subheader("Jumlah Peminjaman Sepeda Berdasarkan Musim (Harian)")
    season_grouped = filtered_data.groupby("season")["cnt"].sum().reset_index()
    fig, ax = plt.subplots()
    ax.bar(season_grouped["season"], season_grouped["cnt"], color="orange")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Jumlah Peminjaman Sepeda Berdasarkan Musim")
    st.pyplot(fig)

elif data_option == "Data Jam":
    st.subheader("Analisis Jam")
    filtered_data = hourly_data[(hourly_data["season"].isin(season_filter)) & 
                                (hourly_data["weathersit"].isin(weather_filter))]

    # Visualization: Pengaruh Cuaca terhadap Peminjaman Sepeda
    st.subheader("Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda (Jam)")
    weather_grouped = filtered_data.groupby("weathersit")["cnt"].mean().reset_index()
    fig, ax = plt.subplots()
    ax.bar(weather_grouped["weathersit"], weather_grouped["cnt"], color="green")
    ax.set_xlabel("Situasi Cuaca")
    ax.set_ylabel("Rata-rata Jumlah Peminjaman")
    ax.set_title("Pengaruh Cuaca terhadap Jumlah Peminjaman")
    st.pyplot(fig)

    # Visualization: Peminjaman Sepeda Berdasarkan Jam dan Musim
    st.subheader("Jumlah Peminjaman Sepeda Berdasarkan Jam dan Musim")
    hourly_grouped = filtered_data.groupby(["hr", "season"])["cnt"].sum().unstack()
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_grouped.plot(kind="line", ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Total Peminjaman")
    ax.set_title("Jumlah Peminjaman Sepeda Berdasarkan Jam dan Musim")
    st.pyplot(fig)

# Insights Section
st.subheader("Insights")
st.write("1. Cuaca cerah cenderung meningkatkan jumlah peminjaman sepeda, baik harian maupun jam.")
st.write("2. Musim panas memiliki tingkat peminjaman tertinggi, terutama pada siang hari.")
