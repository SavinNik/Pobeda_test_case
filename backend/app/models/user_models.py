from backend.app.database.setup import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }

    def __repr__(self):
        return f"<User {self.name}>"