import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.title('Copa QATAR 2022')

st.markdown("""
Estatísticas de Jogadores de Futebol na Copa QATAR 2022!
* **Python libs:** base64, pandas, streamlit
* **Origem:** [fbref.com](https://fbref.com/en/comps/1/stats/World-Cup-Stats).
""")

st.sidebar.header('User Input Features')
#selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))

# Web scraping of NBA player stats
@st.cache
def load_data():
    url = "https://fbref.com/en/comps/1/stats/World-Cup-Stats"
    html = pd.read_html(url, header = 0)
    df = pd.concat(html)
    #df['V5']=df['Last 5'].apply(lambda x: x.count('W'))
    #df['E5']=df['Last 5'].apply(lambda x: x.count('D'))
    #df['D5']=df['Last 5'].apply(lambda x: x.count('L'))
    playerstats = df.drop(['Notes','Rk','L', 'D', 'W', 'GA', 'GF', 'Last 5'], axis=1)


    return playerstats
playerstats = load_data()



# Sidebar - Team selection
sorted_unique_team = sorted(playerstats.Squad.unique())
selected_team = st.sidebar.multiselect('Seleção', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
unique_pos = [0,1,2,3,4]
selected_pos = st.sidebar.selectbox('Partidas Disputadas', unique_pos)

# Filtering data
df_selected_team = playerstats[(playerstats.Squad.isin(selected_team)) & (playerstats.MP==selected_pos)]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

# Heatmap
if st.button('Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True, annot=True)
    st.pyplot()
