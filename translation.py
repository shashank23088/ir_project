import pandas as pd
import numpy as numpy

import os
import nltk
import pickle
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from tqdm import tqdm
from constants import languages

# Preprocess txt
def remove_tags(html):
    soup = BeautifulSoup(html, "html.parser")
    for data in soup(['style', 'script']):
        data.decompose()
    return ' '.join(soup.stripped_strings)

stop_words = set(nltk.corpus.stopwords.words('english'))
wnl = nltk.stem.WordNetLemmatizer()


def preprocess_txt(in_text):
    if pd.notna(in_text):
        in_txt = remove_tags(in_text)
        in_txt = in_txt.lower()
        in_txt = nltk.tokenize.word_tokenize(in_txt)
    
        out_txt1 = []
        for word in in_txt:
            if word not in stop_words:
                out_txt1.append(word)
    
        out_txt2 = []
        for word in out_txt1:
            if word.isalpha():
                out_txt2.append(word)
    
        out_txt3 = []
        for word in out_txt2:
            blank_space_removed_token = word.strip()
            out_txt3.append(blank_space_removed_token)
    
        out_txt4 = []
        for word in out_txt3:
            out_txt4.append(wnl.lemmatize(word))
    
        return out_txt4

    else:
        return []

def translate_to_english(text, filepath):
    try:
        # return ' '.join(preprocess_txt(GoogleTranslator(source='auto', target='english').translate(text)))
        return GoogleTranslator(source='auto', target='english').translate(text)
    except:
        print(f"error processing text for file: {filepath}")

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
    pickle_file_path = f'translations_{lang}.pickle'
    with open(pickle_file_path, 'wb') as file:
        pickle.dump(translations_dict, file)

    print()
    print(f"{lang} Translations saved to", pickle_file_path)
    print()

# to_text = "बिजेंदर बंसल ७ जुरुवात \
# प्रधानमंत्री नरेन्द्र मोदी ने कहा कि \
# कांग्रेस और घमंडिया गठबंधन \
# को अब देश में लाखों करोड़ों की \
# लागत से हो रहे विकास से दिककत \
# | है। उनकी नींद हराम हो गई हैं। वो \
# कह रहे हैं कि मोदी चुनाव की वजह \
# से लाखों करोड़ों के विकास कर रहे \
# | हैं। असल में इनके चश्मे का नंबर \
# आल नेगेटिव है। आल नेगेटिविटी \
# इनका चरित्र बन गया है। ये वो लोग \
# हैं जो चुनावी घोषणाओं की सरकार \
# चलाते थे। ये घोषणा करके घोंसले \
# में घुस गए थे। हाथ पर हाथ धरकर \
# बैठे रहे। अपनी उपलब्धियां गिनाति \
# हुए कहा कि 2024 में तीन माह के \
# भीतर ही 0 लाख करोड़ रुपये की \
# परियोजनाओं का वह स्वयं या तो \
# शिलान्यास कर चुके हैं या लोकार्पण"

# print(f"Original Text: \n{to_text}")
# print()
# print(f"Translated Text: \n{translate_to_english(to_text, 'path')}")