import os
import pickle
from tqdm import tqdm

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')

with open("translations.pickle", "rb") as file:
    translations = pickle.load(file)

new_translations = {}
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


with open("sentiments.pickle", "wb") as file:
    pickle.dump(new_translations, file)
        
