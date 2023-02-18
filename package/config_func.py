import os as OS
import subprocess as SP
import json as JSON
import psutil as PU
import time as Time
import copy as Copy
import package.config_args as ca
import package.parse_args as pa


def __get_profile():
    return ca.gp_profile


def get_check_meta_info():
    isValid = False
    branch_name = None
    repos_names = None
    repos_paths = None

    isValid, branch_name = get_check_branch_name()
    if isValid:
        isValid, repos_names = get_check_repos_names()

    if isValid:
        isValid, repos_paths = get_check_repos_paths()

    return isValid, branch_name, repos_names, repos_paths


def get_check_branch_name():
    isValid = True

    profile = __get_profile()
    branch_name = profile["branch_name"]
    if not pa.__ch_str(branch_name):
        print("Please specify 'branch_name' in " + ca.GC_VCS_P_CFG + \
              "\nAborting command...")
        isValid = False
    return isValid, branch_name


def __build_repos_str(repos):
    repos_names = ""
    for repo in repos:
        repos_names += repo + " "
    return repos_names


def get_check_repos_paths():
    profile = __get_profile()
    cfg_repos = profile["repos"]
    repos_paths = []
    for repo_folder_name in cfg_repos:
        repo_path = OS.path.join(ca.GC_SRC_PATH, repo_folder_name)
        repos_paths.append(repo_path)

    isValid = len(repos_paths) != 0
    if not isValid:
        print("Please specify repo names in " + ca.GC_VCS_P_CFG + \
              "\n or run --init command and specify it in " + ca.GC_VCS_P_CFG + \
              "\nAborting command...")
        return False

    return isValid, repos_paths


def get_check_repos_names():
    profile = __get_profile()
    repos_names = Copy.deepcopy(profile["repos"])

    isValid = len(repos_names) != 0
    if not isValid:
        print("Please specify repo names in " + ca.GC_VCS_P_CFG + \
              "\n or run --init command and specify it in " + ca.GC_VCS_P_CFG + \
              "\nAborting command...")
        return False

    return isValid, repos_names


def __save_cfg_file():
    with open(ca.GC_VCS_P_CFG, 'w+') as f:
        JSON.dump(ca.G_CFG, f, indent=4)


def __switch_branch_cfg(branch):
    if not pa.__ch_str(branch):
        print("Bad branch name (string supposed): " + str(branch) + \
              "\n Please run --init command or specify it manually in " + ca.GC_VCS_P_CFG + \
              "\nAborting command...")
        return False

    profile = __get_profile()
    profile["branch_name"] = branch
    __save_cfg_file()
    return True


def init_repos_json():
    if not OS.path.exists(ca.GC_VCS_P_CFG):
        print("cannot find config file, please use " + pa.GC_ARG_INIT)
        return False

    global G_CFG
    if len(ca.G_CFG["repos"]) != 0:
        print("skipping auto initialization of " + ca.GC_VCS_P_CFG)
        return False

    try:
        with open(ca.GC_VCS_P_CFG, 'r') as f:
            ca.G_CFG = JSON.load(f)
    except ValueError as ve:
        print("Error during JSON parsing: " + ca.GC_VCS_P_CFG + "\
            \n Message: " + str(ve))
        return False

    if ca.G_CFG == None:
        print("Error: cannot load config " + ca.G_CFG)
        return False

    ca.gp_profile = ca.G_CFG["profiles"][ca.G_CFG["profile"]]

    print("\nactive profile: " + ca.gp_profile["branch_name"] + "\n" + str(ca.gp_profile))
    return True


def __add_profile(profile_name):
    repos = ca.G_CFG["repos"]
    profiles = ca.G_CFG["profiles"]

    profile = {}
    profile["branch_name"] = ca.GC_DEFAULT_BRANCH_NAME
    profile["repos"] = repos

    profiles[profile_name] = profile
    ca.G_CFG["profiles"] = profiles


def __commit_default_editor(commit_file_path):
    cmd = ca.GC_EDITOR_COMMIT_DEFAULT + " " + commit_file_path
    OS.system(cmd)
    return


def __commit_alternative_editor(commit_file_path):
    editor_name = G_CFG["editor_commit"]
    PU.Popen([editor_name, commit_file_path], shell=False)
    is_process_running = True
    check_p_cmd = "ps ax | grep " + commit_file_path + " | grep -v grep"
    while is_process_running:
        output = str(SP.check_output(check_p_cmd.split(), shell=True))
        is_process_running = output.find(editor_name) != -1
        Time.sleep(1)
    return