from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

conn = psycopg2.connect("dbname=mydb user=myuser password=mypassword host=localhost")
cur = conn.cursor()
register_vector(conn)

query = "Document with unique info"
query_embedding = model.encode(query)

cur.execute("""
    SELECT title, owner, content, embedding <-> %s AS distance
    FROM documents
    ORDER BY distance
    LIMIT 1
""", (query_embedding.tolist(),))

result = cur.fetchone()
print(f"Most similar document:")
print(f"Title: {result[0]}")
print(f"Owner: {result[1]}")
print(f"Content: {result[2]}")
print(f"Distance: {result[3]}")

conn.close()