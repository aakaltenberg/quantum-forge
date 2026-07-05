#!/usr/bin/env python3
"""
RAG-бот с distilgpt2 для QuantumForge.
"""

import sys
import torch
import logging
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Отключаем предупреждения transformers
logging.getLogger("transformers").setLevel(logging.ERROR)

# ---------------------------------------------------------------------------
# КОНФИГУРАЦИЯ
# ---------------------------------------------------------------------------
MODEL_NAME = "BAAI/bge-m3"
CHROMA_DIR = "../task3/chroma_db"
COLLECTION_NAME = "quantumforge_knowledge"

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
# ЛОКАЛЬНАЯ МОДЕЛЬ distilgpt2
# ---------------------------------------------------------------------------
print("Загрузка distilgpt2...")
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained("distilgpt2")
model.eval()
print("Модель готова.")

# ---------------------------------------------------------------------------
# ПРОМПТ
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = """Ты ассистент. Отвечай строго по документам. Нет информации – скажи "Я не знаю". Сначала шаги, потом ответ.

Пример 1:
В: Кто такой Сидоров Вася?
Шаги: Найдено: "принцесса Чикибамбони, лидер Альянса".
О: Сидоров Вася – принцесса Чикибамбони, лидер Альянса.

Пример 2:
В: Как называется супероружие Империи?
Шаги: Найдено: "Живое Сердце".
О: Живое Сердце (Living Heart).

Теперь вопрос.

Контекст:
{context}

Вопрос: {question}
Шаги:"""

# ---------------------------------------------------------------------------
# ФУНКЦИЯ RAG-ЗАПРОСА
# ---------------------------------------------------------------------------
def ask_question(query: str, k: int = 1) -> str:
    # Поиск 1 чанка
    docs = vectordb.similarity_search(query, k=k)
    context_parts = []
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "неизвестен")
        snippet = doc.page_content[:200]   
        context_parts.append(f"[{source}]: {snippet}")
    context = "\n".join(context_parts)

    prompt = PROMPT_TEMPLATE.format(context=context, question=query)

    # Токенизация с обрезанием до 900 токенов (distilgpt2 лимит 1024)
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=900)
    input_ids = inputs["input_ids"]

    # Генерация
    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=80,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )

    # Декодирование, обрезаем исходный промпт
    full_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    if prompt in full_output:
        answer = full_output.split(prompt)[-1].strip()
    else:
        answer = full_output.strip()

    # Источники
    print("\n--- Использован чанк ---")
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "неизвестен")
        print(f"Файл: {source}, начало: {doc.page_content[:120]}...")
    print("---\n")

    return answer

# ---------------------------------------------------------------------------
# КОНСОЛЬНЫЙ ИНТЕРФЕЙС
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("\n===== RAG-бот QuantumForge (distilgpt2) =====")
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