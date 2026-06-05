import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __str__(self):
        return self.value


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Номер телефону має містити 10 цифр")
        super().__init__(value)

    def __str__(self):
        return self.value


class Birthday(Field):
    def __init__(self, value):
        datetime.datetime.strptime(value, "%d.%m.%Y")
        super().__init__(value)

    def __str__(self):
        return self.value


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

    def __str__(self):
        phones = ", ".join(str(p) for p in self.phones) if self.phones else "Немає телефонів"
        bday = str(self.birthday) if self.birthday else "Немає дати народження"
        return f"{self.name.value}: {phones} | {bday}"


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
            bday_date = datetime.datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
            this_year_bday = bday_date.replace(year=today.year)
            if this_year_bday < today:
                this_year_bday = bday_date.replace(year=today.year + 1)
            delta = (this_year_bday - today).days
            if 0 <= delta <= 7:
                if this_year_bday.weekday() >= 5:
                    this_year_bday += datetime.timedelta(days=7 - this_year_bday.weekday())
                result.append({
                    "name": record.name.value,
                    "birthday": this_year_bday.strftime("%d.%m.%Y")
                })
        return result

    def __str__(self):
        if not self.data:
            return "Адресна книга порожня"
        return "\n".join(str(record) for record in self.data.values())


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Недостатньо аргументів у команді."
        except KeyError:
            return "Контакт не знайдено."
        except AttributeError:
            return "Контакт не знайдено."
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
    record.edit_phone(old_phone, new_phone)
    return "Номер оновлено"


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)
    return ", ".join(p.value for p in record.phones)


@input_error
def show_all(args, book):
    return str(book)


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "День народження додано"


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if not record.birthday:
        return "День народження не знайдено"
    return record.birthday.value


@input_error
def birthdays(args, book):
    data = book.get_upcoming_birthdays()
    if not data:
        return "Немає днів народження на найближчі 7 днів"
    return "\n".join(f"{d['name']} → {d['birthday']}" for d in data)


def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return None, []
    return parts[0].lower(), parts[1:]


def main():
    book = AddressBook()
    print("Вітаю! Я бот-помічник.")
    while True:
        user_input = input("Введіть команду: ")
        command, args = parse_input(user_input)
        if not command:
            continue
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