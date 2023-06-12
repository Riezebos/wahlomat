import logging
import warnings

warnings.filterwarnings("ignore", module="seaborn\..*")
import textwrap

import pandas as pd
import seaborn as sns
import streamlit as st

custom_params = {
    "axes.grid.axis": "both",
}


sns.set_theme(rc=custom_params)
sns.set_context("talk")

st.set_page_config(
    page_title="Kandidattesten - Volt Danmark",
    page_icon="📋",
)

languages = {
    "da": "Dansk",
    "en": "English",
}

language = st.sidebar.radio(
    label="Language",
    options=languages.keys(),
    format_func=lambda x: languages[x],
    horizontal=True,
    index=0,
)

title = (
    "Kandidattesten - Volt Danmark"
    if language == "da"
    else "Candidate test - Volt Denmark"
)


st.title(title)


@st.cache_data
def get_data(language="da"):
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    user = ",".join(f"{k}: {v}" for k, v in st.experimental_user.items())
    log.info(f"New user connected:{user}")
    df = pd.read_csv(f"data/questions-{language}.tsv", sep="\t", index_col="Erklæring")
    df["Din Holdning"] = None
    return df


df = get_data(language)

base_mapping = {
    1: {"da": "Helt uenig", "en": "Strongly disagree"},
    2: {"da": "Uenig", "en": "Disagree"},
    3: {"da": "Enig", "en": "Agree"},
    4: {"da": "Helt enig", "en": "Strongly agree"},
    None: {"da": "Ingen præference", "en": "No preference"},
}
lang_mapping = {v[language]: k for k, v in base_mapping.items()}
inv_mapping = {v: k for k, v in lang_mapping.items()}

for question, uenig, enig in df[["Uenig", "Enig"]].itertuples():
    st.markdown(
        f"### {question}\n\n**{'Enig' if language == 'da' else 'Agree'}:** {enig}\n\n**{'Uenig' if language == 'da' else 'Disagree'}:** {uenig}"
    )
    answer = st.radio(
        label="Vælg venligst din stilling" if language == "da" else "Please select",
        options=lang_mapping.keys(),
        key=question,
        horizontal=True,
        index=4,
    )
    df.loc[question, "Din Holdning"] = lang_mapping[answer]

relevant = df.loc[df["Din Holdning"].notna()]
if relevant.empty:
    st.header("Ingen forudgående" if language == "da" else "No prior")
else:
    similarity = 1 - (
        relevant["Volt Holdning"] - relevant["Din Holdning"]
    ).abs().sum() / (3 * len(relevant))
    text = (
        "Lighed med Volt Danmark"
        if language == "da"
        else "Similarity with Volt Denmark"
    )
    st.markdown(f"### {text}: {similarity*100:.0f}%")

explanation = {
    "da": """Du er ret enig med Volt Danmark, så hvis du vil have flere partier, der er enig med dig så støt Volts opstilling 💜

Støt her: https://www.vaelgererklaering.dk/om-partiet?election=eu&party=e8e2a255-9ebb-40eb-9703-5565eb4253fe

Læs mere her: https://volt.link/stemvolt
""",
    "en": """You are quite in agreement with Volt Denmark, so if you want more parties that agree with you, support Volt's candidacy 💜

Support here: https://www.vaelgererklaering.dk/om-partiet?election=eu&party=e8e2a255-9ebb-40eb-9703-5565eb4253fe

Read more here: https://volt.link/stemvolt

""",
}

st.markdown(explanation[language])

if not relevant.empty:
    df_long = pd.melt(
        relevant[["Volt Holdning", "Din Holdning"]].reset_index(),
        id_vars="Erklæring",
        var_name="Legende",
        value_name="Holdning",
    )
    df_long["Holdning"] = df_long["Holdning"].map(inv_mapping)
    palette = {
        "Volt Holdning": "#502379",
        "Din Holdning": "#82D0F4",
    }
    ax = sns.catplot(
        data=df_long,
        x="Holdning",
        y="Erklæring",
        hue="Legende",
        order=list(lang_mapping)[:-1],
        palette=palette,
        legend=False,
        height=0.5 * len(df_long),
        orient="v",
        aspect=10 / len(df_long),
        sizes=[100, 100],
    )

    ax.set_axis_labels(x_var="", y_var="")
    labels = [
        textwrap.fill(label, 50) for label in df_long["Erklæring"].drop_duplicates()
    ]
    ax.set_yticklabels(labels)
    st.pyplot(ax.figure)
