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
        Force cleans an existing git repo and then checks out the given branch.

        This is intended to get a copy of the given branch with no local changes.

        :param branch_name: The name of the branch to check out
        :return: True if successful, False otherwise
        """
        try:
            repo = git.Repo(path=self.path)

            # Ensure the repository is in a clean state.
            repo.git.reset("HEAD", hard=True)
            repo.git.clean(f=True, d=True, x=True)
            repo.git.checkout(branch_name)
        except git.GitCommandError as e:
            print("Git command failed. Error was: {}".format(e))
            return False
        return True
