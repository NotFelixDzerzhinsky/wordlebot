from multiprocessing.dummy import current_process
import pandas as pd
import numpy as np

df = pd.read_csv("leaderboard.csv")

def save_leaderboard():
    df.to_csv("leaderboard.csv", index=None)

def get_leaderboard():
    sort_list = []
    for index, row in df.iterrows():
        sort_list.append([row['count_wins'], row['full_name'], row['count_games']])

    sort_list = sorted(sort_list)
    sort_list.reverse()

    current_leaderboard = ""

    for c in range(min(10, len(sort_list))):
        current_leaderboard += str(c + 1)
        current_leaderboard += ") "
        current_leaderboard += sort_list[c][1]
        current_leaderboard += " | "
        current_leaderboard += str(sort_list[c][0])
        current_leaderboard += " | "
        current_leaderboard += str(sort_list[c][2])
        current_leaderboard += '\n'
    
    return current_leaderboard

def get_stats(user):
    if len(df.loc[df['username'] == user.id]) == 0:
        df.loc[len(df)] = [user.id, user.full_name, 0, 0, 0, 0, 0, 0, 0, 0]
        save_leaderboard()
    your_stats = ""
    your_stats += "Вы выиграли " + str(df.loc[df["username"] == user.id, 'count_wins'].tolist()[0]) + " игр из " + str(df.loc[df["username"] == user.id, 'count_games'].tolist()[0]) + '\n'
    
    your_stats += "Вы угадывали " + str(df.loc[df["username"] == user.id, 'count_one'].tolist()[0]) + " раз слово с первой попытки\n"
    your_stats += "Вы угадывали " + str(df.loc[df["username"] == user.id, 'count_two'].tolist()[0]) + " раз слово со второй попытки\n"
    your_stats += "Вы угадывали " + str(df.loc[df["username"] == user.id, 'count_three'].tolist()[0]) + " раз слово с третьей попытки\n"
    your_stats += "Вы угадывали " + str(df.loc[df["username"] == user.id, 'count_four'].tolist()[0]) + " раз слово с четвертой попытки\n"
    your_stats += "Вы угадывали " + str(df.loc[df["username"] == user.id, 'count_five'].tolist()[0]) + " раз слово с пятой попытки\n"
    your_stats += "Вы угадывали " + str(df.loc[df["username"] == user.id, 'count_six'].tolist()[0]) + " раз слово с шестой попытки\n"

    return your_stats

def change_leaderboard(user, value : int):
    if len(df.loc[df['username'] == user.id]) == 0:
        df.loc[len(df)] = [user.id, user.full_name, 0, 0, 0, 0, 0, 0, 0, 0]
        save_leaderboard()

    df.loc[df["username"] == user.id, 'count_games'] += 1
    if value > 0:
        df.loc[df["username"] == user.id, 'count_wins'] += 1
    if value == 1:
        df.loc[df["username"] == user.id, 'count_one'] += 1
    if value == 2:
        df.loc[df["username"] == user.id, 'count_two'] += 1
    if value == 3:
        df.loc[df["username"] == user.id, 'count_three'] += 1
    if value == 4:
        df.loc[df["username"] == user.id, 'count_four'] += 1
    if value == 5:
        df.loc[df["username"] == user.id, 'count_five'] += 1
    if value == 6:
        df.loc[df["username"] == user.id, 'count_six'] += 1

    save_leaderboard()