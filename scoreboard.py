import streamlit as st
import pandas as pd
import os
import time

# --- FORMAL & FEMININE OFFICE AESTHETIC ---
st.set_page_config(page_title="Executive Benefits Portal", layout="wide")

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

# --- DATA ENGINE ---
DB_FILE = "office_points.csv"
NAMES = ["Devoiry Fettman", "Rivky Katz", "Shana Klein", "Rachel Blumenfeld", 
         "Rachel Heimfeld", "Miriam Gutman", "Etti gottieb", "Miriam Meisels"]
SECRET_CODE = "points"  # <--- YOUR ACCESS CODE

if not os.path.exists(DB_FILE):
    pd.DataFrame({"Name": NAMES, "Total Points": [0.0]*len(NAMES)}).to_csv(DB_FILE, index=False)

def update_db(name, pts, mode):
    df = pd.read_csv(DB_FILE)
    if mode == "add":
        df.loc[df['Name'] == name, 'Total Points'] += pts
    elif mode == "sub":
        df.loc[df['Name'] == name, 'Total Points'] -= pts
    df.loc[df['Total Points'] < 0, 'Total Points'] = 0
    df.to_csv(DB_FILE, index=False)

# --- USER INTERFACE ---
st.markdown('<div class="title-text">🔥 Bidding Bonanza 🔥</div>', unsafe_allow_html=True)

col_input, col_board = st.columns([1, 1.4], gap="large")

with col_input:
    st.markdown("### 🏆 LOG ACTIVITY")
    with st.container(border=True):
        user = st.selectbox("Select Employee", NAMES)
        pts_in = st.number_input("Points", min_value=0, step=1)
        
        # --- NEW CODE PROTECTION FIELD ---
        input_code = st.text_input("Enter Admin Code to Save", type="password")
        
        st.write("")
        b1, b2 = st.columns(2)
        
        if b1.button("➕ ADD POINTS", use_container_width=True):
            if input_code == SECRET_CODE:
                update_db(user, pts_in, "add")
                # UPDATED VISUALS: Removed st.snow(), kept balloons and big message
                st.balloons()
                st.success(f"# 🎉 WOW! {pts_in} Points Added for {user}! 🎊")
                st.toast(f"Points added for {user}!");
                time.sleep(1); st.rerun()
            else:
                st.error("Incorrect Admin Code!")

        if b2.button("🛍️ REDEEM BID", use_container_width=True):
            if input_code == SECRET_CODE:
                update_db(user, pts_in, "sub")
                st.toast(f"Points redeemed for {user}!"); time.sleep(1); st.rerun()
            else:
                st.error("Incorrect Admin Code!")

with col_board:
    st.markdown("### 🏆 RANKINGS 1-8")
    data = pd.read_csv(DB_FILE).sort_values(by="Total Points", ascending=False).reset_index(drop=True)
    max_pts = data['Total Points'].max() if data['Total Points'].max() > 0 else 1
    
    for rank, row in data.iterrows():
        rank_num = rank + 1
        trophy = "🥇" if rank_num == 1 else "🥈" if rank_num == 2 else "🥉" if rank_num == 3 else "🏆"

        is_leader = (rank == 0 and row['Total Points'] > 0)
        card_class = "glass-card leader-highlight" if is_leader else "glass-card"
        pts = row['Total Points']
        progress_pct = (pts / max_pts) * 100
        
        st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div class="rank-badge">{rank_num}</div>
                        <span style="font-size: 32px;">{trophy}</span>
                        <span class="name-text">{row['Name']}</span>
                    </div>
                    <div class="points-text">{int(pts)} Points</div>
                </div>
                <div class="progress-bg">
                    <div class="progress-fill" style="width: {progress_pct}%;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.caption("© 2025 Office Confidential Dashboard")
