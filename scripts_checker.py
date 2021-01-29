import win32wnet
import os
import sys
import git
import concurrent.futures
# noinspection PyUnresolvedReferences
from win32wnet import error as PywintypesError
from util.channel_access import ChannelAccessUtils


inst_hostnames = [inst['hostName'] for inst in ChannelAccessUtils().get_inst_list()]
different_head, multiple_repos, cannot_connect = [], [], []


def check_inst_scripts(hostname):
    scripts_path = f'\\\\{hostname}\\c$\\Instrument\\scripts'

    # Connect to the instrument shared network resource
    username = f'{hostname}\\{os.environ.get("USER")}'
    password = os.environ.get("PASS")
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
    master_head = repo.heads.master.commit
    if current_head != master_head:
        print(f'WARNING: {hostname} HEAD with commit ID "{current_head}" '
              f'is different than master HEAD with commit ID "{master_head}".')
        different_head.append(hostname)

        return hostname


def check_all_scripts(hostnames):
    print('Starting instrument script checker')
    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
        results = executor.map(check_inst_scripts, hostnames)
    inst_whose_head_not_master = [x for x in results if x is not None]
    return inst_whose_head_not_master


# Manual running (for the time being)
print(check_all_scripts(inst_hostnames))

connected = set(inst_hostnames) ^ set(cannot_connect)
print(f'Checked {len(connected)} instruments out of {len(inst_hostnames)}.')
print(f'Not on master HEAD: {different_head}')
print(f'Multiple repositories: {multiple_repos}')
print(f'Could not connect to: {cannot_connect}')
