import json
import re

import pandas as pd

from src.decorators import log_function_call


@log_function_call
def search_transactions(transactions: pd.DataFrame, keyword: str) -> str:
    """
    Поиск по всем транзакциям, содержащими запрос в описании или категории.
    :param transactions: DataFrame с транзакциями
    :param keyword: Ключевое слово для поиска
    :return: JSON ответ
    """
    df = transactions
    pattern = re.compile(keyword, re.IGNORECASE)
    filtered_df = df[df["Описание"].str.contains(pattern, na=False) |
                     df["Категория"].str.contains(pattern, na=False)]
    result = filtered_df.to_dict(orient="records")
    return json.dumps(result, ensure_ascii=False, indent=4)
