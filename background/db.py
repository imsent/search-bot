from src.configuration import conf
import asyncpg


async def run(query_embedding):
    conn = await asyncpg.connect(user=conf.ps_user,
                                 password=conf.ps_pass,
                                 host=conf.host,
                                 port=conf.ps_port,
                                 database=conf.ps_db)
    values = await conn.fetch(f"SELECT content, 1 - (embedding <=> '{query_embedding}') AS cosine_similarity FROM embeddings ORDER BY cosine_similarity DESC LIMIT 1")
    await conn.close()
    return values[0][0]
