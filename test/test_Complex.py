# -*- coding: utf-8 -*-


import test.util
import unittest

import pygit2
from pylter_branch import RepositoryProcessor, TreeProcessor


class ComplexTest(test.util.RepoTestBase):
    repo_name = 'complex'

    def test_run_complex(self):
        class ComplexProcessor(RepositoryProcessor):
            def __init__(self, *args, **kwargs):
                super(ComplexProcessor, self).__init__(*args, **kwargs)

            def filter_tree(self, tree: TreeProcessor.TreeWrapper):
                tree.rm('secrets/big_secret')
                tree.mv('Src', 'src')
                return tree

            def _replace_message_commit(self, sha):
                object_candidate = self._repository.git_object_lookup_prefix(sha)
                if isinstance(object_candidate, pygit2.Commit):
                    original = object_candidate.oid
                    try:
                        return self.replaced_commits[original].hex[0:len(sha)]
                    except KeyError:
                        pass
                return sha

            def filter_message(self, message):
                match = self.sha1regex.search(message)
                last_end = 0
                result = ''
                while match:
                    result += message[last_end:match.start()]
                    result += self._replace_message_commit(match.group().lower())
                    last_end = match.end()
                    match = self.sha1regex.search(message, last_end)

                result += message[last_end:]
                return result

        processor = ComplexProcessor(self.repo)
        processor.process()
        self.assertEqual('cc23f54deeb91158604ca24889d9d912a9fb6de6', self.repo.references['refs/heads/master'].get_object().hex)
        self.assertEqual('f0ed117cb6aba1ebd7e43bff14c1de8d848c9a40', self.repo.references['refs/heads/feature'].get_object().hex)

if __name__ == '__main__':
    unittest.main()
