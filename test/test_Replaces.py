# -*- coding: utf-8 -*-


import test.util
import unittest
from pygit2 import Oid
from pylter_branch import RepositoryProcessor, GitReplaces


class ReplacesTest(test.util.RepoTestBase):
    repo_name = 'secret_repo_replace'

    def test_replaces(self):
        replaces = GitReplaces.GitReplaces(self.repo)

        # non-replaced commit
        self.assertEqual(Oid(hex='640e5fddd05c5a6a113663ffa1555e9ef4176f77'), replaces[Oid(hex='640e5fddd05c5a6a113663ffa1555e9ef4176f77')])
        self.assertEqual(Oid(hex='640e5fddd05c5a6a113663ffa1555e9ef4176f77'), replaces['640e5fddd05c5a6a113663ffa1555e9ef4176f77'])

        # replaced commit
        self.assertEqual('640e5fddd05c5a6a113663ffa1555e9ef4176f77', replaces['5bcfecc3c7b13f6121cc97aed31bf226777b1b93'].hex)

        self.assertEqual(1, len(replaces))
        self.assertEqual(['5bcfecc3c7b13f6121cc97aed31bf226777b1b93'], [i.hex for i in replaces])

    def test_filter(self):
        processor = RepositoryProcessor(self.repo)
        processor.process()

        self.assertEqual('4db499c392e12fda7122491c9ba3f51ff92e5d49', self.repo.references['refs/heads/master'].get_object().hex)


if __name__ == '__main__':
    unittest.main()
