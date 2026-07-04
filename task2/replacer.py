#!/usr/bin/env python3
"""
Скрипт для замены ключевых терминов вселенной Star Wars на вымышленные аналоги.
Создаёт новую базу знаний, которую модель не сможет угадать по памяти.
"""

import os
import json
import re
from pathlib import Path

# =============================================================================
# 1. СЛОВАРЬ ЗАМЕН (исходный термин -> вымышленный)
# =============================================================================
TERM_MAP = {
    # Персонажи
    "Darth Vader": "Ivanov Ivan",
    "Luke Skywalker": "Petrov Petr",
    "Leia Organa": "Sidorov Vasya",
    "Han Solo": "Golubev Andrey",
    "Obi-Wan Kenobi": "Pushkin Alexandr",
    "Yoda": "Zoshenko Igor",
    "Emperor Palpatine": "Jhon Trumplin",
    "Chewbacca": "Snowman",
    "R2-D2": "ABC-123456789",
    "C-3PO": "CBA-987654321",
    "Boba Fett": "Zvyagencev Ivan",
    "Jabba the Hutt": "Zhirinovsky Artem",

    # Планеты и места
    "Tatooine": "Aljaziro",
    "Death Star": "Living Heart",
    "Alderaan": "Chikibamboni",
    "Hoth": "Vyazniki",
    "Endor": "Limpopo",
    "Coruscant": "Varlog",
    "Dagobah": "Ihtiandico",
    "Bespin": "Pontorez",
    "Star Destroyer": "Heart Builder",
    "Millennium Falcon": "Abstract Machinerium",

    # Расы
    "Wookiee": "Albomnus",
    "Ewok": "Kowegux",
    "Twi'lek": "Inteklop",
    "Hutt": "Guhirum",
    "Jedi": "Zeemanzevy",
    "Sith": "Radiant",
    "Mandalorian": "Politicarugbe",

    # Технологии и концепции
    "The Force": "Newtonlow",
    "lightsaber": "fingerblade",
    "blaster": "suncolt",
    "hyperdrive": "batmobile",
    "X-wing": "yo-mobile",
    "TIE fighter": "istribitel",
    "Droid": "Drone",
    "Stormtrooper": "Soldat",
    "Rebel Alliance": "Alkaida",
    "Galactic Empire": "Naissur Empire",
    "Jedi Order": "Tampliere Orden",
    "Sith Order": "Assasins Orden",
    "Force-sensitive": "Newtonlow-sensitive",

    # События / понятия
    "Clone Wars": "Gybride drone Wars",
    "Galactic Civil War": "3-th Worlds War",
    "Order 66": "Order 67",
}

# Компилируем регулярные выражения для поиска всех терминов (целые слова, регистрозависимые)
# Для словосочетаний используем границы слов \b, но это не всегда срабатывает для фраз.
# Поэтому сделаем несколько проходов: сначала заменяем длинные фразы, потом короткие.
def compile_patterns(term_map):
    """Сортирует ключи по длине (убывание) и компилирует паттерны."""
    patterns = []
    # Сортируем по длине исходной строки в символах, чтобы более длинные совпадения имели приоритет
    for key in sorted(term_map.keys(), key=lambda x: -len(x)):
        # Экранируем спецсимволы regex, но так как наши ключи простые, это не обязательно
        escaped = re.escape(key)
        # Используем границы слов для точного соответствия, если ключ начинается/заканчивается словом
        pattern = re.compile(r'\b' + escaped + r'\b', re.IGNORECASE)
        patterns.append((pattern, term_map[key]))
    return patterns

# =============================================================================
# 2. ФУНКЦИЯ ЗАМЕНЫ
# =============================================================================
def replace_terms_in_text(text, patterns):
    """Применяет замены по списку скомпилированных паттернов."""
    for pattern, replacement in patterns:
        text = pattern.sub(replacement, text)
    return text

# =============================================================================
# 3. ОСНОВНАЯ ЛОГИКА
# =============================================================================
def main():
    # Пути
    raw_dir = Path("raw_docs")          # Папка с исходными текстами
    out_dir = Path("knowledge_base")    # Папка для обработанных файлов
    terms_file = Path("terms_map.json") # Файл словаря замен

    if not raw_dir.exists():
        print(f"❌ Папка {raw_dir} не найдена. Поместите исходные тексты в raw_docs/")
        return

    # Создаём выходную папку
    out_dir.mkdir(exist_ok=True)

    # Компилируем паттерны
    patterns = compile_patterns(TERM_MAP)

    processed = 0
    # Обрабатываем все .txt и .md файлы
    for file_path in raw_dir.glob("*"):
        if file_path.suffix.lower() not in ('.txt', '.md'):
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                original_text = f.read()
        except Exception as e:
            print(f"⚠️ Не удалось прочитать {file_path.name}: {e}")
            continue

        # Замена терминов
        new_text = replace_terms_in_text(original_text, patterns)

        # Сохраняем с тем же именем в knowledge_base/
        out_path = out_dir / file_path.name
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(new_text)

        processed += 1
        print(f"✅ {file_path.name} -> {out_path.name}")

    # Сохраняем словарь замен
    with open(terms_file, 'w', encoding='utf-8') as f:
        json.dump(TERM_MAP, f, ensure_ascii=False, indent=2)

    print(f"\n🎉 Готово! Обработано файлов: {processed}")
    print(f"   Словарь замен сохранён в {terms_file}")

if __name__ == "__main__":
    main()