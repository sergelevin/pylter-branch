# -*- coding: utf-8 -*-


import unittest
import os
import tempfile
import tarfile
import pygit2
import gc
import shutil
import stat


class TempRepoHolder:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.temp_dir = tempfile.mkdtemp()
        data_name = os.path.join(os.path.dirname(__file__), 'data', self.name + '.tar')
        with tarfile.open(name=data_name, mode='r') as archive:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(archive, self.temp_dir)
        return self.temp_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        def del_rw(action, name, exc):
            os.chmod(name, stat.S_IWRITE)
            os.remove(name)

        gc.collect()
        shutil.rmtree(self.temp_dir, onerror=del_rw)



class RepoTestBase(unittest.TestCase):
    repo_name = None

    def setUp(self):
        self.repo_holder = TempRepoHolder(self.repo_name)
        repo_path = self.repo_holder.__enter__()
        self.repo = pygit2.Repository(repo_path)
        super(RepoTestBase, self).setUp()

    def tearDown(self):
        super(RepoTestBase, self).tearDown()
        self.repo = None
        self.repo_holder.__exit__(None, None, None)
