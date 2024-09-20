import json

import pandas as pd
import pytest


@pytest.fixture
def transactions_data():
    data = {
        "Номер карты": ["1234", "1234", "5678", "5678", "5678"],
        "Сумма платежа": [-100, -200, -50, -150, -300],
        "Дата платежа": ["20.12.2021", "21.12.2021", "22.12.2021", "23.12.2021", "24.12.2021"],
        "Категория": ["Супермаркеты", "Рестораны", "Супермаркеты", "Развлечения", "Супермаркеты"],
        "Описание": ["Лента", "Пицца", "Ашан", "Кино", "Магнит"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_user_settings():
    return json.dumps(
        {
            "user_currencies": ["USD", "EUR"],
            "user_stocks": ["AAPL", "GOOGL"],
        }
    )
