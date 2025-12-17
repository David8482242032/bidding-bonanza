import streamlit as st
import pandas as pd
import os
import time

# --- FORMAL & FEMININE OFFICE AESTHETIC ---
st.set_page_config(page_title="Executive Benefits Portal", layout="wide")

st.markdown("""
    <style>
    /* Animated Gradient Background */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #334155);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
    /* Elegant Frosted Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .leader-highlight { 
        border: 2px solid #fbbf24 !important; 
        background: rgba(251, 191, 36, 0.1) !important; 
    }

    .name-text { font-size: 20px; font-weight: 500; color: #f8fafc; }
    .time-text { font-size: 24px; font-weight: 700; color: #fbbf24; }
    .title-text { text-align: center; font-size: 50px; font-weight: 800; color: #ffffff; }

    /* Progress Bar Styling */
    .progress-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 6px; margin-top: 12px; overflow: hidden; }
    .progress-fill { background: #b76e79; height: 100%; border-radius: 10px; transition: width 0.5s ease-in-out; }

    /* Buttons */
    div.stButton > button { border-radius: 8px !important; font-weight: 700 !important; height: 45px; }
    div[data-testid="stHorizontalBlock"] div:nth-child(1) button { background: #10b981 !important; color: white !important; }
    div[data-testid="stHorizontalBlock"] div:nth-child(2) button { background: #ef4444 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA ENGINE ---
DB_FILE = "hours_data.csv"
NAMES = ["Devoiry Fettman", "Rivky Katz", "Shana Klein", "Rachel Blumenfeld", 
         "Rachel Heimfeld", "Miriam Gutman", "Etti gottieb", "Miriam Meisels"]

if not os.path.exists(DB_FILE):
    pd.DataFrame({"Name": NAMES, "Total Minutes": [0.0]*8}).to_csv(DB_FILE, index=False)

def update_db(name, h, m, mode):
    df = pd.read_csv(DB_FILE)
    delta = (h * 60) + m
    if mode == "add": df.loc[df['Name'] == name, 'Total Minutes'] += delta
    else: df.loc[df['Name'] == name, 'Total Minutes'] -= delta
    df.loc[df['Total Minutes'] < 0, 'Total Minutes'] = 0
    df.to_csv(DB_FILE, index=False)

# --- USER INTERFACE ---
st.markdown('<div class="title-text">🔥 Bidding Bonanza 🔥</div>', unsafe_allow_html=True)

col_input, col_board = st.columns([1, 1.4], gap="large")

with col_input:
    st.markdown("### 🕒 LOG ACTIVITY")
    with st.container(border=True):
        user = st.selectbox("Select Employee", NAMES)
        c1, c2 = st.columns(2)
        h_in = c1.number_input("Hours", min_value=0, step=1)
        m_in = c2.number_input("Minutes", min_value=0, max_value=59, step=1)
        st.write("")
        b1, b2 = st.columns(2)
        if b1.button("➕ LOG HOURS", use_container_width=True):
            update_db(user, h_in, m_in, "add")
            st.balloons(); st.snow(); st.toast(f"Wow! 🔥 Added time for {user}! 🔥", icon="🎉")
            time.sleep(1.5); st.rerun()
        if b2.button("🛍️ REDEEM BID", use_container_width=True):
            update_db(user, h_in, m_in, "sub")
            st.toast(f"Points redeemed for {user}!"); time.sleep(1); st.rerun()

with col_board:
    st.markdown("### 🏆 CURRENT STANDINGS")
    data = pd.read_csv(DB_FILE).sort_values(by="Total Minutes", ascending=False).reset_index(drop=True)
    
    # Get Max Minutes for the progress line calculation
    max_mins = data['Total Minutes'].max() if data['Total Minutes'].max() > 0 else 1
    
    for rank, row in data.iterrows():
        emoji = "👑" if rank == 0 else "🥈" if rank == 1 else "🥉" if rank == 2 else "💻"
        is_leader = (rank == 0 and row['Total Minutes'] > 0)
        card_class = "glass-card leader-highlight" if is_leader else "glass-card"
        m = row['Total Minutes']
        
        # Calculate how far they are from the leader
        progress_pct = (m / max_mins) * 100
        
        st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <span style="font-size: 24px;">{emoji}</span>
                        <span class="name-text">{row['Name']}</span>
                    </div>
                    <div class="time-text">{int(m//60)}h {int(m%60)}m</div>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {progress_pct}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.caption("© 2025 Office Confidential Dashboard")
