from src.exceptions import PhoneException, DateFormatException
from src.models.record import Record
from src.models.address_book_fields.fields import Day

from tabulate import tabulate
from src.utils.commands_list import commands_l

from src.utils.show_input_dialog import show_input_dialog

DEFAULT_INPUT_MESSAGE = 'Enter a command'


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            return str(ve)
        except KeyError as ke:
            return str(ke)
        except IndexError:
            return "Enter value"
        except PhoneException:
            return "Phone number must contain 10 digits"
        except DateFormatException:
            return "Following date format required: DD.MM.YYYY"

    return inner


@input_error
def parse_input(user_input):
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args


@input_error
def add_contact(args, address_book):
    name, phone = args
    if name in address_book:
        phones = [p.value for p in address_book[name].phones]
        if phone in phones:
            return "Number already exist for this contact"
        else:
            address_book[name].add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        address_book.add_record(record)

    return "Contact added."


@input_error
def find_contact(args, address_book):
    value = args[0]
    return address_book.find(value)


@input_error
def change_contact(args, address_book):
    name, old_phone, new_phone = args
    if name in address_book:
        address_book[name].edit_phone(old_phone, new_phone)
        return "Contact changed"
    else:
        raise KeyError(f"Contact with name {name} doesn't exist yet")


@input_error
def delete_contact(args, address_book):
    name = args[0]
    if name in address_book:
        address_book.delete(name)
        return f"Contact '{name}' deleted successfully"
    else:
        raise KeyError(f"Contact with name {name} doesn't exist")
    

@input_error
def add_email(args, address_book):
    name, email = args
    if name in address_book:
        address_book[name].add_email(email)
        return f"Email added for {name}"
    else:
        raise KeyError(f"Contact with {name} doesn't exist")


@input_error
def change_email(args, address_book):  
    name, new_email = args
    if name in address_book:
        address_book[name].edit_email(new_email)
        return "Email changed"
    else:
        raise KeyError(f"Contact with name {name} doesn't exist")
    

@input_error
def show_email(args, address_book):
    name = args[0]
    if name in address_book and address_book[name].email:
        return f"Email of {name}: {address_book[name].email.value}"
    else:
        raise KeyError(f"Contact with {name} doesn't exist or email not set")


@input_error
def show_phone(args, address_book):
    name = args[0]
    if name in address_book:
        record = address_book[name]
        return f"Phones of {name}: {', '.join(phone.value for phone in record.phones)}"
    else:
        raise KeyError(f"Contact with name {name} doesn't exist yet")


@input_error
def show_address(args, address_book):
    name = args[0]
    if name in address_book:
        record = address_book[name]
        return f"Address of {name}: {record.address.value}"
    else:
        raise KeyError(f"Contact with name {name} doesn't exist yet")


@input_error
def show_all_contacts(address_book):
    contacts_info = ""
    if address_book.values():
        for record in address_book.values():
            contacts_info += f'{record}\n' 
    else:
        contacts_info = "You don't have any contacts yet"

    return contacts_info 


@input_error
def add_birthday(args, address_book):
    name, birthday = args
    if name in address_book:
        address_book[name].add_birthday(birthday)
        return f"Birthday added for {name}"
    else:
        raise KeyError(f"Contact with {name} doesn't exist")


@input_error
def add_address(args, address_book):
    name, *address = args
    if name in address_book:
        address_book[name].add_address(' '.join(address))
        return f"Address added for {name}"
    else:
        raise KeyError(f"Contact with {name} doesn't exist")


@input_error
def show_birthday(args, address_book):
    name = args[0]
    if name in address_book and address_book[name].birthday:
        return f"Birthday of {name}: {address_book[name].birthday}"
    else:
        raise KeyError(f"Contact with {name} doesn't exist or birthday not set")


@input_error
def birthdays(book):
    while True:
        value = show_input_dialog(DEFAULT_INPUT_MESSAGE, "Enter number of days: ")
        day = Day(value)
        validated_day = day.validate_day()
        if validated_day is not None:
            birthdays_within_days = book.get_birthdays_within_days(validated_day)
            if birthdays_within_days:
                output = ""
                for birthday_date, names in birthdays_within_days.items():
                    output += f"{birthday_date.strftime('%A, %d %B')}: {', '.join(names)}\n"
                return output
            else:
                return "No upcoming birthdays"


@input_error
def add_note(notes):
    title = show_input_dialog(DEFAULT_INPUT_MESSAGE, "Enter title: ")
    text = show_input_dialog(DEFAULT_INPUT_MESSAGE, "Enter text (optional): ")
    tags = show_input_dialog(DEFAULT_INPUT_MESSAGE, 'Enter tags separated by coma (optional): ')
    notes.add_note(title, text, tags)
    return f"Note with tile: '{title}' added."


@input_error
def delete_note(args, notes):
    title = args[0]
    return notes.delete_note_by_title(title)


@input_error
def find_note(args, notes):
    title = args[0]
    return notes.find_note_by_title(title)


@input_error
def find_note_by_tag(args, address_book):
    tag = args[0]
    return address_book.find_note_by_tag(tag)

@input_error
def update_note_by_title(notes):
    title = show_input_dialog(DEFAULT_INPUT_MESSAGE, "Enter title: ")
    text = show_input_dialog(DEFAULT_INPUT_MESSAGE, "Enter new text (optional): ")
    tags = show_input_dialog(DEFAULT_INPUT_MESSAGE, 'Enter new tags separated by coma (optional): ')
    notes.update_note_by_title(title, text, tags)
    return f"Note with tile: '{title}' updated."


def help_me():
    print("\033[94m", "Available commands:", "\033[0m")
    command_d = dict(sorted(commands_l.items()))

    hlp_tbl_headers = [
        "Command",
        "Example",
        "Description"
    ]
    hlp_tbl = [
        [
            command,
            info["example"],
            info["description"]
        ]
        for command, info in command_d.items()
    ]
    return tabulate(hlp_tbl, hlp_tbl_headers, tablefmt="rounded_grid")
