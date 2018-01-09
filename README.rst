######################################################################
pylter-branch - pygit2-based git filter-branch mechanism
######################################################################

Pylter-branch is a pygit2-based small library to create git filter-branch like
utilities with Python. It respects git replaces and git grafts when processing
commits. Pylter-branch is tested to work with Python 3.6

Different filtering aspects are implemented as overridable methods of main
class - `RepositoryProcessor`.
