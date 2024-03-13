from src.models.address_book import AddressBook
from src.bot_commands import *
from src.models.notes import *


def main():
    book = AddressBook()
    book.load_from_file("addressbook.pkl")
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            book.save_to_file("addressbook.pkl") 
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
            print(show_all_contacts(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(book))
        elif command == "add-address":
            print(add_address(args, book))
        elif command == "show-address":
            print(show_address(args, book))
        elif command == "add-email":
            print(add_email(args, book))
        elif command == "show-email":
            print(show_email(args, book))
        elif command == "change-email":
            print(change_email(args, book))
        elif command == "find-contact":
            print(find_contact(args, book))
        elif command == "add-note":
            print(add_note(args, book))
        elif command == "delete-note":
            print(delete_note(args, book))
        elif command == "find-note":
            print(find_note_by_title(args, book))
        
        else:
            print("Invalid command")
            
     # При виході з програми зберігаємо дані у файл
    book.save_to_file("addressbook.pkl")
    
if __name__ == "__main__":
    main()
