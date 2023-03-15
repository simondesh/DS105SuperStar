import streamlit as st
import pandas as pd
from data.Games import games

"""
# About :) 

Welcome to DS105SuperStars steam's API project! \n
We are a group of 3 students from the London School of Economics and Political Science (LSE). 

## Our Team

- [**Simon Deshayes**](https://github.com/simondesh)

## Our Project

Our aim is to study what makes a game successful on steam. We will be using the steam API to gather data on games and their reviews.\n
We will then use this data to create a dashboard that will allow us to explore the data and answer our research questions.
"""

x = games()

show_game_and_id = st.checkbox('show game name and id dataframe')
if show_game_and_id:
    st.dataframe(x.df_game_name_and_id, 700, 500)

x.get_language_dataframes()

show_game_by_language = st.checkbox('show game name and id dataframe by language')
if show_game_by_language:
    language = st.selectbox('select language', ('non_english', 'chinese', 'korean', 'japanese'))
    if language == 'non_english':
        st.dataframe(x.non_english_df, 700, 500)
    elif language == 'chinese':
        st.dataframe(x.chinese_df, 700, 500)
    elif language == 'korean':
        st.dataframe(x.korean_df, 700, 500)
    elif language == 'japanese':
        st.dataframe(x.japanese_df, 700, 500)
        