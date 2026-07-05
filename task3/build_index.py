#!/usr/bin/env python3
"""
build_index.py — создание векторного индекса с прогресс-баром.
"""

import time
from pathlib import Path
from tqdm import tqdm

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# =============================================================================
# КОНФИГУРАЦИЯ
# =============================================================================
SCRIPT_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = SCRIPT_DIR.parent / "task2" / "knowledge_base"
CHROMA_PERSIST_DIR = "chroma_db"
CHUNK_SIZE = 1000      # символов (примерно 250-300 слов)
CHUNK_OVERLAP = 200
MODEL_NAME = "BAAI/bge-m3"
BATCH_SIZE = 100       # вставляем по 100 чанков за раз

# =============================================================================
# ЗАГРУЗКА ДОКУМЕНТОВ
# =============================================================================
if not KNOWLEDGE_DIR.exists():
    raise FileNotFoundError(f"Папка {KNOWLEDGE_DIR} не найдена.")

docs = []
for file_path in KNOWLEDGE_DIR.glob("*.txt"):
    loader = TextLoader(str(file_path), encoding="utf-8")
    loaded_docs = loader.load()
    for doc in loaded_docs:
        doc.metadata["source"] = file_path.name
    docs.extend(loaded_docs)

print(f"Загружено {len(docs)} документов")

# =============================================================================
# РАЗБИЕНИЕ НА ЧАНКИ
# =============================================================================
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
    length_function=len,
)

chunks = text_splitter.split_documents(docs)
print(f"Получено {len(chunks)} чанков")

for i, chunk in enumerate(chunks):
    chunk.metadata["chunk_id"] = f"chunk_{i:04d}"

# =============================================================================
# ИНИЦИАЛИЗАЦИЯ ЭМБЕДДИНГОВ
# =============================================================================
print(f"Загрузка модели эмбеддингов: {MODEL_NAME}")
start_time = time.time()
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_NAME,
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
print(f"Модель загружена за {time.time() - start_time:.2f} сек.")

# =============================================================================
# СОЗДАНИЕ ИНДЕКСА С ПРОГРЕССОМ
# =============================================================================
print("Создание векторного индекса...")
start_time = time.time()

# Удаляем предыдущую коллекцию, если существует (чтобы не было дубликатов)
import shutil
shutil.rmtree(CHROMA_PERSIST_DIR, ignore_errors=True)

# Создаём пустую коллекцию
vectordb = Chroma(
    embedding_function=embeddings,
    persist_directory=CHROMA_PERSIST_DIR,
    collection_name="quantumforge_knowledge",
)

# Добавляем чанки порциями с индикатором прогресса
total = len(chunks)
with tqdm(total=total, desc="Индексация чанков") as pbar:
    for i in range(0, total, BATCH_SIZE):
        batch = chunks[i:i+BATCH_SIZE]
        vectordb.add_documents(batch)
        pbar.update(len(batch))

vectordb.persist()
print(f"\nИндекс построен за {time.time() - start_time:.2f} сек.")
print(f"Сохранён в {CHROMA_PERSIST_DIR}")
print(f"Коллекция содержит {vectordb._collection.count()} записей.")