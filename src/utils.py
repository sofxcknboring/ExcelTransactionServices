import datetime
import json
import os
import re

import pandas as pd
import requests
from dotenv import load_dotenv

from src.decorators import log_function_call

load_dotenv()

USER_SETTING = os.path.join(os.path.dirname(__file__), "..", "user_settings.json")
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")


@log_function_call
def read_excel() -> pd.DataFrame:
    """
    from XLSX to DataFrame
    :return: DataFrame с данными о транзакция
    """
    excel_data = pd.read_excel(DATA_FILE_PATH)
    return excel_data


@log_function_call
def get_greeting() -> str:
    """
    Приветствие в зависимости от текущего времени.
    :return: Str.
    """
    current_time = datetime.datetime.now()
    hour = current_time.hour
    return (
        "Доброе утро"
        if 5 <= hour < 12
        else "Добрый день" if 12 <= hour < 18 else "Добрый вечер" if 18 <= hour < 23 else "Доброй ночи"
    )


@log_function_call
def get_cards(transactions: pd.DataFrame) -> list[dict]:
    """
    Группирует карты и возвращает общую сумму расходов по каждой карте.
    :param transactions: DataFrame с транзакциями.
    :return: [{
        'last_digit: card_number,
        'total_spent: sum(),
        'cashback: cashback,
    }...]
    """
    cards = transactions.groupby(by="Номер карты").agg(total_spent=("Сумма платежа", lambda x: abs(x[x < 0].sum())))
    cards["cashback"] = cards["total_spent"] / 100

    result_cards_list = []

    for card_number, row in cards.iterrows():
        if row["total_spent"] > 0:
            result_cards_list.append(
                {
                    "last_digits": re.sub(r"\*+", "", card_number),
                    "total_spent": f"{row['total_spent']:.2f}",
                    "cashback": f"{row['cashback']:.2f}",
                }
            )

    return result_cards_list


@log_function_call
def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """
    Топ 5 транзакций по сумме платежа.
    :param transactions: DataFrame с транзакциями
    :return: Список словарей.
    """
    result = []

    transactions_copy = transactions.copy()
    transactions_copy["abs_amount"] = transactions_copy["Сумма платежа"].abs()

    top_transactions = transactions_copy.sort_values(by="abs_amount", ascending=False).head(5)

    for i, row in top_transactions.iterrows():
        result.append(
            {
                "date": row["Дата платежа"],
                "amount": f"{row['abs_amount']:.2f}",
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )
    return result


@log_function_call
def get_currency_rates() -> list[dict]:
    """
    Получить текущий курс валют
    :return:"currency_rates": [
    {
      "currency": "USD",
      "rate": 73.21
    },...]
    """
    with open(USER_SETTING, "r") as file:
        currencies = json.load(file)["user_currencies"]

    url = "https://api.apilayer.com/exchangerates_data/convert"
    headers = {"apikey": os.getenv("CURRENCIES_API_KEY")}

    result = []

    for curr in currencies:
        params = {
            "amount": 1,
            "from": curr,
            "to": "RUB",
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            api_response = response.json()
            result.append({"currency": curr, "rate": f"{api_response['result']:.2f}"})
            # time.sleep(5)
        else:
            print(f"Error fetching data for {curr}: {response.status_code}")
            result.append({"currency": curr, "rate": "Error"})
    return result


@log_function_call
def get_stock_prices() -> list[dict]:
    """
    Стоимость акций из S&P500.
    :return:"stock_prices": [
    {
      "stock": "AAPL",
      "price": 150.12
    },...]
    """
    try:
        with open(USER_SETTING) as file:
            stocks = json.load(file)["user_stocks"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError("Ошибка при чтении файла user_settings.json") from e

    url = "https://financialmodelingprep.com/api/v3/profile/"
    result = []

    for stock in stocks:
        try:
            response = requests.get(f'{url}{stock}?apikey={os.getenv("STOCKS_API_KEY")}')
            response.raise_for_status()

            api_response = response.json()
            if api_response:
                result.append({"stock": stock, "price": f"{float(api_response[0]['price']):.2f}"})
                # time.sleep(5)
            else:
                raise ValueError(f"Пустой ответ для акции: {stock}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Ошибка API для акции {stock}: {e}")

    return result
