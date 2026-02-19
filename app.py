import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import time
from data_manager import generate_fake_data, get_kpi_metrics

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="LUKOIL STRATEGIC DASHBOARD v3.0",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. DESIGN SYSTEM (AutoGravity 3.0)
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600&family=JetBrains+Mono:wght@400&display=swap');

    /* A. GLOBAL THEME */
    .stApp {
        background-color: #0f0f12;
        color: #e0e0e0;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600;
        color: #ffffff;
    }
    
    div, p, label, span {
        font-family: 'Space Grotesk', sans-serif;
    }

    /* B. METRICS & DATA */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #0bda68 !important; /* Safety Green */
        font-size: 28px !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #888888 !important;
        font-size: 14px !important;
    }

    /* C. GLASSMORPHISM CARD EFFECT */
    .glass-card {
        background: rgba(27, 38, 49, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }

    /* D. SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0a0a0c;
        border-right: 1px solid #1B2631;
    }
    
    /* E. TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 16px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.03);
        border-radius: 8px;
        color: #888;
        padding: 8px 16px;
        border: 1px solid transparent;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #C0392B; /* Lukoil Red */
        color: white;
        border: 1px solid #C0392B;
    }

    /* F. PLOTLY CHART BACKGROUND */
    .js-plotly-plot .plotly .main-svg {
        background: transparent !important;
    }
    
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. DATA LOADING
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    df = generate_fake_data(n=4000)
    return df

with st.spinner("Initializing AutoGravity Engine... Establishing Secure Connection..."):
    df = load_data()
    # Simulate a small delay for "tech" feel
    time.sleep(0.8)

# Calculate Global Metrics
total_rows, total_brands, avg_price_global, price_gap_global = get_kpi_metrics(df)

# -----------------------------------------------------------------------------
# 4. SIDEBAR LOGIC
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Lukoil_Logo.svg/1200px-Lukoil_Logo.svg.png", width=120)  # Placeholder or local asset if available
    st.markdown("### STRATEGIC DASHBOARD v3.0")
    st.markdown("---")
    
    st.subheader("Control Panel")
    
    # Filters
    selected_region = st.multiselect("Region", df['Region'].unique(), default=df['Region'].unique())
    selected_brands = st.multiselect("Brand Watchlist", df['Brand'].unique(), default=df['Brand'].unique()[:5])
    selected_segment = st.selectbox("Market Segment", ["All"] + list(df['Category'].unique()))
    
    # Apply Filters
    df_filtered = df[df['Region'].isin(selected_region)]
    if selected_brands:
        df_filtered = df_filtered[df_filtered['Brand'].isin(selected_brands)]
    if selected_segment != "All":
        df_filtered = df_filtered[df_filtered['Category'] == selected_segment]
        
    st.markdown("---")
    st.caption("AutoGravity Analytics Node • Online")
    st.caption("Last Sync: 2026-02-19 14:02:11")

# -----------------------------------------------------------------------------
# 5. MAIN LAYOUT
# -----------------------------------------------------------------------------

# Custom Title
st.markdown('<h1 style="font-size: 42px; margin-bottom: 0px;">LUKOIL <span style="color: #C0392B;">INTELLIGENCE</span> NETWORK</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #888; margin-bottom: 32px;">Real-time pricing dynamics & competitive landscape simulation.</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "EXECUTIVE OVERVIEW", 
    "DIGITAL VS PHYSICAL", 
    "COMPETITIVE MATRIX", 
    "SCIENTIFIC TERMINAL"
])

# --- TAB 1: EXECUTIVE OVERVIEW ---
with tab1:
    st.markdown("### The Big Picture")
    
    # KPI Cards Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Items Monitored", f"{len(df_filtered):,}", delta="140 new items")
    with c2:
        st.metric("Brand Coverage", f"{df_filtered['Brand'].nunique()} / 24", delta="100% Active")
    with c3:
        st.metric("Avg. Market Price", f"${df_filtered['Price'].mean():.2f}", delta="-2.4%")
    with c4:
        # Calculate dynamic gap for filtered view
        phys = df_filtered[df_filtered['Channel']=='Physical']['Price'].mean()
        digi = df_filtered[df_filtered['Channel']=='Digital']['Price'].mean()
        gap = ((phys - digi) / digi) * 100 if digi > 0 else 0
        st.metric("Physical Premium Gap", f"{gap:.1f}%", delta="Target: 8%")

    st.markdown("---")
    
    # Charts Row
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Price Trend Projection (Q1 2026)")
        # Resample by date to show trend
        daily_avg = df_filtered.groupby('Date')['Price'].mean().reset_index()
        fig_trend = px.line(daily_avg, x='Date', y='Price', 
                            title=None, 
                            markers=True,
                            line_shape='spline',
                            template='plotly_dark')
        fig_trend.update_traces(line_color='#0bda68', line_width=3)
        fig_trend.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col_right:
        st.subheader("Share by Brand Volume")
        # Top 10 brands
        top_brands = df_filtered['Brand'].value_counts().head(10).reset_index()
        top_brands.columns = ['Brand', 'Count']
        fig_bar = px.bar(top_brands, x='Count', y='Brand', orientation='h',
                         template='plotly_dark',
                         color_discrete_sequence=['#C0392B'])
        fig_bar.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 2: DIGITAL VS PHYSICAL ---
with tab2:
    st.markdown("### Channel Gap Analysis")
    
    row1_c1, row1_c2 = st.columns([3, 2])
    
    with row1_c1:
        st.subheader("Geospatial Heatmap: CDMX & Puebla")
        # Simple Mapbox
        fig_map = px.density_mapbox(df_filtered, lat='Latitude', lon='Longitude', z='Price', radius=8,
                                    center=dict(lat=19.43, lon=-99.13), zoom=6,
                                    mapbox_style="carto-darkmatter",
                                    template="plotly_dark")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_map, use_container_width=True)
        
    with row1_c2:
        st.subheader("Price Correlation: Online vs Store")
        # Scatter plot
        # Need to pivot data a bit? Or just show distribution. 
        # Let's show Price vs Brand colored by Channel
        fig_scatter = px.box(df_filtered, x='Brand', y='Price', color='Channel',
                             color_discrete_map={'Digital': '#0bda68', 'Physical': '#C0392B'},
                             template='plotly_dark')
        fig_scatter.update_layout(legend=dict(orientation="h", y=1.1, x=0.5, xanchor='center'), margin=dict(l=0,r=0,t=30,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_scatter, use_container_width=True)
        
    st.markdown("#### Bundle Intelligence")
    # Quick metric for bundle vs individual
    bundle_pct = (len(df_filtered[df_filtered['Product_Type']=='Bundle']) / len(df_filtered)) * 100
    st.progress(bundle_pct / 100)
    st.caption(f"{bundle_pct:.1f}% of inventory is sold as Bundles/Kits")

# --- TAB 3: COMPETITIVE MATRIX ---
with tab3:
    st.markdown("### Deep Dive Data Grid")
    
    col_search, col_spacer = st.columns([1, 2])
    with col_search:
        search_term = st.text_input("Search SKU Name...", placeholder="e.g. 5W-30")
        
    if search_term:
        filtered_view = df_filtered[df_filtered['SKU_Name'].str.contains(search_term, case=False)]
    else:
        filtered_view = df_filtered
        
    st.dataframe(
        filtered_view[['Brand', 'Product_Type', 'Category', 'Channel', 'Price', 'Region', 'SKU_Name']],
        use_container_width=True,
        height=500
    )

# --- TAB 4: SCIENTIFIC TERMINAL ---
with tab4:
    st.markdown("### System Logs & Extraction Protocol")
    
    st.markdown("""
    <div style="background-color: #000; color: #0f0; padding: 20px; border-radius: 8px; font-family: 'Courier New', monospace; height: 400px; overflow-y: scroll; border: 1px solid #333;">
        <p>[2026-02-19 14:00:01] <span style="color: yellow;">WARN</span>: Initializing Puppeteer cluster (Headless: True)...</p>
        <p>[2026-02-19 14:00:02] INFO: Connected to BrightData Proxy Network (Resdiential IPs).</p>
        <p>[2026-02-19 14:00:05] INFO: Target: homedepot.com.mx/lubricantes...</p>
        <p>[2026-02-19 14:00:08] <span style="color: #0f0;">SUCCESS</span>: Extracted 42 SKUs from Page 1.</p>
        <p>[2026-02-19 14:00:12] INFO: Target: amazon.com.mx/motor-oil...</p>
        <p>[2026-02-19 14:00:15] <span style="color: #0f0;">SUCCESS</span>: Extracted 115 SKUs from Page 1.</p>
        <p>[2026-02-19 14:00:16] INFO: Solving CAPTCHA (ReCaptcha V3)...</p>
        <p>[2026-02-19 14:00:18] <span style="color: #0f0;">SOLVED</span>: Access granted.</p>
        <p>[2026-02-19 14:00:22] INFO: Processing data normalization (Region: CDMX)...</p>
        <p>[2026-02-19 14:00:25] <span style="color: #0f0;">COMPLETE</span>: 4000 records synced to Data Lake.</p>
        <p>...</p>
        <p style="animation: blink 1s step-end infinite;">$ _</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.button("Rerun Extraction Pipeline (Simulated)")