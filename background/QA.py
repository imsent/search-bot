from langchain_community.llms import Ollama
from background.db import vectorstore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import re

prompt = ChatPromptTemplate.from_template("""Перечисли ID сотрудников, которые подходят для ответа на вопрос. Если недостаточно информации для выбора сотрудника, напиши 'Мало информации'. Если вопрос не относится к сотрудникам, напиши 'Нет ответа':

<context>
{context}
</context>

Question: {input}""")

model = Ollama(model="mistral:instruct", temperature=0)

retriever = vectorstore.as_retriever(search_kwargs={'k': 10})

document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)


async def search(query):
    response = retrieval_chain.invoke({"input": query})
    print(response['answer'])
    print(response)
    if 'Нет ответа' in response['answer']:
        return ['Нет ответа']
    if 'Мало информации' in response['answer']:
        return ['Мало информации']
    h = str(response["answer"])
    ids = []
    try:
        for x in range(h.count("ID")):
            ids.append(int(re.sub(r"\D", "", h[h.find('ID') + 3:h.find('ID') + 8])))
            h = h[h.find('ID') + 8:]
        result = [x for x in response['context'] if x.metadata['id'] in ids]
    except:
        result = response['context'][:5]
    return [x.metadata for x in result]
