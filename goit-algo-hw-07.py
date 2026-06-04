import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Номер телефону має містити 10 цифр")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        date = datetime.datetime.strptime(value, "%d.%m.%Y").date()
        self.value = date


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def edit_phone(self, old, new):
        for i, p in enumerate(self.phones):
            if p.value == old:
                self.phones[i] = Phone(new)
                return
        raise ValueError("Старий номер не знайдено")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def get_upcoming_birthdays(self):
        today = datetime.date.today()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            bday = record.birthday.value
            this_year_bday = bday.replace(year=today.year)

            if this_year_bday < today:
                this_year_bday = bday.replace(year=today.year + 1)

            delta = (this_year_bday - today).days

            if 0 <= delta <= 7:
                if this_year_bday.weekday() >= 5:
                    this_year_bday += datetime.timedelta(days=7 - this_year_bday.weekday())

                result.append({
                    "name": record.name.value,
                    "birthday": this_year_bday.strftime("%d.%m.%Y")
                })

        return result


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"Помилка: {str(e)}"

    return wrapper


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Контакт додано."
    else:
        message = "Контакт оновлено."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)

    if not record:
        return "Контакт не знайдено"

    record.edit_phone(old_phone, new_phone)
    return "Номер оновлено"


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)

    if not record:
        return "Контакт не знайдено"

    return ", ".join(p.value for p in record.phones)


@input_error
def show_all(args, book):
    result = []
    for record in book.data.values():
        phones = ", ".join(p.value for p in record.phones)
        bday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "Немає дати народження"
        result.append(f"{record.name.value}: {phones} | {bday}")
    return "\n".join(result)


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)

    if not record:
        return "Контакт не знайдено"

    record.add_birthday(birthday)
    return "День народження додано"


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if not record or not record.birthday:
        return "День народження не знайдено"

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book):
    data = book.get_upcoming_birthdays()
    if not data:
        return "Немає днів народження на найближчі 7 днів"

    return "\n".join(f"{d['name']} → {d['birthday']}" for d in data)


def parse_input(user_input):
    return user_input.strip().split()


def main():
    book = AddressBook()
    print("Вітаю! Я бот-помічник.")

    while True:
        user_input = input("Введіть команду: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("До побачення!")
            break

        elif command == "hello":
            print("Чим можу допомогти?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()