#!/usr/bin/env python3
"""
Ежедневное обновление векторного индекса ChromaDB.
Сканирует папку new_docs/, добавляет новые файлы.
Логирует процесс в update.log.
"""

import os
import json
import hashlib
import logging
import time
from pathlib import Path
from datetime import datetime

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# ---------------------------------------------------------------------------
# КОНФИГУРАЦИЯ
# ---------------------------------------------------------------------------
SOURCE_DIR = Path("new_docs")               # папка с новыми документами
CHROMA_DIR = "task3/chroma_db"           
COLLECTION_NAME = "quantumforge_knowledge"
INDEXED_FILES_LOG = "data/indexed_files.json"    # список уже обработанных файлов

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MODEL_NAME = "/root/.cache/huggingface/hub/models--BAAI--bge-m3/snapshots/5617a9f61b028005a4858fdac845db406aefb181"

LOG_FILE = "data/update.log"

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ---------------------------------------------------------------------------
def get_file_hash(file_path: Path) -> str:
    """Возвращает MD5-хэш полного пути к файлу (как уникальный идентификатор)."""
    return hashlib.md5(str(file_path.resolve()).encode()).hexdigest()

def load_indexed_files() -> set:
    """Загружает множество хэшей уже обработанных файлов."""
    if Path(INDEXED_FILES_LOG).exists():
        with open(INDEXED_FILES_LOG, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_indexed_files(hashes: set):
    """Сохраняет обновлённый список хэшей."""
    with open(INDEXED_FILES_LOG, "w", encoding="utf-8") as f:
        json.dump(list(hashes), f)

# ---------------------------------------------------------------------------
# ОСНОВНАЯ ЛОГИКА ОБНОВЛЕНИЯ
# ---------------------------------------------------------------------------
def update_index():
    start_time = time.time()
    logger.info("===== Запуск обновления индекса =====")
    logger.info(f"Папка-источник: {SOURCE_DIR.resolve()}")

    if not SOURCE_DIR.exists():
        logger.error(f"Папка {SOURCE_DIR} не существует. Обновление прервано.")
        return

    # Инициализация эмбеддингов и ChromaDB
    logger.info("Загрузка модели эмбеддингов...")
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
    initial_count = vectordb._collection.count()
    logger.info(f"Текущий размер индекса: {initial_count} чанков")

    # Загружаем список уже обработанных файлов
    indexed_hashes = load_indexed_files()

    # Сканируем папку и ищем новые файлы
    new_files = []
    for ext in ("*.txt", "*.md"):
        for file_path in SOURCE_DIR.glob(ext):
            file_hash = get_file_hash(file_path)
            if file_hash not in indexed_hashes:
                new_files.append(file_path)

    if not new_files:
        logger.info("Новых файлов не обнаружено.")
        logger.info(f"Обновление завершено за {time.time() - start_time:.2f} сек.")
        return

    logger.info(f"Найдено новых файлов: {len(new_files)}")

    # Разбиваем на чанки и добавляем в индекс
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
        length_function=len,
    )

    added_chunks = 0
    for file_path in new_files:
        logger.info(f"Обработка: {file_path.name}")
        try:
            loader = TextLoader(str(file_path), encoding="utf-8")
            docs = loader.load()
            for doc in docs:
                doc.metadata["source"] = file_path.name
            chunks = text_splitter.split_documents(docs)
            vectordb.add_documents(chunks)
            added_chunks += len(chunks)
            # Помечаем файл как обработанный
            indexed_hashes.add(get_file_hash(file_path))
        except Exception as e:
            logger.error(f"Ошибка при обработке {file_path.name}: {e}")

    # Сохраняем обновлённый список
    save_indexed_files(indexed_hashes)

    # Финальный отчёт
    final_count = vectordb._collection.count()
    logger.info(f"Добавлено чанков: {added_chunks}")
    logger.info(f"Новый размер индекса: {final_count}")
    logger.info(f"Обновление завершено за {time.time() - start_time:.2f} сек.")

if __name__ == "__main__":
    import schedule
    import time

    logger.info("Планировщик запущен. Обновление будет выполняться каждый день в 06:00.")
    update_index()

    # Настройка расписания (ежедневно в 06:00)
    schedule.every().day.at("06:00").do(update_index)

    # Для теста каждую минуту:
    # schedule.every(1).minutes.do(update_index)

    while True:
        schedule.run_pending()
        time.sleep(30)