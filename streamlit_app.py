import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(page_title="Mech Ranking System", page_icon="🤖", layout="wide")

# Styling
st.markdown("""
    <style>
    .rank-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .rank-title { font-size: 24px; font-weight: bold; }
    .rank-progress { font-size: 14px; margin-top: 10px; }
    .match-win { background-color: #2d5016; }
    .match-loss { background-color: #5a1616; }
    </style>
""", unsafe_allow_html=True)

# Sample data
RANKS = {
    "Bronze": {"min_rating": 0, "color": "#CD7F32", "icon": "🥉"},
    "Silver": {"min_rating": 1000, "color": "#C0C0C0", "icon": "🥈"},
    "Gold": {"min_rating": 1500, "color": "#FFD700", "icon": "🥇"},
    "Platinum": {"min_rating": 2000, "color": "#E5E4E2", "icon": "💎"},
    "Diamond": {"min_rating": 2500, "color": "#B9F2FF", "icon": "✨"},
    "Legendary": {"min_rating": 3000, "color": "#FF6B00", "icon": "👑"},
}

MECHS = ["Titan", "Shadow", "Phoenix", "Vortex", "Ironclad"]
MAPS = ["Steel Valley", "Crimson Canyon", "Azure Wastes", "Neon City", "Volcanic Core"]

def get_rank(rating):
    """Get rank tier based on rating."""
    for rank in reversed(list(RANKS.keys())):
        if rating >= RANKS[rank]["min_rating"]:
            return rank
    return "Bronze"

def generate_sample_players(count=10):
    """Generate sample player data."""
    players = []
    for i in range(count):
        rating = random.randint(500, 3500)
        rank = get_rank(rating)
        players.append({
            "Username": f"Pilot_{random.choice(['Alpha', 'Beta', 'Gamma', 'Delta', 'Sigma'])}_{i+1}",
            "Rank": rank,
            "Rating": rating,
            "Wins": random.randint(10, 200),
            "Losses": random.randint(5, 100),
            "Winrate": f"{random.randint(45, 75)}%",
            "Main Mech": random.choice(MECHS),
            "Last Played": f"{random.randint(1, 7)} days ago"
        })
    return sorted(players, key=lambda x: x["Rating"], reverse=True)

def generate_match_history(count=10):
    """Generate sample match history."""
    matches = []
    for i in range(count):
        result = random.choice(["Win", "Loss"])
        rating_change = random.randint(15, 35) if result == "Win" else -random.randint(10, 25)
        matches.append({
            "Date": datetime.now() - timedelta(days=random.randint(0, 30)),
            "Result": result,
            "Opponent": f"Pilot_{random.choice(['Omega', 'Zeta', 'Eta', 'Theta'])}_{random.randint(1, 100)}",
            "Map": random.choice(MAPS),
            "Mech Used": random.choice(MECHS),
            "Rating Change": f"{rating_change:+d}",
            "Duration": f"{random.randint(5, 15)} min"
        })
    return sorted(matches, key=lambda x: x["Date"], reverse=True)

def get_rank_progress(rating):
    """Get progress to next rank."""
    current_rank = get_rank(rating)
    rank_list = list(RANKS.keys())
    current_idx = rank_list.index(current_rank)
    
    if current_idx == len(rank_list) - 1:
        return current_rank, 100, "Max rank achieved!"
    
    next_rank = rank_list[current_idx + 1]
    current_min = RANKS[current_rank]["min_rating"]
    next_min = RANKS[next_rank]["min_rating"]
    
    progress = ((rating - current_min) / (next_min - current_min)) * 100
    return next_rank, min(progress, 100), f"To {next_rank}"

# Main app
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏆 Leaderboard", "👤 My Profile", "📊 Stats", "📜 Match History", "🎯 Rank Info"])

with tab1:
    st.header("🏆 Global Leaderboard")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        rank_filter = st.selectbox("Filter by Rank:", ["All"] + list(RANKS.keys()), key="rank_filter")
    with col2:
        region = st.selectbox("Region:", ["Global", "North America", "Europe", "Asia"])
    
    players = generate_sample_players(25)
    
    if rank_filter != "All":
        players = [p for p in players if p["Rank"] == rank_filter]
    
    df = pd.DataFrame(players)
    df_display = df.copy()
    df_display["Rank"] = df_display["Rank"].apply(lambda x: f"{RANKS[x]['icon']} {x}")
    
    st.dataframe(
        df_display[["Rank", "Username", "Rating", "Wins", "Losses", "Winrate", "Main Mech"]],
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.header("👤 My Profile")
    
    # Player stats
    col1, col2, col3, col4 = st.columns(4)
    
    current_rating = 2150
    current_rank = get_rank(current_rating)
    next_rank, progress, progress_text = get_rank_progress(current_rating)
    
    with col1:
        st.metric("Current Rating", current_rating, "+50")
    with col2:
        st.metric("Total Wins", 156)
    with col3:
        st.metric("Win Rate", "62%", "+2%")
    with col4:
        st.metric("Matches Played", 252)
    
    # Rank display
    st.markdown("---")
    st.subheader("Rank Progression")
    
    rank_col1, rank_col2 = st.columns([1, 2])
    
    with rank_col1:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 48px;">{RANKS[current_rank]['icon']}</div>
            <div style="font-size: 28px; font-weight: bold; color: {RANKS[current_rank]['color']};">{current_rank}</div>
            <div style="font-size: 14px; color: gray;">Current Rank</div>
        </div>
        """, unsafe_allow_html=True)
    
    with rank_col2:
        st.write(f"**Progress to {next_rank}**")
        st.progress(progress / 100, text=f"{progress:.1f}%")
        st.write(f"{current_rating} / {RANKS[next_rank]['min_rating']} rating")
        st.info(f"📈 {progress_text}")
    
    # Preferred mech
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🤖 Preferred Mech")
        preferred_mech = "Phoenix"
        st.write(f"**{preferred_mech}**")
        st.metric("Winrate with Phoenix", "71%")
        st.metric("Matches Played", 89)
    
    with col2:
        st.subheader("🏅 Achievements")
        achievements = [
            "🎖️ First Victory",
            "🔥 Hot Streak (5 wins)",
            "💯 Perfect Game",
            "⚡ Sharpshooter (1000 damage)",
            "🛡️ Defender (survived 10 min)",
            "🎯 Ranked 100"
        ]
        for achievement in achievements:
            st.write(achievement)

with tab3:
    st.header("📊 Statistics & Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Mech Performance")
        mech_stats = pd.DataFrame({
            "Mech": MECHS,
            "Matches": [45, 38, 31, 25, 113],
            "Winrate": ["68%", "65%", "60%", "58%", "71%"]
        })
        st.dataframe(mech_stats, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("Map Performance")
        map_stats = pd.DataFrame({
            "Map": MAPS,
            "Matches": [52, 48, 45, 41, 66],
            "Winrate": ["65%", "58%", "61%", "72%", "60%"]
        })
        st.dataframe(map_stats, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Rating Over Time")
        rating_data = pd.DataFrame({
            "Days Ago": list(range(30, 0, -1)),
            "Rating": sorted([1800 + random.randint(-100, 400) for _ in range(30)])
        })
        st.line_chart(rating_data.set_index("Days Ago"))
    
    with col2:
        st.subheader("Win/Loss Distribution")
        wl_data = pd.DataFrame({
            "Result": ["Wins", "Losses"],
            "Count": [156, 96]
        })
        st.bar_chart(wl_data.set_index("Result"))

with tab4:
    st.header("📜 Match History")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        result_filter = st.selectbox("Result:", ["All", "Win", "Loss"], key="result_filter")
    with col2:
        mech_filter = st.selectbox("Mech:", ["All"] + MECHS, key="mech_filter")
    with col3:
        limit = st.selectbox("Show:", [5, 10, 20, 50], key="match_limit")
    
    matches = generate_match_history(limit)
    
    if result_filter != "All":
        matches = [m for m in matches if m["Result"] == result_filter]
    
    if mech_filter != "All":
        matches = [m for m in matches if m["Mech Used"] == mech_filter]
    
    for match in matches:
        result_color = "🟢" if match["Result"] == "Win" else "🔴"
        rating_color = "green" if match["Result"] == "Win" else "red"
        
        st.markdown(f"""
        <div style="background-color: {'#1d3d1d' if match['Result'] == 'Win' else '#3d1d1d'}; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 20px; font-weight: bold;">{result_color} {match['Result']}</span>
                    <span style="margin-left: 10px;">vs {match['Opponent']}</span>
                </div>
                <div style="text-align: right;">
                    <div style="color: {rating_color}; font-weight: bold;">{match['Rating Change']}</div>
                    <small>{match['Date'].strftime('%m/%d %H:%M')}</small>
                </div>
            </div>
            <div style="margin-top: 10px; display: flex; gap: 20px; font-size: 14px;">
                <span>🤖 {match['Mech Used']}</span>
                <span>🗺️ {match['Map']}</span>
                <span>⏱️ {match['Duration']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab5:
    st.header("🎯 Rank Information")
    
    for rank_name, rank_info in RANKS.items():
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            st.markdown(f"<div style='font-size: 40px; text-align: center;'>{rank_info['icon']}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<div style='font-size: 20px; font-weight: bold; color: {rank_info['color']};'>{rank_name}</div>", unsafe_allow_html=True)
            st.write(f"Rating: **{rank_info['min_rating']}+**")
        
        with col3:
            rank_rewards = {
                "Bronze": ["1 Mech Blueprint", "100 Credits"],
                "Silver": ["2 Mech Blueprints", "250 Credits"],
                "Gold": ["3 Mech Blueprints", "500 Credits", "1 Weapon Skin"],
                "Platinum": ["4 Mech Blueprints", "1000 Credits", "2 Weapon Skins"],
                "Diamond": ["5 Mech Blueprints", "2000 Credits", "3 Weapon Skins", "1 Exclusive Skin"],
                "Legendary": ["Exclusive Mech", "5000 Credits", "All Skins", "Title: Legendary"]
            }
            st.write("**Season Rewards:**")
            for reward in rank_rewards.get(rank_name, []):
                st.write(f"• {reward}")
        
        st.divider()
