# -*- coding: utf-8 -*-
# pylint: disable=
"""
Test BibRepo
"""
import string

import pytest  # pylint: disable=import-error
from biblishelf.core.bib_repo import BibRepo
from biblishelf.core.bib_repo import DamagedBibRepo
from biblishelf.core.bib_repo import NotCorrectBibRepo


def test_bib_init(fs):
    """
    BibRepo get a usable meta date directory
    :param fs:
    :return:
    """
    fs.CreateFile("/test")
    with pytest.raises(NotCorrectBibRepo):
        BibRepo("/")

    with pytest.raises(NotCorrectBibRepo):
        BibRepo("/test")


def test_bib_current(fs):
    """
    test
    /mnt/DATA-1/.bib/current correct or not
    /mnt/DATA-1/.bib/repo/{uuid}/meta.json  correct or not
    /mnt/DATA-1/.bib/repo/{uuid}/db.sqlite exist or not
    :param fs:
    :return:
    """
    fake_rope_id = "1234-5678-1234-5678-1234"
    fs.CreateDirectory("/mnt/DATA-1/.bib")
    bib_repo = BibRepo("/mnt/DATA-1/.bib/")

    def damage_test():
        """
        must fail
        :return:
        """
        with pytest.raises(DamagedBibRepo) as ex:
            bib_repo.get_current_repo_info()
        return ex

    damage_test()
    current = fs.CreateFile(
        file_path="/mnt/DATA-1/.bib/current",
        contents="""{"uuid """,
        encoding="utf-8"
    )
    damage_test()

    current.SetContents("""{}""")
    damage_test()

    current.SetContents(
        string.Template("""
        {
            "uuid": "${repo_id}"
        }
        """).substitute(
            repo_id=fake_rope_id
        )
    )
    assert damage_test().value.args[0] == "Meta Data Lose"
    current_meta = fs.CreateFile(
        file_path="/mnt/DATA-1/.bib/repo/{}/meta.json".format(fake_rope_id),
        contents=""""""
    )
    assert damage_test().value.args[0] == "Database Lose"

    fs.CreateFile(
        file_path="/mnt/DATA-1/.bib/repo/{}/db.sqlite".format(fake_rope_id),
        contents="""""",
    )
    assert damage_test().value.args[0] == "Meta Loader Error"

    current_meta.SetContents(
        "{}",
        encoding="utf-8"
    )

    bib_repo.get_current_repo_info()
