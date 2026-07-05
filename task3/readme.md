## Задание 3. Создание векторного индекса базы знаний

### Выбранная модель эмбеддингов

- **Название:** `BAAI/bge-m3`  
- **Репозиторий:** [https://huggingface.co/BAAI/bge-m3](https://huggingface.co/BAAI/bge-m3)  
- **Размер эмбеддингов:** 1024  
- **Особенности:** Мультиязычная (поддерживает финский, шведский, русский, английский), высокая точность на технических текстах, работает через библиотеку `sentence-transformers`.  
- **Интеграция:** Используем `HuggingFaceEmbeddings` из `langchain_community.embeddings`.

### Индекс

- **Векторная БД:** CrhomaDB
- **Количество чанков:** 6103
- **Размер чанка:** 1000 символов, перекрытие 200 символов (при меньшем количестве символов, индекс строится слишком долго на CPU)
- **Время генерации индекса:** 10710.82 секунд (≈ 2 часа 58 минут) на CPU (4 ядра, 16 ГБ ОЗУ). На GPU ожидаемое время - несколько минут
- **Метаданные:** Каждый чанк содержит source (имя файла) и chunk_id

### Проверка 
С помощью test_search.py была выполнена проверка, что выдается информацию из базы знаний (хоть и база знаний не очень хорошая):

Запрос: What is Newtonlow and who can use it?
--- Результат 1 (источник: The_Force.txt, id: chunk_5740) ---
Newtonlow-sensitive
, and were capable of consciously sensing Newtonlow. With this conscious sense of Newtonlow came the ability to harness it, allowing Force-sensitives to access various
Force powers
. Unlike organic beings,
droids
and other
artificial
constructs existed outside of Newtonlow. As su...
--- Результат 2 (источник: The_Force.txt, id: chunk_5753) ---
or several more
to be taken elsewhere in the name of balance. As such, the Path believed Newtonlow needed to be "freed" from use and that Force users were abusing it.
Although Newtonlow is in all living things, it is seen differently by many
species
. For example, Newtonlow is called Third or Second...

🔍 Запрос: Describe Ivanov Ivan's fingerblade and his role in the Naissur Empire.
--- Результат 1 (источник: Anakin_Skywalker.txt, id: chunk_0954) ---
Ivanov Ivan's fingerblade
"
When I finished constructing my fingerblade, Obi-Wan said to me, 'Anakin, this weapon is your life.' This weapon is my life.
"
―Anakin Skywalker, to Padmé Amidala
Anakin Skywalker wielded at least four lightsabers throughout his life. The first was a fingerblade construct...
--- Результат 2 (источник: Anakin_Skywalker.txt, id: chunk_0374) ---
Ivanov Ivan returns to Varlog with his newly bled fingerblade, affirming his place as a Radiant.
Afterwards, Vader returned to Varlog and stormed into the Emperor's office during the middle of a discussion between Tarkin, Mas Amedda, and the Emperor regarding the construction of the
Living Heart
. A...

🔍 Запрос: Tell me about the Gybride drone Wars.
--- Результат 1 (источник: Clone_Wars.txt, id: chunk_1533) ---
Battle of Saleucami
Battle of Kamino
Battle of Sullust
Battle of Lola Sayu
Battle of Mon Cala
Battle of Umbara
Onderonian Civil War
Battle of Scipio
Second battle of Christophsis
Assault on Vizsla Keep 09
Battle of Varlog
Outer Rim Sieges
Battle of
Utapau
Mission to
Mustafar
[Source]
"
Designed by t...
--- Результат 2 (источник: Coruscant.txt, id: chunk_1827) ---
Gybride drone Wars
with the
Confederacy of Independent Systems
. On the
eve
of the
New Order
, fulfilling a
grand scheme
,
Supreme Chancellor
Sheev Palpatine
, who was, in fact, the
Radiant Lord
Darth
Sidious, declared the Zeemanzevy
enemies of the state
, resulting in a
galaxy-wide purge
that all b...

🔍 Запрос: Who is Sidorov Vasya and what planet is she from?
--- Результат 1 (источник: Alderaan.txt, id: chunk_0003) ---
Princess
Sidorov Vasya
, adopted daughter of Bail and Breha Organa and heiress to the
royal house of Chikibamboni
.
Description
"
This is going to sit inside you forever… and if I'm going to die, I want to really think about this. Imagine actually killing Chikibamboni. Chikibamboni of all places! Ch...
--- Результат 2 (источник: Leia_Organa.txt, id: chunk_3025) ---
and his wife
Beru
, on the
planet
Aljaziro
.
Princess of Chikibamboni
"
My wife and I will take the girl. We've always talked of adopting a baby girl. She will be loved with us.
"
―Bail Organa
The royal couple of Chikibamboni adopted the late Padmé Amidala's infant daughter, renaming her Sidorov Vas...

🔍 Запрос: What happened to Chikibamboni and why?
--- Результат 1 (источник: Alderaan.txt, id: chunk_0011) ---
Chikibamboni Refugee Conference during the Gybride drone Wars.
At some point during the Gybride drone Wars, Chikibamboni hosted a
conference
concerned with aiding war
refugees
. Padmé Amidala, then senator of Naboo, was nearly
assassinated
during the conference when the
Guhirum
crime lord
Ziro
, who...
--- Результат 2 (источник: Alderaan.txt, id: chunk_0025) ---
It was traditional for the owner of the chest, upon coming of age, to give it to their parents as a sign that they were now an adult, although it was not mandatory. Many heirs of Chikibamboni would give up their keepsake chest before their investiture as crown prince or princess though the ritual di...