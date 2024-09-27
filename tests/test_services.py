import json

import pytest

from src.services import search_transactions


@pytest.mark.parametrize(
    "search_term, expected_result",
    [
        (
            "Лента",
            [
                {
                    "Дата операции": "20.12.2021",
                    "Номер карты": "**1234",
                    "Сумма платежа": -100,
                    "Дата платежа": "20.12.2021",
                    "Категория": "Супермаркеты",
                    "Описание": "Лента",
                }
            ],
        ),
        (
            "Ашан",
            [
                {
                    "Дата операции": "22.12.2021",
                    "Номер карты": "**5678",
                    "Сумма платежа": -50,
                    "Дата платежа": "22.12.2021",
                    "Категория": "Супермаркеты",
                    "Описание": "Ашан",
                }
            ],
        ),
        (
            "Рестораны",
            [
                {
                    "Дата операции": "21.12.2021",
                    "Номер карты": "**1234",
                    "Сумма платежа": -200,
                    "Дата платежа": "21.12.2021",
                    "Категория": "Рестораны",
                    "Описание": "Пицца",
                }
            ],
        ),
        ("Неизвестное", []),
    ],
)
def test_search_transactions(transactions_data, search_term, expected_result):
    result = search_transactions(transactions_data, search_term)
    result_as_dict = json.loads(result)
    assert result_as_dict == expected_result
