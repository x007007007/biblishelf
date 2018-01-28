# pylint: disable=import-error,missing-docstring,R0903,R1710
"""
Core Database Schema
"""
from sqlalchemy import Text
from sqlalchemy import Binary
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # pylint: disable=invalid-name


class Repo(Base):
    __tablename__ = "core_repo"
    id = Column(Integer, primary_key=True)
    uuid = Column(String(length=128), unique=True)


class Location(Base):
    __tablename__ = "core_location"
    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey("core_repo.id"), nullable=True)
    normal_file_id = Column(Integer, ForeignKey('core_normal_file.id'), nullable=True)
    normal_file = relationship("NormalFile")
    small_file_id = Column(Integer, ForeignKey('core_small_file.id'), nullable=True)
    small_file = relationship("SmallFile")
    large_file_id = Column(Integer, ForeignKey('core_large_file.id'), nullable=True)
    large_file = relationship("LargeFile")

    uri = Column(Text)

    @property
    def file(self):
        if self.normal_file:
            return self.normal_file
        if self.large_file:
            return self.large_file
        if self.small_file:
            return self.small_file


class Resource(Base):
    __tablename__ = 'core_resource'

    id = Column(Integer, primary_key=True)


class BaseFile(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    size = Column(Integer)
    md5 = Column(Binary(length=128))

    @declared_attr
    def resource(cls):  # pylint: disable=no-self-argument,R0201
        return relationship("Resource")

    @declared_attr
    def resource_id(cls):  # pylint: disable=no-self-argument,R0201
        return Column(Integer, ForeignKey('core_resource.id'))


class SmallFile(BaseFile):
    __tablename__ = 'core_small_file'


class NormalFile(BaseFile):
    __tablename__ = 'core_normal_file'
    ed2k = Column(Binary(length=128))
    sha256 = Column(Binary(length=256))


class LargeFile(BaseFile):
    __tablename__ = 'core_large_file'
    ed2k = Column(Binary(length=128))
    sha256 = Column(Binary(length=256))
    sha512 = Column(Binary(length=512))
