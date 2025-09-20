import pickle
from addressbook import AddressBook, Record


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter the argument for the command"
        except KeyError:
            return "Contact not defined!"
        except AttributeError:
            return "Contact not defined!"
    return inner


def invalid_birthday(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and birthday in format DD.NN.YYYY please."
        except AttributeError:
            return "Contact have not a date of birth!"
    return inner


@input_error
def parse_input(user_input: str) -> list[str]:
    """
    takes a user_input and splits it into commands
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook) -> str:
    """
    adds a contact to the address book
    """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@invalid_birthday
def add_birthday(args, book: AddressBook) -> str:
    """
    stores the birthday of the specified contact
    """
    name, birthday_str, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not defined!"
    record.add_birthday(birthday_str)
    return "Contact birthday update!"


@input_error
@invalid_birthday
def show_birthday(args, book: AddressBook) -> str:
    """
    returns the birthday of the specified contact
    """
    name, *_ = args
    record = book.find(name)
    if record:
        return f"Birthday {name} : {record.birthday.value}"
        


@input_error
def birthdays(book: AddressBook):
    """
    displays a list of users to be greeted within the next 7 days
    """
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays in the next 7 days."
    return "\n".join(f"Name {u['name']} : congratulation date: {u['congratulation_date']}" for u in upcoming)


@input_error
def change_contact(args, book: AddressBook) -> str:
    """
    changes an existing contact
    """
    name, old_phone, new_phone = args
    record = book.find(name)
    return record.edit_phone(old_phone, new_phone)


@input_error
def show_phone(args, book: AddressBook) -> str:
    """
    returns a list of phones of an existing contact
    """
    name = args[0]
    record = book.find(name)
    return f"Contact name: {name}, phones: {'; '.join(p.value for p in record.phones)}"


def show_all(book: AddressBook) -> str:
    """
    return the phone number and birth date for all contacts
    """
    if not book:
        return "No contacts."

    return str(book)


def save_data(book: AddressBook, filename: str = 'addressbook.pkl'):
    """
    saves address book
    """
    with open(filename, 'wb') as file:
        pickle.dump(book, file)


def load_data(filename: str = 'addressbook.pkl') -> AddressBook:
    """
    loads the address book
    """

    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except Exception:
        return AddressBook()


def main():
    # create an empty list for further filling
    book = load_data()
    print("Welcome to the assistant bot!")
    # an infinite loop in which the main logic of the program is processed
    while True:
        # receive input from the user
        user_input = input("Enter a command: ")
        # separate user input into commands and arguments
        command, *args = parse_input(user_input)
        # condition for completing an infinite loop
        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book)
            break
        # condition for making changes to an existing contact
        elif command == "change":
            print(change_contact(args, book))
        # condition for displaying one contact in the console
        elif command == "phone":
            print(show_phone(args, book))
        # condition for displaying all contacts in the console
        elif command == "all":
            print(show_all(book))
        # condition for displaying a welcome message
        elif command == "hello":
            print("How can I help you?")
        # condition for adding new phone number to dictionary
        elif command == "add":
            print(add_contact(args, book))
        # condition for all unforeseen commands
        elif command == "add-birthday":
            print(add_birthday(args, book))
        # command to display the birthday of the specified contact
        elif command == "show-birthday":
            print(show_birthday(args, book))
        # display a list of contacts whose birthday is between today and +7 days
        elif command == "birthdays":
            print(birthdays(book))
        # invalid command message
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
