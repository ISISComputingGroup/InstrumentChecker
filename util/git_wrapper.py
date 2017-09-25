import git


class GitUtils(object):
    """
    Wrapper around the git library to provide a few useful high-level operations.
    """

    def __init__(self, path):
        """
        Defines where this class will look for it's git repository.
        :param path: The path of the repository
        """
        self.path = path

    def force_clean_checkout(self, branch_name):
        """
        Force cleans an existing git repo and then checks out and pulls the given branch.

        This is intended to get the latest copy of the given branch with no local changes
        (i.e. emulate a freshly cloned repository as closely as possible).

        :param branch_name: The name of the branch to check out
        :return: True if successful, False otherwise
        """
        try:
            repo = git.Repo(path=self.path)

            # Ensure the repository is in a clean state.
            repo.git.reset("HEAD", hard=True)
            repo.git.clean(f=True, d=True, x=True)

            # Fetch before checkout in case our branch is new and we don't know about it yet
            # repo.git.fetch(all=True)
            repo.git.checkout(branch_name)
            # Actually get the latest changes
            # self.repo.git.pull()
        except git.GitCommandError as e:
            print("Git command failed. Error was: {}".format(e))
            return False
        return True
