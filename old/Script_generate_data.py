from main import db, app
from datetime import datetime
from api.models import Book, Author, User
from faker import Faker
app.app_context().push()
fake = Faker()
# Create 100 User records
for i in range(100):
    user = User(
        name=fake.name(),
        email=fake.email(),
        phone=fake.phone_number(),
        address=fake.address()
    )
    db.session.add(user)

# Create 100 Book records
for i in range(100):
    book = Book(
        name=fake.catch_phrase(),
        due_date=fake.future_date(end_date='+30d'),
        author=fake.random_int(min=1, max=100),
        borrow_by=fake.random_int(min=1, max=100),
    )
    db.session.add(book)

# Create 100 Author records
for i in range(100):
    author = Author(
        name=fake.name(),
        #books=[Book(name="aaa")]
    )
    db.session.add(author)

# Commit the changes to the database
db.session.commit()



