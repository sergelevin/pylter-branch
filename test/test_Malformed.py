# -*- coding: utf-8 -*-


import test.util
import unittest
from pylter_branch import RepositoryProcessor


class MalformedTest(test.util.RepoTestBase):
    repo_name = 'malformed'

    def test_filter(self):
        processor = RepositoryProcessor(self.repo)
        processor.process()
        self.assertEqual('b3b40b57cca2c3a8f1b48cc2f3afc41f04bbaa16', self.repo.references['refs/heads/master'].get_object().hex)

    def test_double_pass(self):
        processor = RepositoryProcessor(self.repo)
        processor.process()
        processor.process()
        self.assertEqual('b3b40b57cca2c3a8f1b48cc2f3afc41f04bbaa16', self.repo.references['refs/heads/master'].get_object().hex)

    def test_cache(self):
        replaced_commits = {}
        processor = RepositoryProcessor(self.repo, replaced_commits = replaced_commits)
        processor.process()
        processor = RepositoryProcessor(self.repo, replaced_commits = replaced_commits)
        processor.process()
        self.assertEqual('b3b40b57cca2c3a8f1b48cc2f3afc41f04bbaa16', self.repo.references['refs/heads/master'].get_object().hex)


if __name__ == '__main__':
    unittest.main()
