import pandas as pd

import os
import pickle
import json
from tqdm import tqdm

with open("sentiments.pickle", "rb") as file:
    sentiments = pickle.load(file)


def normalize_list(values):

    min_val = min(values)
    max_val = max(values)
    normalized_values = [(val - min_val) / (max_val - min_val) for val in values]
    
    return normalized_values


def convert_to_integral_number(string):
    parts = string.split()
    numeric_part = parts[0]
    suffix = numeric_part[-1]
    numeric_part = numeric_part[:-1]
    numeric_value = float(numeric_part)

    if suffix == 'K':
        numeric_value *= 1000
    elif suffix == 'M':
        numeric_value *= 1000000
    elif suffix == 'B':
        numeric_value *= 1000000000

    integral_number = int(numeric_value)    
    return integral_number


def read_likes_views(json_file, reqd_post_ph):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = file.readlines()

        for line in data:
            post_data = json.loads(line)
            post_ph = post_data.get('post_ph')

            if reqd_post_ph == post_ph:
                likes = post_data.get('likes')
                views = post_data.get('number_of_views')
                return likes, views
            else:
                continue


def overall_sentiment(pos, neu, neg):
    if pos >= neg and pos >= neu:
        return "Positive"
    elif neg >= pos and neg >= neu:
        return "Negative"
    else:
        return "Neutral" 


leader_mappings = {"5ZEBpp": "Arvind Kejrival", "lew5Am": "Rahul Gandhi", "m6d09W": "Narendra Modi"}
leader_scores = {}
for folder_path, files in sentiments.items():
    print(f"Processing Folder: {folder_path}")
    leader_hash = folder_path[-7:-1]
    pos_scores = []
    neu_scores = []
    neg_scores = []
    likes_lst = []
    views_lst = []
    for filename, file_data in tqdm(files.items(), desc = "Calculating Average Sentiment Scores"):
        likes, views = read_likes_views(f"sharechat_scraper/{leader_hash}.jsonl", filename[:-4])
        views = convert_to_integral_number(views)

        likes_lst.append(likes)
        views_lst.append(views)
        scaling_factor = int(views) / int(likes)

        unscaled_pos = file_data["scores"]["pos"]
        unscaled_neu = file_data["scores"]["neu"]
        unscaled_neg = file_data["scores"]["neg"]

        scaled_pos = scaling_factor * unscaled_pos
        scaled_neu = scaling_factor * unscaled_neu
        scaled_neg = scaling_factor * unscaled_neg

        pos_scores.append(scaled_pos)
        neu_scores.append(scaled_neu)
        neg_scores.append(scaled_neg)
   
    normalized_pos = normalize_list(pos_scores)
    normalized_neu = normalize_list(neu_scores)
    normalized_neg = normalize_list(neg_scores)

    df = pd.DataFrame(columns = ['pos', 'neu', 'neg', 'likes', 'views'])
    df['pos'] = normalized_pos
    df['neu'] = normalized_neu
    df['neg'] = normalized_neg
    df['likes'] = likes_lst
    df['views'] = views_lst
    file_to_save = f'{leader_mappings[leader_hash]}.csv'
    df.to_csv(file_to_save)
    print()
    print(f'Successfully saved {file_to_save}!')
    print()

    avg_leader_pos = sum(normalized_pos) / len(normalized_pos)
    avg_leader_neu = sum(normalized_neu) / len(normalized_neu)
    avg_leader_neg = sum(normalized_neg) / len(normalized_neg)

    print("***************************************")
    print(f"Leader: {leader_mappings[leader_hash]}")
    print(f"Avg. Positive Score: {avg_leader_pos}")
    print(f"Avg. Neutral Score: {avg_leader_neu}")
    print(f"Avg. Negative Score: {avg_leader_neg}")
    print(f"Overall Leader Sentiment: {overall_sentiment(avg_leader_pos, avg_leader_neu, avg_leader_neg)}")
    print("***************************************")
    print()

    leader_scores[leader_hash] = {"avg_pos": avg_leader_pos, "avg_neg": avg_leader_neg, "avg_neu": avg_leader_neu}

    with open("results.pickle", "wb") as file:
        pickle.dump(leader_scores, file)