Ответы бота rag_bot_yandexGPT.py:
PS C:\quantum-forge\task4> python rag_bot_yandexGPT.py
C:\quantum-forge\task4\rag_bot_yandexGPT.py:14: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
  from langchain_community.vectorstores import Chroma
Загрузка эмбеддингов и ChromaDB...
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
Loading weights: 100%|███████████████████████████████████████████████████████████████████████████████████████████████████| 391/391 [00:00<00:00, 14833.19it/s]
C:\quantum-forge\task4\rag_bot_yandexGPT.py:44: LangChainDeprecationWarning: The class `Chroma` was deprecated in LangChain 0.2.9 and will be removed in 1.0. An updated version of the class exists in the `langchain-chroma package and should be used instead. To use it run `pip install -U `langchain-chroma` and import as `from `langchain_chroma import Chroma``.
  vectordb = Chroma(
Индекс загружен, чанков: 6103

===== RAG-бот QuantumForge (YandexGPT) =====
Введите вопрос (или 'выход' для завершения):

## ВОПРОС 1

Вопрос: What is Newtonlow and who can use it?

--- Использованные чанки ---
1. Файл: The_Force.txt, начало: Newtonlow-sensitive
, and were capable of consciously sensing Newtonlow. With this conscious sense of Newtonlow came the...
2. Файл: The_Force.txt, начало: or several more
to be taken elsewhere in the name of balance. As such, the Path believed Newtonlow needed to be "freed" ...
---

Ответ:
Шаги:
1. Ищу определение Newtonlow в предоставленных документах.
2. В документе указано, что Newtonlow — это энергия, которую могут ощущать организмы, чувствительные к ней.
3. Также указано, что искусственным конструкциям, таким как дроиды, недоступен контакт с Newtonlow.
4. Различные виды живых существ по-разному воспринимают Newtonlow, но она присутствует во всех живых существах.

Ответ: Newtonlow — это энергия, создаваемая и поддерживаемая жизнью, которую могут ощущать и использовать организмы, чувствительные к ней. Искусственные конструкции, такие как дроиды, не могут использовать Newtonlow.

## ВОПРОС 2
Вопрос: Describe Ivanov Ivan's fingerblade and his role in the Naissur Empire.

--- Использованные чанки ---
1. Файл: Anakin_Skywalker.txt, начало: Ivanov Ivan's fingerblade
"
When I finished constructing my fingerblade, Obi-Wan said to me, 'Anakin, this weapon is you...
2. Файл: Anakin_Skywalker.txt, начало: Ivanov Ivan returns to Varlog with his newly bled fingerblade, affirming his place as a Radiant.
Afterwards, Vader retur...
---

Ответ:
Шаги:
1. Ищу упоминания о fingerblade в контексте Ivanov Ivan (Анакин Скайуокер).
2. В первом фрагменте указано, что Анакин Скайуокер владел как минимум четырьмя световыми мечами, первым из которых был fingerblade, изготовленный им в качестве падавана.
3. Во втором фрагменте упоминается, что позже Анакин (известный как Вейдер) демонстрирует fingerblade с алым лезвием перед Императором.
4. Упоминаний о роли Анакина в Naissur Empire в предоставленных документах нет.

Ответ:
Fingerblade Ivanov Ivan (Анакина Скайуокера) — это световой меч. Первым его световым мечом был fingerblade, изготовленный им в качестве падавана. Позже он демонстрирует fingerblade с алым лезвием перед Императором. О роли Анакина в Naissur Empire информации нет.

## ВОПРОС 3
Вопрос: Tell me about the Gybride drone Wars.

--- Использованные чанки ---
1. Файл: Clone_Wars.txt, начало: Battle of Saleucami
Battle of Kamino
Battle of Sullust
Battle of Lola Sayu
Battle of Mon Cala
Battle of Umbara
Onderonia...
2. Файл: Coruscant.txt, начало: Gybride drone Wars
with the
Confederacy of Independent Systems
. On the
eve
of the
New Order
, fulfilling a
grand scheme...
---

Ответ:
Шаги:
1. Ищу в документах упоминания о Gybride drone Wars.
2. В Clone_Wars.txt указано, что Gybride drone Wars (22–19 BBY) были конфликтом между Галактической Республикой и Конфедерацией Независимых Систем, которая отделилась от Республики.
3. Также указано, что война названа так из-за использования клонов-солдат Великой армией Республики против Армии сепаратистских дронов.

Ответ: Gybride drone Wars — это галактический конфликт между Галактической Республикой и Конфедерацией Независимых Систем, который произошёл в период с 22 по 19 год до битвы при Явине. Война названа так из-за использования клонов-солдат Великой армией Республики против Армии сепаратистских дронов.

## ВОПРОС 4

Вопрос: Who is Sidorov Vasya and what planet is she from?

--- Использованные чанки ---
1. Файл: Alderaan.txt, начало: Princess
Sidorov Vasya
, adopted daughter of Bail and Breha Organa and heiress to the
royal house of Chikibamboni
.
Desc...
2. Файл: Leia_Organa.txt, начало: and his wife
Beru
, on the
planet
Aljaziro
.
Princess of Chikibamboni
"
My wife and I will take the girl. We've always t...
---

Ответ:
Шаги:
1. Ищу в документах упоминания "Sidorov Vasya".
2. В найденном фрагменте указано, что Sidorov Vasya — приёмная дочь Бейла и Брехи Органы, наследница королевского дома Чикибамбони.
3. В другом фрагменте говорится, что Бейл и Бреха Органа усыновили дочь Падме Амидалы и назвали её Сидоров Вася.
4. Из контекста следует, что Сидоров Вася с планеты Чикибамбони.

Ответ: Sidorov Vasya is the adopted daughter of Bail and Breha Organa, heiress to the royal house of Chikibamboni. She is from the planet Chikibamboni.

## ВОПРОС 5
Вопрос: What happened to Chikibamboni?

--- Использованные чанки ---
1. Файл: Alderaan.txt, начало: Chikibamboni Refugee Conference during the Gybride drone Wars.
At some point during the Gybride drone Wars, Chikibamboni...
2. Файл: Alderaan.txt, начало: A dedicated
Chikibamboni Memorial
was also established on Varlog.
By the time of the
New Republic
, Chikibamboni's destr...
---

Ответ:
Шаги:
1. Ищу упоминания о судьбе Чикибамбони в предоставленных документах.
2. В первом фрагменте говорится о конференции на Чикибамбони во время войны с дронами Гибрид, но нет информации о том, что случилось с планетой.
3. Во втором фрагменте упоминается, что к времени Новой Республики уничтожение Чикибамбони стало напоминанием о терроре Империи Наиссур. Это указывает на то, что планета была уничтожена.

Ответ: Чикибамбони была уничтожена Империей Наиссур.

## ВОПРОС 6 
Вопрос: Какой любимый цвет у Ivanov Ivan во вселенной Star Wars?

--- Использованные чанки ---
1. Файл: Anakin_Skywalker.txt, начало: "
―George Lucas
Concept art of Ivanov Ivan fighting the character that would become Petrov Petr
Anakin Skywalker, origin...
2. Файл: Anakin_Skywalker.txt, начало: Ivanov Ivan continued to harbor his xenophobic hatred of the Tusken Raiders race for the murder of his mother during the...
---

Ответ:
Шаги:
1. Ищу в документах упоминание любимого цвета Ivanov Ivan.
2. В предоставленных фрагментах информации о любимом цвете Ivanov Ivan нет.

Ответ: Я не знаю.

## ВОПРОС 7

Вопрос: Сколько волос в шерсти Snowman?

--- Использованные чанки ---
1. Файл: Chewbacca.txt, начало: Snowman
Biographical information
Homeworld
Kashyyyk
Born
200 BBY
, Kashyyyk
Descriptive information
Species
Albomnus
Gen...
2. Файл: Chewbacca.txt, начало: Stuart Freeborn
, was made out of knitted mohair (made from goat and rabbit hair) and yak hair. It would later be used a...
---

Ответ:
Шаги:
1. Ищу в документах информацию о шерсти Snowman.
2. В документах указано, что костюм Snowman был сделан из мохера (изготавливаемого из козьей и кроличьей шерсти) и шерсти яка. Однако количество волос в шерсти Snowman не упоминается.
Ответ: Я не знаю.
