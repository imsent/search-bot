import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import spacy


nlp = spacy.load("ru_core_news_lg")

with open("src/bot/Background/employees_info.json", "r") as file:
    data = json.load(file)

embeddings = []
texts = []

for industry, departments in data.items():
    for department, employees in departments.items():
        for employee, info in employees.items():
            text = f"{employee} работает в отделе {department}, подразделения {industry}, занимает должность {info['Должность']} и выполняет функции:"
            for function in info['Функции']:
                text += f" {function},"
            text = text[:-1] + '.'
            doc = nlp(text)
            texts.append(f"ФИО: {employee}, Отдел: {department}, подразделение: {department}")
            embedding = doc.vector
            embeddings.append(embedding)


def search(query_embedding, threshold=0.71):
    similarities = cosine_similarity([nlp(query_embedding).vector], embeddings)
    similar_indices = np.where(similarities > threshold)[1]
    similar_employees = [texts[i] for i in similar_indices]
    return similar_employees