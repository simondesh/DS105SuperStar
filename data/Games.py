import requests
import json
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize


class games:
    def __init__(self):
        self.df_game_name_and_id = self.get_game_name_and_id()
        self.non_english_df = pd.DataFrame()
        self.chinese_df = pd.DataFrame()
        self.korean_df = pd.DataFrame()
        self.japanese_df = pd.DataFrame()

    # create a function to extract game name and id and create a dataframe

    def get_game_name_and_id(self):
        # Get data from steam api
        url = 'https://api.steampowered.com/ISteamApps/GetAppList/v2/'
        # connect and get data, then transform it to readable data
        response = requests.get(url)
        response = json.loads(response.text)
        # extract game name and id
        game_name = [app['name'] for app in response['applist']['apps']]
        game_id = [app['appid'] for app in response['applist']['apps']]
        df_game_name_and_id = pd.DataFrame({'game_name': game_name, 'game_id': game_id})

        ###########################-CLEAN UP-###############################
        df_game_name_and_id = df_game_name_and_id.replace(r'^\s*$', np.nan, regex=True)
        # remove rows with null values
        df_game_name_and_id = df_game_name_and_id.dropna()
        # revise index
        df_game_name_and_id = df_game_name_and_id.reset_index(drop=True)
        
        return df_game_name_and_id
    
    def get_language_dataframes(self):
        # Filter out games that are not English
        non_english_pattern = r'[^\x00-\x7F]+'
        # Filter the dataframe to only include rows where the 'game_name' column contains non-English characters
        self.non_english_df = self.df_game_name_and_id[self.df_game_name_and_id['game_name'].str.contains(non_english_pattern)]

        # Filter out games in Chinese
        chinese_pattern = r'[\u4e00-\u9fff]+'
        self.chinese_df= self.non_english_df[self.non_english_df['game_name'].str.contains(chinese_pattern)]

        # extract korean games from the chinese dataframe
        korean_pattern = r'[ㄱ-ㅎㅏ-ㅣ가-힣]+'
        # Filter the dataframe to only include rows where the 'game_name' column contains Korean characters
        korean_df_1 = self.chinese_df[self.chinese_df['game_name'].str.contains(korean_pattern)]
        # extract korean games from the original dataframe
        # Filter the dataframe to only include rows where the 'game_name' column contains Korean characters
        korean_df_2 = self.df_game_name_and_id[self.df_game_name_and_id['game_name'].str.contains(korean_pattern)]
        # combine the two korean dataframes
        korean_df = pd.concat([korean_df_1, korean_df_2])
        # drop duplicates
        self.korean_df = korean_df.drop_duplicates(subset=['game_name'])

        # extract japanese games from the chinese dataframe
        japanese_pattern = r'[\u3040-\u30ff]+'
        japanese_df_1= self.chinese_df[self.chinese_df['game_name'].str.contains(japanese_pattern)]
        japanese_df_2= self.df_game_name_and_id[self.df_game_name_and_id['game_name'].str.contains(japanese_pattern)]
        # Merge the two Japanese dataframes
        japanese_df = pd.concat([japanese_df_1, japanese_df_2])
        # drop duplicates
        self.japanese_df = japanese_df.drop_duplicates(subset=['game_name'])

