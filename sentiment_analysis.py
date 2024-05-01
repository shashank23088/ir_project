import os
import pickle
import pandas as pd
from tqdm import tqdm
from constants import languages

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')


for lang in languages:

    print()
    print(f"Getting sentiments for language: {lang}")
    print()

    with open(f"translations/translations_{lang}.pickle", "rb") as file:
        translations = pickle.load(file)

    new_translations = {}
    actual_labels_df = pd.DataFrame(columns = ["file", "text", "label"])
    file_locs = []
    texts = []
    for folder, files in translations.items():
        new_translations[folder] = {}
        print(f"Analyzing Folder: {folder}")
        for filename, sentence in tqdm(files.items(), desc = "Analyzing Sentiment"):
            if sentence["translation"] is not None:
                sid = SentimentIntensityAnalyzer()
                sentiment_scores = sid.polarity_scores(sentence["translation"])
                if not (sentiment_scores["pos"] == 0 and sentiment_scores["neu"] == 0 and sentiment_scores["neg"] == 0):
                    new_translations[folder][filename] = {}
                    new_translations[folder][filename]["scores"] = sentiment_scores
                    print(f"{filename}: {sentiment_scores}")

                    # actual labels csv making
                    file_locs.append(f"{folder}{filename}")
                    texts.append(sentence["translation"])


    print()
    print(f"Making csv for actual label insertion....")
    actual_labels_df["file"] = file_locs
    actual_labels_df["text"] = texts
    actual_labels_df.to_csv(f"actual_labels/actual_labels_{lang}.csv")
    print(f"actual label csv successfully saved!")
    print()

    with open(f"sentiments/sentiments_{lang}.pickle", "wb") as file:
        pickle.dump(new_translations, file)