import json

import pandas as pd

from src.utils import get_cards, get_currency_rates, get_greeting, get_stock_prices, get_top_transactions, read_excel


def get_homepage_json(filter_date: str) -> str:
    """
    Возвращает данные с начала месяца, на который выпадает входящая дата, по входящую дату.
    Курс валют и акции.
    :param filter_date: %d.%m.%Y
    :return:{
        "greeting": str,
        "cards": list[dict],
        "top_transactions": list[dict],
        "currency_rates": list[dict],
        "stock_prices": list[dict],
    }
    """

    df = read_excel()

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)

    parsed_filter_date = pd.to_datetime(filter_date, dayfirst=True)

    start_date = parsed_filter_date.replace(day=1)
    end_date = parsed_filter_date

    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    result_data = {
        "greeting": get_greeting(),
        "cards": get_cards(filtered_df),
        "top_transactions": get_top_transactions(filtered_df),
        "currency_rates": get_currency_rates(),
        "stock_prices": get_stock_prices(),
    }

    return json.dumps(result_data, ensure_ascii=False)

