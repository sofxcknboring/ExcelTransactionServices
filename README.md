# README

### Приложение для анализа транзакций.
#### Генерирует JSON-данные для веб-страниц.
#### Формирует Excel-отчеты.
#### Предоставляет другие сервисы.


## Установка

1. Убедитесь, что установлен [Poetry](https://python-poetry.org/).
2. Клонируйте репозиторий:
```bash
git clone <URL_репозитория>
cd <имя_папки_репозитория>
```
3. Установите зависимости:
```bash
poetry install
```

## Использование

Вы можете выгрузить и использовать собственный файл из личного кабинета «Тинькофф Банка» («Т-Банка»).

#### views.py

Возвращает данные с начала месяца, на который выпадает входящая дата, по входящую дату.
    Курс валют и акции.
```python
def get_homepage_json(filter_date: str) -> str
        :param filter_date: %d.%m.%Y
        :return:{
            "greeting": str,
            "cards": list[dict],
            "top_transactions": list[dict],
            "currency_rates": list[dict],
            "stock_prices": list[dict],
        }
```

#### services.py
Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями, содержащими запрос в описании или категории
```python
def search_transactions(transactions: pd.DataFrame, keyword: str) -> str:
    """
    Поиск по всем транзакциям, содержащими запрос в описании или категории.
    :param transactions: DataFrame с транзакциями
    :param keyword: Ключевое слово для поиска
    :return: JSON ответ
    """
```

#### reports.py

Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).

```python
def spending_by_category(transactions: pd.DataFrame, category: str, date_str: Optional[str] = None) -> str:
    """
    :param transactions: DataFrame с данными о транзакциях
    :param category: Категория для фильтра
    :param date_str: "%d.%m.%Y". Если дата не передана, то берется текущая дата.
    """
```

#### main.py

Модуль для простого ознакомления.

## Тестирование

Чтобы запустить тесты, выполните следующую команду в терминале:

```bash
  poetry run pytest
```

## Логирование

Реализовано в decorators.py
Автоматически логирует начало и конец выполнения функции и выводит информацию в консоль, 
а также ее возникшие ошибки.


