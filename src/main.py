from src.utils import read_excel
from src.views import get_homepage_json
from src.reports import spending_by_category
from src.services import search_transactions
import json

def main():
    user_input = None
    while True:
        if user_input is None:
            user_input = int(input('''
            1. Страница "Главная"
            2. Простой поиск по описанию или категории.
            3. Отчет. Траты по категории.
            '''))
        else:
            print(f'Выбранное действие: {user_input}. Для повторного ввода введите 0, чтобы выбрать другое действие.')
            new_input = input('Введите новое действие или 0 для повторного ввода: ')
            if new_input == '0':
                user_input = int(input('''
                1. Страница "Главная"
                2. Простой поиск по описанию или категории.
                3. Отчет. Траты по категории.
                '''))
            else:
                user_input = int(new_input)

        if user_input == 1:
            print('Выбрана Страница "Главная".\n')
            user_date_input = input('Введите дату (пример: 10.10.2021): ')
            print(get_homepage_json(user_date_input))
        elif user_input == 2:
            print('Выбран Простой поиск по описанию или категории.\n')
            user_keyword = input('Введите ключевое слово для поиска: ')
            print(search_transactions(read_excel(), user_keyword))
        elif user_input == 3:
            print('Выбран Отчет. Траты по категориям.\n')
            user_category = input('Введите категорию: ')
            user_date_input = input('Укажите дату: ')
            print(spending_by_category(read_excel(), user_category, user_date_input))
        else:
            print('Некорректный ввод. Пожалуйста, выберите действие от 1 до 3.')


if __name__ == "__main__":
    main()
