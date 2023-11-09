import streamlit as st
import pandas as pd
import os
os.chdir(os.path.dirname(__file__))

primary_color = "#00AADB"

# dane dot. followersów
df = pd.read_excel('./df_followers_transformed.xlsx', index_col=0)
df = df.replace(0, '-')

# dane dot. periodyczności
mapa = pd.read_excel('./mapa_typy_pism.xlsx')
df = df.merge(mapa, on='Tytuł', how='left')
df = df[df['Typ']!='NIEUWZGLĘDNIONE']
df.set_index(df.columns[0], inplace=True)

st.set_page_config(page_title="Obserwujący w mediach społecznościowych",
                    page_icon=":book:")
st.title('Obserwujący w mediach społecznościowych')



typ = list(df['Typ'].unique())
selected_typ = st.multiselect('Wybierz grupę pism:', options=typ, default=typ)
if selected_typ:
    filtered_df = df[df['Typ'].isin(selected_typ)]


media=list(df.columns.drop(['Suma', 'Typ']))
st.write('Wybierz media społecznościowe: ')
col1, col2 = st.columns(2)
with col1:
    facebook = st.checkbox('Facebook', value=True)
    x = st.checkbox('X', value=True)
    linkedin = st.checkbox('LinkedIn', value=True)
with col2:
    youtube = st.checkbox('YouTube', value=True)
    tiktok = st.checkbox('TikTok', value=True)
    pinterest = st.checkbox('Pinterest', value=True)

medialist = [
    (facebook, 'Facebook'),
    (youtube, 'YouTube'),
    (x, 'X'),
    (linkedin, 'LinkedIn'),
    (tiktok, 'TikTok'),
    (pinterest, 'Pinterest')
]
selected_columns = [x[1] for x in medialist if x[0]]
filtered_df = filtered_df[selected_columns]

try:
    st.write(filtered_df)
except NameError:
    filtered_df = df
    st.write(filtered_df)
