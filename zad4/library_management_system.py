from datetime import datetime, timedelta


def search_database(filename, record_id):  # sprawdzanie czy rekord jest w bazie danych
    with open(f'database/{filename}.txt', encoding='utf-8') as file:
        for line_number, line in enumerate(file):
            if line.strip() != "":
                if int(record_id) == int(line.split()[1]):
                    return True
    return False


def extend_book_loan_menu(username):  # cytelnik może przedłużyć wypożyczenie książki o 7 dni
    print('=' * 15 + ' EXTEND BOOK LOAN ' + '=' * 15)
    book_id = input('Book ID: ')
    while True:
        choice = input('Do you want to extend loan period of this book? (Y/N): ')
        if choice == 'Y':
            found = search_database("books", book_id) # sprawdzanie czy książka jest w bibliotece
            if not found:
                print('Book with given ID does not exist in database')
                break

            with open('database/loans.txt', encoding='utf-8') as file:  # sprawdzanie czy użytkonik wypożyczył książkę
                for line_number, line in enumerate(file):
                    if line.strip() != "":
                        if int(book_id) == int(line.split()[1]) and username == line.split()[3]:
                            you_loaned = True

            if not you_loaned:
                print("You did not loan book with given ID")
                break

            with open('database/loans.txt', encoding='utf-8') as file_read:  # cytelnik przedłużył wypożyczenie ksiązki
                lines = file_read.readlines()
                with open('database/loans.txt', 'w', encoding='utf-8') as file_write:
                    for line in lines:
                        if int(line.split()[1]) == int(book_id):
                            modified_line = line.split()
                            dt = datetime.strptime(str(modified_line[7]), '%Y/%m/%d') + timedelta(days=7)
                            modified_line[7] = dt.strftime('%Y/%m/%d')
                            file_write.write(" ".join(modified_line) + "\n")
                        else:
                            file_write.write(line)
            break
        elif choice == 'N':
            break


def reserve_book_menu(username):  # Ccytelnik może zarezerwować książkę
    print('=' * 15 + ' RESERVE BOOK ' + '=' * 15)
    book_id = input('Book ID: ')
    while True:
        choice = input('Do you want to reserve this book? (Y/N): ')
        if choice == 'Y':
            found = search_database("books", book_id)  # sprawdzanie czy książka jest w bibliotece
            if not found:
                print('Book with given ID does not exist in database')
                break

            reserved = search_database("reservations", book_id)  # sprawdzanie czy książka jest zarezerwowana
            if reserved:
                print("Chosen book is already loaned and reserved.")
                break

            with open('database/reservations.txt', 'a', encoding='utf-8') as file:  # rezerwacja książki przez czytelnika
                file.write("book_id: " + book_id + " username: " + username + " start: " +
                           datetime.today().strftime('%Y/%m/%d') + "\n")
                break
        elif choice == 'N':
            break


def loan_book_menu(username):  # czytelnik może wypożyczyć książkę
    print('=' * 15 + ' LOAN BOOK ' + '=' * 15)
    book_id = input('Book ID: ')
    while True:
        choice = input('Do you want to loan this book? (Y/N): ')
        if choice == 'Y':
            found = search_database("books", book_id)  # sprawdzanie czy książka jest w bibliotece
            if not found:
                print('Book with given ID does not exist in database')
                break

            loaned = search_database("loans", book_id)  # sprawdzanie czy książka jest wypożyczona
            if loaned:
                print("Chosen book is already loaned. You can reserve this book through menu.")
                break

            with open('database/loans.txt', 'a', encoding='utf-8') as file:  # wypożyczenie książki przez czytelnika
                end_date = datetime.today() + timedelta(days=7)
                file.write("book_id: " + book_id + " username: " + username + " start: " +
                           datetime.today().strftime('%Y/%m/%d') + " end: " + end_date.strftime('%Y/%m/%d') + "\n")
                break
        elif choice == 'N':
            break


def reader_main_menu(username):  # menu korzystania z biblioteki przez czytelnika
    menu_options = {1: 'Loan book', 2: 'Reserve book', 3: 'Extend the loan period', 4: 'Search book', 0: 'Exit'}
    menu_functions = {"1": loan_book_menu, "2": reserve_book_menu, "3": extend_book_loan_menu, "4": search_book_menu,
                      "0": exit}
    while True:
        print('='*15 + ' MAIN MENU ' + '='*15)
        for option, text in menu_options.items():
            print(str(option) + '. ' + text)
        choice = input("Enter your choice: ")
        try:
            menu_functions.get(choice)(username)
        except (KeyError, TypeError):
            print("Invalid choice. Please try again!")


def search_book_menu(username=None):  # bibliotekarz i czytelnik mogą przeglądać katalog
    print('=' * 15 + ' SEARCH BOOK ' + '=' * 15)
    search_word = input("Search book by name, author or keyword: ")
    with open('database/books.txt', encoding='utf-8') as file:
        for line_number, line in enumerate(file):
            if search_word in line and search_word != '':
                print(line)
    input("Press key to go to main menu: ")


def add_reader_menu():  # bibliotekarz może dodawać czytelników
    print('=' * 15 + ' ADD NEW READER ' + '=' * 15)
    username = input('Username: ')
    password = input('Password: ')
    while True:
        choice = input('Do you want to save changes? (Y/N): ')
        if choice == 'Y':
            with open('database/users.txt', 'a', encoding='utf-8') as file:
                file.write("login: " + "\"" + username + "\"" + " password: " + "\"" + password + "\"" + "\n")
            break
        elif choice == 'N':
            break


def delete_book_menu():  # bibliotekarz usuwa książkę z bazy danych biblioteki
    print('=' * 15 + ' DELETE BOOK ' + '=' * 15)
    delete_database_record("books")


def add_book_menu():  # bibliotekarz może dodać książkę
    print('=' * 15 + ' ADD NEW BOOK ' + '=' * 15)
    book_id = input('Book ID: ')
    name = [n for n in input("Book name: ").split()]
    author = [a for a in input("Author: ").split()]
    keywords = [keyword for keyword in input("Keywords: ").split()]
    while True:
        choice = input('Do you want to save changes? (Y/N): ')
        if choice == 'Y':
            found = search_database("books", book_id)  # sprawdzanie czy książka jest w bibliotece
            if found:
                print('Book with given ID exists in database')
                break
            with open('database/books.txt', 'a', encoding='utf-8') as file:
                file.write("id: " + str(book_id) + " name: " + "\"" + " ".join(name) + "\"" + " author: " + "\"" +
                           " ".join(author) + "\"" + " keywords: " + "\"" + " ".join(keywords) + "\"" + "\n")
                file.close()
            break
        elif choice == 'N':
            break


def delete_database_record(filename):  # funkcja usuwajaca rekord w pliku TXT o podanej nazwie
    book_id = input('Book ID: ')
    while True:
        choice = input('Do you want to save changes? (Y/N): ')
        if choice == 'Y':
            with open(f'database/{filename}.txt', encoding='utf-8') as file_read:
                lines = file_read.readlines()
                with open(f'database/{filename}.txt', 'w', encoding='utf-8') as file_write:
                    for line in lines:
                        if int(line.split()[1]) != int(book_id):
                            file_write.write(line)
            break
        elif choice == 'N':
            break


def accept_book_return_menu():  # bibliotekarz akceptuje zwrot książki
    print('=' * 15 + ' ACCEPT BOOK RETURN ' + '=' * 15)
    delete_database_record("loans")


def librarian_main_menu():  # menu obsługi biblioteki przez bibliotekarza
    menu_options = {1: 'Accept book return', 2: 'Add book', 3: 'Delete book', 4: 'Add reader',  5: 'Search book', 0: 'Exit'}
    menu_functions = {"1": accept_book_return_menu, "2": add_book_menu, "3": delete_book_menu, "4": add_reader_menu,
                      "5": search_book_menu, "0": exit}
    while True:
        print('='*15 + ' MAIN MENU ' + '='*15)
        for option, text in menu_options.items():
            print(str(option) + '. ' + text)
        choice = input("Enter your choice: ")
        try:
            menu_functions.get(choice)()
        except (KeyError, TypeError):
            print("Invalid choice. Please try again!")


def log_in_menu():  # menu logowania do systemu
    print('='*15 + ' LOG IN ' + '='*15)
    while True:
        username = input("Username: ")
        password = input("Password: ")
        user_status = log_in_validator(username, password)
        if user_status == 'librarian':
            librarian_main_menu()
            break
        elif user_status == 'reader':
            reader_main_menu(username)
            break
        else:
            print('Incorrect username, password or both. Try again!')


def log_in_validator(username, password):  # walidacja podanej nazwy użytkownika i hasła oraz określenie jego statusu
    line_counter = 0
    for line in open('database/users.txt', encoding='utf-8'):
        user_details = line.split()
        if username == user_details[1][1:-1] and password == user_details[3][1:-1]:
            if line_counter == 0:
                return 'librarian'
            else:
                return 'reader'
        line_counter += 1
    return ''


if __name__ == '__main__':
    log_in_menu()