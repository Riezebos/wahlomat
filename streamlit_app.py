import pandas as pd
import seaborn as sns
import streamlit as st

custom_params = {
    "axes.grid.axis": "both",

}
import textwrap

sns.set_theme(rc=custom_params)
sns.set_context("talk")


@st.cache(allow_output_mutation=True)
def get_data():
    df = pd.read_csv("questions.tsv", sep="\t", index_col="Erklæring")
    df["Din Holdning"] = None
    return df


df = get_data()

st.title("Kandidattesten - Volt Danmark")

mapping = {
    "Helt uenig": 1,
    "Uenig": 2,
    "Enig": 3,
    "Helt enig": 4,
    "Ingen præference": None,
}
inv_mapping = {v: k for k, v in mapping.items()}
labels_format_mapping = {v.replace(" ","\n"): k for k, v in mapping.items()}

for question, uenig, enig in df[["Uenig", "Enig"]].itertuples():
    st.markdown(f"### {question}\n\n**Enig:** {enig}\n\n**Uenig:** {uenig}")
    answer = st.radio(
        label="Vælg venligst din stilling",
        options=mapping.keys(),
        key=question,
        horizontal=True,
        index=4,
    )
    df.loc[question, "Din Holdning"] = mapping[answer]

relevant = df.loc[df["Din Holdning"].notna()]
if relevant.empty:
    st.header("Ingen forudgående")
else:
    similarity = 1 - (
        relevant["Volt Holdning"] - relevant["Din Holdning"]
    ).abs().sum() / (3 * len(relevant))
    st.markdown(f"### Lighed med Volt Danmark: {similarity*100:.0f}%")


st.markdown(
    """
Du er ret enig med Volt Danmark, så hvis du vil have flere partier, der er enig med dig så støt Volts opstilling 💜

Støt her: https://www.vaelgererklaering.dk/om-partiet?election=eu&party=e8e2a255-9ebb-40eb-9703-5565eb4253fe

Læs mere her: https://volt.link/stemvolt
"""
)

if not relevant.empty:
    df_long = pd.melt(
        relevant[["Volt Holdning", "Din Holdning"]].reset_index(),
        id_vars="Erklæring",
        var_name="Legende",
        value_name="Holdning",
    )
    df_long["Holdning"] = df_long["Holdning"].map(labels_format_mapping)
    palette = {
        "Volt Holdning": "#502379",
        "Din Holdning": "#82D0F4",
    }
    ax = sns.catplot(
        data=df_long,
        x="Holdning",
        y="Erklæring",
        hue="Legende",
        order=list(mapping)[:-1],
        palette=palette,
        legend=False,
        height=0.5*len(df_long),
        orient="v",
        aspect=10/len(df_long),
        sizes=[100,100],
    )

    ax.set_axis_labels(x_var="", y_var="")
    labels = [textwrap.fill(label, 50) for label in df_long["Erklæring"].drop_duplicates()]
    ax.set_yticklabels(labels)
    st.pyplot(ax.figure)
