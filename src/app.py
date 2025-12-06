import streamlit as st
import pandas as pd

# --- Load data ---
@st.cache_data
def load_data():
    url = "https://en.wikipedia.org/wiki/List_of_European_Cup_and_UEFA_Champions_League_finals"
    # Add User-Agent header to avoid 403 Forbidden error
    tables = pd.read_html(
        url,
        storage_options={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    
    # Find table with winners information
    for table in tables:
        if 'Season' in table.columns or 'Winners' in table.columns:
            winners_table = table
            break
    
    # Standardize column names
    column_mapping = {}
    for col in winners_table.columns:
        col_lower = str(col).lower()
        if 'season' in col_lower:
            column_mapping[col] = 'Season'
        elif 'winner' in col_lower:
            column_mapping[col] = 'Winner'
    
    winners_table.rename(columns=column_mapping, inplace=True)
    
    if 'Winner' in winners_table.columns:
        winners_table.dropna(subset=['Winner'], inplace=True)
    
    return winners_table

# Load the dataset
df = load_data()

# --- Streamlit App ---
st.title("UEFA Champions League Winners Checker 🏆⚽")
st.write("Check if your football team has ever won the UEFA Champions League!")

# List of teams
teams = df['Winner'].unique()

# User input
team_input = st.text_input("Enter the team name:")

if st.button("Check"):
    # Find teams containing the user input
    found_teams = [
        team for team in teams
        if isinstance(team, str) and team_input.lower() in team.lower()
    ]

    if found_teams:
        for team in found_teams:
            title_count = df[df['Winner'] == team].shape[0]
            seasons = df[df['Winner'] == team]['Season'].tolist()
            st.success(f"✅ {team} has won the UEFA Champions League {title_count} times!")
            st.write(f"Winning seasons: {', '.join(map(str, seasons))}")
    else:
        st.error(f"❌ {team_input} has never won the UEFA Champions League.")

st.markdown("---")
st.caption("App by Wojciech Domino - 2025")
