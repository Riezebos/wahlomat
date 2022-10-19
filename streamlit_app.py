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
    answer = st.radio(label="Vælg venligst din stilling",options=mapping.keys(),key=question,horizontal=True)
    value = abs(volt - mapping[answer])
    diff_total += value

similarity = 100 - diff_total
st.header(f"Lighed med Volt Danmark: {similarity}%")

st.markdown(
"""
Du er ret enig med Volt Danmark, så hvis du vil have flere partier, der er enig med dig så støt Volts opstilling 💜

Støt her: https://www.vaelgererklaering.dk/om-partiet?election=eu&party=e8e2a255-9ebb-40eb-9703-5565eb4253fe

Læs mere her: https://volt.link/stemvolt
"""
)
