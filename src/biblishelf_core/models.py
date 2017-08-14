import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship


class Resource(Base):
    __tablename__ = 'resource'

    id = Column(Integer, primary_key=True )
    uuid = Column(String(64))
    name = Column(String(128))
    create_time = Column(DateTime(), nullable=True)
    modify_time = Column(DateTime(), nullable=True)
    files = relationship("File", back_populates="resource")


class Repo(Base):
    __tablename__ = "repo"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(64))
    is_local = Column(Boolean)
    is_archive = Column(Boolean)
    paths = relationship("Path", back_populates="repo")


class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True)
    size = Column(Integer)
    ed2k = Column(String(32))
    md5 = Column(String(32))
    sha1 = Column(String(150))
    mime_type_id = Column("mime_type_id", Integer, ForeignKey("mime_type.id"))
    resource_id = Column("resource_id", Integer, ForeignKey("resource.id"))

    resource = relationship("Resource", back_populates="files")
    mime_type = relationship("MimeType", back_populates="files")
    paths = relationship("Path", back_populates="file")



class MimeType(Base):
    __tablename__ = "mime_type"

    id = Column(Integer, primary_key=True)
    mime = Column(String(32))
    full_mime = Column(String(512))
    files = relationship("File", back_populates="mime_type")


class Path(Base):
    __tablename__ = "path"

    id = Column(Integer, primary_key=True)
    path = Column(Text)
    modify_time = Column(DateTime, nullable=True)
    create_time = Column(DateTime, nullable=True)
    access_time = Column(DateTime, nullable=True)
    file_id = Column("file_id", Integer, ForeignKey("file.id"))
    repo_id = Column("repo_id", Integer, ForeignKey("repo.id"))
    repo = relationship("Repo", back_populates="paths")
    file = relationship("File", back_populates="paths")