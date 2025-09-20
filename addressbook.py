from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value: str):
        if not Phone.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits")
        super().__init__(value)

    @staticmethod
    def validate(value: str) -> bool:
        return value.strip().isdigit() and len(value.strip()) == 10


class Birthday(Field):
    def __init__(self, value: str):
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)

    def __str__(self):
        return f"| Birthday: {self.value}"


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday_date: str):
        self.birthday = Birthday(birthday_date)

    def find_phone(self, searched_phone: str):
        for phone in self.phones:
            if phone.value == searched_phone:
                return phone

    def edit_phone(self, old_phone: str, new_phone: str):
        phone = self.find_phone(old_phone)
        if not phone:
            return f"{old_phone} not defined!"
        if not Phone.validate(new_phone):
            raise ValueError(f"{new_phone} not valid phone number!")
        phone.value = new_phone
        return "Contact updated!"

    def remove_phone(self, removing_phone: str):
        phone = self.find_phone(removing_phone)
        if phone:
            self.phones.remove(phone)

    def __str__(self):
        if self.birthday is None:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        else:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)} {self.birthday}"


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()
        limit_date = today + timedelta(days=days)
        for record in self.data.values():
            birthday_str = getattr(record, 'birthday', None)
            if not birthday_str or not getattr (birthday_str, 'value', None):
                continue
            try:
                birthday_dt_object = datetime.strptime(birthday_str.value, "%d.%m.%Y").date()
            except ValueError:
                continue
            birthday_this_year = birthday_dt_object.replace(year=today.year)
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(
                    year=today.year + 1)
            if today <= birthday_this_year <= limit_date:
                birthday_this_year = AddressBook.adjust_for_weekend(
                    birthday_this_year)
                upcoming_birthdays.append(
                    {"name": record.name.value, "congratulation_date": AddressBook.date_to_string(birthday_this_year)})
        return upcoming_birthdays

    @staticmethod
    def date_to_string(input_date):
        return input_date.strftime("%d.%m.%Y")

    @staticmethod
    def find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    @staticmethod
    def adjust_for_weekend(birthday):
        if birthday.weekday() >= 5:
            return AddressBook.find_next_weekday(birthday, 0)
        return birthday

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
