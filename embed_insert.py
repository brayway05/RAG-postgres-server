import argparse
import textwrap
from sentence_transformers import SentenceTransformer
import psycopg2
from pgvector.psycopg2 import register_vector

def chunk_text(text, chunk_size):
    return textwrap.wrap(text, chunk_size, break_long_words=False, replace_whitespace=False)

def main(file_path, chunk_size, doc_title, doc_owner):
    # Load Sentence Transformer model
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # PostgreSQL connection
    conn = psycopg2.connect("dbname=mydb user=myuser password=mypassword host=localhost")
    cur = conn.cursor()
    register_vector(conn)

    def get_embedding(text):
        return model.encode(text)

    def insert_document(title, owner, content, embedding):
        cur.execute(
            "INSERT INTO documents (title, owner, content, embedding) VALUES (%s, %s, %s, %s)",
            (title, owner, content, embedding.tolist())
        )

    # Read the document
    with open(file_path, 'r') as file:
        document_text = file.read()

    # Chunk the document
    chunks = chunk_text(document_text, chunk_size)

    # Process each chunk
    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        chunk_title = f"{doc_title} - Chunk {i+1}"
        insert_document(chunk_title, doc_owner, chunk, embedding)

    # Commit changes and close connection
    conn.commit()
    cur.close()
    conn.close()

    print(f"Document '{doc_title}' embedded and inserted successfully in {len(chunks)} chunks.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed and insert a document into PostgreSQL")
    parser.add_argument("--file_path", help="Path to the document text file")
    parser.add_argument("--chunk_size", type=int, help="Size of document chunks")
    parser.add_argument("--doc_title", help="Title of the document")
    parser.add_argument("--doc_owner", help="Owner of the document")
    
    args = parser.parse_args()

    main(args.file_path, args.chunk_size, args.doc_title, args.doc_owner)