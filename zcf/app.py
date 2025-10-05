import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from pygwalker.api.streamlit import StreamlitRenderer
from st_aggrid import AgGrid

st.set_page_config(
    page_title="NeoFinancial Analytics Pro",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50% }
        50% { background-position: 100% 50% }
        100% { background-position: 0% 50% }
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 30px;
        border-radius: 25px;
        margin-bottom: 40px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
        position: relative;
        overflow: hidden;
    }
    
    .main-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .main-header {
        font-size: 4rem;
        text-align: center;
        font-weight: 900;
        margin: 0;
        padding: 40px 0;
        font-family: 'Segoe UI', 'Inter', sans-serif;
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 30%, #e9ecef 70%, #dee2e6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 10px 30px rgba(0,0,0,0.3);
        position: relative;
        animation: textGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes textGlow {
        0% { text-shadow: 0 10px 30px rgba(0,0,0,0.3); }
        100% { text-shadow: 0 15px 40px rgba(255,255,255,0.4); }
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,249,250,0.8) 100%);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 
            0 15px 35px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.6);
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
        transition: left 0.7s;
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-12px) scale(1.03);
        box-shadow: 
            0 25px 50px rgba(102, 126, 234, 0.3),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, rgba(44, 62, 80, 0.95) 0%, rgba(52, 152, 219, 0.9) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 30px;
        text-align: center;
        font-weight: 700;
        font-size: 1.3rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: linear-gradient(135deg, rgba(248,249,250,0.9) 0%, rgba(233,236,239,0.8) 100%);
        padding: 15px;
        border-radius: 20px;
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background: linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(248,249,250,0.8) 100%);
        border-radius: 15px;
        padding: 15px 25px;
        font-weight: 700;
        border: 2px solid transparent;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        color: #2c3e50;
        position: relative;
        overflow: hidden;
    }
    
    .stTabs [data-baseweb="tab"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
        transition: left 0.5s;
    }
    
    .stTabs [data-baseweb="tab"]:hover::before {
        left: 100%;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #667eea;
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: #667eea;
        box-shadow: 0 15px 30px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    .stDownloadButton button {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        border: none;
        padding: 18px 32px;
        border-radius: 15px;
        font-weight: 800;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        width: 100%;
        box-shadow: 0 10px 25px rgba(39, 174, 96, 0.4);
        position: relative;
        overflow: hidden;
        font-size: 1.1rem;
    }
    
    .stDownloadButton button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s;
    }
    
    .stDownloadButton button:hover::before {
        left: 100%;
    }
    
    .stDownloadButton button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 0 20px 40px rgba(39, 174, 96, 0.6);
    }
    
    .chart-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(250,251,252,0.9) 100%);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 25px;
        box-shadow: 
            0 20px 40px rgba(0,0,0,0.1),
            inset 0 1px 0 rgba(255,255,255,0.8);
        margin-bottom: 30px;
        border: 1px solid rgba(255,255,255,0.4);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .chart-container::before {
        content: '';
        position: absolute;
        top: -10px;
        left: -10px;
        right: -10px;
        bottom: -10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        z-index: -1;
        border-radius: 30px;
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .chart-container:hover::before {
        opacity: 0.1;
    }
    
    .chart-container:hover {
        transform: translateY(-8px);
        box-shadow: 
            0 30px 60px rgba(0,0,0,0.15),
            inset 0 1px 0 rgba(255,255,255,0.9);
    }
    
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        border: 3px solid #f8f9fa;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .stat-card {
        background: linear-gradient(135deg, rgba(248,249,250,0.9) 0%, rgba(233,236,239,0.8) 100%);
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border-left: 6px solid;
        border-image: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) 1;
        margin: 15px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 15px 35px rgba(39, 174, 96, 0.2);
    }
    
    .insight-success {
        background: linear-gradient(135deg, rgba(212, 237, 218, 0.9) 0%, rgba(195, 230, 203, 0.8) 100%);
        border-left: 6px solid #28a745;
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 15px 35px rgba(40, 167, 69, 0.15);
        transition: all 0.4s ease;
    }
    
    .insight-warning {
        background: linear-gradient(135deg, rgba(255, 243, 205, 0.9) 0%, rgba(255, 234, 167, 0.8) 100%);
        border-left: 6px solid #ffc107;
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 15px 35px rgba(255, 193, 7, 0.15);
        transition: all 0.4s ease;
    }
    
    .insight-info {
        background: linear-gradient(135deg, rgba(209, 236, 241, 0.9) 0%, rgba(190, 229, 235, 0.8) 100%);
        border-left: 6px solid #17a2b8;
        padding: 25px;
        border-radius: 20px;
        margin: 15px 0;
        box-shadow: 0 15px 35px rgba(23, 162, 184, 0.15);
        transition: all 0.4s ease;
    }
    
    .footer {
        background: linear-gradient(135deg, rgba(44, 62, 80, 0.95) 0%, rgba(52, 73, 94, 0.9) 100%);
        backdrop-filter: blur(20px);
        color: white;
        padding: 50px;
        border-radius: 25px;
        text-align: center;
        margin-top: 50px;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        overflow: hidden;
    }
    
    .logo-container {
        animation: float3D 8s ease-in-out infinite;
    }
    
    @keyframes float3D {
        0%, 100% { transform: translateY(0px) rotateX(0deg) rotateY(0deg); }
        25% { transform: translateY(-15px) rotateX(5deg) rotateY(5deg); }
        50% { transform: translateY(-5px) rotateX(-5deg) rotateY(-5deg); }
        75% { transform: translateY(-10px) rotateX(3deg) rotateY(-3deg); }
    }
    
    .stSelectbox > div > div, .stMultiSelect > div > div {
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
    }
    
    .stSelectbox > div > div:hover, .stMultiSelect > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)
col_img, col_title = st.columns([1, 4])

with col_img:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("data/a.png", width=600)
    except:
        st.markdown("""
        <div style='width: 180px; height: 120px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 25px; display: flex; align-items: center; justify-content: center; 
                    color: white; font-weight: bold; font-size: 28px; box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
                    animation: pulse 2s ease-in-out infinite;'>
            ✨
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_title:
    st.markdown('<h1 class="main-header">NEOFINANCIAL ANALYTICS PRO</h1>', unsafe_allow_html=True)
    st.markdown("""
    <p style='text-align: center; color: rgba(255,255,255,0.95); font-size: 1.4rem; margin-top: -15px; 
               font-weight: 300; letter-spacing: 2px; text-shadow: 0 5px 15px rgba(0,0,0,0.3); margin: 50px'>
        Jangan Menghakimi Diri Sendiri Sebagai Sosok Yang Gagal Kau Sedang Belajar dan dalam proses belajar kesalahan adalah mutlak
    </p>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 🚀 INTERACTIVE DATA EXPLORER")
with st.container():
    st.markdown("""
    <div style='background: linear-gradient(135deg, rgba(255,255,255,0.15) 0%, rgba(248,249,250,0.1) 100%); 
                backdrop-filter: blur(20px); padding: 25px; border-radius: 20px; 
                border-left: 6px solid #667eea; margin-bottom: 25px; border: 1px solid rgba(255,255,255,0.2);'>
        <h4 style='margin: 0; color: white; font-weight: 700;'>🚀 Adina ajha</h4>
        <p style='margin: 10px 0 0 0; color: rgba(255,255,255,0.9);'>Jangan Menghakimi Diri Sendiri Sebagai Sosok Yang Gagal Kau Sedang Belajar Dan Dalam Proses Belajar Kesalahan Adalah Mutlak</p>
    </div>
    """, unsafe_allow_html=True)
    
    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        df = pd.read_csv("data.csv")
        return StreamlitRenderer(df, spec="./gw_config.json", spec_io_mode="rw")
    
    try:
        renderer = get_pyg_renderer()
        renderer.explorer()
    except Exception as e:
        st.error(f"PyGWalker Error: {e}")
        st.info("Using traditional dashboard as fallback...")

df = pd.read_csv('data.csv')
AgGrid(df)

@st.cache_data
def load_sample_data():
    """Load sample data based on your structure"""
    data = {
        'Business Unit': ['Software'] * 12,
        'Account': ['Sales'] * 12,
        'Currency': ['USD'] * 12,
        'Year': [2024] * 12,
        'Scenario': ['Actuals'] * 12,
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Amount': [90924002, 82606134, 72780220, 52943701, 77528109, 96384524,
                  77345061, 98290873, 79879127, 95373403, 54887908, 8270359]
    }
    return pd.DataFrame(data)

with st.sidebar:
    st.markdown('<div class="stInfo">📤 UPLOAD DATA</div>', unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Pilih file CSV/Excel", 
        type=['csv', 'xlsx', 'xls'],
        help="Unggah file data Anda untuk dianalisis"
    )

    if uploaded_file is not None:
        try:
            with st.spinner('🔄 Memproses data...'):
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
            st.success("✅ File berhasil diunggah!")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            df = load_sample_data()
    else:
        df = load_sample_data()
        st.info("ℹ️ Menggunakan data contoh")

def preprocess_data(df):
    """Preprocess the dataframe"""
    df_clean = df.copy()
    
    month_columns = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    if any(month in df.columns for month in month_columns):
        available_months = [col for col in month_columns if col in df.columns]
        id_vars = [col for col in df.columns if col not in available_months]
        
        df_clean = df.melt(
            id_vars=id_vars,
            value_vars=available_months,
            var_name='Month',
            value_name='Amount'
        )
    
    df_clean['Amount'] = pd.to_numeric(df_clean['Amount'], errors='coerce')
    
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    df_clean['Month'] = pd.Categorical(df_clean['Month'], categories=month_order, ordered=True)
    
    return df_clean

df_processed = preprocess_data(df)

with st.sidebar:
    st.markdown('<div class="stInfo">🔍 FILTER DATA</div>', unsafe_allow_html=True)
    
    available_accounts = df_processed['Account'].unique() if 'Account' in df_processed.columns else ['Sales']
    selected_accounts = st.multiselect(
        "Pilih Akun",
        options=available_accounts,
        default=available_accounts,
        help="Pilih satu atau beberapa akun untuk dianalisis"
    )

    if 'Scenario' in df_processed.columns:
        available_scenarios = df_processed['Scenario'].unique()
        selected_scenario = st.selectbox(
            "Pilih Skenario",
            options=available_scenarios,
            help="Pilih skenario bisnis yang ingin dianalisis"
        )

    if 'Year' in df_processed.columns:
        available_years = sorted(df_processed['Year'].unique())
        selected_year = st.selectbox(
            "Pilih Tahun",
            options=available_years,
            help="Pilih tahun untuk analisis"
        )

filtered_df = df_processed.copy()
if 'Account' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Account'].isin(selected_accounts)]
if 'Scenario' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Scenario'] == selected_scenario]
if 'Year' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Year'] == selected_year]

st.markdown("### 🔍 ANALISIS DETAIL")

tab1, tab2, tab3 = st.tabs(["📋 DATA TABEL", "📊 STATISTIK", "💡 INSIGHTS"])

with tab1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 📋 DATA TERFILTER")
    
    display_df = filtered_df.sort_values('Month').copy()
    display_df['Amount'] = display_df['Amount'].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(display_df, use_container_width=True, height=400)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 UNDUH DATA SEBAGAI CSV",
        data=csv,
        file_name="financial_data_analysis.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("### 📊 INDIKATOR KINERJA UTAMA")

total_amount = filtered_df['Amount'].sum()
average_monthly = filtered_df['Amount'].mean()
max_amount = filtered_df['Amount'].max() if not filtered_df.empty else 0
min_amount = filtered_df['Amount'].min() if not filtered_df.empty else 0
max_month = filtered_df.loc[filtered_df['Amount'].idxmax(), 'Month'] if not filtered_df.empty else 'N/A'
min_month = filtered_df.loc[filtered_df['Amount'].idxmin(), 'Month'] if not filtered_df.empty else 'N/A'

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="💰 TOTAL PENDAPATAN",
        value=f"${total_amount:,.0f}",
        delta=f"${max_amount:,.0f} (Peak)"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="📅 RATA-RATA BULANAN",
        value=f"${average_monthly:,.0f}",
        delta=f"${(max_amount - average_monthly):,.0f} above avg"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="🚀 BULAN TERBAIK",
        value=str(max_month),
        delta=f"${max_amount:,.0f}"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric(
        label="📉 BULAN TERENDAH",
        value=str(min_month),
        delta=f"${min_amount:,.0f}",
        delta_color="inverse"
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style='height: 3px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            border-radius: 10px; margin: 40px 0;'></div>
""", unsafe_allow_html=True)

st.markdown("### 📈 ANALISIS VISUAL")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 📈 TREN PENDAPATAN BULANAN")
    
    monthly_data = filtered_df.groupby('Month', as_index=False)['Amount'].sum()
    
    # Gunakan Streamlit native chart sebagai pengganti Plotly
    st.line_chart(monthly_data.set_index('Month')['Amount'], height=400)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 📊 PERBANDINGAN BULANAN")
    
    # Gunakan Streamlit native bar chart
    st.bar_chart(monthly_data.set_index('Month')['Amount'], height=400)
    st.markdown('</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 💰 PENDAPATAN KUMULATIF")
    
    monthly_data['Cumulative'] = monthly_data['Amount'].cumsum()
    st.area_chart(monthly_data.set_index('Month')['Cumulative'], height=400)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 📅 PERFORMANCE BULANAN")
    
    monthly_data['Performance'] = monthly_data['Amount'] - average_monthly
    st.bar_chart(monthly_data.set_index('Month')['Performance'], height=400)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 📊 ANALISIS STATISTIK")
    
    if not filtered_df.empty:
        stats = filtered_df['Amount'].describe()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Count", f"{stats['count']:,.0f}")
            st.metric("Mean", f"${stats['mean']:,.2f}")
            st.metric("Std Dev", f"${stats['std']:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="stat-card">', unsafe_allow_html=True)
            st.metric("Min", f"${stats['min']:,.2f}")
            st.metric("25%", f"${stats['25%']:,.2f}")
            st.metric("50%", f"${stats['50%']:,.2f}")
            st.metric("75%", f"${stats['75%']:,.2f}")
            st.metric("Max", f"${stats['max']:,.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("#### 📈 METRIK TAMBAHAN")
        col3, col4, col5 = st.columns(3)
        
        with col3:
            st.metric("Varians", f"${filtered_df['Amount'].var():,.0f}")
        with col4:
            st.metric("Range", f"${filtered_df['Amount'].max() - filtered_df['Amount'].min():,.0f}")
        with col5:
            cv = (filtered_df['Amount'].std() / filtered_df['Amount'].mean()) * 100
            st.metric("Coef of Variation", f"{cv:.2f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown("#### 💡 INSIGHTS BISNIS")
    
    if not filtered_df.empty:
        monthly_totals = filtered_df.groupby('Month')['Amount'].sum()
        growth_rate = ((monthly_totals.iloc[-1] - monthly_totals.iloc[0]) / monthly_totals.iloc[0]) * 100
        best_month = monthly_totals.idxmax()
        worst_month = monthly_totals.idxmin()
   
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            st.markdown('<div class="insight-success">', unsafe_allow_html=True)
            st.markdown("**🎯 PERFORMANCE HIGHLIGHTS**")
            st.write(f"**📈 Pertumbuhan Tahunan:** {growth_rate:+.1f}%")
            st.write(f"**🏆 Bulan Terbaik:** {best_month} (${monthly_totals.max():,.0f})")
            st.write(f"**📉 Bulan Terendah:** {worst_month} (${monthly_totals.min():,.0f})")
            st.write(f"**💰 Total Volume:** ${total_amount:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="insight-info">', unsafe_allow_html=True)
            st.markdown("**📊 INDIKATOR BULANAN**")
            for month, amount in monthly_totals.items():
                performance = "✅ Above Avg" if amount > average_monthly else "⚠️ Below Avg"
                st.write(f"{month}: ${amount:,.0f} {performance}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with insight_col2:
            st.markdown('<div class="insight-warning">', unsafe_allow_html=True)
            st.markdown("**🚀 REKOMENDASI STRATEGIS**")
            st.write("**1. Optimalkan Bulan Puncak**")
            st.write("   - Analisis faktor kesuksesan di bulan", best_month)
            st.write("   - Replikasi strategi ke bulan lainnya")
            
            st.write("**2. Tingkatkan Performa Bulan Rendah**")
            st.write("   - Identifikasi penyebab di bulan", worst_month)
            st.write("   - Implementasi program improvement")
            
            st.write("**3. Ekspansi Model Sukses**")
            st.write("   - Scale up strategi yang terbukti efektif")
            st.write("   - Monitoring berkelanjutan")
            
            st.write("**4. Optimasi Alokasi Resource**")
            st.write("   - Sesuaikan dengan pola seasonal")
            st.write("   - Improve resource utilization")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with st.sidebar:
    with st.expander("🔧 INFO SISTEM", expanded=False):
        st.write("**📊 STATUS DATA:**")
        st.success(f"✓ Records: {filtered_df.shape[0]:,}")
        st.info(f"📈 Columns: {len(filtered_df.columns)}")
        st.warning(f"💾 Memory: {filtered_df.memory_usage(deep=True).sum() / 1024 ** 2:.2f} MB")
        st.write(f"**🔄 DATA UPDATE:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

st.markdown("---")
st.markdown(
    """
    <div class="footer">
        <h3 style='margin: 0; position: relative;'>✨ Motivasi Hari Ini</h3>
        <p style='margin: 15px 0 0 0; opacity: 0.95; font-size: 1.1rem; position: relative;'>
        by Adina Ajha | Enterprise-Grade Business Intelligence
        </p>
        <p style='margin: 10px 0 0 0; opacity: 0.8; font-size: 1rem; position: relative;'>
        "Transforming Data into Strategic Insights for Tomorrow's Leaders"
        </p>
        <div style='margin-top: 20px; position: relative;'>
            <span style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 8px 20px; border-radius: 20px; font-size: 0.9rem;'>
                🚀 AI-Powered Analytics
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)