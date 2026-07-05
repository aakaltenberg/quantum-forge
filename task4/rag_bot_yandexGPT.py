#!/usr/bin/env python3
"""
RAG-бот с YandexGPT для QuantumForge.
"""

import os
import sys
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Отключаем лишние предупреждения
logging.getLogger("transformers").setLevel(logging.ERROR)

load_dotenv()

# ---------------------------------------------------------------------------
# КОНФИГУРАЦИЯ
# ---------------------------------------------------------------------------
MODEL_NAME = "BAAI/bge-m3"
CHROMA_DIR = "../task3/chroma_db"
COLLECTION_NAME = "quantumforge_knowledge"

YC_API_KEY = os.getenv("YC_API_KEY")
YC_FOLDER_ID = os.getenv("YC_FOLDER_ID")
if not YC_API_KEY or not YC_FOLDER_ID:
    print("❌ Установите переменные YC_API_KEY и YC_FOLDER_ID в .env")
    sys.exit(1)

# ---------------------------------------------------------------------------
# ЭМБЕДДИНГИ И ВЕКТОРНАЯ БАЗА
# ---------------------------------------------------------------------------
print("Загрузка эмбеддингов и ChromaDB...")
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
print(f"Индекс загружен, чанков: {vectordb._collection.count()}")

# ---------------------------------------------------------------------------
# YANDEXGPT
# ---------------------------------------------------------------------------
def call_yandex_gpt(prompt: str, temperature: float = 0.0, max_tokens: int = 500) -> str:
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Authorization": f"Api-Key {YC_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "modelUri": f"gpt://{YC_FOLDER_ID}/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": temperature,
            "maxTokens": str(max_tokens)
        },
        "messages": [{"role": "user", "text": prompt}]
    }
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f"YandexGPT error {resp.status_code}: {resp.text}")
    result = resp.json()
    return result["result"]["alternatives"][0]["message"]["text"]

# ---------------------------------------------------------------------------
# ПРОМПТ (Few-shot и CoT)
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = """Ты — корпоративный ассистент компании QuantumForge. Отвечай на вопросы сотрудников на основе внутренней базы знаний.
Твоя база знаний содержит документы о вымышленной вселенной (заменённые термины из Star Wars).
Ты должен отвечать строго на основе предоставленных фрагментов документов. Если ответа нет, честно скажи: "Я не знаю".

Инструкция по формату ответа:
1. Сначала покажи свои рассуждения (шаги), как ты пришёл к ответу.
2. Затем дай окончательный ответ, используя информацию из документов.
3. Если информации недостаточно, ответь: "Я не знаю".

Примеры (Few-shot):
---
Вопрос: Кто такой Сидоров Вася?
Шаги:
1. Ищу в документах упоминания "Сидоров Вася".
2. В найденном фрагменте указано: "Сидоров Вася — принцесса Чикибамбони, лидер Альянса".
Ответ: Сидоров Вася — принцесса планеты Чикибамбони, приёмная дочь Бейла Органы, один из лидеров Альянса за восстановление Республики.

---
Вопрос: Как называется боевая станция Империи, способная уничтожать планеты?
Шаги:
1. Ищу описание супероружия Империи.
2. В документах говорится о "Живом Сердце" (Living Heart), луноподобной станции с суперлазером.
Ответ: Имперская боевая станция, уничтожившая Чикибамбони, называется "Живое Сердце" (Living Heart).

---
Теперь ответь на новый вопрос, следуя той же структуре.

Контекст (из базы знаний):
{context}

Вопрос: {question}
Помни: сначала шаги, потом ответ.
"""

# ---------------------------------------------------------------------------
# ФУНКЦИЯ RAG-ЗАПРОСА
# ---------------------------------------------------------------------------
def ask_question(query: str, k: int = 2) -> str:
    # Поиск чанков
    docs = vectordb.similarity_search(query, k=k)
    context_parts = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "неизвестен")
        snippet = doc.page_content[:800]
        context_parts.append(f"[{source}]:\n{snippet}")
    context = "\n\n".join(context_parts)

    prompt = PROMPT_TEMPLATE.format(context=context, question=query)

    answer = call_yandex_gpt(prompt)

    # Печать источников
    print("\n--- Использованные чанки ---")
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "неизвестен")
        print(f"{i+1}. Файл: {source}, начало: {doc.page_content[:120]}...")
    print("---\n")

    return answer

# ---------------------------------------------------------------------------
# КОНСОЛЬНЫЙ ИНТЕРФЕЙС
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n===== RAG-бот QuantumForge (YandexGPT) =====")
    print("Введите вопрос (или 'выход' для завершения):\n")
    while True:
        user_input = input("Вопрос: ")
        if user_input.lower() in ["выход", "exit", "quit"]:
            break
        if not user_input.strip():
            continue
        try:
            answer = ask_question(user_input)
            print(f"Ответ:\n{answer}\n")
        except Exception as e:
            print(f"Ошибка: {e}")