import asyncio
import aiohttp
import json
import time
from typing import List, Dict

# Конфигурация
API_URL = "http://130.193.59.4/api/request"
OUTPUT_FILE = "test_dataset.json"
DELAY_BETWEEN_REQUESTS = 1  # в секундах

questions = [
    {
        "id": 1,
        "query": "В каком году был основан Университет ИТМО?\n1. 1899\n2. 1900\n3. 1930\n4. 1957"
    },
    {
        "id": 2,
        "query": "Сколько раз команда ИТМО выигрывала чемпионат мира по программированию ICPC?\n1. 5\n2. 7\n3. 9\n4. 11"
    },
    {
        "id": 3,
        "query": "В каком районе Санкт-Петербурга расположен главный кампус ИТМО?\n1. Петроградский\n2. Калининский\n3. Василеостровский\n4. Невский"
    },
    {
        "id": 4,
        "query": "Какой факультет НЕ входит в состав ИТМО?\n1. Факультет фотоники\n2. Факультет искусственного интеллекта\n3. Факультет робототехники\n4. Факультет биотехнологий"
    },
    {
        "id": 5,
        "query": "Какое из этих направлений НЕ является приоритетным для ИТМО?\n1. Квантовые технологии\n2. Гастрономическая физика\n3. Нейротехнологии\n4. Умные материалы"
    },
    {
        "id": 6,
        "query": "В каком предметном рейтинге QS ИТМО входит в топ-100?\n1. Computer Science\n2. Физика\n3. Математика\n4. Инженерия"
    },
    {
        "id": 7,
        "query": "С каким IT-гигантом у ИТМО есть совместная магистерская программа?\n1. Яндекс\n2. Google\n3. JetBrains\n4. 1С"
    },
    {
        "id": 8,
        "query": "Сколько общежитий имеет Университет ИТМО?\n1. 3\n2. 5\n3. 7\n4. 9"
    },
    {
        "id": 9,
        "query": "Какой из этих научных центров НЕ принадлежит ИТМО?\n1. Центр квантовых коммуникаций\n2. Центр AR/VR технологий\n3. Центр геномных исследований\n4. Центр урбанистики"
    },
    {
        "id": 10,
        "query": "Какой проект ИТМО связан с квантовыми технологиями?\n1. Российский квантовый центр\n2. Центр квантовых коммуникаций\n3. Лаборатория квантового ИИ\n4. Квантовый вычислительный кластер"
    },
    {
        "id": 11,
        "query": "Какое достижение ИТМО в области фотоники?\n1. Создание квантового компьютера\n2. Разработка фотонных чипов\n3. Изобретение лазера\n4. Создание OLED-дисплеев"
    },
    {
        "id": 12,
        "query": "Какой факультет ИТМО самый старый?\n1. Фотоника\n2. Компьютерные технологии\n3. Системы управления\n4. Точная механика"
    },
    {
        "id": 13,
        "query": "Какая компания сотрудничает с ИТМО в области ИИ?\n1. Tesla\n2. Samsung\n3. Huawei\n4. Яндекс"
    },
    {
        "id": 14,
        "query": "Какой процент иностранных студентов в ИТМО?\n1. 5-10%\n2. 15-20%\n3. 25-30%\n4. Более 40%"
    },
    {
        "id": 15,
        "query": "Какое событие ИТМО проводит ежегодно?\n1. Хакерскую олимпиаду\n2. Фестиваль света\n3. Международный форум AI\n4. Киберспортивный турнир"
    },
    {
        "id": 16,
        "query": "Расскажите о последних достижениях ИТМО в области квантовых технологий."
    },
    {
        "id": 17,
        "query": "Какие международные партнерства есть у ИТМО?"
    },
    {
        "id": 18,
        "query": "Опишите основные направления исследований в ИТМО."
    },
    {
        "id": 19,
        "query": "Какие инновационные образовательные программы предлагает ИТМО?"
    },
    {
        "id": 20,
        "query": "Расскажите о стартап-экосистеме ИТМО и наиболее успешных проектах."
    }
]

async def send_request(session, query, id):
    payload = {
        "query": query,
        "id": id
    }
    async with session.post(API_URL, json=payload) as response:
        return await response.json()

async def generate_dataset(questions: List[Dict]) -> List[Dict]:
    dataset = []
    async with aiohttp.ClientSession() as session:
        for question in questions:
            print(f"Обрабатывается вопрос {question['id']}...")
            response = await send_request(session, question["query"], question["id"])
            if response:
                dataset.append(response)
            await asyncio.sleep(DELAY_BETWEEN_REQUESTS)
    return dataset

def save_to_file(dataset: List[Dict], filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

async def main():
    print("Начало генерации датасета...")
    start_time = time.time()
    dataset = await generate_dataset(questions)
    save_to_file(dataset, OUTPUT_FILE)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Готово! Результаты сохранены в {OUTPUT_FILE}")
    print(f"Обработано вопросов: {len(dataset)}/{len(questions)}")
    print(f"Затрачено времени: {elapsed_time:.2f} секунд")

if __name__ == "__main__":
    asyncio.run(main())
