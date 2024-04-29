import pandas as pd

import os
import pickle
import json
from tqdm import tqdm
from math import pow
from constants import languages


leader_mappings = {"5ZEBpp": "Arvind_Kejrival", "lew5Am": "Rahul_Gandhi", "m6d09W": "Narendra_Modi", "VO6Zjy": "Akhilesh_Yadav", "VO6ZVy": "Asaduddin_Owaisi"}


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


for lang in languages:
    
    labels = []
    file_paths = []
    positive_scores = []
    neutral_scores = []
    negative_scores = []
    with open(f"sentiments/sentiments_{lang}.pickle", "rb") as file:
        sentiments = pickle.load(file)

        leader_scores = {}
        for folder_path, files in sentiments.items():
            print(f"Processing Folder: {folder_path}")
            leader_hash = folder_path.split('/')[-2][:6]
            pos_scores = []
            neu_scores = []
            neg_scores = []
            likes_lst = []
            views_lst = []
            for filename, file_data in tqdm(files.items(), desc = "Calculating Average Sentiment Scores"):
                file_paths.append(folder_path + filename)
                likes, views = read_likes_views(f"sharechat_scraper/jsonl/output_{leader_hash}_{lang}.jsonl", filename[:-4])
                views = convert_to_integral_number(views)

                likes_lst.append(likes)
                views_lst.append(views)
                scaling_factor = int(likes) + pow(10, -4) / int(views) + pow(10, -4)

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

            positive_scores.extend(normalized_pos)
            neutral_scores.extend(normalized_neu)
            negative_scores.extend(normalized_neg)

            df = pd.DataFrame(columns = ['pos', 'neu', 'neg', 'likes', 'views'])
            df['pos'] = normalized_pos
            df['neu'] = normalized_neu
            df['neg'] = normalized_neg
            df['likes'] = likes_lst
            df['views'] = views_lst

            file_to_save = f'leader_sentiment_scores/{leader_mappings[leader_hash]}_{lang}.csv'
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

            with open(f"results/results_{lang}.pickle", "wb") as file:
                pickle.dump(leader_scores, file)

        for pos_score, neu_score, neg_score, filepath in zip(positive_scores, neutral_scores, negative_scores, file_paths):
            max_score = max(pos_score, neu_score, neg_score)
            if max_score == pos_score:
                label = 1
            elif max_score == neu_score:
                label = 0
            else:
                label = -1
            labels.append((filepath, label))

        df_labels = pd.DataFrame(labels, columns=['filepath', 'label'])
        df_labels.to_csv(f'gen_labels/gen_labels_{lang}.csv')