# -*- coding: utf -*-
# pylint: disable=no-member,invalid-name,missing-docstring
"""
handle .bib index repository
.bib is a directory
"""
import json
import pathlib


class NotCorrectBibRepo(Exception):
    pass


class DamagedBibRepo(Exception):
    pass


class BibRepo(object):
    def __init__(self, bib_abs_path):
        """

        :param abspath: where is bib repository directory
        """
        self._update_bib_repo(bib_abs_path)

    def _update_bib_repo(self, bib_abs_path):
        self.bib_abs_path = pathlib.Path(bib_abs_path)
        if not self.bib_abs_path.is_dir():
            raise NotCorrectBibRepo("bib repo meta directory should is directory")
        self.abs_path = self.bib_abs_path.parent
        if not self.abs_path != self.bib_abs_path:
            raise NotCorrectBibRepo("bib repo path should't is root")

    def get_current_repo_info(self):
        """

        :return: Dict[]
        """
        path = self.bib_abs_path.joinpath('current')
        if not (path.exists() and path.is_file()):
            raise DamagedBibRepo()
        with path.open(encoding="utf-8") as fp:
            try:
                info = json.load(fp)
                return self.get_repo_meta(info['uuid'])
            except json.JSONDecodeError:
                raise DamagedBibRepo("json decode error")
        raise DamagedBibRepo("current no date")

    def get_remote_repo_info(self):
        """

        :return: List[Dict[]]
        """
        path = self.bib_abs_path.joinpath('remote-asset')
        if not (path.exists() and path.is_file()):
            raise DamagedBibRepo()
        with path.open(encoding="utf-8") as fp:
            try:
                res = []
                for info in json.load(fp):
                    info['meta'] = (self.get_repo_meta(info["uuid"]))
                    res.append(info)
                return res
            except json.JSONDecodeError:
                raise DamagedBibRepo("json decode error")

    def get_repo_meta(self, repo_uuid):
        """

        :param repo_uuid:
        :return:
        """
        meta_path = self.bib_abs_path.joinpath("repo/{repo_uuid}/meta.json".format(repo_uuid=repo_uuid))
        db_path = self.bib_abs_path.joinpath("repo/{repo_uuid}/db.sqlite".format(repo_uuid=repo_uuid))
        if not (meta_path.exists() and meta_path.is_file()):
            raise DamagedBibRepo("meta.data.lose", repo_uuid)
        if not (db_path.exists() and db_path.is_file()):
            raise DamagedBibRepo("Database lose", repo_uuid)

        with meta_path.open(encoding="utf-8") as fp:
            try:
                return json.load(fp)
            except json.JSONDecodeError:
                raise DamagedBibRepo("json decode error, {}".format(meta_path))
