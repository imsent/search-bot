from langchain_community.llms import Ollama
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
import json

model = Ollama(model="mistral:instruct")
with open('employees_info.json', 'r') as f:
    data = json.load(f)

content = []
for industry, departments in data.items():
    for department, employees in departments.items():
        for employee, info in employees.items():
            text = f"{employee} работает в отделе {department}, подразделения {industry}, занимает должность {info['Должность']} и выполняет функции:"
            for function in info['Функции']:
                text += f" {function},"
            text = text[:-1] + '.'
            content.append(text)
chunking = content
embeddings = OllamaEmbeddings(model="mistral:instruct")
vectorstore = FAISS.from_texts(chunking, embeddings)
retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 5})
qa = RetrievalQA.from_chain_type(
    llm=model,
    retriever=retriever,
    return_source_documents=True,
)


async def search(query):
    responses = qa.invoke({"query": query})
    return [x.page_content for x in responses['source_documents']]
