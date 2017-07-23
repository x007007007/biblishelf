from biblishelf_core.models import Base
from biblishelf_core.models import Resource
from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "book_author"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    books = relationship('Book', secondary='book_with_author', back_populates='authors')

book_with_author = Table('book_with_author', Base.metadata,
    Column('author_id', ForeignKey('book_author.id'), primary_key=True),
    Column('book_id', ForeignKey('book.id'), primary_key=True)
)

class Book(Resource):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    resource_id = Column(ForeignKey("resource.id"), primary_key=True)
    resource = relationship("Resource")

    authors = relationship('Author', secondary='book_with_author', back_populates='books')