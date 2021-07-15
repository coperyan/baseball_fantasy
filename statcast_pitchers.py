import io
import pandas as pd
import requests

DATA_URL = 'https://baseballsavant.mlb.com/leaderboard/custom?year=2021&type=pitcher&filter=&sort=1&sortDir=desc&min=10&selections=p_game,p_formatted_ip,p_total_hits,p_single,p_double,p_triple,p_home_run,p_strikeout,p_walk,p_k_percent,p_bb_percent,batting_avg,slg_percent,on_base_percent,on_base_plus_slg,p_earned_run,p_run,p_save,p_blown_save,p_win,p_loss,p_era,p_starting_p,xba,xslg,woba,xwoba,xobp,xiso,exit_velocity_avg,barrel_batted_rate,hard_hit_percent,whiff_percent,groundballs_percent,&chart=false&x=p_game&y=p_game&r=no&chartType=beeswarm&csv=true'
SAVE_PATH = 'data/statcast_pitchers.csv'

def refresh_data():
    res = requests.get(DATA_URL,timeout=None).content
    data = pd.read_csv(io.StringIO(res.decode('utf-8')))
    data = data.drop(['Unnamed: 38'], axis=1)
    data.to_csv(SAVE_PATH,index=False)

def get_df():
    df = pd.read_csv(SAVE_PATH)
    df = df.rename(columns=lambda x: x.strip())
    df['first_name'] = df.apply(lambda x: x.first_name.strip(),axis=1)
    df['full_name'] = df.apply(lambda x: x.first_name.strip() + ' ' + x.last_name.strip(),axis=1)
    return df



