from biblishelf_core.models import Base
from biblishelf_core.models import Resource
from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, UnicodeText
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
    page = Column(Integer, nullable=True)
    isbn = Column(String(32), nullable=True)
    cover_img_path = Column(UnicodeText, nullable=True)
    resource_id = Column('resource_id', ForeignKey("resource.id"), primary_key=True)
    resource = relationship("Resource")

    authors = relationship('Author', secondary='book_with_author', back_populates='books')

    @property
    def cover_img(self):
        from biblishelf_core.conf.repo import current_repo, RepoConfig
        if isinstance(current_repo, RepoConfig):
            return current_repo.path.joinpath(self.cover_img_path).open()