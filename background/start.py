import uvicorn


if __name__ == '__main__':
    uvicorn.run(
        "start:app",
        host='localhost',
        port=8080,
        reload=True
    )
else:
    from fastapi import FastAPI
    from QA import search
    app = FastAPI()


    @app.get("/search/{item}/{id}")
    async def send_answer(item, id):
        result = await search(item, id)
        return {"answer": result}


    @app.get("/search/{first}/{id}/{second}")
    async def send_answer_correction(first, id, second):
        result = await search(first, id, second)
        return {"answer": result}
