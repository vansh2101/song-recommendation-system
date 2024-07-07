import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
import numpy as np

#* Global Functions
def sort_list_by_labels(true_labels, labels, scores):
    sorted_scores = []

    for label in true_labels:
        if label in labels:
            index = labels.index(label)
            sorted_scores.append(scores[index])
        else:
            return Exception("Label not found in the list")

    return sorted_scores


def probabilities_to_logits(probabilities):
    logits = np.log(probabilities)
    logits -= np.mean(logits)
    
    return logits.tolist()


#* Language Detector Class
class LanguageDetector:
    def __init__(self):
        self.model_name = "papluca/xlm-roberta-base-language-detection"
        self.model = pipeline("text-classification", model=self.model_name)
    
    def detect_language(self, text):
        res = self.model(text, top_k=3, truncation=True)
        out = [lang['label'] for lang in res if lang['score'] > (res[0]['score'] - 0.15)]

        return out
    

#* Zero Shot Classifier Class
class ZeroShotClassifier:
    def __init__(self):
        self.model_name = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0"
        self.classifier = pipeline("zero-shot-classification", model=self.model_name)

    def classify(self, text, labels, multi_label=False, return_logits=False):
        res = self.classifier(text, labels, multi_label=multi_label)

        out = sort_list_by_labels(labels, res["labels"], res["scores"])

        if return_logits:
            out = probabilities_to_logits(out)

        return out