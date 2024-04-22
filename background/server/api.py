from fastapi import FastAPI
from background.QA import search
app = FastAPI()


@app.get("/search/{item}")
async def send_answer(item):
    result = await search(item)
    return {"answer": result}