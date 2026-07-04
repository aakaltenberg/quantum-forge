#!/usr/bin/env python3
"""
Скрипт для загрузки и очистки текстов с Fandom-вики (starwars.fandom.com).
Сохраняет чистый текст каждой страницы в папку raw_docs/.
"""

import os
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# =============================================================================
# НАСТРОЙКИ
# =============================================================================
BASE_URL = "https://starwars.fandom.com/wiki/"
# Список страниц для загрузки
PAGES = [
    "Anakin_Skywalker",
    "Luke_Skywalker",
    "Leia_Organa",
    "Han_Solo",
    "Obi-Wan_Kenobi",
    "Yoda",
    "Palpatine",
    "Chewbacca",
    "R2-D2",
    "C-3PO",
    "Boba_Fett",
    "Jabba_Desilijic_Tiure",
    "Tatooine",
    "Death_Star",
    "Alderaan",
    "Hoth",
    "Endor",
    "Coruscant",
    "Dagobah",
    "Bespin",
    "Star_Destroyer",
    "Millennium_Falcon",
    "Wookiee",
    "Ewok",
    "Twi%27lek",
    "Hutt",
    "Jedi",
    "Sith",
    "Mandalorian",
    "The_Force",
    "Lightsaber",
    "Blaster",
    "Hyperdrive",
    "X-wing_starfighter",
    "TIE/ln_starfighter",
    "Droid",
    "Stormtrooper",
    "Rebel_Alliance",
    "Galactic_Empire",
    "Clone_Wars",
]

OUTPUT_DIR = Path("raw_docs")
DELAY_SECONDS = 2

# =============================================================================
# ФУНКЦИИ
# =============================================================================
def fetch_page_text(url: str) -> str:
    """
    Загружает страницу, извлекает основной текст из блока mw-parser-output.
    Возвращает очищенный текст.
    """
    print(f"  Загрузка: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Основной контент на Fandom находится в div с классом mw-parser-output
    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        print(f"  ⚠️ Не найден блок контента на странице {url}")
        return ""
    
    # Удаляем ненужные элементы: таблицы, инфобоксы, навигационные панели
    for unwanted in content_div.select(
        "table, .toc, .navbox, .mbox, .metadata, .noprint, .reference, "
        "sup.reference, .mw-editsection, .hidden, .collapsible, "
        "script, style, .sidebar, .infobox"
    ):
        unwanted.decompose()
    
    # Извлекаем текст, разделяя абзацы переносом строки
    text = content_div.get_text(separator="\n", strip=True)
    
    # Дополнительная очистка: удаляем лишние пустые строки
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)


def sanitize_filename(name: str) -> str:
    """Превращает заголовок страницы в безопасное имя файла."""
    # Заменяем пробелы и спецсимволы на подчёркивания
    safe = "".join(c if c.isalnum() or c in " _-" else "_" for c in name)
    safe = safe.strip().replace(" ", "_")
    return safe[:100]  # Ограничим длину


# =============================================================================
# ОСНОВНАЯ ЛОГИКА
# =============================================================================
def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    for page_path in PAGES:
        # Формируем полный URL
        url = BASE_URL + page_path
        
        try:
            text = fetch_page_text(url)
        except requests.exceptions.HTTPError as e:
            print(f"  ❌ Ошибка HTTP: {e}")
            continue
        except Exception as e:
            print(f"  ❌ Не удалось загрузить: {e}")
            continue
        
        if not text:
            print(f"  ⚠️ Пропускаем (пустой контент)")
            continue
        
        # Имя файла = последний сегмент URL без параметров
        raw_name = page_path.split("/")[-1]
        # Декодируем URL-encoded символы (например, %27 -> ')
        raw_name = requests.utils.unquote(raw_name)
        file_name = sanitize_filename(raw_name) + ".txt"
        file_path = OUTPUT_DIR / file_name
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        
        print(f"  ✅ Сохранено: {file_path}")
        
        time.sleep(DELAY_SECONDS)
    
    print(f"\n🎉 Готово! Файлы сохранены в {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()