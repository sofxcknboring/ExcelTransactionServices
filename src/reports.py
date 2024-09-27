import json
from datetime import datetime
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

from src.decorators import log_function_call, report_decorator


@log_function_call
@report_decorator("reports.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date_str: Optional[str] = None) -> str:
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    :param transactions: DataFrame с данными о транзакциях
    :param category: Категория для фильтра
    :param date_str: "%d.%m.%Y". Если дата не передана, то берется текущая дата.
    """
    if date_str is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date_str, "%d.%m.%Y")

    three_months_ago = date - relativedelta(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    filtered_df = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] > three_months_ago)
        & (transactions["Дата операции"] < date)
    ].copy()

    filtered_df["Дата операции"] = filtered_df["Дата операции"].dt.strftime("%d.%m.%Y %H:%M:%S")

    if filtered_df.empty:
        return json.dumps([])

    return json.dumps(filtered_df.to_dict(orient="records"), ensure_ascii=False, indent=4)
