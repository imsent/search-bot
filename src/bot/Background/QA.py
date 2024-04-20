import psycopg2
import spacy
from src.configuration import conf

nlp = spacy.load("ru_core_news_lg")
conn = psycopg2.connect(
    user=conf.ps_user,
    password=conf.ps_pass,
    host=conf.ps_host,
    port=conf.ps_port,
    database=conf.ps_db
)
cur = conn.cursor()


def search(query):
    query_embedding = nlp(query).vector.tolist()
    cur.execute(
        f"SELECT content, 1 - (embedding <=> '{query_embedding}') AS cosine_similarity FROM embeddings ORDER BY cosine_similarity DESC LIMIT 1"
    )
    return cur.fetchall()[0][0]
