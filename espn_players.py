import io
import pandas as pd
import requests

DATA_URL = 'https://fantasy.espn.com/apis/v3/games/flb/seasons/2021/segments/0/leaguedefaults/1?view=kona_player_info&view=mStatRatings'
SAVE_PATH = 'data/espn_players.csv'

positions = {
    '1': 'SP',
    '2': 'C',
    '3': '1B',
    '4': '2B',
    '6': 'SS',
    '5': '3B',
    '7': 'LF',
    '8': 'CF',
    '9': 'RF',
    '10': 'DH',
    '11': 'RP'
}

#Column list
col_list = ['id','firstName','lastName','fullName','defaultPositionId','active','injured','injuryStatus']


def refresh_data():

    #Blank dataframe
    df = pd.DataFrame(columns=col_list)

    #Headers for GET
    headers = {
        'authority': 'fantasy.espn.com',
        'accept': 'application/json',
        'x-fantasy-filter': '{"players":{"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,19,21,22,23]},"sortRating":{"sortAsc":false,"sortPriority":1,"value":0},"limit":50000,"filterStatsForTopScoringPeriodIds":{"value":5,"additionalValue":["002021","102021","002020","012021","022021","032021","042021","010002021"]}}}',
    }

    #Get data
    res = requests.get(DATA_URL,headers=headers,timeout=None)
    data = res.json()

    #Iterate through player info
    for player in [x['player'] for x in data['players']]:
        base_dict = dict.fromkeys(col_list)
        for col in col_list:
            #Some have missing cols
            try:
                base_dict[col] = player[col]
            except:
                #if no valid ID, break
                if col == 'id':
                    break
                else:
                    base_dict[col] = ''
        df = df.append(base_dict,ignore_index=True)
                
    df['positionName'] = df.apply(lambda x: positions[str(x.defaultPositionId)],axis=1)

    df.to_csv(SAVE_PATH,index=False)

def get_df():
    df = pd.read_csv(SAVE_PATH)
    return df


