from src.configuration import conf
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres import PGVector

embeddings = HuggingFaceEmbeddings(model_name="DeepPavlov/rubert-base-cased")
vectorstore = PGVector(
    embeddings=embeddings,
    collection_name=conf.ps_cname,
    connection=f"postgresql+psycopg://{conf.ps_user}:{conf.ps_pass}@{conf.host}:{conf.ps_port}/{conf.ps_db}",
    use_jsonb=True,
)
