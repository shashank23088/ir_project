import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

from sklearn.preprocessing import label_binarize
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

# from constants import languages

sentiment_labels = [1, 0, -1]
languages = ["Hindi", "Punjabi", "Bengali"]
for lang in languages:
    print()
    print(f"Evaluating for language: {lang}")
    print()
    gen_labels = pd.read_csv(f'gen_labels/gen_labels_{lang}.csv')
    actual_labels = pd.read_csv(f'actual_labels/actual_labels_{lang}.csv')
    # actual_labels['label'] = np.random.choice(sentiment_labels, size = len(actual_labels))
    merged_df = pd.merge(gen_labels, actual_labels, left_on = 'filepath', right_on = 'file', how = 'inner')
    y_true = merged_df['label_y']
    y_pred = merged_df['label_x']

    # calculating eval metrics
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average = 'macro')
    recall = recall_score(y_true, y_pred, average = 'macro')
    f1 = f1_score(y_true, y_pred, average = 'macro')
    # roc_auc = roc_auc_score(y_true, y_pred, multi_class = 'ovo')

    # results
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")
    # print(f"ROC AUC: {roc_auc:.4f}")

    # saving the results
    with open(f'eval/eval_{lang}.txt', 'w') as f:
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1-score: {f1:.4f}\n")
        # f.write(f"ROC AUC: {roc_auc:.4f}\n")

    print(f"Evaluation results saved to 'eval/eval_{lang}.txt'")
