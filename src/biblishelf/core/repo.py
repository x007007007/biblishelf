# -*- coding: utf-8; mode: python; python-indent: 4; tab-width: 4; indent-tabs-mode: t; -*-
# vim: set fenc=utf-8 nocompatible expandtab number showmatch cursorline ts=4 sw=4 ss=4:syntax on
# pylint: disable=too-few-public-methods
# yapf: disable
# yapf: enable
# # noqa:
"""
Bridge of filesystem ORM and SqlAlchemy engine and session
"""
from sqlalchemy import create_engine  # pylint: disable=import-error
from sqlalchemy.orm import sessionmaker  # pylint: disable=import-error


class RepoIndex(object):  # pylint: disable=too-many-instance-attributes
    """
    repository index
    """
    uuid = None
    readonly = False
    engine = None
    Session = None  # pyline: disable=invalid-name
    _database_uri = None

    def __init__(self, repo_uuid, meta, repo=None, remote=None):
        """

        :param repo_uuid:
        :param meta:
        :param repo:
        :param remote:
        """
        self._repo = repo
        self._remote = remote
        self.meta = meta
        self.uuid = repo_uuid
        self.readonly = meta.get("readonly", False)

    def connect_db(self, default="sqlite://db.sqlite", **kwargs):
        """
        called by loader or generate
        :param default:
        :param kwargs:
        :return:
        """
        self._database_uri = self.meta.get("db", default)
        self.engine = create_engine(self._database_uri, **kwargs)
        self.Session = sessionmaker()  # pylint: disable=invalid-name
        self.Session.configure(bind=self.engine)


class RemoteRepoIndex(object):
    """
    remote info of a repository index
    """
    repo_index = None

    def __init__(self, repo_index, sync_time):
        """

        :param repo_index:
        :param sync_time:
        """
        assert isinstance(repo_index, RepoIndex)
        self.repo_index = repo_index
        self.sync_time = sync_time


class Repo(object):
    """
    Repo
    """

    def __init__(self, index, remote_indexes):
        """

        :param index:
        :param remote_indexes:
        """
        assert isinstance(index, RepoIndex)
        assert isinstance(remote_indexes, list)
        self.index = index
        self.remote_indexes = remote_indexes

    def iter_index(self):
        """

        :return:
        """
        yield self.index
        for remote_index in self.remote_indexes:
            assert isinstance(remote_index, RemoteRepoIndex)
            yield remote_index.repo_index
