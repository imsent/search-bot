from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from background.db import vectorstore

model = Ollama(model="mistral:instruct")

retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 5})
qa = RetrievalQA.from_chain_type(
    llm=model,
    retriever=retriever,
    return_source_documents=True,
)


async def search(query):
    responses = qa.invoke({"query": query})
    return [x.page_content for x in responses['source_documents']]
