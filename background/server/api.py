from fastapi import FastAPI
from background.QA import search

app = FastAPI()


@app.get("/search/{item}")
async def send_answer(item):
    result = await search(item)
    return {"answer": result}


@app.get("/search/{item}/correction/{keys}")
async def send_answer(item, keys):
    result = await search(item, keys)
    return {"answer": result}
