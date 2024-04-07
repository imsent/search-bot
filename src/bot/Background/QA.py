import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import spacy


def calculate_precision_recall(actual_answers, predicted_answers):
    true_positives = len(set(actual_answers) & set(predicted_answers))
    false_positives = len(predicted_answers) - true_positives
    false_negatives = len(actual_answers) - true_positives

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    return precision, recall


nlp = spacy.load("ru_core_news_lg")

with open("src/bot/Background/employees_info.json", "r") as file:
    data = json.load(file)

embeddings = []
texts = []

for industry, departments in data.items():
    for department, employees in departments.items():
        for employee, info in employees.items():
            text = f"{industry} {department} {employee} {info['Должность']}"
            for function in info['Функции']:
                text += f" {function}"
            texts.append(text)
            doc = nlp(text.lower())
            embedding = doc.vector
            embeddings.append(embedding)


def search(query_embedding, threshold=0.71):
    similarities = cosine_similarity([nlp(query_embedding).vector], embeddings)
    similar_indices = np.where(similarities > threshold)[1]
    similar_employees = [texts[i] for i in similar_indices]
    return similar_employees