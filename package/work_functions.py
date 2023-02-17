import shutil as Shutil
import os as OS
import pygit2 as GIT
from pathlib import Path
import config_args as ca
import parse_args as pa
import config_func as cf
import subprocess


def work_init():
    if not OS.path.exists(ca.GC_SRC_PATH):
        OS.mkdir(ca.GC_SRC_PATH)

    cmd = "vcs import " + ca.GC_SRC_PATH + " < " + ca.GC_REPOS_NAME
    OS.system(cmd)

    repos = []
    entries = OS.scandir(ca.GC_SRC_PATH)
    for entry in entries:
        ename = entry.name
        if not ename.startswith('.') and not entry.is_file():
            repos.append(ename)
            print("adding: " + ename + " ...")

    ca.G_CFG["repos"] = repos
    cf.__add_profile(ca.GC_DEFAULT_PROFILE_NAME)
    cf.__save_cfg_file()


def work_show_repos():
    isValid, repo_paths = cf.get_check_repos_paths()
    if not isValid:
        print("Error: cannot load repos paths!" /
              "Please check profiles/<active_profile>/repos in " + str(ca.GC_VCS_P_CFG))
        return

    isValid, repo_names = cf.get_check_repos_names()
    if not isValid:
        print("Error: cannot load repos names!" /
              "Please check profiles/<active_profile>/repos in " + str(ca.GC_VCS_P_CFG))
        return

    print("repo paths:")
    for r in repo_paths:
        print(r)

    print("\nrepo names:")
    for r in repo_names:
        print(r)


def work_status():
    check_main_repo()
    isValid, repos_paths = cf.get_check_repos_paths()
    if not isValid:
        return

    repos_str = cf.__build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args status"
    OS.system(cmd)
    subprocess.call(["git", "status"])
    return


def work_add_profile(profile):
    cf.__add_profile(profile)
    print("New profile has been added: " + profile + "\
        \nCheck it in editor")
    cf.__save_cfg_file()


def work_checkoutb(branch):
    check_main_repo()
    isValid, repos_paths = cf.get_check_repos_paths()
    if not isValid:
        return

    cf.__switch_branch_cfg(branch)
    subprocess.call(["git", "checkout", "-b", branch])
    repos_str = cf.__build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args checkout -b " + branch
    OS.system(cmd)


def work_checkout(branch):
    check_main_repo()
    isValid, repos_paths = cf.get_check_repos_paths()
    if not isValid:
        return

    cf.__switch_branch_cfg(branch)
    subprocess.call(["git", "checkout", branch])
    repos_str = cf.__build_repos_str(repos_paths)

    cmd = "vcs custom --git --repos " + repos_str + " --args checkout " + branch
    OS.system(cmd)


def work_fetch():
    check_main_repo()
    isValid, repos_paths = cf.get_check_repos_paths()
    if not isValid:
        return

    repos_str = cf.__build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args fetch"
    OS.system(cmd)
    subprocess.call(["git", "fetch"])


def work_pull():
    check_main_repo()
    isValid, branch_name, _, repos_paths = cf.get_check_meta_info()
    if not isValid:
        return

    repos_str = cf.__build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args pull origin " + branch_name
    OS.system(cmd)
    subprocess.call(["git", "pull", "origin", branch_name])


def work_push():
    check_main_repo()
    isValid, branch_name, _, repos_paths = cf.get_check_meta_info()
    if not isValid:
        return

    repos_str = cf.__build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args push -u origin " + branch_name
    OS.system(cmd)
    subprocess.call(["git", "push", "-u", "origin", branch_name])


def work_clear():
    entries = OS.scandir(ca.GC_SRC_PATH)
    for entry in entries:
        ename = entry.name
        if not ename.startswith('.') and not entry.is_file():
            dir_path = OS.path.join(ca.GC_SRC_PATH, ename)
            Shutil.rmtree(dir_path)
            print("deleted: " + ename + " ...")

    vcs_cfg_path = OS.path.join(ca.GC_FOLDER_PATH, ca.GC_VCS_P_CFG)
    if not OS.path.exists(vcs_cfg_path):
        print("cannot find config: " + vcs_cfg_path)
    else:
        OS.remove(vcs_cfg_path)
        print("config is deleted: " + vcs_cfg_path)
    return


def work_sync():
    work_checkout(ca.gp_profile["branch_name"])
    return


def work_orep(repo):
    isValid, repos_names = cf.get_check_repos_names()
    if not isValid:
        return

    if repo not in repos_names:
        print("Bad repo name (string supposed): " + str(repo) + \
              "\nCheck repo name in active profile in " + ca.GC_VCS_P_CFG + \
              "\nor use " + str(pa.GC_ARG_SHOW_REPOS) + " to show" + \
              "\nActual repos: " + str(repos_names)
              )
        return

    cmd = "gnome-terminal --working-directory=$(pwd)/src/" + repo
    OS.system(cmd)
    return


def work_oallrepos():
    isValid, repos_paths = cf.get_check_repos_paths()
    if not isValid:
        return

    for repo in repos_paths:
        cmd = "gnome-terminal --working-directory=" + repo
        OS.system(cmd)

    return


def work_add():
    check_main_repo()
    isValid, repos_names = cf.get_check_repos_paths()
    if not isValid:
        return

    repos_str = cf.__build_repos_str(repos_names)
    cmd = "vcs custom --git --repos " + repos_str + " --args add ."
    OS.system(cmd)
    subprocess.call(["git", "add", "."])


def work_commit():
    check_main_repo()
    isValid, branch_name, _, repos_paths = cf.get_check_meta_info()
    if not isValid:
        return

    with open(ca.GC_COMMIT_FILE_NAME, 'w+') as f:
        f.close()

    commit_file_path = OS.path.join(ca.GC_FOLDER_PATH, ca.GC_COMMIT_FILE_NAME)
    if ca.G_CFG["editor_commit"] == ca.GC_EDITOR_COMMIT_DEFAULT:
        cf.__commit_default_editor(commit_file_path)
    else:
        cf.__commit_alternative_editor(commit_file_path)

    commit_message = ""
    with open(ca.GC_COMMIT_FILE_NAME, 'r') as f:
        commit_message = f.read()

    if not pa.__ch_str(commit_message):
        print("Please specify commit message in opened editor\n" \
              "Error: Cannot find a commit message\n" \
              "Check: \" " + ca.G_CFG["editor_commit"] + "\" field in main JSON: " + ca.GC_VCS_P_CFG
              )
        return

    commit_message += "\n On branch " + branch_name + \
                      " \n pm-Development: " + ca.G_CFG["autor"]

    repos_str = cf.__build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args commit -m \"" + commit_message + "\""
    OS.system(cmd)

    OS.remove(commit_file_path)
    subprocess.call(["git", "commit", "-m", commit_message])
    return


def work_docker_open():
    OS.system(ca.GC_DOCKER_OPEN_CMD)


def check_main_repo():
    if get_active_branch_name() != ca.gp_profile["branch_name"]:
        subprocess.call(["git", "checkout", get_active_branch_name()])


def get_active_branch_name():
    head_dir = Path("..") / ".git" / "HEAD"
    with head_dir.open("r") as f:
        content = f.read().splitlines()

    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]
