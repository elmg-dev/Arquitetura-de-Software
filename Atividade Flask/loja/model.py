from loja.ext.database import db, SerializerMixin, mapped_column, Mapped
from flask_login import UserMixin

class Product(db.Model, SerializerMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(unique=True)
    price: Mapped[float]

class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

def populate_db():
    products = [
        Product(id=1, description="Resistor 470 ohms", price=0.05),
        Product(id=2, description="Arduino Nano R3", price=50.00),
        Product(id=3, description="Raspberry PI 3", price=200.00),
    ]

    db.session.add_all(products)
    db.session.commit()
