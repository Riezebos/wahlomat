import math
from collections import namedtuple

import altair as alt
import pandas as pd
import streamlit as st


@st.cache
def get_data():
    return pd.read_csv("questions.tsv",sep="\t")

df = get_data()

st.title("Kandidattesten - Volt Danmark")

mapping = {
    "Helt uenig": 1,
    "Uenig": 2,
    "Enig": 3,
    "Helt enig": 4,
}
diff_total = 0
for _, question, uenig, enig, volt in df.itertuples():
    st.markdown(f"## {question}\n\n**Enig:** {enig}\n\n**Uenig:** {uenig}")
    answer = st.select_slider(label="Vælg venligst din stilling",options=mapping.keys(),key=question)
    value = abs(volt - mapping[answer])
    diff_total += value

similarity = 100 - diff_total
st.header(f"Lighed med Volt Danmark: {similarity}%")


# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

#     Point = namedtuple('Point', 'x y')
#     data = []

#     points_per_turn = total_points / num_turns

#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))
