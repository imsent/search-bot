from background.db import run
import spacy

nlp = spacy.load("ru_core_news_lg")


async def search(query):
    query_embedding = nlp(query).vector.tolist()
    result = await run(query_embedding)
    return result
