from datetime import datetime, timedelta

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Author, Book, User

@convert_kwargs_to_snake_case
def resolve_add_user(obj, info, name, email, phone, address):
        
    user=User(name=name, email=email, phone=phone, address=address)
        
    db.session.add(user)
    db.session.commit()
        
    return user.to_dict()

@convert_kwargs_to_snake_case
def resolve_update_user(obj, info, user_id, name, email, phone, address):
    user = User.query.get(user_id)
    if user:
        if name:
            user.name= name
        if email:
            user.email= email
        if phone:
            user.phone= phone
        if address:
            user.address= address
    db.session.add(user)
    db.session.commit()
    return user.to_dict()

    
    
    
    
@convert_kwargs_to_snake_case
def resolve_add_author(obj, info, name):
    author=Author(name=name)
        
    db.session.add(author)
    db.session.commit()
    return author.to_dict()
    
    
    
@convert_kwargs_to_snake_case
def resolve_add_book(obj, info, name, author):
    book=Book(name=name, author=author)
    book.borrow_by=0
    book.due_date=datetime(1,1,1).date()
    db.session.add(book)
    db.session.commit()
    return book.to_dict()
    
    

@convert_kwargs_to_snake_case
def resolve_borrow_book(obj, info, book_id, user_id):
    book = Book.query.get(book_id)
    book.borrow_by=user_id
    # get the current date
    current_date = datetime.today().date()

    # add two weeks to the current date
    two_weeks = timedelta(days=14)
    future_date = current_date + two_weeks
    book.due_date = future_date
    db.session.add(book)
    db.session.commit()
    return True
    
    
@convert_kwargs_to_snake_case
def resolve_return_book(obj, info, book_id):
    book = Book.query.get(book_id)
    book.borrow_by=0
    book.due_date=datetime(1,1,1).date()
    db.session.add(book)
    db.session.commit()
    return True
