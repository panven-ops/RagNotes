import fitz
import os
import sys
import chromadb
from fastembed import TextEmbedding


PDF_FOLDER = "./pdfs"
TEXT_CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
COLLECTION_NAME = "notes"

def load_pdf(folder):  #διαβασμα pdfs
    docs = []

    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            doc = fitz.open(path)
            text = ""

            for page in doc:
                text += page.get_text()

            docs.append({"filename": filename, "text": text})
            print(f"Φορτώθηκε επιτυχώς: {filename} ({len(doc)} σελίδες)")

    return docs


def cut_chunks(text, filename):
    words = text.split()
    chunks = []

    i = 0
    chunk_id = 0
    while  i < len(words):
        chunk_words = words[i:i + TEXT_CHUNK_SIZE]
        chunk_text = " ".join(chunk_words)
        chunks.append({"id": f"{filename}_chunk_{chunk_id}",
                       "text": chunk_text,
                       "source": filename
                       })
        i += TEXT_CHUNK_SIZE - CHUNK_OVERLAP
        chunk_id += 1

    return chunks


def ingest():
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
        print(f"Φτιάχτηκε ο φάκελος {PDF_FOLDER} - βάλε όλα τα αρχεία εκεί και τρέξε από την αρχή")
        sys.exit(0)

    docs = load_pdf(PDF_FOLDER)
    if not docs:
        print(f"Δεν βρέθηκε τίποτα στον φάκελο")
        sys.exit(0)

    all_chunks = []
    for doc in docs:
        chunks = cut_chunks(doc["text"], doc["filename"])
        all_chunks.extend(chunks)
        print(f" {doc['filename']}: {len(chunks)} chunks")

    print(f"\nΣύνολο chunks: {len(all_chunks)}")
    print(f"\nΦόρτωμα embedding model...")
    embedding_model = TextEmbedding("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    client = chromadb.PersistentClient(path = "./chroma_db")

    try:
        client.delete_collection(COLLECTION_NAME)

    except:
        pass

    collection = client.create_collection(COLLECTION_NAME)

    print("Δημιουργία embeddings...")
    texts = [c["text"] for c in all_chunks]
    ids = [c["id"] for c in all_chunks]
    metadatas = [{"source": c["source"]} for c in all_chunks]

    embeddings = list(embedding_model.embed(texts))
    embeddings = [e.tolist() for e in embeddings]

    collection.add(documents = texts,
                   embeddings = embeddings,
                   ids = ids,
                   metadatas = metadatas)
    print(f"\n''Ολα έτοιμα Boss! {len(all_chunks)} chunks αποθηκεύτηκαν στο ChromaDB.")

if __name__ == "__main__":
    ingest()
