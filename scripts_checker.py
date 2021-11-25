import win32wnet
import os
import sys
import git
import concurrent.futures
# noinspection PyUnresolvedReferences
# Workaround for AttributeError when concurrent.futures.thread._threads_queues.clear()
from concurrent.futures import thread
# noinspection PyUnresolvedReferences
from win32wnet import error as PywintypesError
from util.channel_access import ChannelAccessUtils

REMOTE_URL = 'https://github.com/ISISNeutronMuon/InstrumentScripts'


class MissingEnvironmentVariable(KeyError):
    """
    Raised when accessed an environment variable that does not exist.
    """
    def __init__(self, err_msg):
        super().__init__(err_msg)


def _get_env_var(var_name):
    """
    Return the value of environment variable with given name, or raise an exception if it doesn't exist.
    """
    var = os.environ.get(var_name)
    if var is None:
        raise MissingEnvironmentVariable(f'Tried accessing environment variable "{var_name}" that does not exist')
    return var


def ls_remote(url):
    """
    List references in the remote repository.
    """
    remote_refs = {}
    g = git.cmd.Git()
    for ref in g.ls_remote(url).split('\n'):
        hash_ref_list = ref.split('\t')
        remote_refs[hash_ref_list[1]] = hash_ref_list[0]
    return remote_refs


remote_head = ls_remote(REMOTE_URL)['HEAD']  # Get the remote master HEAD commit ID
# inst_hostnames = [inst['hostName'] for inst in ChannelAccessUtils().get_inst_list()]
inst_hostnames = ["NDXMAPS"]
different_head, multiple_repos, cannot_connect = [], [], []


def check_inst_scripts(hostname):
    scripts_path = f'\\\\{hostname}\\InstScripts$'

    # Connect to the instrument shared network resource
    username = f'{hostname}\\{_get_env_var("USER")}'
    password = _get_env_var("PASS")

    try:
        # dwType, lpLocalName, lpRemoteName[, lpProviderName, Username, Password, flags]
        # noinspection PyArgumentList
        win32wnet.WNetAddConnection2(0, None, scripts_path, None, username, password)
    except PywintypesError as e:
        sys.stderr.write(f'Error {e.winerror} connecting to {hostname}: {e.strerror}\n')
        cannot_connect.append(hostname)
        return

    repo = git.Repo(path=scripts_path)

    if len(repo.remotes) > 1:
        print(f'WARNING: {hostname} has multiple remote repositories: \n{repo.git.remote("-v")}\n')
        multiple_repos.append(hostname)

    current_head = repo.head.commit
    if current_head != remote_head:
        print(f'WARNING: {hostname} HEAD with commit ID "{current_head}" '
              f'is different from remote master HEAD with commit ID "{remote_head}".')
        different_head.append(hostname)

        return hostname


def check_all_scripts(hostnames):
    print('Starting instrument script checker')
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        futures = [executor.submit(check_inst_scripts, hostname) for hostname in hostnames]
        try:
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        except KeyboardInterrupt:
            # noinspection PyProtectedMember
            executor._threads.clear()
            # noinspection PyProtectedMember, PyUnresolvedReferences
            concurrent.futures.thread._threads_queues.clear()
            raise

    inst_whose_head_not_master = [x for x in results if x is not None]
    return inst_whose_head_not_master


# Manual running (for the time being)
print(check_all_scripts(inst_hostnames))

connected = set(inst_hostnames) ^ set(cannot_connect)
print(f'Checked {len(connected)} instruments out of {len(inst_hostnames)}.')
print(f'Not on master HEAD: {different_head}')
print(f'Multiple repositories: {multiple_repos}')
print(f'Could not connect to: {cannot_connect}')
