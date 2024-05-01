import pandas as pd
import numpy as numpy

import os
import nltk
import regex
import pickle
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from tqdm import tqdm
from constants import languages
# from inltk.inltk import tokenize

# Preprocess txt
def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)


def remove_special_chars(text):
    cleaned_text = regex.sub(r'[^\u0900-\u097F\s]', '', text)
    return cleaned_text


stop_words = set(nltk.corpus.stopwords.words('english'))
wnl = nltk.stem.WordNetLemmatizer()


def preprocess_txt(in_text):
    if pd.notna(in_text):
        in_txt = remove_special_chars(in_text)
        in_txt = remove_tags(in_txt)
        in_txt = in_txt.lower()
        in_txt = nltk.tokenize.word_tokenize(in_txt)
    
        # out_txt1 = []
        # for word in in_txt:
        #     if word not in stop_words:
        #         out_txt1.append(word)
    
        out_txt2 = []
        for word in in_txt:
            if word.isalpha():
                out_txt2.append(word)
    
        out_txt3 = []
        for word in out_txt2:
            blank_space_removed_token = word.strip()
            out_txt3.append(blank_space_removed_token)
    
        # out_txt4 = []
        # for word in out_txt3:
        #     out_txt4.append(wnl.lemmatize(word))
    
        return out_txt3

    else:
        return []

def translate_to_english(text, filepath):
    try:
        if len(text) > 2000:
            text = text[:2000]
        # return ' '.join(preprocess_txt(GoogleTranslator(source='auto', target='english').translate(remove_special_chars(text))))
        return ' '.join( nltk.tokenize.word_tokenize( GoogleTranslator(source='auto', target='english').translate(remove_special_chars(text)) ) )
    except:
        print(len(text))
        print()
        print(text)
        print()
        print(f"error processing text for file: {filepath}")
        exit(1)

def read_files_and_translate(directory):
    translations = {}
    print(f"Processing {directory} directory")
    for filename in tqdm(os.listdir(directory), desc = 'translating files'):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                text = file.read()
                translation = translate_to_english(text, filepath)
                translations[filename] = {"translation": translation}
    return translations

for lang in languages:

    print()
    print(f"Processing for language: {lang}..")
    print()

    directories = [f'sharechat_scraper/updated_tesseract/{lang}/5ZEBpp_{lang}/', f'sharechat_scraper/updated_tesseract/{lang}/lew5Am_{lang}/', f'sharechat_scraper/updated_tesseract/{lang}/m6d09W_{lang}/',
                    f'sharechat_scraper/updated_tesseract/{lang}/VO6Zjy_{lang}/', f'sharechat_scraper/updated_tesseract/{lang}/VO6ZVy_{lang}/']

    # Dictionary to store translations
    translations_dict = {}

    # Read files and translate text
    for directory in directories:
        translations = read_files_and_translate(directory)
        translations_dict[directory] = translations

    # Save translations to a pickle file
    pickle_file_path = f'translations/translations_{lang}.pickle'
    with open(pickle_file_path, 'wb') as file:
        pickle.dump(translations_dict, file)

    print()
    print(f"{lang} Translations saved to", pickle_file_path)
    print()

# to_text = "छ छु -र \
#  \
# dora ICN \
#  \
#   \
#  \
# Cala इ \
# हमें कह दो पाकिस्तान = \
# चले जाओ हमफिर |: \
# Kc ड \
# अपनी संघि कर लेते \
#  \
# EIS Esr Cnt hp \
# कररही है? \
#  \
# हांपंजाब सरकार \
# कररहीहै “he \
# boi \
# "

# print(f"Original Text: \n{to_text}")
# print()
# print(f"Special char removed Text: {remove_special_chars(to_text)}")
# print()
# print(f"Translated Text: \n{translate_to_english(to_text, 'path')}")