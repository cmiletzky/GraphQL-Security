from .models import Author, Book, User
from ariadne import convert_kwargs_to_snake_case
from datetime import datetime


@convert_kwargs_to_snake_case
def resolve_get_book_by_name(obj, info, book_name):
    books = []
    for book in Book.query.all():
        if book.to_dict()["name"] == book_name:
            books.append(book.to_dict())
    payload = books

    return payload
    

@convert_kwargs_to_snake_case
def resolve_available(obj, info, book_id):
    book = Book.query.get(book_id)
    if datetime.today().date().strftime('%d-%m-%Y') <= book.to_dict()["due_date"]:
        return False
    return True
    
    
@convert_kwargs_to_snake_case
def resolve_get_books_by_author(obj, info, author_id):
    author = Author.query.get(author_id)
    books = []
    for book in Book.query.all():
        if str(book.to_dict()["author"]) == str(author_id):
            books.append(book.to_dict())
    payload = books

    return payload


def resolve_get_all_authors(obj, info):
    authors = [author.to_dict() for author in Author.query.all()]
    payload = authors
    return payload
    
def resolve_get_all_books(obj, info):
    books = [book.to_dict() for book in Book.query.all()]
    payload = books
    return payload
    
@convert_kwargs_to_snake_case
def resolve_get_user_details(obj, info, user_id):
    user = User.query.get(user_id)
    payload = user.to_dict()

    return payload


@convert_kwargs_to_snake_case
def resolve_get_books_hold_by_user_id(obj, info, user_id):
    books=[]
    for book in Book.query.all():
        if str(book.to_dict()["borrow_by"]) == str(user_id):
            books.append(book.to_dict())
    payload = books

    return payload

@convert_kwargs_to_snake_case
def resolve_get_books_hold_by_user_name(obj, info, user_name):
    books=[]
    for user in User.query.all():
        if user.to_dict()["name"] == user_name:
            for book in Book.query.all():
                if str(book.to_dict()["borrow_by"]) == str(user.to_dict()["id"]):
                    books.append(book.to_dict())
    payload = books

    return payload