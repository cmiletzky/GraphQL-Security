from main import db, app
app.app_context().push()
db.create_all()
from datetime import datetime
from api.models import Author, Book, User
today = datetime.today().date()
author = a=Author(name="Ariel")
author.to_dict()
db.session.add(author)
db.session.commit()