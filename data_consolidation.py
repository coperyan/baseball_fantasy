import pandas as pd
import os
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import statcast_batters as batter_data
import statcast_pitchers as pitcher_data
import espn_players as espn_data

refresh_ind = False

#List of accepted player status
accepted_status = [
    'ACTIVE',
    'BEREAVEMENT',
    'DAY_TO_DAY',
    'OUT'
]

#Helper function to get fantasy score based on current stats
def get_batter_points(player):
    
    with open('batter_points.json') as f:
        stat_points = json.load(f)

    points_total = 0

    for stat in stat_points['stats']:
        points_total += player[stat['stat_col']] * stat['points']

    return points_total

#Helper function to get fantasy score based on current stats
def get_pitcher_points(player):
    
    with open('pitcher_points.json') as f:
        stat_points = json.load(f)

    points_total = 0

    for stat in stat_points['stats']:
        points_total += player[stat['stat_col']] * stat['points']

    return points_total

if refresh_ind:
    batter_data.refresh_data()
    pitcher_data.refresh_data()
    espn_data.refresh_data()

batter_df = batter_data.get_df()
pitcher_df = pitcher_data.get_df()
espn_df = espn_data.get_df()

#Helper function to join tables
def fuzzy_merge(df1,df2,key1,key2,threshold=95,limit=1):
    s = df2[key2].tolist()
    
    m = df1[key1].apply(lambda x: process.extract(x,s,limit=limit))
    df1['matches'] = m

    m2 = df1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df1['matches'] = m2

    return df1

#Working with batter data
batter_merged_df = fuzzy_merge(batter_df,espn_df,'full_name','fullName',threshold=95,limit=1)
batter_merged_df = batter_merged_df.merge(espn_df,how='left',left_on='matches',right_on='fullName')
batter_merged_df = batter_merged_df[batter_merged_df['positionName'].notna()]
batter_merged_df = batter_merged_df[batter_merged_df['injuryStatus'].isin(accepted_status)]
batter_merged_df['fantasy_points'] = batter_merged_df.apply(lambda x: get_batter_points(x),axis=1)
batter_merged_df['fantasy_rank'] = batter_merged_df['fantasy_points'].rank(method='dense',ascending=False)
batter_merged_df['fantasy_position_rank'] = batter_merged_df.groupby('positionName')['fantasy_points'].rank(method='dense',ascending=False)

#Working with pitcher data
pitcher_merged_df = fuzzy_merge(pitcher_df,espn_df,'full_name','fullName',threshold=95,limit=1)
pitcher_merged_df = pitcher_merged_df.merge(espn_df,how='left',left_on='matches',right_on='fullName')
pitcher_merged_df = pitcher_merged_df[pitcher_merged_df['positionName'].notna()]
pitcher_merged_df = pitcher_merged_df[pitcher_merged_df['injuryStatus'].isin(accepted_status)]
pitcher_merged_df['fantasy_points'] = pitcher_merged_df.apply(lambda x: get_pitcher_points(x),axis=1)
pitcher_merged_df['fantasy_rank'] = pitcher_merged_df['fantasy_points'].rank(method='dense',ascending=False)
pitcher_merged_df['fantasy_position_rank'] = pitcher_merged_df.groupby('positionName')['fantasy_points'].rank(method='dense',ascending=False)


#Saving to CSVs
batter_merged_df.to_csv('data/batters_final.csv',index=False)
pitcher_merged_df.to_csv('data/pitchers_final.csv',index=False)


