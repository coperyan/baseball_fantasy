import io
import pandas as pd
import requests

DATA_URL = 'https://baseballsavant.mlb.com/leaderboard/custom?year=2021&type=batter&filter=&sort=1&sortDir=desc&min=10&selections=b_ab,b_total_pa,b_total_hits,b_single,b_double,b_triple,b_home_run,b_strikeout,b_walk,b_k_percent,b_bb_percent,batting_avg,slg_percent,on_base_percent,on_base_plus_slg,isolated_power,b_rbi,b_total_bases,r_total_stolen_base,b_hit_by_pitch,xba,xslg,woba,xwoba,xobp,xiso,barrel_batted_rate,hard_hit_percent,&chart=false&x=b_ab&y=b_ab&r=no&chartType=beeswarm&csv=true'
SAVE_PATH = 'data/statcast_batters.csv'

def refresh_data():
    res = requests.get(DATA_URL,timeout=None).content
    data = pd.read_csv(io.StringIO(res.decode('utf-8')))
    data = data.drop(['Unnamed: 32'], axis=1)
    data.to_csv(SAVE_PATH,index=False)

def get_df():
    df = pd.read_csv(SAVE_PATH)
    return df





