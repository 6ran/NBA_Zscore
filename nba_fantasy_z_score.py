import pandas as pd


#location of the json file
nba_json = pd.read_json(r'C:\Users\nba_stats.json', orient='columns')

#this will clean the data being used
def prepare_stats(nba_stats):

    nba_df = pd.DataFrame(nba_stats)
    drop_list = ["GROUP_SET", "W", "L", "W_PCT", "FGM", "FGA",
             "FG3A", "FG3_PCT", "FTM", "FTA", "OREB", "DREB",
             "BLKA", "PF", "PFD", "PLUS_MINUS","DD2", "TD3",
             "FAN_DUEL_PTS", "NBA_FANTASY_PTS"]
    nba_df = nba_df.drop(drop_list, axis =1)
    nba_df = nba_df[~(nba_df['MIN'] <= 10)]
    nba_df = nba_df.rename(columns={'GROUP_VALUE':'SEASON'})
    first_column = nba_df.pop('Name')
    nba_df.insert(0, 'Name', first_column)
    return nba_df

#calculates the zscore
def calculate_zscore(df):
    df_col_names = []

    for col in df.drop(['SEASON','Name'], axis=1):
        stat_mean = df[str(col)].mean()
        stat_std = df[str(col)].std()
        df[col]= (df[col] - stat_mean)/stat_std
        df_col_names.append(str(col))

    df['TOV'] = df['TOV'] * -1
    df['z_score_total'] = nba_df[df_col_names].sum(axis=1)
    df = df.sort_values(by=['z_score_total'], ascending=False)

    return df


nba_df = prepare_stats(nba_json)
nba_df = calculate_zscore(nba_df)


print(nba_df)

nba_df.to_csv('nba_proj.csv',encoding='utf-8',index=False)
