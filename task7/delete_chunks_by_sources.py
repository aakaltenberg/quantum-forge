from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

MODEL_NAME = "BAAI/bge-m3"
CHROMA_DIR = "../task3/chroma_db" 

embeddings = HuggingFaceEmbeddings(model_name=MODEL_NAME, model_kwargs={"device": "cpu"}, encode_kwargs={"normalize_embeddings": True})
vectordb = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings, collection_name="quantumforge_knowledge")

for source in ["The_Force.txt", "Darth_Vader.txt", "Death_Star.txt", "Galactic_Empire.txt", "Anakin_Skywalker.txt", "Alderaan.txt", "Coruscant.txt", "Clone_Wars.txt", "Dark side artifact.txt"]:
    vectordb._collection.delete(where={"source": source})
    print(f"Удалён {source}")

print("Текущий размер индекса:", vectordb._collection.count())