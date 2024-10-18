from __future__ import print_function

from builtins import object

import git


class GitUtils(object):
    """
    Wrapper around the git library to provide a few useful high-level operations.
    """

    def __init__(self, path: str) -> None:
        """
        Defines where this class will look for its git repository.
        :param path: The path of the repository
        """
        self.path = path

    def force_clean_checkout(self, name: str, is_tag: bool) -> bool:
        """
        Force cleans an existing git repo and then checks out the given branch.

        This is intended to get a copy of the given branch with no local changes.

        :param name: The name of the branch/tag to check out
        :param is_tag: if we are checking out to a tag or a branch
        :return: True if successful, False otherwise
        """
        try:
            repo = git.Repo(path=self.path)

            # Ensure the repository is in a clean state.
            repo.git.reset("HEAD", hard=True)
            repo.git.clean(f=True, d=True, x=True)
            if is_tag:
                repo.git.checkout("tags/{}".format(name), force=True)
            else:
                repo.git.checkout("origin/{}".format(name), force=True)
        except (git.GitCommandError, git.InvalidGitRepositoryError) as e:
            print("Git command failed. Error was: {}".format(e))
            return False
        return True

    def update_branch(self, branch: str, is_tag: bool = False) -> bool:
        try:
            repo = git.Repo(path=self.path)
            repo.git.fetch(all=True)
            if not self.force_clean_checkout(branch, is_tag):
                return False
        except (git.GitCommandError, git.InvalidGitRepositoryError) as e:
            print("Git command failed. Error was: {}".format(e))
            return False
        return True

    def fetch_all(self) -> None:
        repo = git.Repo(path=self.path)
        repo.git.fetch(all=True)
