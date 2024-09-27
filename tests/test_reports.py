import json
import os

from src.reports import spending_by_category


def test_spending_by_category_with_date(transactions_data):
    result = spending_by_category(transactions_data, "Супермаркеты", "24.12.2021")
    expected = [
        {
            "Дата операции": "20.12.2021 00:00:00",
            "Номер карты": "**1234",
            "Сумма платежа": -100,
            "Дата платежа": "20.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Лента",
        },
        {
            "Дата операции": "22.12.2021 00:00:00",
            "Номер карты": "**5678",
            "Сумма платежа": -50,
            "Дата платежа": "22.12.2021",
            "Категория": "Супермаркеты",
            "Описание": "Ашан",
        },
    ]
    assert json.loads(result) == expected


def test_spending_by_category_no_transactions(transactions_data):
    result = spending_by_category(transactions_data, "Недвижимость", "24.12.2021")
    expected = []
    assert json.loads(result) == expected


def test_report_file_creation(transactions_data):

    spending_by_category(transactions_data, "Супермаркеты", "24.12.2021")

    assert os.path.exists("reports.json")

    with open("reports.json", "r", encoding="utf-8") as file:
        content = file.read()
        expected = [
            {
                "Дата операции": "20.12.2021 00:00:00",
                "Номер карты": "**1234",
                "Сумма платежа": -100,
                "Дата платежа": "20.12.2021",
                "Категория": "Супермаркеты",
                "Описание": "Лента",
            },
            {
                "Дата операции": "22.12.2021 00:00:00",
                "Номер карты": "**5678",
                "Сумма платежа": -50,
                "Дата платежа": "22.12.2021",
                "Категория": "Супермаркеты",
                "Описание": "Ашан",
            },
        ]
        assert json.loads(content) == expected
