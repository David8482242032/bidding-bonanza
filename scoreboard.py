import streamlit as st
import pandas as pd
import time

# --- CONFIG ---
st.set_page_config(page_title="Executive Benefits Portal", layout="wide")

# YOUR GOOGLE SHEET LINK
SHEET_URL = "docs.google.com"
SECRET_CODE = "points"

# --- STYLE ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(-45deg, #0f172a, #1e293b, #334155); color: #f8fafc; font-family: 'Segoe UI', sans-serif; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin-bottom: 12px; }
    .leader-highlight { border: 2px solid #fbbf24 !important; background: rgba(251, 191, 36, 0.1) !important; }
    .name-text { font-size: 20px; font-weight: 500; color: #f8fafc; }
    .points-text { font-size: 24px; font-weight: 700; color: #fbbf24; }
    .title-text { text-align: center; font-size: 50px; font-weight: 800; color: #ffffff; padding: 20px; }
    .rank-badge { background: #fbbf24; color: #0f172a; border-radius: 50%; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; font-weight: bold; margin-right: -10px; border: 2px solid #0f172a; }
    .progress-bg { background: rgba(255, 255, 255, 0.1); border-radius: 10px; height: 8px; margin-top: 12px; overflow: hidden; }
    .progress-fill { background: #b76e79; height: 100%; border-radius: 10px; transition: width 0.5s ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
if 'df' not in st.session_state:
    try:
        st.session_state.df = pd.read_csv(SHEET_URL)
    except:
        NAMES = ["Devoiry Fettman", "Rivky Katz", "Shana Klein", "Rachel Blumenfeld", 
                 "Rachel Heimfeld", "Miriam Gutman", "Etti gottieb", "Miriam Meisels"]
        st.session_state.df = pd.DataFrame({"Name": NAMES, "Total Points": [0.0]*len(NAMES)})

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
                # --- VISUAL EFFECTS ---
                st.balloons()
                st.snow()
                st.toast(f"Points added for {user}!")
                time.sleep(1.5)  # Wait for effects to be seen before rerun
                st.rerun()
            else: st.error("Wrong Code")

        if b2.button("🛍️ REDEEM BID", use_container_width=True):
            if input_code == SECRET_CODE:
                st.session_state.df.loc[st.session_state.df['Name'] == user, 'Total Points'] -= pts_in
                st.session_state.df.loc[st.session_state.df['Total Points'] < 0, 'Total Points'] = 0
                st.toast("Redeemed!")
                time.sleep(0.5)
                st.rerun()
            else: st.error("Wrong Code")
    
    st.write("---")
    st.markdown("#### 💾 Save Progress")
    csv_data = st.session_state.df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 DOWNLOAD BACKUP CSV", data=csv_data, file_name="bidding_backup.csv", mime="text/csv")
    
    if st.button("🔄 REFRESH FROM CLOUD"):
        del st.session_state.df
        st.rerun()

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
