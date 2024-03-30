import pickle
from tqdm import tqdm

with open("sentiments.pickle", "rb") as file:
    sentiments = pickle.load(file)

all_count = 0
zero_count = 0

for folder, files in sentiments.items():
    print(f"Analyzing Folder: {folder}")
    for filename, sentence in tqdm(files.items(), desc = "Counting Zero-Score entries"):
        all_count += 1
        if sentence["scores"]["compound"] == 0.0:
            zero_count += 1

print(f"all counts: {all_count}")
print(f"zero counts: {zero_count}")
print(f"non-zero counts: {all_count - zero_count}")
print(f"percentage zero counts: {zero_count / all_count}")
