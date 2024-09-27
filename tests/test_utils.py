import datetime
from unittest.mock import patch

import pandas as pd
import pytest
import requests

from src.utils import (DATA_FILE_PATH, get_cards, get_currency_rates, get_greeting, get_stock_prices,
                       get_top_transactions, read_excel)


def test_read_excel_success():
    test_data = {"Column1": [1, 2, 3], "Column2": ["A", "B", "C"]}
    test_df = pd.DataFrame(test_data)

    with patch("pandas.read_excel", return_value=test_df) as mock_read_excel:
        result = read_excel()

        pd.testing.assert_frame_equal(result, test_df)
        mock_read_excel.assert_called_once_with(DATA_FILE_PATH)


def test_read_excel_file_not_found():
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            read_excel()


def test_read_excel_invalid_data():
    with patch("pandas.read_excel", return_value=None):
        result = read_excel()
        assert result is None


@pytest.mark.parametrize(
    "mock_time, expected_greeting",
    [
        (datetime.datetime(2023, 1, 1, 9, 0), "Доброе утро"),
        (datetime.datetime(2023, 1, 1, 15, 0), "Добрый день"),
        (datetime.datetime(2023, 1, 1, 20, 0), "Добрый вечер"),
        (datetime.datetime(2023, 1, 1, 23, 30), "Доброй ночи"),
        (datetime.datetime(2023, 1, 1, 0, 0), "Доброй ночи"),
    ],
)
def test_get_greeting(mock_time, expected_greeting):
    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_time
        assert get_greeting() == expected_greeting


def test_get_cards(transactions_data):
    expected_result = [
        {"last_digits": "1234", "total_spent": "300.00", "cashback": "3.00"},
        {"last_digits": "5678", "total_spent": "500.00", "cashback": "5.00"},
    ]

    result = get_cards(transactions_data)
    assert result == expected_result


def test_get_top_transactions(transactions_data):
    expected_result = [
        {"date": "24.12.2021", "amount": "300.00", "category": "Супермаркеты", "description": "Магнит"},
        {"date": "21.12.2021", "amount": "200.00", "category": "Рестораны", "description": "Пицца"},
        {"date": "23.12.2021", "amount": "150.00", "category": "Развлечения", "description": "Кино"},
        {"date": "20.12.2021", "amount": "100.00", "category": "Супермаркеты", "description": "Лента"},
        {"date": "22.12.2021", "amount": "50.00", "category": "Супермаркеты", "description": "Ашан"},
    ]

    result = get_top_transactions(transactions_data)
    assert result == expected_result


def test_get_cards_no_transactions():
    transactions = pd.DataFrame(columns=["Номер карты", "Сумма платежа"])
    expected_result = []

    result = get_cards(transactions)
    assert result == expected_result


def test_get_top_transactions_no_transactions():
    transactions = pd.DataFrame(columns=["Номер карты", "Сумма платежа", "Дата платежа", "Категория", "Описание"])
    expected_result = []

    result = get_top_transactions(transactions)
    assert result == expected_result


@patch("requests.get")
def test_get_currency_rates_success(mock_get):
    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {"result": 75.0}

    result = get_currency_rates()

    assert result == [{"currency": "USD", "rate": "75.00"}, {"currency": "EUR", "rate": "75.00"}]
    mock_get.assert_called()


@patch("requests.get")
def test_get_currency_rates_404(mock_get):
    mock_get.return_value.status_code = 404

    result = get_currency_rates()
    assert result == [{"currency": "USD", "rate": "Error"}, {"currency": "EUR", "rate": "Error"}]
    mock_get.assert_called()


@patch("requests.get")
def test_get_stock_prices_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        [{"price": 150.12}],
        [{"price": 200.00}],
        [{"price": 2500.00}],
        [{"price": 300.00}],
        [{"price": 700.00}],
    ]

    result = get_stock_prices()

    assert result == [
        {"stock": "AAPL", "price": "150.12"},
        {"stock": "AMZN", "price": "200.00"},
        {"stock": "GOOGL", "price": "2500.00"},
        {"stock": "MSFT", "price": "300.00"},
        {"stock": "TSLA", "price": "700.00"},
    ]

    assert mock_get.call_count == 5


@patch("requests.get")
def test_get_stock_prices_api_error(mock_get):
    mock_get.return_value.status_code = 404
    mock_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error: Not Found for url"
    )

    with pytest.raises(ValueError, match="Ошибка API для акции AAPL"):
        get_stock_prices()


@patch("requests.get")
def test_get_stock_prices_empty_response(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = []

    with pytest.raises(ValueError, match="Пустой ответ для акции: AAPL"):
        get_stock_prices()
