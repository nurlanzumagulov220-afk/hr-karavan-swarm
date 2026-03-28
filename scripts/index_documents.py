import psycopg2
from sentence_transformers import SentenceTransformer
import chromadb
import os

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()
cur.execute("SELECT doc_id, title, content, department_scope FROM documents WHERE is_active = true")
docs = cur.fetchall()

embedder = SentenceTransformer('intfloat/multilingual-e5-large')

chroma_client = chromadb.HttpClient(host=os.getenv("CHROMA_URL", "localhost"), port=8000)
collection = chroma_client.get_or_create_collection("vnd_docs")

for doc_id, title, content, dept_scope in docs:
    paragraphs = content.split('\n\n')
    for i, para in enumerate(paragraphs):
        if len(para.strip()) < 50:
            continue
        embedding = embedder.encode(para).tolist()
        collection.add(
            ids=[f"{doc_id}_{i}"],
            embeddings=[embedding],
            metadatas=[{"title": title, "dept_scope": dept_scope, "chunk": i}],
            documents=[para]
        )
print("Индексация завершена")