import sqlite3
import datetime
import os
import time


def clear_screen(code:int = 0):
    if code != 1:
        input("\n\n  Press enter key to continue ..........")

    time.sleep(.5)
    os.system('cls')

def print_table(data: list, no_of_column: int):
    max_len = int(65/no_of_column)

    for i in data:
        for j in i:
            if (len(j) > max_len):
                max_len = len(j)

    print("+" + "-"*(max_len*no_of_column + no_of_column*2 - 1) + "+")

    head = len("-"*(max_len*no_of_column + no_of_column*2 - 1)) - 25

    print(
        "|" + " "*int(head/2) + "LIBRARY MANAGEMENT SYSTEM" +
        " "*(head - int(head/2)) + "|"
    )

    print("+" + "-"*(max_len*no_of_column + no_of_column*2 - 1) + "+")

    for index, row in enumerate(data):
        for _ in row:
            print("|" + " "*(max_len - len(_)) + _, end=" ")
        print("|")

        if index == 0:
            print("+" + "-"*(max_len*no_of_column + no_of_column*2 - 1) + "+")

    print("+" + "-"*(max_len*no_of_column + no_of_column*2 - 1) + "+")


def add_book_details(
    book_name: str, book_code: str, total_no_of_books: str, book_subject: str
):
    sql = (
        "insert into books_details "
        f"values('{book_name}', '{book_code}','{book_subject}',"
        f" '{total_no_of_books}', '{total_no_of_books}' );"
    )

    connection_obj.execute(sql)

    connection_obj.commit()


def issue_book(
    student_name: str, reg_no: str, book_code: str
):
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sql = (
        "insert into issue_and_submit_book_data "
        f"values('{student_name}', '{reg_no}', '{book_code}', '{date}', "
        "'Not Submitted', 'Not Submitted');"
    )

    connection_obj.execute(sql)

    sql = f"""
        Update books_details 
        Set available_no_of_books = available_no_of_books - 1
        Where book_code = "{book_code}";
    """

    connection_obj.execute(sql)

    connection_obj.commit()


def submit_book(
    reg_no: str, book_code: str
):
    date = date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = (
        "Update issue_and_submit_book_data "
        "Set book_status = 'Submitted', submission_date_time "
        f"= '{date}'"
        f"Where book_code = '{book_code}' And reg_no = '{reg_no}';"
    )

    connection_obj.execute(sql)

    sql = f"""
        Update books_details 
        Set available_no_of_books = available_no_of_books + 1
        Where book_code = '{book_code}';
    """

    connection_obj.execute(sql)

    connection_obj.commit()


def delete_book(
    book_code: str
):
    sql = f"""
        Delete from issue_and_submit_book_data
        Where book_code = '{book_code}';
    """

    connection_obj.execute(sql)

    sql = f"""
        Delete from books_details 
        Where book_code = '{book_code}';
    """

    connection_obj.execute(sql)

    connection_obj.commit()


def display_student_details():
    sql = f"""
        Select * from issue_and_submit_book_data 
        Order by book_status, issuing_date_time;
    """

    data = list(connection_obj.execute(sql))

    data.insert(0, [
        "Name", "Reg. No.", "Book Code", "Issued Date",
        "Book Status", "Submission Date"
    ])

    print_table(data, 6)


def display_book_details():
    sql = f"""
        Select * from books_details
        Order by book_name;
    """

    data = list(connection_obj.execute(sql))

    data.insert(0, [
        "Book Name", "Book Code", "Subject",
        "Available Books", "Total Books"
    ])

    print_table(data, 5)


def main():
    clear_screen(1)

    data = [
        " "*20 + "LIBRARY MANAGEMENT SYSTEM", "1. Add Book Details",
        "2. Issue Book", "3. Submit Book", "4. Delete Book Details",
        "5. Display Student Details", "6. Display Books Details", "7. Exit"
    ]

    for index, pop in enumerate(data):

        if index == 0:
            print("+" + "-"*65 + "+")
            print("|" + pop + " "*(65 - len(pop)) + "|")
            print("+" + "-"*65 + "+")
        else:
            pop = "  " + pop
            print("|" + pop + " "*(65 - len(pop)) + "|")

    print("+" + "-"*65 + "+")

    data = input("  Enter you choice :").strip()

    if data == "1":
        clear_screen()

        book_name = input("  Enter book name :")
        book_code = input("  Enter book code :")
        total_no_of_books = input("  Enter total number of book :")
        book_subject = input("  Enter book subject :")

        add_book_details(
            book_name, book_code, total_no_of_books, book_subject
        )

        print("  Book details added successfully")
        clear_screen()

    elif data == "2":
        clear_screen()

        student_name = input("  Enter student name :")
        reg_no = input("  Enter student registration number :")
        book_code = input("  Enter book code :")

        issue_book(student_name, reg_no, book_code)

        print("  Book issued successfully")
        clear_screen()

    elif data == "3":
        clear_screen()

        reg_no = input("  Enter student registration number :")
        book_code = input("  Enter book code :")

        submit_book(reg_no, book_code)

        print("  Book submitted successfully")
        clear_screen()

    elif data == "4":
        clear_screen()

        book_code = input("  Enter book code :")

        delete_book(book_code)

        print("  Book deleted successfully")
        clear_screen()

    elif data == "5":
        clear_screen()
        display_student_details()
        clear_screen()

    elif data == "6":
        clear_screen()
        display_book_details()
        clear_screen()

    elif data == "7":
        clear_screen()
        exit()

    else:
        print(f"\n  Invalid input {data}")
        clear_screen()

    main()


if __name__ == "__main__":
    connection_obj = sqlite3.Connection("library.db")

    sql = """
        Create table books_details(
            book_name varchar(100),
            book_code varchar(100),
            book_subject varchar(100),
            available_no_of_books varchar(100),
            total_no_of_books varchar(100)
        );
    """

    try:
        connection_obj.execute(sql)
    except sqlite3.OperationalError:
        pass

    sql = """
        Create table issue_and_submit_book_data(
            student_name varchar(100),
            reg_no varchar(100),
            book_code varchar(100),
            issuing_date_time varchar(100),
            book_status varchar(100),
            submission_date_time varchar(100)
        );
    """

    try:
        connection_obj.execute(sql)
    except sqlite3.OperationalError:
        pass

    main()
