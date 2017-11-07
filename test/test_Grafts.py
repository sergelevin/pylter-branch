# -*- coding: utf-8 -*-


import test.util
import unittest
from pygit2 import Oid
from pylter_branch import RepositoryProcessor
from pylter_branch.GitGrafts import GitGrafts


class GraftsTest(test.util.RepoTestBase):
    repo_name = 'secret_repo_grafts'

    def test_grafts(self):
        grafts = GitGrafts(self.repo)

        # non-grafted commit
        self.assertEqual((Oid(hex='5bcaacc7f74359ac1c8c4886dacb43c8840dd8a4'), ), grafts[Oid(hex='640e5fddd05c5a6a113663ffa1555e9ef4176f77')])
        self.assertEqual((Oid(hex='5bcaacc7f74359ac1c8c4886dacb43c8840dd8a4'), ), grafts['640e5fddd05c5a6a113663ffa1555e9ef4176f77'])

        # grafted commit
        self.assertEqual((Oid(hex='640e5fddd05c5a6a113663ffa1555e9ef4176f77'), ), grafts['f21d222ddda26d99379257010bdc24536087e7cc'])

        self.assertEqual(1, len(grafts))
        self.assertEqual(['f21d222ddda26d99379257010bdc24536087e7cc'], [i.hex for i in grafts])

    def test_filter(self):
        processor = RepositoryProcessor(self.repo)
        processor.process()

        self.assertEqual('4db499c392e12fda7122491c9ba3f51ff92e5d49', self.repo.references['refs/heads/master'].get_object().hex)


if __name__ == '__main__':
    unittest.main()
