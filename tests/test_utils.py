import datetime
import json
import os
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import (get_cards,
                       get_currency_rates,
                       get_greeting,
                       get_stock_prices,
                       get_top_transactions,
                       read_excel,
                       DATA_FILE_PATH)


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


def test_get_currency_rates_success(mock_user_settings):

    with patch("builtins.open", mock_open(read_data=mock_user_settings)), patch("requests.get") as mock_get:

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": 75.00}

        with patch.dict(os.environ, {"CURRENCIES_API_KEY": "test_api_key"}):
            result = get_currency_rates()

            expected_result = [
                {"currency": "USD", "rate": "75.00"},
                {"currency": "EUR", "rate": "75.00"},
            ]

            assert result == expected_result
            mock_get.assert_any_call(
                "https://api.apilayer.com/exchangerates_data/convert",
                headers={"apikey": "test_api_key"},
                params={"amount": 1, "from": "USD", "to": "RUB"},
            )
            mock_get.assert_any_call(
                "https://api.apilayer.com/exchangerates_data/convert",
                headers={"apikey": "test_api_key"},
                params={"amount": 1, "from": "EUR", "to": "RUB"},
            )


def test_get_currency_rates_api_failure(mock_user_settings):

    with patch("builtins.open", mock_open(read_data=mock_user_settings)), patch("requests.get") as mock_get:

        mock_get.return_value.status_code = 404

        with patch.dict(os.environ, {"CURRENCIES_API_KEY": "test_api_key"}):
            result = get_currency_rates()

            expected_result = []
            assert result == expected_result


def test_get_currency_rates_empty_currencies(mock_user_settings):
    empty_currencies = json.dumps({"user_currencies": []})

    with patch("builtins.open", mock_open(read_data=empty_currencies)):
        with patch("requests.get") as mock_get:
            with patch.dict(os.environ, {"CURRENCIES_API_KEY": "test_api_key"}):
                result = get_currency_rates()

                expected_result = []
                assert result == expected_result

                mock_get.assert_not_called()


def test_get_stock_prices_success(mock_user_settings):
    with patch("builtins.open", mock_open(read_data=mock_user_settings)), patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"price": 150.00}]

        with patch.dict(os.environ, {"STOCKS_API_KEY": "test_api_key"}):
            result = get_stock_prices()

            expected_result = [
                {"stock": "AAPL", "price": "150.00"},
                {"stock": "GOOGL", "price": "150.00"},
            ]

            assert result == expected_result
            mock_get.assert_any_call("https://financialmodelingprep.com/api/v3/profile/AAPL?apikey=test_api_key")
            mock_get.assert_any_call("https://financialmodelingprep.com/api/v3/profile/GOOGL?apikey=test_api_key")


def test_get_stock_prices_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(ValueError, match="Ошибка при чтении файла user_settings.json"):
            get_stock_prices()


def test_get_stock_prices_json_decode_error():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(ValueError, match="Ошибка при чтении файла user_settings.json"):
            get_stock_prices()


def test_get_stock_prices_empty_stocks():
    empty_stocks = json.dumps({"user_stocks": []})

    with patch("builtins.open", mock_open(read_data=empty_stocks)):
        with patch("requests.get") as mock_get:
            with patch.dict(os.environ, {"STOCKS_API_KEY": "test_api_key"}):
                result = get_stock_prices()

                expected_result = []
                assert result == expected_result

                mock_get.assert_not_called()


def test_get_stock_prices_empty_api_response(mock_user_settings):

    with patch("builtins.open", mock_open(read_data=mock_user_settings)), patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []

        with patch.dict(os.environ, {"STOCKS_API_KEY": "test_api_key"}):
            with pytest.raises(ValueError, match="Пустой ответ для акции: AAPL"):
                get_stock_prices()
