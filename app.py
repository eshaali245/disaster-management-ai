"""
=================================================
ResQ-AI: Disaster Management System - Dashboard
=================================================
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pickle
import json
import os
import time
import random
import psutil
from datetime import datetime
import sys
sys.path.insert(0, '.')

# ─── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="ResQ-AI Disaster Management",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Theme Session State ──────────────────────────────────
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# ─── Theme Variables ──────────────────────────────────────
def get_theme():
    if st.session_state.dark_mode:
        return {
            'bg_main'        : '#060d1a',
            'bg_gradient'    : 'linear-gradient(145deg, #060d1a 0%, #0c1829 40%, #060d1a 100%)',
            'bg_sidebar'     : 'linear-gradient(180deg, #080f1e 0%, #0c1829 100%)',
            'bg_card'        : 'rgba(14, 30, 54, 0.85)',
            'bg_card_hover'  : 'rgba(18, 38, 68, 0.95)',
            'glass'          : 'rgba(255,255,255,0.04)',
            'border_main'    : 'rgba(0, 200, 255, 0.18)',
            'border_glow'    : 'rgba(0, 200, 255, 0.35)',
            'text_main'      : '#dce8f8',
            'text_sub'       : '#6a9fcc',
            'text_muted'     : '#3a6a9a',
            'accent'         : '#00c8ff',
            'accent2'        : '#00ff88',
            'accent_red'     : '#ff3d5a',
            'accent_gold'    : '#ffcc00',
            'accent_orange'  : '#ff8c42',
            'accent_purple'  : '#b388ff',
            'plot_bg'        : 'rgba(6,13,26,0)',
            'paper_bg'       : 'rgba(6,13,26,0)',
            'grid_color'     : 'rgba(0,200,255,0.08)',
            'font_color'     : '#c0d8f0',
            'scroll_track'   : '#060d1a',
            'scroll_thumb'   : '#1a4a7a',
            'btn_bg'         : 'linear-gradient(135deg, #00c8ff 0%, #0077bb 100%)',
            'btn_color'      : '#060d1a',
            'btn_hover'      : 'linear-gradient(135deg, #00ff88 0%, #00aa55 100%)',
            'glow_blue'      : '0 0 30px rgba(0,200,255,0.25)',
            'glow_red'       : '0 0 30px rgba(255,61,90,0.25)',
            'glow_green'     : '0 0 30px rgba(0,255,136,0.25)',
            'glow_gold'      : '0 0 30px rgba(255,204,0,0.25)',
            'glow_purple'    : '0 0 30px rgba(179,136,255,0.25)',
            'toggle_label'   : '☀️  Light Mode',
            'toggle_icon'    : '🌙',
            'mode_name'      : 'DARK',
            'heatmap_cs'     : 'Blues',
            'tag_bg'         : 'rgba(0,200,255,0.12)',
            'tag_border'     : 'rgba(0,200,255,0.3)',
            'sidebar_item'   : 'rgba(0,200,255,0.06)',
        }
    else:
        return {
            'bg_main'        : '#f0f5fc',
            'bg_gradient'    : 'linear-gradient(145deg, #eaf1fb 0%, #f5f9ff 40%, #eaf1fb 100%)',
            'bg_sidebar'     : 'linear-gradient(180deg, #ffffff 0%, #e8f1fb 100%)',
            'bg_card'        : 'rgba(255,255,255,0.92)',
            'bg_card_hover'  : 'rgba(245,250,255,0.98)',
            'glass'          : 'rgba(255,255,255,0.6)',
            'border_main'    : 'rgba(0, 100, 200, 0.18)',
            'border_glow'    : 'rgba(0, 100, 200, 0.30)',
            'text_main'      : '#0f2040',
            'text_sub'       : '#3560a0',
            'text_muted'     : '#7090b8',
            'accent'         : '#0055cc',
            'accent2'        : '#008844',
            'accent_red'     : '#cc1133',
            'accent_gold'    : '#aa7700',
            'accent_orange'  : '#cc5500',
            'accent_purple'  : '#6633cc',
            'plot_bg'        : 'rgba(240,245,252,0)',
            'paper_bg'       : 'rgba(240,245,252,0)',
            'grid_color'     : 'rgba(0,80,180,0.1)',
            'font_color'     : '#0f2040',
            'scroll_track'   : '#eaf1fb',
            'scroll_thumb'   : '#90aacf',
            'btn_bg'         : 'linear-gradient(135deg, #0055cc 0%, #003399 100%)',
            'btn_color'      : '#ffffff',
            'btn_hover'      : 'linear-gradient(135deg, #008844 0%, #005522 100%)',
            'glow_blue'      : '0 4px 24px rgba(0,85,204,0.12)',
            'glow_red'       : '0 4px 24px rgba(200,20,50,0.12)',
            'glow_green'     : '0 4px 24px rgba(0,136,68,0.12)',
            'glow_gold'      : '0 4px 24px rgba(170,120,0,0.12)',
            'glow_purple'    : '0 4px 24px rgba(100,50,200,0.12)',
            'toggle_label'   : '🌙  Dark Mode',
            'toggle_icon'    : '☀️',
            'mode_name'      : 'LIGHT',
            'heatmap_cs'     : 'Blues',
            'tag_bg'         : 'rgba(0,85,204,0.08)',
            'tag_border'     : 'rgba(0,85,204,0.2)',
            'sidebar_item'   : 'rgba(0,85,204,0.05)',
        }

T = get_theme()

# ─── Inject CSS ──────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@700;800&display=swap');

/* ── Reset & Base ── */
html, body, [class*="css"] {{
    background-color: {T['bg_main']} !important;
    color: {T['text_main']} !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 17px !important;
}}
.stApp {{ background: {T['bg_gradient']} !important; min-height: 100vh; }}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {T['bg_sidebar']} !important;
    border-right: 1px solid {T['border_main']} !important;
    backdrop-filter: blur(20px) !important;
}}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stSlider label {{
    font-size: 1rem !important;
    font-weight: 600 !important;
    color: {T['text_sub']} !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}}
[data-testid="stSidebar"] [data-baseweb="select"] > div {{
    background: {T['sidebar_item']} !important;
    border: 1px solid {T['border_main']} !important;
    border-radius: 8px !important;
    color: {T['text_main']} !important;
    font-size: 1rem !important;
}}

/* ── Metric Widgets (native) ── */
[data-testid="stMetricValue"] {{
    color: {T['accent']} !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}}
[data-testid="stMetricLabel"] {{
    color: {T['text_sub']} !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
}}

/* ── KPI Cards ── */
.metric-box {{
    background: {T['bg_card']};
    border: 1px solid {T['border_main']};
    border-radius: 16px;
    padding: 22px 20px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: {T['glow_blue']}, inset 0 1px 0 rgba(255,255,255,0.06);
    transition: all 0.3s ease;
    backdrop-filter: blur(12px);
}}
.metric-box::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, transparent 0%, {T['accent']} 50%, transparent 100%);
    opacity: 0.8;
}}
.metric-box:hover {{
    border-color: {T['border_glow']};
    transform: translateY(-2px);
}}
.metric-icon {{
    font-size: 1.8rem;
    margin-bottom: 8px;
    display: block;
}}
.metric-title {{
    font-size: 0.92rem;
    color: {T['text_sub']};
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 600;
    margin-bottom: 10px;
}}
.metric-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.3rem;
    font-weight: 700;
    color: {T['accent']};
    line-height: 1.1;
    letter-spacing: -0.5px;
}}
.metric-value.red    {{ color: {T['accent_red']};    text-shadow: 0 0 20px rgba(255,61,90,0.4); }}
.metric-value.green  {{ color: {T['accent2']};        text-shadow: 0 0 20px rgba(0,255,136,0.4); }}
.metric-value.gold   {{ color: {T['accent_gold']};   text-shadow: 0 0 20px rgba(255,204,0,0.4); }}
.metric-value.blue   {{ color: {T['accent']};         text-shadow: 0 0 20px rgba(0,200,255,0.4); }}
.metric-value.purple {{ color: {T['accent_purple']}; text-shadow: 0 0 20px rgba(179,136,255,0.4); }}

/* ── Section Headers ── */
.section-header {{
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    color: {T['accent']};
    text-transform: uppercase;
    letter-spacing: 3px;
    border-left: 4px solid {T['accent']};
    padding: 8px 0 8px 14px;
    margin: 28px 0 18px 0;
    background: linear-gradient(90deg, {T['tag_bg']} 0%, transparent 100%);
    border-radius: 0 8px 8px 0;
}}

/* ── Main Title ── */
.main-title {{
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(135deg, {T['accent']} 0%, {T['accent2']} 60%, {T['accent_purple']} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
    letter-spacing: 1px;
    line-height: 1.15;
}}
.sub-title {{
    text-align: center;
    color: {T['text_sub']};
    font-size: 1.05rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 6px;
}}
.status-bar {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 20px;
    margin-bottom: 28px;
    flex-wrap: wrap;
}}
.status-pill {{
    background: {T['tag_bg']};
    border: 1px solid {T['tag_border']};
    border-radius: 30px;
    padding: 6px 16px;
    font-size: 0.9rem;
    color: {T['accent']};
    font-weight: 600;
    letter-spacing: 1px;
    font-family: 'JetBrains Mono', monospace;
}}
.status-dot {{
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: {T['accent2']};
    margin-right: 6px;
    animation: pulse-dot 2s infinite;
}}
@keyframes pulse-dot {{
    0%,100% {{ opacity:1; transform:scale(1); }}
    50%      {{ opacity:0.5; transform:scale(0.8); }}
}}

/* ── Node Cards (Simulation) ── */
.node-card {{
    background: {T['bg_card']};
    border: 1px solid {T['border_main']};
    border-radius: 12px;
    padding: 16px 18px;
    margin: 8px 0;
    border-left: 4px solid {T['accent']};
    backdrop-filter: blur(8px);
}}
.node-card-label {{
    font-size: 0.92rem;
    color: {T['text_sub']};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
}}
.node-card-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.7rem;
    font-weight: 700;
    color: {T['accent']};
}}

/* ── Sidebar Brand ── */
.sidebar-brand {{
    text-align: center;
    padding: 16px 0 20px;
    border-bottom: 1px solid {T['border_main']};
    margin-bottom: 20px;
}}
.sidebar-logo {{
    font-size: 2.4rem;
    display: block;
    margin-bottom: 6px;
}}
.sidebar-title {{
    font-family: 'Syne', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    color: {T['accent']};
    letter-spacing: 3px;
    text-transform: uppercase;
}}
.sidebar-subtitle {{
    font-size: 0.88rem;
    color: {T['text_muted']};
    letter-spacing: 2px;
    margin-top: 3px;
}}
.filter-label {{
    font-size: 0.95rem;
    font-weight: 700;
    color: {T['text_sub']};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin: 18px 0 10px;
    padding-left: 4px;
}}
.sysmon-row {{
    display: flex;
    gap: 10px;
    margin: 8px 0;
}}
.sysmon-item {{
    flex:1;
    background: {T['sidebar_item']};
    border: 1px solid {T['border_main']};
    border-radius: 10px;
    padding: 10px;
    text-align: center;
}}
.sysmon-label {{
    font-size: 0.88rem;
    color: {T['text_muted']};
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 4px;
    font-weight: 600;
}}
.sysmon-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: {T['accent']};
}}
.progress-track {{
    background: {T['border_main']};
    border-radius: 6px;
    height: 7px;
    margin: 8px 0 3px;
    overflow: hidden;
}}
.progress-fill {{
    height: 7px;
    border-radius: 6px;
    transition: width 0.4s ease;
}}
.progress-meta {{
    font-size: 0.88rem;
    color: {T['text_muted']};
    font-weight: 500;
    letter-spacing: 0.5px;
}}
.time-display {{
    text-align: center;
    padding: 12px 0 4px;
    font-size: 0.9rem;
    color: {T['text_muted']};
    letter-spacing: 1px;
    font-weight: 500;
}}
.time-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    font-weight: 600;
    color: {T['accent']};
}}

/* ── Buttons ── */
.stButton > button {{
    background: {T['btn_bg']} !important;
    color: {T['btn_color']} !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 13px 24px !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(0,150,220,0.3) !important;
}}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,150,220,0.4) !important;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {T['bg_card']} !important;
    border-bottom: 1px solid {T['border_main']} !important;
    border-radius: 12px 12px 0 0 !important;
    padding: 4px 8px 0 !important;
    gap: 4px !important;
}}
.stTabs [data-baseweb="tab"] {{
    color: {T['text_sub']} !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    padding: 12px 22px !important;
    border-radius: 8px 8px 0 0 !important;
}}
.stTabs [aria-selected="true"] {{
    color: {T['accent']} !important;
    background: {T['tag_bg']} !important;
    border-bottom: 3px solid {T['accent']} !important;
}}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {{
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid {T['border_main']} !important;
}}

/* ── Alerts & Info ── */
.stAlert {{
    border-radius: 10px !important;
    font-size: 1rem !important;
}}

/* ── Download Button ── */
.stDownloadButton > button {{
    background: {T['btn_bg']} !important;
    color: {T['btn_color']} !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border-radius: 10px !important;
    border: none !important;
}}

/* ── Divider ── */
hr {{ border-color: {T['border_main']} !important; }}

/* ── Scrollbar ── */
::-webkit-scrollbar       {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {T['scroll_track']}; }}
::-webkit-scrollbar-thumb {{ background: {T['scroll_thumb']}; border-radius: 4px; }}

/* ── Footer ── */
.footer {{
    text-align: center;
    padding: 20px;
    color: {T['text_muted']};
    font-size: 0.95rem;
    letter-spacing: 1.5px;
    border-top: 1px solid {T['border_main']};
    margin-top: 30px;
}}
.footer span {{ color: {T['accent']}; font-weight: 600; }}

/* ── Prediction Result Box ── */
.pred-result {{
    background: {T['bg_card']};
    border: 1px solid {T['border_main']};
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    margin-top: 20px;
    backdrop-filter: blur(12px);
}}
.pred-label {{
    font-size: 0.95rem;
    font-weight: 700;
    color: {T['text_sub']};
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 12px;
}}
.pred-value {{
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: 2px;
}}
.pred-conf {{
    font-size: 1rem;
    color: {T['text_sub']};
    margin-top: 10px;
    font-weight: 500;
}}
.model-stat {{
    background: {T['bg_card']};
    border: 1px solid {T['border_main']};
    border-radius: 12px;
    padding: 18px;
    text-align: center;
    margin-bottom: 12px;
}}
.model-stat-label {{
    font-size: 0.95rem;
    color: {T['text_sub']};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}}
.model-stat-value {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.1rem;
    font-weight: 700;
}}
</style>
""", unsafe_allow_html=True)

# ─── Plotly chart layout ──────────────────────────────────
CHART_LAYOUT = dict(
    plot_bgcolor  = T['plot_bg'],
    paper_bgcolor = T['paper_bg'],
    font          = dict(color=T['font_color'], family='Space Grotesk', size=14),
    xaxis         = dict(
        gridcolor=T['grid_color'],
        linecolor=T['grid_color'],
        zeroline=False,
        tickfont=dict(size=13)
    ),
    yaxis         = dict(
        gridcolor=T['grid_color'],
        linecolor=T['grid_color'],
        zeroline=False,
        tickfont=dict(size=13)
    ),
    margin        = dict(t=50, b=45, l=55, r=25),
    hoverlabel    = dict(
        bgcolor=T['bg_card'],
        bordercolor=T['border_main'],
        font=dict(family='Space Grotesk', size=14, color=T['text_main'])
    ),
)
COLORS = [
    '#00c8ff', '#ff3d5a', '#ffcc00', '#00ff88',
    '#ff8c42', '#b388ff', '#fd79a8', '#74b9ff'
]

# ─── Load Data & Models ───────────────────────────────────
@st.cache_data
def load_data():
    if os.path.exists('disaster_dataset.csv'):
        return pd.read_csv('disaster_dataset.csv')
    st.error("disaster_dataset.csv not found! Run: python generate_dataset.py")
    st.stop()

@st.cache_resource
def load_models():
    m = {}
    for k, p in [('rf',       'models/rf_model.pkl'),
                 ('encoders', 'models/encoders.pkl'),
                 ('results',  'models/model_results.json')]:
        if os.path.exists(p):
            with open(p, 'rb' if p.endswith('.pkl') else 'r') as f:
                m[k] = pickle.load(f) if p.endswith('.pkl') else json.load(f)
    return m

df     = load_data()
models = load_models()

# ════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════
with st.sidebar:
    # Brand
    st.markdown(f"""
    <div class='sidebar-brand'>
        <span class='sidebar-logo'>🚨</span>
        <div class='sidebar-title'>ResQ-AI</div>
        <div class='sidebar-subtitle'>DISASTER MANAGEMENT</div>
    </div>
    """, unsafe_allow_html=True)

    # Theme toggle
    if st.button(T['toggle_label'], key='theme_btn'):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

    st.markdown(f"<div style='height:16px;'></div>", unsafe_allow_html=True)

    # Filters
    st.markdown("<div class='filter-label'>🔍 Filters</div>", unsafe_allow_html=True)
    selected_disaster = st.selectbox(
        "Disaster Type",
        ["All"] + sorted(df['Disaster'].unique().tolist())
    )
    selected_location = st.selectbox(
        "Location",
        ["All"] + sorted(df['Location'].unique().tolist())
    )
    selected_severity = st.selectbox(
        "Severity Level",
        ["All"] + sorted(df['Severity'].unique().tolist())
    )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # System Monitor
    st.markdown("<div class='filter-label'>🖥 System Monitor</div>", unsafe_allow_html=True)
    cpu_pct = psutil.cpu_percent(interval=0.1)
    mem_pct = psutil.virtual_memory().percent

    cpu_color = (T['accent_red'] if cpu_pct > 80
                 else T['accent_gold'] if cpu_pct > 50
                 else T['accent2'])
    mem_color = (T['accent_red'] if mem_pct > 80
                 else T['accent_gold'] if mem_pct > 60
                 else T['accent2'])

    st.markdown(f"""
    <div class='sysmon-row'>
        <div class='sysmon-item'>
            <div class='sysmon-label'>CPU</div>
            <div class='sysmon-value' style='color:{cpu_color};'>{cpu_pct}%</div>
        </div>
        <div class='sysmon-item'>
            <div class='sysmon-label'>RAM</div>
            <div class='sysmon-value' style='color:{mem_color};'>{mem_pct}%</div>
        </div>
    </div>
    <div class='progress-track'>
        <div class='progress-fill' style='width:{cpu_pct}%;background:{cpu_color};'></div>
    </div>
    <div class='progress-meta'>CPU Load &nbsp;·&nbsp; {psutil.cpu_count()} Cores Available</div>
    <div style='height:8px;'></div>
    <div class='progress-track'>
        <div class='progress-fill' style='width:{mem_pct}%;background:{mem_color};'></div>
    </div>
    <div class='progress-meta'>Memory Usage</div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"""
    <div class='time-display'>
        LAST UPDATED<br>
        <span class='time-value'>{datetime.now().strftime('%H:%M:%S')}</span>
    </div>
    """, unsafe_allow_html=True)

# ─── Apply Filters ────────────────────────────────────────
filtered = df.copy()
if selected_disaster != "All":
    filtered = filtered[filtered['Disaster'] == selected_disaster]
if selected_location != "All":
    filtered = filtered[filtered['Location'] == selected_location]
if selected_severity != "All":
    filtered = filtered[filtered['Severity'] == selected_severity]

# ════════════════════════════════════════════════════════
# MAIN HEADER
# ════════════════════════════════════════════════════════
st.markdown(f"""
<div class='main-title'>🚨 ResQ-AI Dashboard</div>
<div class='sub-title'>Parallel Processing · Real-Time Simulation · AI Prediction</div>
<div class='status-bar'>
    <span class='status-pill'><span class='status-dot'></span>LIVE</span>
    <span class='status-pill'>{T['toggle_icon']} {T['mode_name']} MODE</span>
    <span class='status-pill'>🕐 {datetime.now().strftime('%d %b %Y')}</span>
    <span class='status-pill'>📊 {len(filtered):,} Cases</span>
</div>
""", unsafe_allow_html=True)

# ─── KPI Row ──────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
kpis = [
    ("TOTAL CASES",      len(filtered),                                        "blue",   "📊"),
    ("CRITICAL",         len(filtered[filtered['Priority'] == 'Critical']),    "red",    "🚨"),
    ("PEOPLE AFFECTED",  f"{filtered['People_Affected'].sum():,.0f}",          "gold",   "👥"),
    ("AVG RESPONSE",     f"{filtered['Response_Time'].mean():.0f} min",        "green",  "⏱"),
    ("AMBULANCES",       filtered['Ambulance_Needed'].sum(),                   "purple", "🚑"),
]
for col, (title, val, color, icon) in zip([k1, k2, k3, k4, k5], kpis):
    col.markdown(f"""
    <div class='metric-box'>
        <span class='metric-icon'>{icon}</span>
        <div class='metric-title'>{title}</div>
        <div class='metric-value {color}'>{val}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs(
    ["📊  Analytics", "🤖  AI Prediction", "⚡  Simulation", "📋  Data Explorer"]
)

# ────────────────────────────────────────────────────────
# TAB 1 – ANALYTICS
# ────────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-header'>Disaster Cases by Type</div>",
                    unsafe_allow_html=True)
        dc = filtered['Disaster'].value_counts().reset_index()
        dc.columns = ['Disaster', 'Count']
        fig = px.bar(dc, x='Disaster', y='Count',
                     color='Count', color_continuous_scale='Blues', text='Count')
        fig.update_traces(
            textposition='outside',
            textfont=dict(color=T["font_color"], size=14),
            marker_line_width=0,
        )
        fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False,
                          xaxis_title='', yaxis_title='Cases',
                          bargap=0.3)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("<div class='section-header'>Priority Distribution</div>",
                    unsafe_allow_html=True)
        pc   = filtered['Priority'].value_counts()
        pull = [0.06 if p == 'Critical' else 0 for p in pc.index]
        fig  = go.Figure(go.Pie(
            labels=pc.index, values=pc.values, hole=0.58, pull=pull,
            marker=dict(
                colors=[T['accent_red'], T['accent_orange'],
                        T['accent_gold'], T['accent2']],
                line=dict(color=T['bg_main'], width=2)
            ),
        ))
        fig.update_traces(
            textinfo='label+percent',
            textfont=dict(color=T["font_color"], size=14)
        )
        fig.update_layout(
            paper_bgcolor=T['paper_bg'], plot_bgcolor=T['plot_bg'],
            font=dict(color=T['font_color'], family='Space Grotesk', size=13),
            showlegend=False,
            margin=dict(t=40, b=20, l=20, r=20),
            annotations=[dict(
                text=f"<b>{len(filtered)}</b><br>Cases",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=T['accent'], family='JetBrains Mono')
            )]
        )
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("<div class='section-header'>Top 10 Cities by Cases</div>",
                    unsafe_allow_html=True)
        city = filtered['Location'].value_counts().head(10).reset_index()
        city.columns = ['City', 'Cases']
        fig = px.bar(city, x='Cases', y='City', orientation='h',
                     color='Cases', color_continuous_scale='Teal', text='Cases')
        fig.update_traces(
            textposition='outside',
            textfont=dict(color=T["font_color"], size=14),
            marker_line_width=0,
        )
        fig.update_layout(**CHART_LAYOUT, coloraxis_showscale=False,
                          xaxis_title='Cases', yaxis_title='', bargap=0.25)
        fig.update_yaxes(categoryorder='total ascending',
                         gridcolor=T['grid_color'], tickfont=dict(size=14))
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        st.markdown("<div class='section-header'>Severity Distribution</div>",
                    unsafe_allow_html=True)
        fig = px.histogram(filtered, x='People_Affected', nbins=30,
                           color='Severity',
                           color_discrete_map={
                               'Low'     : T['accent2'],
                               'Medium'  : T['accent_gold'],
                               'High'    : T['accent_orange'],
                               'Critical': T['accent_red'],
                           })
        fig.update_layout(**CHART_LAYOUT, barmode='overlay', bargap=0.08,
                          xaxis_title='People Affected', yaxis_title='Frequency',
                          legend=dict(
                              bgcolor=T['bg_card'],
                              bordercolor=T['border_main'],
                              font=dict(size=12)
                          ))
        fig.update_traces(opacity=0.78)
        st.plotly_chart(fig, use_container_width=True)

    # Response Time Trend
    st.markdown("<div class='section-header'>Response Time by Severity</div>",
                unsafe_allow_html=True)
    trend = filtered.reset_index(drop=True).reset_index()
    trend.columns = ['Index'] + list(filtered.columns)
    fig = go.Figure()
    for sev, col_clr in zip(
        ['Critical', 'High', 'Medium', 'Low'],
        [T['accent_red'], T['accent_orange'], T['accent_gold'], T['accent2']]
    ):
        sub = trend[trend['Severity'] == sev]
        fig.add_trace(go.Scatter(
            x=sub['Index'], y=sub['Response_Time'],
            mode='markers', name=sev,
            marker=dict(color=col_clr, size=6, opacity=0.78,
                        line=dict(color=T['bg_main'], width=1)),
        ))
    fig.update_layout(
        **CHART_LAYOUT,
        xaxis_title='Case Index', yaxis_title='Response Time (min)',
        legend=dict(
            bgcolor=T['bg_card'], bordercolor=T['border_main'],
            font=dict(size=13), title_font_size=13
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.markdown("<div class='section-header'>Disaster × Location Heatmap</div>",
                unsafe_allow_html=True)
    heat = filtered.groupby(['Disaster', 'Location']).size().unstack(fill_value=0)
    fig  = px.imshow(heat, color_continuous_scale=T['heatmap_cs'],
                     text_auto=True, aspect='auto')
    fig.update_layout(
        paper_bgcolor=T['paper_bg'], plot_bgcolor=T['plot_bg'],
        font=dict(color=T['font_color'], family='Space Grotesk', size=13),
        margin=dict(t=30, b=45, l=130, r=25),
        coloraxis_colorbar=dict(tickfont=dict(size=14))
    )
    fig.update_xaxes(tickfont=dict(size=14))
    fig.update_yaxes(tickfont=dict(size=14))
    st.plotly_chart(fig, use_container_width=True)

# ────────────────────────────────────────────────────────
# TAB 2 – AI PREDICTION
# ────────────────────────────────────────────────────────
with tab2:
    st.markdown("<div class='section-header'>AI Priority Prediction Engine</div>",
                unsafe_allow_html=True)

    if 'rf' in models and 'encoders' in models:
        enc    = models['encoders']
        col_a, col_b = st.columns([1, 1])

        with col_a:
            p_disaster  = st.selectbox("Disaster Type",    enc['disaster'].classes_)
            p_location  = st.selectbox("Location",         enc['location'].classes_)
            p_severity  = st.selectbox("Severity Level",   enc['severity'].classes_)
            p_people    = st.slider("People Affected",  100, 50000, 5000, step=100)
            p_ambulance = st.slider("Ambulances Needed",  1,    50,    10)
            p_resources = st.slider("Resources Needed",  10,   500,   100)
            p_response  = st.slider("Response Time (min)", 5,  240,    60)

            if st.button("🚀  PREDICT PRIORITY"):
                X_new = np.array([[
                    enc['disaster'].transform([p_disaster])[0],
                    enc['location'].transform([p_location])[0],
                    enc['severity'].transform([p_severity])[0],
                    p_people, p_ambulance, p_resources, p_response
                ]])
                pred_enc   = models['rf'].predict(X_new)[0]
                pred_proba = models['rf'].predict_proba(X_new)[0]
                pred_label = enc['priority'].inverse_transform([pred_enc])[0]
                conf       = max(pred_proba) * 100

                c = {
                    'Critical': (T['accent_red'],    '0 0 30px rgba(255,61,90,0.5)'),
                    'High':     (T['accent_orange'],  '0 0 30px rgba(255,140,66,0.5)'),
                    'Medium':   (T['accent_gold'],    '0 0 30px rgba(255,204,0,0.5)'),
                }.get(pred_label, (T['accent2'], '0 0 30px rgba(0,255,136,0.5)'))

                st.markdown(f"""
                <div class='pred-result' style='border-color:{c[0]};'>
                    <div class='pred-label'>🎯 Predicted Priority</div>
                    <div class='pred-value' style='color:{c[0]};text-shadow:{c[1]};'>
                        {pred_label.upper()}
                    </div>
                    <div class='pred-conf'>Confidence: <strong>{conf:.1f}%</strong></div>
                </div>""", unsafe_allow_html=True)

                st.session_state['last_proba']   = pred_proba
                st.session_state['last_classes'] = list(enc['priority'].classes_)

        with col_b:
            if 'results' in models:
                res = models['results']
                r1, r2 = st.columns(2)
                r1.markdown(f"""
                <div class='model-stat'>
                    <div class='model-stat-label'>🌲 Random Forest</div>
                    <div class='model-stat-value' style='color:{T["accent2"]};'>
                        {res['random_forest_accuracy']}%
                    </div>
                </div>""", unsafe_allow_html=True)
                r2.markdown(f"""
                <div class='model-stat'>
                    <div class='model-stat-label'>🌳 Decision Tree</div>
                    <div class='model-stat-value' style='color:{T["accent"]};'>
                        {res['decision_tree_accuracy']}%
                    </div>
                </div>""", unsafe_allow_html=True)

            # Fixed: replaced use_column_width with use_container_width
            for img_path, caption in [
                ('graphs/model_accuracy.png',    '📊 Model Accuracy Comparison'),
                ('graphs/feature_importance.png','📈 Feature Importance'),
                ('graphs/confusion_matrix.png',  '🔢 Confusion Matrix'),
            ]:
                if os.path.exists(img_path):
                    st.markdown(f"<div class='section-header'>{caption}</div>",
                                unsafe_allow_html=True)
                    st.image(img_path, use_container_width=True)

            if 'last_proba' in st.session_state:
                st.markdown("<div class='section-header'>Prediction Confidence</div>",
                            unsafe_allow_html=True)
                pfig = go.Figure(go.Bar(
                    x=st.session_state['last_classes'],
                    y=[p * 100 for p in st.session_state['last_proba']],
                    marker_color=COLORS[:len(st.session_state['last_classes'])],
                    marker_line_width=0,
                    text=[f"{p*100:.1f}%" for p in st.session_state['last_proba']],
                    textposition='outside',
                    textfont=dict(color=T['font_color'], size=14),
                ))
                pfig.update_layout(
                    **CHART_LAYOUT,
                    yaxis_title='Confidence (%)',
                    xaxis_title='Priority Class',
                    bargap=0.35
                )
                st.plotly_chart(pfig, use_container_width=True)
    else:
        st.warning("⚠️  Models not found. Please run: `python train_model.py`")
        st.code("python train_model.py", language='bash')

# ────────────────────────────────────────────────────────
# TAB 3 – SIMULATION
# ────────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-header'>Parallel Disaster Simulation Engine</div>",
                unsafe_allow_html=True)

    s1, s2 = st.columns([1, 2])

    with s1:
        num_dis = st.slider("Disasters to Simulate", 4, 24, 12)
        st.markdown(f"""
        <div class='node-card'>
            <div class='node-card-label'>🖥 Parallel Nodes</div>
            <div class='node-card-value'>4 Active</div>
        </div>
        <div class='node-card' style='border-left-color:{T["accent2"]};'>
            <div class='node-card-label'>⚙️ CPU Cores</div>
            <div class='node-card-value' style='color:{T["accent2"]};'>
                {psutil.cpu_count()} Available
            </div>
        </div>
        <div class='node-card' style='border-left-color:{T["accent_gold"]};'>
            <div class='node-card-label'>📡 Status</div>
            <div class='node-card-value' style='color:{T["accent_gold"]};'>READY</div>
        </div>
        """, unsafe_allow_html=True)
        run_sim = st.button("▶  Run Simulation")

    with s2:
        sim_results, sim_time = [], 0
        if os.path.exists('simulation_results/latest_simulation.json'):
            with open('simulation_results/latest_simulation.json') as f:
                saved       = json.load(f)
            sim_results = saved['results']
            sim_time    = saved['total_time']

        if run_sim:
            with st.spinner("⚡ Running parallel simulation..."):
                d_list  = ['Flood','Earthquake','Fire','Cyclone',
                           'Landslide','Tsunami','Drought','Heatwave']
                l_list  = ['Karachi','Lahore','Islamabad','Peshawar',
                           'Quetta','Multan','Faisalabad','Rawalpindi']
                s_list  = ['Low','Medium','High','Critical']
                s_fac   = {'Low':0.3,'Medium':0.6,'High':0.85,'Critical':1.0}

                sim_results = []
                t0 = time.time()
                for i in range(num_dis):
                    sev    = random.choice(s_list)
                    factor = s_fac[sev]
                    people = int(random.randint(500, 10000) * factor)
                    res    = max(10, int(people/100) + random.randint(0, 50))
                    sim_results.append({
                        'id'                    : i + 1,
                        'disaster_type'         : random.choice(d_list),
                        'location'              : random.choice(l_list),
                        'severity'              : sev,
                        'people_affected'       : people,
                        'ambulances_dispatched' : max(1, int(people * factor / 500)),
                        'resources_allocated'   : min(res, int(res * factor)),
                        'response_time_min'     : max(5, int((1-factor)*120)+random.randint(5,30)),
                        'node'                  : f"Node-{(i%4)+1}",
                        'status'                : ('CRITICAL' if factor >= 0.85
                                                   else 'HIGH' if factor >= 0.6
                                                   else 'MEDIUM' if factor >= 0.3
                                                   else 'LOW'),
                    })
                sim_time = round(time.time() - t0, 3)

                os.makedirs('simulation_results', exist_ok=True)
                with open('simulation_results/latest_simulation.json','w') as f:
                    json.dump({
                        'results': sim_results,
                        'total_time': sim_time,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }, f)
                st.success(f"✅ Simulation complete in {sim_time}s!")

        if sim_results:
            sim_df = pd.DataFrame(sim_results)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("⏱ Sim Time",    f"{sim_time}s")
            m2.metric("👥 People",     f"{sim_df['people_affected'].sum():,}")
            m3.metric("🚑 Ambulances", sim_df['ambulances_dispatched'].sum())
            m4.metric("📦 Resources",  sim_df['resources_allocated'].sum())

            # Node workload chart
            nd  = sim_df.groupby('node').size().reset_index(name='Tasks')
            fig = px.bar(nd, x='node', y='Tasks',
                         color='Tasks', color_continuous_scale='Blues', text='Tasks')
            fig.update_layout(
                **CHART_LAYOUT,
                coloraxis_showscale=False,
                xaxis_title='Compute Node',
                yaxis_title='Tasks Processed',
                bargap=0.35,
                title=dict(
                    text='Node Workload Distribution',
                    font=dict(family='Syne', size=15, color=T['accent']),
                    x=0.02
                )
            )
            fig.update_traces(
                textposition='outside',
                textfont=dict(color=T['font_color'], size=14),
                marker_line_width=0
            )
            st.plotly_chart(fig, use_container_width=True)

            # Results table
            disp = sim_df[[
                'id','disaster_type','location','severity',
                'people_affected','ambulances_dispatched',
                'response_time_min','node','status'
            ]].copy()
            disp.columns = [
                'ID','Disaster','Location','Severity','People',
                'Ambulances','Response (min)','Node','Status'
            ]
            st.dataframe(disp, use_container_width=True, hide_index=True)
        else:
            st.info("▶  Click **Run Simulation** to activate the parallel engine.")

# ────────────────────────────────────────────────────────
# TAB 4 – DATA EXPLORER
# ────────────────────────────────────────────────────────
with tab4:
    st.markdown("<div class='section-header'>Dataset Explorer</div>",
                unsafe_allow_html=True)

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Total Rows",     f"{len(df):,}")
    d2.metric("Columns",        len(df.columns))
    d3.metric("Missing Values", df.isnull().sum().sum())
    d4.metric("Duplicates",     df.duplicated().sum())

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    csv = filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇  Download Filtered Data as CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

    st.markdown("<div class='section-header'>Statistical Summary</div>",
                unsafe_allow_html=True)
    st.dataframe(filtered.describe().round(2), use_container_width=True)

# ─── Footer ───────────────────────────────────────────────
st.markdown(f"""
<div class='footer'>
    🚨 <span>ResQ-AI</span> Disaster Management System &nbsp;·&nbsp;
    Streamlit + Random Forest + Multiprocessing &nbsp;·&nbsp;
    {T['toggle_icon']} <span>{T['mode_name']} MODE</span>
</div>
""", unsafe_allow_html=True)