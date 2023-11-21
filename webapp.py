import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
os.chdir(os.path.dirname(__file__))

def format_number_with_spaces(number_str):
    # formatowanie liczb do formatu 1 111 111
    reversed_str = str(int(number_str))[::-1]
    groups = [reversed_str[i:i + 3] for i in range(0, len(reversed_str), 3)]
    return ' '.join(groups)[::-1]


my_colors = {
    'Facebook': '#0070C0',
    'YouTube': '#981923',
    'X': '#193441',
    'LinkedIn': '#006683',
    'TikTok': '#00F0F0',
    'Pinterest': '#E0404B',
    'Instagram': "#5B0F15"
}


# dane dot. followersów
df = pd.read_excel('./df_followers.xlsx', index_col=0)
df = df.replace(0, '-')

# dane dot. periodyczności
mapa = pd.read_excel('./mapa_typy_pism.xlsx')
df = df.merge(mapa, on='Tytuł', how='left')
df = df[df['Typ']!='NIEUWZGLĘDNIONE']
df.set_index(df.columns[0], inplace=True)

st.set_page_config(page_title="Obserwujący w mediach społecznościowych",
                    page_icon=":book:")
st.markdown("<h1 style='margin-top: -80px; text-align: center;'>Obserwujący w mediach społecznościowych</h1>", unsafe_allow_html=True)
# st.title('Obserwujący w mediach społecznościowych')


typ = list(df['Typ'].unique())
selected_typ = st.multiselect('Wybierz grupę pism:', options=typ, default=typ)
if selected_typ:
    filtered_df = df[df['Typ'].isin(selected_typ)]
else:
     filtered_df = df


media=list(df.columns.drop(['Typ']))
st.markdown('<p style="font-size: 14px;">Wybierz media społecznościowe:</p>', unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    facebook = st.checkbox('Facebook', value=True)
    x = st.checkbox('X', value=True)
    linkedin = st.checkbox('LinkedIn', value=True)
    instagram = st.checkbox('Instagram', value=True)
with col2:
    youtube = st.checkbox('YouTube', value=True)
    tiktok = st.checkbox('TikTok', value=True)
    pinterest = st.checkbox('Pinterest', value=True)
    suma = st.checkbox('Suma', value=True)

medialist = [
    (facebook, 'Facebook'),
    (youtube, 'YouTube'),
    (x, 'X'),
    (linkedin, 'LinkedIn'),
    (tiktok, 'TikTok'),
    (pinterest, 'Pinterest'),
    (instagram, 'Instagram'),
    (suma, 'Suma')
]
selected_columns = [x[1] for x in medialist if x[0]]
filtered_df = filtered_df[selected_columns]

output_type = st.radio('Wybierz tryb wyświetlania danych:', ['Tabela', 'Wykresy'], horizontal=True)

if output_type == 'Tabela':
    filtered_df.index.name = None
    filtered_df = filtered_df.style.set_table_styles([
        {'selector': 'table', 'props': [('text-align', 'center')]},
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]},
        {'selector': 'th.col0, td.col0', 'props': [('text-align', 'left')]}
    ])

    filtered_df_html = filtered_df.to_html()
    filtered_df_html = filtered_df_html.replace('<table', "<table class='sticky-header'")
    
    css_style = """
        <style>
            table.sticky-header thead tr {
                position: sticky;
                top: 0;
                background-color: #f0f2f6;
                border: 0.2em solid ##77AADB;
            }

            table.sticky-header {
                font-size: 0.89em; /* Adjust the font size as needed */
                max-width: 100%; /* Adjust the width as needed */
            }
        </style>
    """
    
    st.markdown(css_style, unsafe_allow_html=True)
    st.markdown(f"<div style='overflow-x: scroll; max-width: 100%'>{filtered_df_html}</div>", unsafe_allow_html=True)

else:
    for column in selected_columns:
        aux = filtered_df[filtered_df[column]!='-'][column].sort_values(ascending=False).head(10)

        if len(aux)==0:
            st.write(f'Brak danych dla kategorii {column}')
            continue
        # przypadki gdzie jest mniej niż 10 pism w danej kategorii
        while len(aux)<10:
            aux = pd.concat([aux, pd.Series({' '*len(aux): 0})], axis=0)
        
        fig, ax = plt.subplots(figsize=(8, 6))
        plt.barh(aux.index, aux, color=my_colors[column], height=0.5)
        plt.gca().spines[:].set_visible(False)
        plt.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plt.tick_params(axis='y', which='both', length=0, labelleft=False) # labelleft=False żeby wykresy zaczynały się w tym samym miejscu
        plt.gca().invert_yaxis()

        plt.title(f'Top 10 pism: obserwujący w serwisie {column}',
                   loc='left',
                   fontdict={'fontsize': 14, 'fontweight': 'bold', 'fontname': 'Lato'})
        for index, value in enumerate(list(aux)):
            if value>0:
                plt.text(value, index+.1, format_number_with_spaces(value))
            
        for index, pismo in enumerate(list(aux.index)):
            plt.text(0, index-0.48, pismo, ha='left', va='center', fontdict={'fontsize': 10.8, 'fontname': 'Lato'})
        st.pyplot(fig)


st.markdown("""<div style="font-size:12px">Źródło: Opracowanie własne PBC, dane na dzień 11.11.2023</div>""", unsafe_allow_html=True)