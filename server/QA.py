from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from server.db import vectorstore

user_history = {}

template = """
Контекст:

{document}

Задача:

Пожалуйста, извлеките ID сотрудников, которые подходят для ответа на вопрос:

{question}

Формат ответа:

Список ID подходящих сотрудников.

Пример ответа:
ID сотрудников: [12345, 67890, 11223]

Ответ:
"""

prompt = PromptTemplate(
    input_variables=["document", "question"], template=template
)

model = Ollama(model="phi3:14b", temperature=0)

retriever = vectorstore.as_retriever(search_kwargs={'k': 20})

chain = prompt | model | StrOutputParser()


async def search(query, user_id, correction=None):
    if correction is not None:
        retrieved_docs = user_history[user_id]
    else:
        user_history[user_id] = retriever.invoke(query)
        retrieved_docs = retriever.invoke(query)

    llm_answer = chain.invoke({"document": [x.page_content for x in retrieved_docs], "question": query})

    print(llm_answer)
    print(retrieved_docs)
    print(query)
    h = llm_answer
    ids = []
    try:
        ids = list(map(int, h[h.find("[") + 1: h.find(']')].replace('.', '').split(',')))
    except:
        pass
    print(ids)
    result = [x for x in retrieved_docs if x.metadata['id'] in ids]
    print(result)

    return [x.metadata for x in result]
