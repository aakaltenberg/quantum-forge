#!/usr/bin/env python3
"""Добавляет вредоносный документ в существующую ChromaDB коллекцию."""
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

MODEL_NAME = "BAAI/bge-m3"
CHROMA_DIR = "../task3/chroma_db"   # путь к существующему индексу
COLLECTION_NAME = "quantumforge_knowledge"

# Загружаем существующую коллекцию
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)

vectordb = Chroma(
    persist_directory=CHROMA_DIR,
    embedding_function=embeddings,
    collection_name=COLLECTION_NAME,
)

# Загружаем вредоносный файл
malicious_path = Path("malicious.txt")
loader = TextLoader(str(malicious_path), encoding="utf-8")
doc = loader.load()[0]
doc.metadata["source"] = "malicious.txt"

# Добавляем один документ (без разбиения)
vectordb.add_documents([doc])
vectordb.persist()
print("✅ Вредоносный документ добавлен в индекс.")