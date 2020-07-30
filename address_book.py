"""
Program: address_book.py
Author: Kelly Klein
Last date modified: 7/29/2020
This program will use a gui to get user input and display
    a list as an address book
"""
import sqlite3
from sqlite3 import Error
import tkinter as tk
from tkinter import END

first_name_text = ''
last_name_text = ''
phone_text = ''
birthday_text = ''
address_text = ''
city_text = ''
state_text = ''
zipcode_text = ''

"""
first_name_text_edit = ''
last_name_text_edit = ''
phone_text_edit = ''
birthday_text_edit = ''
address_text_edit = ''
city_text_edit = ''
state_text_edit = ''
zipcode_text_edit = ''
"""


# connect to a database
def create_connection(db):
    """ Connect to a SQLite database
    :param db: filename of database
    :return connection if no error, otherwise None"""
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as err:
        print(err)
    return None


# create the tree
def create_table(conn, sql_create_table):
    """ Creates table with give sql statement
    :param conn: Connection object
    :param sql_create_table: a SQL CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_table)
    except Error as e:
        print(e)


def create_tables(database):
    sql_create_person_table = """ CREATE TABLE IF NOT EXISTS person (
                                        id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                                        first_name text NOT NULL,
                                        last_name text NOT NULL,
                                        phone text NOT NULL,
                                        birthday text NOT NULL
                                    ); """

    sql_create_address_table = """ CREATE TABLE IF NOT EXISTS address(
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        address text,
                                        city text,
                                        state text,
                                        zipcode text,
                                        FOREIGN KEY (id) REFERENCES person (id)
                                    ); """

    # create a database connection
    conn = create_connection(database)
    if conn is not None:
        # create person table
        create_table(conn, sql_create_person_table)
        # create address table
        create_table(conn, sql_create_address_table)
    else:
        print("Unable to connect to " + str(database))


def create_person(conn, person):
    """create person for table
    :param conn:
    :param person
    :return person id
    """

    sql = ''' INSERT INTO person(first_name, last_name, phone, birthday)
            VALUES(?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, person)
    return cur.lastrowid


def update_person(conn, person):
    """update an existing record in the table
    :param conn:
    :param person
    """
    record_id = select_box_text.get()
    sql = '''UPDATE person SET first_name = ?,
                                last_name = ?,
                                phone = ?,
                                birthday = ?
                            WHERE oid=''' + record_id

    cur = conn.cursor()
    cur.execute(sql, person)
    conn.commit()


def create_address(conn, address):
    """create address for table
    :param conn:
   :param address
    """
    sql = '''INSERT INTO address(address, city, state, zipcode)
            VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, address)
    return cur.lastrowid


def update_address(conn, address):
    """update an existing record in the table
    :param conn:
    :param address
    """
    record_id = select_box_text.get()
    sql = '''UPDATE address SET address = ?,
                                city = ?,
                                state = ?,
                                zipcode = ?
                            WHERE oid=''' + record_id

    cur = conn.cursor()
    cur.execute(sql, address)
    conn.commit()
    edit_window.destroy()


# create function to submit records
def add_record():
    add_person_label = tk.Label(window, text="Person added").grid(row=15, column=1)

    conn = sqlite3.connect('address_book.db')
    insert_person_tuple = (first_name_text.get(), last_name_text.get(), phone_text.get(), birthday_text.get())
    with conn:
        create_person(conn, insert_person_tuple)

    conn1 = sqlite3.connect('address_book.db')
    insert_address_tuple = (address_text.get(), city_text.get(), state_text.get(), zipcode_text.get())
    with conn1:
        create_address(conn1, insert_address_tuple)

    conn.commit()
    conn1.commit()
    conn.close()
    conn1.close()

    first_name.delete(0, END)
    last_name.delete(0, END)
    phone.delete(0, END)
    birthday.delete(0, END)
    address.delete(0, END)
    city.delete(0, END)
    state.delete(0, END)
    zipcode.delete(0, END)


def see_address_book():
    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()

    cur.execute("SELECT *, oid FROM person")
    people = cur.fetchall()
    print_people = ''
    for person in people:
        print_people += str(person) + "\n"

    conn1 = sqlite3.connect('address_book.db')
    cur1 = conn1.cursor()

    cur1.execute("SELECT *, oid FROM address")
    address = cur1.fetchall()
    print_address = ''
    for address in address:
        print_address += str(address) + "\n"

    show_people_label = tk.Label(window, text=print_people)
    show_people_label.grid(row=15, column=0)
    show_address_label = tk.Label(window, text=print_address)
    show_address_label.grid(row=15, column=1)

    conn.commit()
    conn1.commit()
    conn.close()
    conn.close()
    return


def edit_entry():
    global edit_window
    edit_window = tk.Tk()
    edit_window.title('Edit or update an Entry')

    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()

    entry_id = select_box_text.get()
    cur.execute("SELECT * from person WHERE oid = " + entry_id)
    people = cur.fetchall()

    conn1 = sqlite3.connect('address_book.db')
    cur1 = conn1.cursor()
    cur1.execute("SELECT * from address WHERE oid = " + entry_id)
    addresses = cur1.fetchall()

    tk.Label(edit_window, text="First Name: ").grid(row=0, column=0)
    tk.Label(edit_window, text="Last Name: ").grid(row=1, column=0)
    tk.Label(edit_window, text="Phone Number: ").grid(row=2, column=0)
    tk.Label(edit_window, text="Birthday: ").grid(row=3, column=0)
    tk.Label(edit_window, text="Address: ").grid(row=4, column=0)
    tk.Label(edit_window, text="City: ").grid(row=5, column=0)
    tk.Label(edit_window, text="State: ").grid(row=6, column=0)
    tk.Label(edit_window, text="Zipcode: ").grid(row=7, column=0)

    global first_name_text_edit
    global last_name_text_edit
    global phone_text_edit
    global birthday_text_edit
    global address_text_edit
    global city_text_edit
    global state_text_edit
    global zipcode_text_edit

    first_name_text_edit = tk.StringVar()
    first_name_edit = tk.Entry(edit_window, textvariable=first_name_text_edit)
    first_name_edit.grid(row=0, column=1)
    last_name_text_edit = tk.StringVar()
    last_name_edit = tk.Entry(edit_window, textvariable=last_name_text_edit)
    last_name_edit.grid(row=1, column=1)
    phone_text_edit = tk.StringVar()
    phone_edit = tk.Entry(edit_window, textvariable=phone_text_edit)
    phone_edit.grid(row=2, column=1)
    birthday_text_edit = tk.StringVar()
    birthday_edit = tk.Entry(edit_window, textvariable=birthday_text_edit)
    birthday_edit.grid(row=3, column=1)
    address_text_edit = tk.StringVar()
    address_edit = tk.Entry(edit_window, textvariable=address_text_edit)
    address_edit.grid(row=4, column=1)
    city_text_edit = tk.StringVar()
    city_edit = tk.Entry(edit_window, textvariable=city_text_edit)
    city_edit.grid(row=5, column=1)
    state_text_edit = tk.StringVar()
    state_edit = tk.Entry(edit_window, textvariable=state_text_edit)
    state_edit.grid(row=6, column=1)
    zipcode_text_edit = tk.StringVar()
    zipcode_edit = tk.Entry(edit_window, textvariable=zipcode_text_edit)
    zipcode_edit.grid(row=7, column=1)

    save_button = tk.Button(edit_window, text='Save Entry', command=save_entry)
    save_button.grid(row=8, column=0, columnspan=2)

    for person in people:
        first_name_edit.insert(0, person[1])
        last_name_edit.insert(0, person[2])
        phone_edit.insert(0, person[3])
        birthday_edit.insert(0, person[4])

    for address in addresses:
        address_edit.insert(0, address[1])
        city_edit.insert(0, address[2])
        state_edit.insert(0, address[3])
        zipcode_edit.insert(0, address[4])


def save_entry():
    conn = sqlite3.connect('address_book.db')

    insert_person_tuple = (first_name_text_edit.get(), last_name_text_edit.get(), phone_text_edit.get(), birthday_text_edit.get())
    with conn:
        update_person(conn, insert_person_tuple)

    conn.commit()

    conn1 = sqlite3.connect('address_book.db')

    insert_address_tuple = (address_text_edit.get(), city_text_edit.get(), state_text_edit.get(), zipcode_text_edit.get())
    with conn1:
        update_address(conn, insert_address_tuple)

    conn1.commit()


def delete_entry():
    conn = sqlite3.connect('address_book.db')
    cur = conn.cursor()
    cur.execute("DELETE from person WHERE oid =" + select_box_text.get())

    conn.commit()

    conn1 = sqlite3.connect('address_book.db')
    cur1 = conn1.cursor()
    cur1.execute("DELETE from address WHERE oid =" + select_box_text.get())

    conn1.commit()

    see_address_book()

    select_box.delete(0, END)


window = tk.Tk()
window.title("Address Book")

#  create labels
tk.Label(window, text="First Name: ").grid(row=0, column=0)
tk.Label(window, text="Last Name: ").grid(row=1, column=0)
tk.Label(window, text="Phone Number: ").grid(row=2, column=0)
tk.Label(window, text="Birthday: ").grid(row=3, column=0)
tk.Label(window, text="Address: ").grid(row=4, column=0)
tk.Label(window, text="City: ").grid(row=5, column=0)
tk.Label(window, text="State: ").grid(row=6, column=0)
tk.Label(window, text="Zipcode: ").grid(row=7, column=0)
tk.Label(window, text="Enter id to delete or edit: ").grid(row=12, column=0)


# create textboxes
first_name_text = tk.StringVar()
first_name = tk.Entry(window, textvariable=first_name_text)
first_name.grid(row=0, column=1)
last_name_text = tk.StringVar()
last_name = tk.Entry(window, textvariable=last_name_text)
last_name.grid(row=1, column=1)
phone_text = tk.StringVar()
phone = tk.Entry(window, textvariable=phone_text)
phone.grid(row=2, column=1)
birthday_text = tk.StringVar()
birthday = tk.Entry(window, textvariable=birthday_text)
birthday.grid(row=3, column=1)
address_text = tk.StringVar()
address = tk.Entry(window, textvariable=address_text)
address.grid(row=4, column=1)
city_text = tk.StringVar()
city = tk.Entry(window, textvariable=city_text)
city.grid(row=5, column=1)
state_text = tk.StringVar()
state = tk.Entry(window, textvariable=state_text)
state.grid(row=6, column=1)
zipcode_text = tk.StringVar()
zipcode = tk.Entry(window, textvariable=zipcode_text)
zipcode.grid(row=7, column=1)
select_box_text = tk.StringVar()
select_box = tk.Entry(window, textvariable=select_box_text)
select_box.grid(row=12, column=1)


# create buttons
add_entry_button = tk.Button(window, text="Add Record", command=add_record).grid(row=8, column=0, columnspan=2)
create_db_table_button = tk.Button(window, text="Create Database and Table", command=lambda: [create_connection('address_book.db'), create_tables('address_book.db')]).grid(row=9, column=0, columnspan=2)
show_entries_button = tk.Button(window, text="See address book", command=see_address_book).grid(row=10, column=0, columnspan=2)
program_exit_button = tk.Button(window, text="Exit", command=window.quit).grid(row=11, column=0, columnspan=2)
edit_button = tk.Button(window, text='Edit entry', command=edit_entry).grid(row=13, column=0, columnspan=2)
delete_button = tk.Button(window, text='Delete entry', command=delete_entry).grid(row=14, column=0, columnspan=2)

window.mainloop()

