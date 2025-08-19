import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Csapatelosztó", page_icon="⚽", layout="centered")

# Excel betöltése
df = pd.read_excel("jatekosok.xlsx")

# Ha nincs Összpont oszlop, számoljuk
if "Összpont" not in df.columns:
    df["Összpont"] = df[["Támadás", "Védekezés", "Gyorsaság"]].sum(axis=1)

st.title("⚽ Amatőr Foci Csapatelosztó")

st.markdown("Jelöld ki, kik vannak ma jelen:")

# Játékos kiválasztás
megjelentek = st.multiselect("", df["Név"].tolist())

if st.button("Csapatok kiosztása"):
    jatekosok = df[df["Név"].isin(megjelentek)].copy()
    jatekosok = jatekosok.sample(frac=1, random_state=random.randint(1, 1000)).reset_index(drop=True)

    csapat1, csapat2 = [], []
    pont1, pont2 = 0, 0

    for _, row in jatekosok.iterrows():
        if pont1 <= pont2:
            csapat1.append(row["Név"])
            pont1 += row["Összpont"]
        else:
            csapat2.append(row["Név"])
            pont2 += row["Összpont"]

    st.success("✅ Csapatok elkészültek!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Csapat 1")
        for j in csapat1:
            st.write("•", j)
        st.write("**Pontszám:**", pont1)

    with col2:
        st.subheader("Csapat 2")
        for j in csapat2:
            st.write("•", j)
        st.write("**Pontszám:**", pont2)
