import streamlit as pd
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 1. Setup Konfigurasi Halaman (Mobile Friendly)
st.set_page_config(page_title="FRC Delivery Cost Dashboard", layout="tight")

st.title("📊 FRC - SG Facility Cost Dashboard")
st.write("Monitoring Realisasi vs RKAP Biaya Pengiriman")

# 2. Load Data
data = {
    'Kemasan': ['ZAK', 'ZAK', 'ZAK', 'ZAK', 'CURAH', 'CURAH', 'LAUT', 'LAUT'],
    'Provinsi': ['JAWA TENGAH', 'JAWA TIMUR', 'BALI', 'KALIMANTAN BARAT', 'JAWA TENGAH', 'JAWA TIMUR', 'AREA AP 4 (ZAK)', 'AREA AP 4 (CURAH)'],
    'Vol_RKAP': [105864, 236827, 30595, 6847, 9973, 7774, 6926, 540],
    'Biaya_RKAP': [9142701648, 25835544906, 2737387348, 1606679344, 1276422452, 1047332321, 1848856718, 0],
    'OA_Ton_RKAP': [86363, 109090, 89472, 234658, 127985, 134718, 266927, 0],
    'Vol_Realisasi': [55840, 76430, 10879, 2864, 14700, 14114, 94, 12514],
    'Biaya_Realisasi': [5050779764, 8132725248, 1144515860, 829111988, 3064535637, 2160156372, 4283580, 0],
    'OA_Ton_Realisasi': [90451, 106408, 105204, 289525, 208468, 153047, 45570, 0],
    'Persen_OA': [1.05, 0.98, 1.18, 1.23, 1.63, 1.14, 0.17, 0.0]
}

df = pd.DataFrame(data)

# 3. Filter Interaktif (Sangat mudah ditekan di HP)
st.sidebar.header("🎛️ Filter Data")
filter_kemasan = st.sidebar.multiselect("Pilih Jenis Kemasan:", options=df['Kemasan'].unique(), default=df['Kemasan'].unique())
filter_provinsi = st.sidebar.multiselect("Pilih Wilayah/Provinsi:", options=df['Provinsi'].unique(), default=df['Provinsi'].unique())

# Filter data berdasarkan input user
df_filtered = df[(df['Kemasan'].isin(filter_kemasan)) & (df['Provinsi'].isin(filter_provinsi))]

# 4. Ringkasan KPI Utama (Menyoroti Lonjakan)
st.subheader("📌 Ringkasan Efisiensi")
if not df_filtered.empty:
    total_rkap = df_filtered['Biaya_RKAP'].sum()
    total_realisasi = df_filtered['Biaya_Realisasi'].sum()
    total_persen = (total_realisasi / total_rkap * 100) if total_rkap > 0 else 0
    
    col1, col2 = st.columns(2)
    col1.metric("Total Realisasi Biaya", f"Rp {total_realisasi:,.0f}")
    col2.metric("Rata-rata % OA", f"{total_persen:.1f}%", delta=f"{total_persen-100:.1f}% vs Target", delta_color="inverse")

st.markdown("---")

# 5. Grafik 1: Perbandingan Volume RKAP vs Realisasi (Bar Chart Berdampingan)
st.subheader("📊 Volume: RKAP vs Realisasi")
if not df_filtered.empty:
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Bar(x=df_filtered['Provinsi'] + " (" + df_filtered['Kemasan'] + ")", y=df_filtered['Vol_RKAP'], name='RKAP Vol', marker_color='#1f77b4'))
    fig_vol.add_trace(go.Bar(x=df_filtered['Provinsi'] + " (" + df_filtered['Kemasan'] + ")", y=df_filtered['Vol_Realisasi'], name='Realisasi Vol', marker_color='#ff7f0e'))
    
    fig_vol.update_layout(barmode='group', xaxis_tickangle=-45, margin=dict(l=20, r=20, t=20, b=100), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_vol, use_container_width=True)
else:
    st.write("Tidak ada data yang cocok dengan filter.")

# 6. Grafik 2: Tren & Lonjakan Tarif OA / TON (Line + Scatter)
st.subheader("📈 Pantauan Tarif OA / TON")
if not df_filtered.empty:
    fig_oa = go.Figure()
    # Garis Target RKAP
    fig_oa.add_trace(go.Scatter(x=df_filtered['Provinsi'] + " (" + df_filtered['Kemasan'] + ")", y=df_filtered['OA_Ton_RKAP'], mode='lines+markers', name='Target (RKAP)', line=dict(dash='dash', color='gray')))
    # Realisasi Aktual
    fig_oa.add_trace(go.Scatter(x=df_filtered['Provinsi'] + " (" + df_filtered['Kemasan'] + ")", y=df_filtered['OA_Ton_Realisasi'], mode='lines+markers', name='Aktual (Realisasi)', line=dict(color='red', width=3)))
    
    fig_oa.update_layout(xaxis_tickangle=-45, margin=dict(l=20, r=20, t=20, b=100), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_oa, use_container_width=True)

# 7. Tabel Detail Otomatis di bawah
st.subheader("📋 Data Detail")
st.dataframe(df_filtered[['Kemasan', 'Provinsi', 'Vol_RKAP', 'Vol_Realisasi', 'OA_Ton_RKAP', 'OA_Ton_Realisasi', 'Persen_OA']])
