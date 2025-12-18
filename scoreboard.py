import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import time

# --- CONFIG ---
st.set_page_config(page_title="Executive Benefits Portal", layout="wide")

# The secret code is now secure in Streamlit Secrets, not hardcoded.
SECRET_CODE = "points" 

# --- STYLE ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #334155);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #f8fafc;
        font-family: 'Segoe UI', sans-serif;
    }
    @keyframes gradient { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    
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
    .points-text { font-size: 24px; font-weight: 700; color: #fbbf24; }
    .title-text { text-align: center; font-size: 50px; font-weight: 800; color: #ffffff; padding: 20px; }

    .rank-badge {
        background: #fbbf24;
        color: #0f172a;
        border-radius: 50%;
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 14px;
        margin-right: -10px;
        z-index: 2;
        border: 2px solid #0f172a;
    }

    .progress-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 8px; margin-top: 12px; overflow: hidden; }
    .progress-fill { background: #b76e79; height: 100%; border-radius: 10px; transition: width 0.5s ease-in-out; }
    </style>
    """, unsafe_allow_html=True)


# --- DATA LOADING & PERSISTENCE (LIVE SYNC) ---
# Connect using the secrets configured in Streamlit Cloud
conn = st.connection("gsheets", type=GSheetsConnection, spreadsheet="1wJ5cTvW6-H3w83wk81mu4SBpi5fSoBBQeMjd5DYjQnE")

def load_data():
    # Use conn.read() with ttl=0 to always fetch the latest data from the sheet
    df = conn.read(ttl=0, worksheet="Sheet1") 
    # Ensure 'Total Points' column exists and is numeric
    if 'Total Points' not in df.columns:
        df['Total Points'] = 0.0
    df['Total Points'] = pd.to_numeric(df['Total Points'], errors='coerce').fillna(0).astype(float)
    return df

def save_data(df_to_save):
    # Use conn.update() to write changes back to the actual Google Sheet permanently
    conn.update(worksheet="Sheet1", data=df_to_save) 
    st.toast("Data Synced with Google Sheets!")

if 'df' not in st.session_state:
    st.session_state.df = load_data()


# --- USER INTERFACE ---
st.markdown('<div class="title-text">🔥 Bidding Bonanza 🔥</div>', unsafe_allow_html=True)

col_input, col_board = st.columns([1, 1.4], gap="large")

with col_input:
    st.markdown("### 🏆 LOG ACTIVITY")
    with st.container(border=True):
        user = st.selectbox("Select Employee", st.session_state.df['Name'].tolist())
        pts_in = st.number_input("Points", min_value=0, step=1)
        input_code = st.text_input("Enter Admin Code", type="password")
        
        b1, b2 = st.columns(2)
        if b1.button("➕ ADD POINTS", use_container_width=True):
            if input_code == SECRET_CODE:
                st.session_state.df.loc[st.session_state.df['Name'] == user, 'Total Points'] += pts_in
                save_data(st.session_state.df) # <--- Writes back to Google Sheet
                st.balloons(); st.snow(); time.sleep(1.5); st.rerun()
            else: st.error("Wrong Code")

        if b2.button("🛍️ REDEEM BID", use_container_width=True):
            if input_code == SECRET_CODE:
                st.session_state.df.loc[st.session_state.df['Name'] == user, 'Total Points'] -= pts_in
                st.session_state.df.loc[st.session_state.df['Total Points'] < 0, 'Total Points'] = 0
                save_data(st.session_state.df) # <--- Writes back to Google Sheet
                st.toast("Redeemed!"); time.sleep(0.5); st.rerun()
            else: st.error("Wrong Code")
    
    st.write("---")
    st.caption("All updates are saved live to your Google Sheet.")

with col_board:
    st.markdown("### 🏆 RANKINGS 1-8")
    data = st.session_state.df.sort_values(by="Total Points", ascending=False).reset_index(drop=True)
    max_pts = data['Total Points'].max() if data['Total Points'].max() > 0 else 1
    
    for rank, row in data.iterrows():
        rank_num = rank + 1
        trophy = "🥇" if rank_num == 1 else "🥈" if rank_num == 2 else "🥉" if rank_num == 3 else "🏆"
        pts = row['Total Points']
        
        st.markdown(f"""
            <div class="glass-card {'leader-highlight' if rank==0 and pts>0 else ''}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div class="rank-badge">{rank_num}</div>
                        <span style="font-size: 32px;">{trophy}</span>
                        <span class="name-text">{row['Name']}</span>
                    </div>
                    <div class="points-text">{int(pts)} Points</div>
                </div>
                <div class="progress-bg"><div class="progress-fill" style="width: {(pts/max_pts)*100}%;"></div></div>
            </div>
        """, unsafe_allow_html=True)

st.caption("© 2025 Office Confidential Dashboard")
