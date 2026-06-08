import chromadb
from fastembed import TextEmbedding
import ollama

COLLECTION_NAME = "notes"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
OLLAMA_MODEL = "llama3.2:1b"
TOP_K = 3

def load_collection():
    client = chromadb.PersistentClient(path = "./chroma_db")
    collection = client.get_collection(COLLECTION_NAME)
    return collection

def retrieve(question, collection, embedding_model):

    question_vector = list(embedding_model.embed([question]))[0].tolist()

    result = collection.query(query_embeddings = [question_vector],
                              n_results = TOP_K,
                              include = ["documents", "metadatas", "distances"])

    chunks = []
    for i in range(len(result["documents"][0])):
        chunks.append({"text": result["documents"][0][i],
                       "source": result["metadatas"][0][i]["source"],
                       "distance": result["distances"][0][i]})

    return chunks

def ask(question, chunks):

    context = "\n\n---\n\n".join([f"Απο: {c['source']}\n{c['text']}" for c in chunks])

    prompt = f"""Απάντησε στην ερώτηση βασιζόμενος ΜΟΝΟ στο παρακάτω κείμενο από τις σημειώσεις.
Αν η απάντηση δεν υπάρχει στο κείμενο, πες "Δεν βρήκα αυτή την πληροφορία στις σημειώσεις."
Απάντησε στα ελληνικά.

ΣΗΜΕΙΩΣΕΙΣ:
{context}

ΕΡΩΤΗΣΗ: {question}

ΑΠΑΝΤΗΣΗ:"""

    response = ollama.chat(
        model = OLLAMA_MODEL,
        messages = [{"role": "user", "content": prompt}])

    return response["message"]["content"]

def main():
    print("Φόρτωμα μοντέλου embeddings...")
    embedding_model = TextEmbedding(EMBEDDING_MODEL)

    print("Σύνδεση με βάση δεδομένων...")
    collection = load_collection()

    print(f"\n✅ Όλα έτοιμα! ({collection.count()} chunks στη βάση)")
    print("Γράψε 'exit' για να βγεις\n")

    while True:
        question = input("Ερώτηση: ").strip()

        if question.lower() == "exit":
            break

        if not question:
            continue

        chunks = retrieve(question, collection, embedding_model)

        print("\n📚 Βρήκα σχετικά κομμάτια από:")
        for c in chunks:
            print(f"  - {c['source']} (distance: {c['distance']:.3f})")

        del embedding_model
        import gc
        gc.collect()

        print("\n Απάντηση:")
        answer = ask(question, chunks)
        print(answer)
        print("\n" + "─"*50 + "\n")

        embedding_model = TextEmbedding(EMBEDDING_MODEL)

if __name__ == "__main__":
    main()

