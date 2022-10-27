import streamlit as st
import pandas as pd
import altair as alt

st.title('Top Juniors Rating Progress')

@st.cache
def load_data():
    games = pd.read_csv("games.csv")
    months = pd.read_csv("months.csv")
    players = list(games.player.unique())
    return games, months, players

games, months, players = load_data()

with st.sidebar:
    players_ = st.multiselect("Players", players, players)
    x = st.radio("X axis", ["Games", "Months"])
    if x == "Games":
        df = games
        x_label = "total_games"
    elif x == "Months":
        df = months
        x_label = "months"
    x_min = int(df[x_label].min())
    x_max = int(df[x_label].max())
    x_range = st.slider(x, x_min, x_max, (x_min, x_max))

filtered = df[df.player.isin(players_)]
filtered = filtered[filtered[x_label].between(*x_range)]

def line_chart():
    return alt.Chart(filtered).mark_line().encode(
        x=x_label,
        y = alt.Y('rating', scale = alt.Scale(domain=(1700,2900))),
        color='player',
        tooltip='player'
    ).interactive()

st.altair_chart(line_chart(), use_container_width=True)
#
# def get_gain(player, df):
#     pdf = df[player].dropna()
#     gain = pdf.iloc[-1] - pdf.iloc[0]
#     return gain
#
# def make_bar_chart(df):
#     gains = [get_gain(p, df) for p in players_]
#     source = pd.DataFrame({
#         'Player': players_,
#         'Rating Gain': gains
#     })
#     c = alt.Chart(source).mark_bar().encode(
#         x='Player',
#         y='Rating Gain'
#     )
#     return c
#
# bar = make_bar_chart(filtered)
# st.altair_chart(bar, use_container_width=True)
