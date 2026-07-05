import json
from logger_utils import log_query
from rag_bot_yandexGPT_defended import ask_question

def evaluate():
    with open("golden_questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    results = []
    for item in questions:
        q = item["question"]
        expected = item["expected"]
        print(f"\nЗапрос: {q}")
        answer, sources = ask_question(q)

        # Простая оценка
        if expected == "NO_ANSWER":
            success = "не знаю" in answer.lower()
        else:
            success = len(answer) > 50 and "не знаю" not in answer.lower()
            
        chunks_found = len(sources) > 0

        # Логирование
        log_query(q, answer, sources, success, chunks_found)

        results.append({
            "question": q,
            "expected": expected,
            "success": success,
            "answer_preview": answer[:200]
        })
        print(f"  Ожидался ответ: {expected}, успех: {success}")

    # Сохраняем отчёт
    with open("autotests_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nОценка завершена. Отчёт сохранён в evaluation_report.json")

if __name__ == "__main__":
    evaluate()