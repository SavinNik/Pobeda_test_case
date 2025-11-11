from ..database.setup import db


class User(db.Model):
    """Модель пользователя для хранения в базе данных"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.name}>"