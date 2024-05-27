import re

from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from background.db import vectorstore

template = """
<context>
{document}
</context>

Перечисли ID сотрудников из context, которые явно подходят для ответа на вопрос: {question}
"""

user_history = {}

prompt = PromptTemplate(
    input_variables=["document", "question"], template=template
)

model = Ollama(model="mistral:instruct", temperature=0)

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

    for x in range(h.count("ID")):
        try:
            ids.append(int(re.sub(r"\D", "", h[h.find('ID') + 3:h.find('ID') + 8])))
        except:
            pass
        h = h[h.find('ID') + 8:]
    result = [x for x in retrieved_docs if x.metadata['id'] in ids]
    if not result:
        result = retrieved_docs[:10]

    return [x.metadata for x in result]
