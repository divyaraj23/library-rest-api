import sqlite3
from sqlite3.dbapi2 import Cursor, connect
import datetime

#Helpful in updating the latest activity
currentDateTime = datetime.datetime.now()

#Database connection subroutine
def db_connect():
    connection = sqlite3.connect('library.db',detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
    return connection

#Tables with the proper Entity relationship created here
def initialize_db_tables():
    try:
        conn = db_connect()
        conn.execute('''
        CREATE TABLE if not exists books (book_id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(100), author_name VARCHAR(30), isbn_num varchar(20),genre VARCHAR(20), description varchar(400)); 
        ''')
        conn.execute('''
        CREATE TABLE if not exists library_books (library_book_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, library_id INTEGER, book_id INTEGER, last_library_activity_id INTEGER NULL, FOREIGN KEY (library_id) REFERENCES books(library_id), FOREIGN KEY (last_library_activity_id) REFERENCES library_activities(library_activity_id));
        ''')
        conn.execute('''
        CREATE TABLE if not exists users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100));
        ''')
        conn.execute('''
        CREATE TABLE if not exists library_activities (library_activity_id INTEGER PRIMARY KEY AUTOINCREMENT, activity_type TEXT CHECK(activity_type IN ('CHECKIN','CHECKOUT')) NOT NULL, user_id INTEGER, library_book_id INTEGER, checked_out_at DATETIME, checked_in_at DATETIME, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (library_book_id) REFERENCES library_books(library_book_id));
        ''')
        conn.execute('''
        CREATE TABLE if not exists libraries (library_id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50), city VARCHAR(20), state VARCHAR(20), postal_code VARCHAR(10));
        ''')
        conn.commit()
        print("Tables created successfully!")
    except Exception as e:
        print("Failure in table creation "+str(e))
    finally:
        conn.close()

# Basic function to search a book by its name
def get_book_by_name(book_name):
    book = {}
    try:
        conn = db_connect()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM books WHERE title = ?", (book_name,))
        row = curs.fetchone()

        book["book_id"] = row["book_id"]
        book["title"] = row["title"]
        book["author_name"] = row["author_name"]
        book["isbn_num"] = row["isbn_num"]
        book["genre"] = row["genre"]
        book["description"] = row["description"]
    except:
        book = {}

    return book


def get_book_by_id(book_id):
    book = {}
    try:
        conn = db_connect()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
        row = curs.fetchone()

        book["book_id"] = row["book_id"]
        book["title"] = row["title"]
        book["author_name"] = row["author_name"]
        book["isbn_num"] = row["isbn_num"]
        book["genre"] = row["genre"]
        book["description"] = row["description"]
    except:
        book = {}

    return book

def get_library_by_id(library_id):
    library = {}
    try:
        conn = db_connect()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM libraries WHERE library_id = ?", (library_id,))
        row = curs.fetchone()

        library["name"] = row["name"]
        library["city"] = row["city"]
        library["state"] = row["state"]
        library["postal_code"] = row["postal_code"]
    except:
        library = {}

    return library


def get_user_by_id(user_id):
    user = {}
    try:
        conn = db_connect()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = curs.fetchone()

        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
    except:
        user = {}

    return user

def get_library_book_id(library_book):
    book = {}
    try:
        conn = db_connect()
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        curs.execute("SELECT * FROM library_books WHERE library_book_id = ?", (library_book,))
        row = curs.fetchone()

        book["library_book_id"] = row["library_book_id"]
        book["library_id"] = row["library_id"]
        book["book_id"] = row["book_id"]
        book["last_library_activity_id"] = row["last_library_activity_id"]
    except:
        book = {}

    return book


#Adds books to the books table
def add_book(book):
    created_book = {}
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO books (title, author_name, isbn_num, genre, description) VALUES (?, ?, ?, ?, ?)", (   
                    book['title'], book['author_name'], book['isbn_num'],   
                    book['genre'], book['description']))
        conn.commit()
        created_book = get_book_by_id(cur.lastrowid)
    except:
        conn.rollback()

    finally:
        conn.close()

    return created_book

#adds new libraries to the libraries table
def add_library(library):
    created_library = {}
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO libraries (name, city, state, postal_code) VALUES (?, ?, ?, ?)", (   
                    library['name'], library['city'], library['state'],   
                    library['postal_code']
        ))
        conn.commit()
        created_library = get_library_by_id(cur.lastrowid)
    except:
        conn.rollback()

    finally:
        conn.close()
        
    return created_library

#adds new users
def add_user(user):
    user_created = {}
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name) VALUES (?)", (
            (user['name'],)
        ))
        conn.commit()
        user_created = get_user_by_id(cur.lastrowid)
    except Exception as e:
        print(str(e))
        conn.rollback()

    finally:
        conn.close()
    
    return user_created

#adds books from the books tables to the library to be ready for borrowing
def add_book_to_library(add_book_lib):
    book_added = {}
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT * from library_books where book_id = ? and library_id = ?",(
            add_book_lib['book_id'], add_book_lib['library_id']
        ))

        if cur.fetchone():
            return "Book id exists"
        else:
            cur1 = conn.cursor()
            cur1.execute("INSERT INTO library_books (library_id, book_id, last_library_activity_id) VALUES (?, ?, ?)", (   
                    add_book_lib['library_id'], add_book_lib['book_id'], 0))
            conn.commit()
            book_added = get_library_book_id(cur1.lastrowid)
    
    except:
        conn.rollback()
    
    finally:
        conn.close()
    
    return book_added

#Checkout a book
def checkout_book(checkout):
    checked_book = {}
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT * from library_books where book_id = ? and library_id = ?",(
            checkout['book_id'], checkout['library_id']
        ))
        row = cur.fetchone()
        if row:
            checked_book['library_book_id'] = row[0]
        else:
            return "book or library not present/library doesn't have the book"

        lib_cursor = conn.cursor()
        lib_cursor.execute("SELECT MAX(library_activity_id) as latest_activity,activity_type, user_id, checked_in_at, checked_out_at from library_activities where library_book_id = ?", (
            checked_book['library_book_id'],
        ))
        row1 = lib_cursor.fetchone()
        if row1:
            if row1[1] == 'CHECKOUT':
                return "book already checked out by user "+str(get_user_by_id(row1[2])['name'])
            else:
                co_cursor = conn.cursor()
                co_cursor.execute("INSERT INTO library_activities (activity_type, user_id, library_book_id, checked_out_at, checked_in_at) VALUES (?, ?, ?, ?, ?)", (   
                    "CHECKOUT", checkout['user_id'], checked_book['library_book_id']
                    , currentDateTime, "1/1/1900"
                    ))
                l = co_cursor.lastrowid
                l_cur = conn.cursor()
                l_cur.execute("UPDATE library_books SET last_library_activity_id = ? where library_book_id = ?",(
                    l, checked_book['library_book_id'],
                ))

                conn.commit()
    except Exception as e:
        print (str(e))
        conn.rollback()
        
    finally:
        conn.close()

#Check in a checkedout book
def checkin_book(checkin):
    checked_book = {}
    try:
        conn = db_connect()
        cur = conn.cursor()
        cur.execute("SELECT * from library_books where book_id = ? and library_id = ?",(
            checkin['book_id'], checkin['library_id']
        ))
        row = cur.fetchone()
        if row:
            print (row)
            checked_book['library_book_id'] = row[0]
        else:
            return "book or library not present/library doesn't have the book"

        lib_cursor = conn.cursor()
        lib_cursor.execute("SELECT MAX(library_activity_id) as latest_activity,activity_type, user_id, checked_in_at, checked_out_at from library_activities where library_book_id = ?", (
            checked_book['library_book_id'],
        ))
        row1 = lib_cursor.fetchone()
        if row1:
            if (str(row1[1]) == 'CHECKOUT') and (str(row1[2]) == str(checkin['user_id'])):
                l1_cur = conn.cursor()
                l1_cur.execute("UPDATE library_activities SET activity_type = ? , checked_in_at = ? where library_activity_id = ?",(
                    "CHECKIN", currentDateTime, row1[0]
                ))
                
                conn.commit()   
            else:
               return "Check if the correct user is returning the book"

            
    except Exception as e:
        print (str(e))
        conn.rollback()
        
    finally:
        conn.close()
        


            






        



