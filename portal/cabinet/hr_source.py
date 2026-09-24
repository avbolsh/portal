from datetime import date

MOCK_PROFILES = [
    {
        "full_name": "Большаков Алексей Валерьевич",
        "birth_date": date(1982, 12, 23),
        "inn": "771234567890",
        "snils": "112-233-445 95",
        "marital_status": "женат",
        "children": [
            {"name": "Большакова Анна Алексеевна", "birth_date": date(2010, 5, 14)},
            {"name": "Большаков Михаил Алексеевич", "birth_date": date(2015, 9, 2)},
        ],
        "position": "Инженер-программист",
        "department": "Отдел разработки",
        "rate": 1.0,
    },
    {
        "full_name": "Соколова Марина Игоревна",
        "birth_date": date(1990, 6, 14),
        "inn": "500677812344",
        "snils": "087-654-303 21",
        "marital_status": "замужем",
        "children": [
            {"name": "Соколова Ева Дмитриевна", "birth_date": date(2019, 2, 27)},
        ],
        "position": "Ведущий бухгалтер",
        "department": "Бухгалтерия",
        "rate": 1.0,
    },
    {
        "full_name": "Кузнецов Дмитрий Сергеевич",
        "birth_date": date(1975, 9, 2),
        "inn": "770988456122",
        "snils": "634-105-728 46",
        "marital_status": "разведён",
        "children": [],
        "position": "Начальник отдела кадров",
        "department": "Отдел кадров",
        "rate": 0.5,
    },
]


def get_employee_profile(uuid):
    if uuid:
        return MOCK_PROFILES[uuid.int % len(MOCK_PROFILES)]
    return MOCK_PROFILES[0]
