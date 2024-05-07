import re
from datetime import datetime
from typing import List, NamedTuple

# Шрифт
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Валидаторы
def validate_date(date_str: str) -> bool:
    """
    Проверяет, соответствует ли строка формату даты 'ДД.ММ.ГГГГ'.

    Args:
        date_str: Строка, содержащая дату для проверки.

    Returns:
        bool: Возвращает True, если строка соответствует формату, иначе False.
    """
    if re.match(r'\d{2}\.\d{2}\.\d{4}', date_str):
        try:
            datetime.strptime(date_str, '%d.%m.%Y')
            return True
        except ValueError:
            return False
    return False

def validate_category(category_str: str) -> bool:
    """
    Проверяет, соответствует ли строка одной из двух допустимых категорий: 'Доход' или 'Расход'.

    Args:
        category_str: Строка, содержащая категорию для проверки.

    Returns:
        bool: Возвращает True, если строка является 'Доход' или 'Расход', иначе False.
    """
    return category_str in ['Доход', 'Расход']


# Определение структуры записи
class Record(NamedTuple):
    date: str
    category: str
    amount: float
    description: str


# Функция для добавления записи
def add_record(records: List[Record]) -> None:
    """
    Запрашивает у пользователя данные и добавляет новую запись в список записей.

    Args:
        records: Список существующих записей.

    Returns:
        None
    """

    date_str = input("Введите дату (ДД.ММ.ГГГГ): ")
    while not validate_date(date_str):
        print("Неверный формат даты. Попробуйте снова.")
        date_str = input("Введите дату (ДД.ММ.ГГГГ): ")

    category = input("Введите категорию (Доход/Расход): ")
    while not validate_category(category):
        print("Неверная категория. Введите 'Доход' или 'Расход'.")
        category = input("Введите категорию (Доход/Расход): ")

    while True:
        amount = input("Введите сумму: ")
        if not amount.isdigit():
            print("Неверный формат суммы. Введите число.")
        else:
            break

    description = input("Введите описание: ")
    record = Record(
        date=date_str,
        category=category,
        amount=amount,
        description=description
    )
    records.append(record)
    save_records(records)
    print(f"\n\n{GREEN}Запись успешно добавлена.{RESET}")

# Функция для сохранения записей в файл
def save_records(records: List[Record]) -> None:
    """
    Сохраняет список записей в текстовый файл.

    Args:
        records: Список записей для сохранения.

    Returns:
        None
    """

    with open('records.txt', 'w') as f:
        for record in records:
            f.write(f"{record.date},{record.category},{record.amount},{record.description}\n")


# Функция для загрузки записей из файла
def load_records() -> List[Record]:
    """
    Загружает записи из текстового файла и возвращает их в виде списка.

    Returns:
        List[Record]: Список загруженных записей.
    """

    records = []
    try:
        with open('records.txt', 'r') as f:
            for line in f:
                date_str, category, amount, description = line.strip().split(',')
                records.append(Record(
                    date=date_str,
                    category=category,
                    amount=float(amount),
                    description=description
                ))
    except FileNotFoundError:
        print(f"\n{RED}Данных нет. Сначала добавьте запись.{RESET}")
    return records

# Функция для вывода баланса
def print_balance(records: List[Record]) -> None:
    """
    Выводит текущий баланс, общую сумму доходов и расходов.

    Args:
        records: Список записей для расчета баланса.

    Returns:
        None
    """

    total_income = sum(record.amount for record in records if record.category.lower() == 'доход')
    total_expense = sum(record.amount for record in records if record.category.lower() == 'расход')
    print(f"\n{BOLD}Баланс: {RESET}{total_income - total_expense}")
    print(f"{BOLD}Доходы: {RESET}{total_income}")
    print(f"{BOLD}Расходы: {RESET}{total_expense}")


# Функция для редактирования записи
def edit_record(records: List[Record]) -> None:
    """
    Позволяет пользователю редактировать существующую запись.

    Args:
        records: Список записей, одна из которых будет отредактирована.

    Returns:
        None
    """

    # Показываем все записи с их индексами для удобства выбора
    for index, record in enumerate(records):
        print(f"{index + 1}. {record.date} - {record.category} - {record.amount} - {record.description}")

    # Запрашиваем у пользователя номер записи для редактирования
    try:
        record_number = int(input("Введите номер записи для редактирования: "))
        if 1 <= record_number <= len(records):
            # Получаем запись из списка
            record = records[record_number - 1]

            # Запрашиваем у пользователя новые данные для записи
            new_date_str = input(f"Введите новую дату (ДД.ММ.ГГГГ) [{record.date}]: ") or record.date
            while not validate_date(new_date_str):
                print("Неверный формат даты. Попробуйте снова.")
                new_date_str = input(f"Введите новую дату (ДД.ММ.ГГГГ) [{record.date}]: ") or record.date

            new_category = input(f"Введите новую категорию (Доход/Расход) [{record.category}]: ") or record.category
            while not validate_category(new_category):
                print("Неверная категория. Введите 'Доход' или 'Расход'.")
                new_category = input(f"Введите новую категорию (Доход/Расход) [{record.category}]: ") or record.category

            while True:
                new_amount = input(f"Введите новую сумму [{record.amount}]: ") or record.amount
                if not new_amount.isdigit():
                    print("Неверный формат суммы. Введите число.")
                else:
                    break

            new_description = input(f"Введите новое описание [{record.description}]: ") or record.description

            # Создаем новую запись с обновленными данными
            updated_record = Record(
                date=new_date_str,
                category=new_category,
                amount=float(new_amount),
                description=new_description
            )

            # Обновляем запись в списке
            records[record_number - 1] = updated_record
            save_records(records)  # Сохраняем обновленные данные в файл
            print(f"{GREEN}Запись успешно обновлена.{RESET}")
        else:
            print(f"\n{RED}Неверный номер записи. Попробуйте снова.{RESET}")
    except ValueError:
        print(f"\n{RED}Ошибка: Введено не число. Пожалуйста, введите целое число.{RESET}")


# Функция для поиска записи
def search_records(records: List[Record]) -> None:
    """
    Позволяет пользователю искать записи по дате, категории или сумме.

    Args:
        records: Список записей для поиска.

    Returns:
        None
    """

    search_type = input("Выберите тип поиска (дата, категория, сумма): ").lower()
    found_records = []

    if search_type == 'дата':
        search_date = input("Введите дату для поиска (ДД.ММ.ГГГГ): ")
        search_date = search_date
        found_records = [record for record in records if record.date == search_date]

    elif search_type == 'категория':
        search_category = input("Введите категорию для поиска (Доход/Расход): ")
        search_category = search_category
        found_records = [record for record in records if record.category.lower() == search_category.lower()]

    elif search_type == 'сумма':
        try:
            search_amount = float(input("Введите сумму для поиска: "))
            found_records = [record for record in records if record.amount == search_amount]
        except ValueError:
            print(f"\n{RED}Введите непустое значение{RESET}")

    else:
        print("Неверный тип поиска. Попробуйте снова.")
        return

    if found_records:
        print("Найденные записи:")
        for record in found_records:
            print(f"{record.date} - {record.category} - {record.amount} - {record.description}")
    else:
        print("Записи не найдены.")



# Основной цикл приложения
def main():
    """
    Основной цикл приложения, обеспечивающий интерфейс командной строки для взаимодействия с пользователем.
    
    """

    records = load_records()
    while True:
        print("\nЛичный финансовый кошелек")
        print("1. Вывести баланс")
        print("2. Добавить запись")
        print("3. Редактировать запись")
        print("4. Поиск по записям")
        print("5. Выход")
        choice = input(f"\n{YELLOW}Выберите действие: {RESET}")

        if choice == '1':
            print_balance(records)
        elif choice == '2':
            add_record(records)
        elif choice == '3':
            edit_record(records)
        elif choice == '4':
            search_records(records)
        elif choice == '5':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Выход из программы.")

