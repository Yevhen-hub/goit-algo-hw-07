import datetime

class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must have 10 digits")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

class AddressBook:
    def __init__(self):
        self.data = {}

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

            delta_days = (this_year_bday - today).days

            if 0 <= delta_days <= 7:
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
            return f"Error: {str(e)}"
    return wrapper

@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)

    if not record:
        return "Contact not found"

    record.phones = [Phone(new_phone) if p.value == old_phone else p for p in record.phones]
    return "Phone updated"


@input_error
def show_phone(args, book):
    name = args[0]
    record = book.find(name)

    if not record:
        return "Contact not found"

    return ", ".join(p.value for p in record.phones)


@input_error
def show_all(args, book):
    result = []
    for record in book.datavalues():
        phones = ", ".join(p.value for p in record.phones)
        bday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else "No birthday"
        result.append(f"{record.name.value}: {phones} | {bday}")
    return "\n".join(result)


@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)

    if not record:
        return "Contact not found"

    record.add_birthday(birthday)
    return "Birthday added"


@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)

    if not record or not record.birthday:
        return "Birthday not found"

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book):
    data = book.get_upcoming_birthdays()
    if not data:
        return "No upcoming birthdays"

    return "\n".join(f"{d['name']} -> {d['birthday']}" for d in data)

def parse_input(user_input):
    return user_input.strip().split()

def main():
    book = AddressBook()

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

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
            print("Invalid command.")


if __name__ == "__main__":
    main()