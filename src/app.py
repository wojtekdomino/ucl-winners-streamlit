import streamlit as st
import pandas as pd

st.title("UEFA Champions League Winners Analysis")

# --- Load data ---
st.header("Loading and Cleaning Data")
@st.cache_data
def load_data():
    url = "https://pl.wikipedia.org/wiki/Liga_Mistrz%C3%B3w_UEFA"
    tables = pd.read_html(url, match="Sezon")
    winners_table = tables[0]  # First table on the page
    winners_table.rename(columns={"Zwycięzca": "Winner"}, inplace=True)
    winners_table.dropna(inplace=True)
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
            seasons = df[df['Winner'] == team]['Sezon'].tolist()
            st.success(f"✅ {team} has won the UEFA Champions League {title_count} times!")
            st.write(f"Winning seasons: {', '.join(seasons)}")
    else:
        st.error(f"❌ {team_input} has never won the UEFA Champions League.")

st.markdown("---")
st.caption("App by Wojciech Domino - 2025")
