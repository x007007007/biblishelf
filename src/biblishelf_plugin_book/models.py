from biblishelf_core.models import Base
from biblishelf_core.models import Resource
from sqlalchemy import Table
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, UnicodeText
from sqlalchemy.orm import relationship, backref


class BookAuthor(Base):
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
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    resource_id = Column("resource_id", Integer, ForeignKey("resource.id"))
    page = Column(Integer, nullable=True)
    isbn = Column(String(32), nullable=True)
    cover_img_path = Column(UnicodeText, nullable=True)
    resource = relationship("Resource", backref="plugin_book")
    authors = relationship('BookAuthor', secondary='book_with_author', back_populates='books')

    @property
    def cover_img(self):
        from biblishelf_core.conf.repo import current_repo, RepoConfig
        if isinstance(current_repo, RepoConfig):
            return current_repo.path.joinpath(self.cover_img_path).open()


class PdfBookProducer(Base):
    __tablename__ = "book_pdf_producer"
    id = Column(Integer, primary_key=True)
    name = Column(String(254))

class PdfBookCreator(Base):
    __tablename__ = "book_pdf_creator"
    id = Column(Integer, primary_key=True)
    name = Column(String(254))


class PdfBook(Book):
    __tablename__ = "book_pdf"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    book = relationship("Book")
    pdf_book_creator_id = Column(Integer, ForeignKey("book_pdf_creator.id"))
    pdf_book_producer_id = Column(Integer, ForeignKey("book_pdf_producer.id"))
    pdf_book_creator = relationship(PdfBookCreator)
    pdf_book_producer = relationship(PdfBookProducer)
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)


class CatalogItem(Base):
    __tablename__ = "book_catalog_item"
    id =Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id"))
    parent_id = Column(Integer, ForeignKey("book_catalog_item.id"), nullable=True)
    children = relationship("CatalogItem")
    parent = relationship("CatalogItem", remote_side=[id])
    book = relationship("Book")