import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv('dashboard/cleaned_day.csv')
hour_df = pd.read_csv('dashboard/cleaned_hour.csv')

# Sidebar untuk filter data
st.sidebar.title('Filter Data')
year_filter = st.sidebar.selectbox('Pilih Tahun', day_df['yr'].unique())
season_filter = st.sidebar.multiselect('Pilih Musim', day_df['season'].unique(), default=day_df['season'].unique())

# Filter data berdasarkan input user
filtered_data = day_df[(day_df['yr'] == year_filter) & (day_df['season'].isin(season_filter))]

# Dashboard layout
st.title('Dashboard Penyewaan Sepeda')

st.subheader('Data Penyewaan Sepeda')
st.write('Data di bawah ini sudah difilter berdasarkan tahun dan musim yang dipilih.')
st.dataframe(filtered_data.head())

# Visualisasi 1: Tren Penyewaan Sepeda
day_df['mnth'] = pd.Categorical(day_df['mnth'], categories=[
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
    ordered=True)
st.subheader('Tren Penyewaan Sepeda Bulanan')
monthly_counts = filtered_data.groupby(by=["mnth","yr"]).agg({"cnt": "sum"}).reset_index()
fig, ax = plt.subplots()
sns.lineplot(data=monthly_counts, x="mnth", y="cnt", hue="yr", palette="mako", marker="o", ax=ax)
ax.set_title("Tren Penyewaan Sepeda")
ax.set_xlabel(None)
ax.set_ylabel("Jumlah Penyewaan Sepeda")
st.pyplot(fig)

# Visualisasi 2: Korelasi Cuaca dan Penyewaan Sepeda
st.subheader('Korelasi Cuaca dan Penyewaan Sepeda')
correlation = filtered_data[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
fig, ax = plt.subplots()
sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
ax.set_title('Korelasi antara Cuaca dan Penyewaan Sepeda')
st.pyplot(fig)

# Visualisasi 3: Penyewaan per Jam
st.subheader('Rata-rata Penyewaan Sepeda per Jam')
hour_counts = hour_df.groupby(by="hr").agg({"cnt": "mean"}).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=hour_counts, x='hr', y='cnt', palette='viridis', ax=ax)
ax.set_title('Rata-rata Penyewaan Sepeda per Jam')
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Penyewaan Sepeda (Rata-rata)')
st.pyplot(fig)

# Visualisasi 4: Penyewaan Sepeda di Hari Libur vs Hari Kerja
st.subheader('Penyewaan Sepeda: Hari Libur vs Hari Kerja')
holiday_counts = filtered_data.groupby('holiday')['cnt'].sum().reset_index()
fig, ax = plt.subplots()
sns.barplot(data=holiday_counts, x='holiday', y='cnt', palette='coolwarm', ax=ax)
ax.set_title('Total Penyewaan Sepeda: Hari Libur vs Hari Kerja')
ax.set_xlabel('Hari Libur')
ax.set_ylabel('Jumlah Penyewaan Sepeda')
ax.set_xticks([0, 1])
ax.set_xticklabels(['Tidak', 'Ya'])
st.pyplot(fig)

# Visualisasi 5: Pengguna Kasual vs Terdaftar
st.subheader('Pengguna Kasual vs Terdaftar')
user_type_counts = filtered_data.groupby('workingday').agg({'casual': 'mean', 'registered': 'mean'}).reset_index()
user_type_counts = user_type_counts.melt(id_vars='workingday', var_name='User Type', value_name='Average Rentals')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=user_type_counts, x='workingday', y='Average Rentals', hue='User Type', palette='viridis', ax=ax)
ax.set_title('Perbandingan Penyewaan Sepeda: Pengguna Kasual vs Terdaftar')
ax.set_xlabel('Jenis Hari')
ax.set_ylabel('Rata-rata Penyewaan Sepeda')
ax.set_xticks([0, 1])
ax.set_xticklabels(['Holiday', 'Workingday'])
ax.legend(title='Tipe Pengguna')
st.pyplot(fig)