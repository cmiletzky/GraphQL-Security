from main import db


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
        
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    author = db.Column(db.Integer)
    borrow_by = db.Column(db.Integer)
    due_date = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "author": self.author,
            "borrow_by": self.borrow_by,
            "due_date": str(self.due_date.strftime('%d-%m-%Y'))
        }
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    address = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address
        }