from langchain_community.llms import Ollama
from background.db import vectorstore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
import re

prompt = ChatPromptTemplate.from_template("""Перечисли ID и должность сотрудников, которые явно подходят для ответа на вопрос:

<context>
{context}
</context>

Вопрос: {input}
Ответ в виде списка
""")


model = Ollama(model="mistral:instruct", temperature=0)

retriever = vectorstore.as_retriever(search_kwargs={'k': 15})

document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)


async def search(query):
    response = retrieval_chain.invoke({"input": query})
    # print(response['answer'])
    # print(response)
    h = str(response["answer"])
    ids = []

    for x in range(h.count("ID")):
        try:
            ids.append(int(re.sub(r"\D", "", h[h.find('ID') + 3:h.find('ID') + 8])))
        except:
            pass
        h = h[h.find('ID') + 8:]
    result = [x for x in response['context'] if x.metadata['id'] in ids]
    if not result:
        result = response['context'][:10]

    return [x.metadata for x in result]

