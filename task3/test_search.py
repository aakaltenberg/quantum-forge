from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

MODEL_NAME = "BAAI/bge-m3"
CHROMA_PERSIST_DIR = "chroma_db"

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vectordb = Chroma(
    persist_directory=CHROMA_PERSIST_DIR,
    embedding_function=embeddings,
    collection_name="quantumforge_knowledge",
)

# Тестовые запросы в терминах вымышленного мира
queries = [
    "What is Newtonlow and who can use it?",
    "Describe Ivanov Ivan's fingerblade and his role in the Naissur Empire.",
    "Tell me about the Gybride drone Wars.",
    "Who is Sidorov Vasya and what planet is she from?",
    "What happened to Chikibamboni and why?",
]

for q in queries:
    print(f"\n🔍 Запрос: {q}")
    docs = vectordb.similarity_search(q, k=2)
    for i, doc in enumerate(docs):
        print(f"--- Результат {i+1} (источник: {doc.metadata.get('source')}, id: {doc.metadata.get('chunk_id')}) ---")
        print(doc.page_content[:300] + "...")