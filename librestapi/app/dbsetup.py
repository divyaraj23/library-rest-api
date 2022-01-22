import datetime

from app import db,ma
from sqlalchemy import func

negDate = datetime.date(1900, 1, 1)



class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    author_name = db.Column(db.String(30))
    isbn_num = db.Column(db.String(100))
    genre = db.Column(db.String(20))
    description = db.Column(db.String(400))

    def __init__(self, title, author_name, isbn_num, genre, description):
        self.title = title
        self.author_name = author_name
        self.isbn_num = isbn_num
        self.genre = genre
        self.description = description

class BooksSchema(ma.Schema):
    class Meta:
        fields = ('book_id','title','author_name','isbn_num','genre','description')


class Libraries(db.Model):
    __tablename__ = 'libraries'
    library_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    postal_code = db.Column(db.String(10))

    def __init__(self, name, city, state, postal_code):
        self.name = name
        self.city = city
        self.state = state
        self.postal_code = postal_code

class LibrariesSchema(ma.Schema):
    class Meta:
        fields = ('library_id','name','city','state','postal_code')

class Library_books(db.Model):
    __tablename__ = 'library_books'
    library_book_id = db.Column(db.Integer, primary_key = True)
    library_id = db.Column(db.Integer, db.ForeignKey('libraries.library_id'), nullable = False)
    book_id = db.Column(db.Integer)
    last_library_activity_id = db.Column(db.Integer,db.ForeignKey('library_activities.library_activity_id'), nullable = True)


    def __init__(self, library_id, book_id, last_library_activity_id):

        self.library_id = library_id
        self.book_id = book_id
        self.last_library_activity_id = last_library_activity_id

class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))

    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('user_id','name')   
    
class Library_Activities(db.Model):
    __tablename__ = 'library_activities'
    library_activity_id = db.Column(db.Integer, primary_key = True)
    activity_type = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)
    library_book_id = db.Column(db.Integer, db.ForeignKey('library_books.library_book_id'), nullable = False)
    checked_out_at = db.Column(db.DateTime)
    checked_in_at = db.Column(db.DateTime)

    def __init__(self, activity_type, user_id, library_book_id, checked_out_at, checked_in_at):
        #self.library_activity_id = library_activity_id
        self.activity_type = activity_type
        self.user_id = user_id
        self.library_book_id = library_book_id
        self.checked_out_at = checked_out_at
        self.checked_in_at = checked_in_at

db.create_all()

def get_book_by_name(book_name):

    fetched_books = Books.query.filter(Books.title.ilike("%"+book_name+"%")).first()
    
    
    book_schema= BooksSchema()
    book_searched = book_schema.dump(fetched_books)

    if book_searched:
        print("found!")
    else:
        print("not found")
        return "Book not found"

    return book_searched

def add_book(book):
    
    
    book_to_add = Books(book['title'], book['author_name'], book['isbn_num'], book['genre'], book['description'])
    db.session.add(book_to_add)
    db.session.commit()

    book_schema= BooksSchema()
    book_added = book_schema.dump(book_to_add)
    

    return book_added

#adds new libraries to the libraries table
def add_library(library):
        
    library_to_add = Libraries(library['name'], library['city'], library['state'], library['postal_code'])
    db.session.add(library_to_add)
    db.session.commit()

    library_schema = LibrariesSchema()
    library_added = library_schema.dump(library_to_add)

    return library_added


def add_user(user):
    
    user_to_add = Users(user['name'])
    db.session.add(user_to_add)
    db.session.commit()

    user_schema = UsersSchema()
    user_added = user_schema.dump(user_to_add)
    
    return user_added

def get_user_id(user):
    fetched_user = Users.query.filter(Users.name.ilike("%"+user+"%")).first()
       
    
    user_schema= UsersSchema()
    user_searched = user_schema.dump(fetched_user)

    if user_searched:
        print("found!")
    else:
        print("not found")
        return "User not found"

    return user_searched['user_id']


def add_book_to_library(add_book_lib):
    
    fetch_book_to_add = get_book_by_name(add_book_lib['book_name'])
    fetch_library = Libraries.query.filter(Libraries.name.ilike("%"+add_book_lib['library_name']+"%")).first()

    if fetch_book_to_add == "Book not found" or not fetch_library:
        return "Book/Library not present, Please check inventory"
    else:
        check_if_book_added = Library_books.query.filter_by(library_id = fetch_library.library_id , book_id = fetch_book_to_add['book_id']).first() 
        if check_if_book_added:
            return "Book already added to library"
        add_book_to_lib = Library_books(fetch_library.library_id,fetch_book_to_add['book_id'],0)
        
        db.session.add(add_book_to_lib)
        db.session.commit()
    
    return "Book added to Library"



#Checkout a book
def checkout_book(book_co):
    currentDateTime = datetime.datetime.now()
    user_id_co = get_user_id(book_co['checkout_user'])
    if not user_id_co:
        return "user not found"
    co_book = get_book_by_name(book_co['book_name'])
    if co_book == "Book not found":
        return "Book not found, please check inventory"
    else:
        book_id_co = co_book['book_id']
        
        lib_data = Library_books.query.filter_by(book_id = book_id_co).first()
        
        if not lib_data:
            
            return "Book not found in any library, please add from inventory"
        else:
            
            lib_data_book = lib_data.library_book_id
            max_act = db.session.query(func.max(Library_Activities.library_activity_id),Library_Activities.activity_type, Library_Activities.user_id).filter_by(library_book_id = lib_data_book).first()
            
            if max_act.activity_type == 'CHECKOUT':
                etched_user = Users.query.filter_by(user_id = max_act.user_id).first()
                usr_str = "Book checkout already by user "+str(etched_user.name)
                return usr_str
            else:
            
                l_A = Library_Activities('CHECKOUT', user_id_co , lib_data_book, currentDateTime, negDate)
                db.session.add(l_A)
                db.session.commit()
                lib_bo = Library_books.query.filter_by(library_book_id = lib_data_book).first()
                lib_bo.last_library_activity_id = l_A.library_activity_id
                db.session.commit()
                etched_user = Users.query.filter_by(user_id = user_id_co).first()
                usr_str = "Book checked out by user "+str(etched_user.name)+" successfully!"
                return usr_str

#Checkout a book
def checkin_book(book_co):
    currentDateTime = datetime.datetime.now()
    user_id_co = get_user_id(book_co['checkin_user'])
    if not user_id_co:
        return "user not found"
    co_book = get_book_by_name(book_co['book_name'])
    if co_book == "Book not found":
        return "Book not found, please check inventory"
    else:
        book_id_co = co_book['book_id']
        
        lib_data = Library_books.query.filter_by(book_id = book_id_co).first()
        
        if not lib_data:
            
            return "Book not found in any library, please add from inventory"
        else:
            
            lib_data_book = lib_data.library_book_id
            max_act = db.session.query(func.max(Library_Activities.library_activity_id),Library_Activities.library_activity_id,Library_Activities.activity_type, Library_Activities.user_id).filter_by(library_book_id = lib_data_book).first()
            
            if max_act.activity_type == 'CHECKIN':
                usr_str = "Book already checkedin"
                return usr_str
            else:
                lib_act = Library_Activities.query.filter_by(library_activity_id = max_act.library_activity_id).first()
                etched_user = Users.query.filter_by(user_id = max_act.user_id).first()
                if max_act.user_id != user_id_co:
                    u_str = "Different user checkin the book in. Was checked out by "+str(etched_user.name)
                    return  u_str
                lib_act.activity_type = 'CHECKIN'
                lib_act.checked_in_at = currentDateTime
                db.session.commit()
                etched_user = Users.query.filter_by(user_id = user_id_co).first()
                usr_str = "Book checked in by user "+str(etched_user.name)+" successfully!"
                return usr_str


        



