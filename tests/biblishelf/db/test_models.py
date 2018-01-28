# pylint: disable=import-error,missing-docstring,R0903,R1710,ungrouped-imports
"""
Test biblishelf.db.models
Try to establish and handle database in memory
"""
import hashlib

from sqlalchemy import create_engine
from biblishelf.db import models
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)  # pylint: disable=invalid-name
Session = sessionmaker()  # pylint: disable=invalid-name
Session.configure(bind=engine)


def setup_module(module):  # pylint: disable=unused-argument
    """ setup any state specific to the execution of the given module."""
    models.Base.metadata.create_all(engine)


def teardown_module(module):  # pylint: disable=unused-argument
    """ teardown any state that was previously setup with a setup_module
    method.
    """
    print("Good Bye")


def generate_files(res):
    sf1 = models.SmallFile(
        resource=res,
        size=102
    )
    nf1 = models.NormalFile(
        resource=res,
        size=1029,
        md5=hashlib.new('md5', b'hello').digest(),
        ed2k=hashlib.new('md5', b'hello').digest(),
        sha256=hashlib.new('sha256', b'hello').digest(),
    )
    bf1 = models.LargeFile(
        resource=res,
        size=10290,
        md5=hashlib.new('md5', b'hello world').digest(),
        ed2k=hashlib.new('md5', b'hello world').digest(),
        sha256=hashlib.new('sha256', b'hello world').digest(),
        sha512=hashlib.new('sha512', b'hello world').digest(),
    )

    return sf1, nf1, bf1


def test_file_with_resource():
    session = Session()

    res = models.Resource()
    session.add(res)

    sf1, nf1, bf1 = generate_files(res)
    session.add(sf1)
    session.add(nf1)
    session.add(bf1)

    session.commit()

    query = session.query(models.LargeFile).filter_by(md5=hashlib.new('md5', b'hello world').digest())
    assert query.count() == 1
    assert query[0].size == 10290
    assert isinstance(query[0].resource, models.Resource)


def test_location_with_file():
    session = Session()
    res = models.Resource()
    session.add(res)
    sf1, nf1, bf1 = generate_files(res)
    session.add(sf1)
    session.add(nf1)
    session.add(bf1)
    session.commit()

    loc1 = models.Location(small_file=sf1, uri="/small/file")
    loc2 = models.Location(large_file=bf1, uri="/large/file")
    loc3 = models.Location(normal_file=nf1, uri="/normal/file")
    session.add(loc1)
    session.add(loc2)
    session.add(loc3)
    session.commit()

    assert session.query(models.Location).filter_by(uri="/small/file").first().file.size == 102
    assert session.query(models.Location).filter_by(uri="/large/file").first().file.size == 10290
    assert session.query(models.Location).filter_by(uri="/normal/file").first().file.size == 1029
