import streamlit as st
import pandas as pd
import altair as alt

st.title('Rating Progression')

df = pd.read_csv("final.csv", index_col=0)

with st.sidebar:
    min_months = int(df.index[0])
    max_months = int(df.index[-1])
    months = st.slider("Age Range (Months)", min_months, max_months, (120, 240))

    players = list(df.columns)
    players_ = st.multiselect("Players", players, players)

filtered = df.loc[months[0]:months[1], players_]

data = filtered.reset_index().melt('months')
data.columns = ['Age (Months)', 'Player', 'Rating']

c = alt.Chart(data).mark_line().encode(
    x='Age (Months)',
    y = alt.Y('Rating', scale = alt.Scale(domain=(1700,2900))),
    color='Player',
    tooltip='Player',
).interactive()

st.altair_chart(c, use_container_width=True)

def get_gain(player, df):
    pdf = df[player].dropna()
    gain = pdf.iloc[-1] - pdf.iloc[0]
    return gain

def make_bar_chart(df):
    gains = [get_gain(p, df) for p in players_]
    source = pd.DataFrame({
        'Player': players_,
        'Rating Gain': gains
    })
    c = alt.Chart(source).mark_bar().encode(
        x='Player',
        y='Rating Gain'
    )
    return c

bar = make_bar_chart(filtered)
st.altair_chart(bar, use_container_width=True)
