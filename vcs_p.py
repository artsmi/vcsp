#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

#  Artem Smirnov by Promobot
#  TODO: to add auto complete function 
# see https://kislyuk.github.io/argcomplete

import os as OS
import subprocess as SP
import json as JSON
import argparse as ARGP
import pathlib as Pathlib
import shutil as Shutil
import psutil as PU
import time as Time
import copy as Copy


GC_VCS_P_CFG = "vcs_p.json"
GC_SRC_NAME = "src"
GC_REPOS_NAME = ".repos"
GC_DEFAULT_BRANCH_NAME = "master"
GC_DEFAULT_PROFILE_NAME = "default"
GC_COMMIT_FILE_NAME = "_commit.vcs_p"
GC_EDITOR_COMMIT_DEFAULT = "nano"
GC_DOCKER_OPEN_CMD = "docker run --rm -it -v $(pwd):/ws -w /ws 192.168.89.202:5000/promobot/pm_meta:latest"

G_CFG = {}
G_CFG["repos"] = []
G_CFG["profile"] = "default"
G_CFG["profiles"] = {}

gp_profile = None

GC_FOLDER_PATH = Pathlib.Path(__file__).parent.resolve()
GC_REPOS_PATH = OS.path.join(GC_FOLDER_PATH, GC_REPOS_NAME)
GC_SRC_PATH = OS.path.join(GC_FOLDER_PATH, GC_SRC_NAME)


def __ch_str(s):
    return s is not None and len(s) != 0


GC_ARG_INIT = "--init"
GC_ARG_CHECKOUT_B = "--checkoutb"
GC_ARG_CHECKOUT = "--checkout"
GC_ARG_CFG_BRANCH = "--cfgb"
GC_ARG_FETCH = "--fetch"
GC_ARG_PULL = "--pull"
GC_ARG_PUSH = "--push"
GC_ARG_STATUS = "--status"
GC_ARG_SHOW_REPOS = "--show_repos"
GC_ARG_CLEAR = "--clear"
GC_ARG_EDIT = "--edit"
GC_ARG_SYNC = "--sync"
GC_ARG_PROFILE = "--profile"
GC_ARG_ADD = "--add"
GC_ARG_OREP = "--orep"
GC_ARG_OALL = "--oallrepos"
GC_ARG_COMMIT = "--commit"
GC_ARG_DOCKER = "--docker"


def parse_args():
    C_DESCRIPTION = "\nThe Tool to work with multi-repositories project. Based on VCS\
                     \nAdditional information is in CONFIG FILE: " + GC_VCS_P_CFG + "\
                     \n\n!!! Please use only config file to work with branches !!!\
                     \n!!! All commands are applying only to active profile !!!"
    
    C_DESC_INIT = "primary initialization of repository"
    C_DESC_CHECKOUT_B = "<branch_name> - create new branch for all repos"
    C_DESC_CHECKOUT = "<branch_name> - checkout branch for all repos"
    C_DESC_CFG_BRANCH = "<branch_name> - save branch to the config"
    C_DESC_FETCH = "fetch all branches for all repos"
    C_DESC_PULL = "pull all repos"
    C_DESC_PUSH = "push all repos"
    C_DESC_STATUS = "print status for all repos"
    C_DESC_SHOW_REPOS = "show all actual repos"
    C_DESC_CLEAR = "clear all meta data and repos"
    C_DESC_EDIT = "edit config files and profiles"
    C_DESC_SYNC = "sync profile - checkout all repos to the its branch"
    C_DESC_PROFILE = "<branch_name> - create profile with name"
    C_DESC_ADD = "use git add . command to all repos"
    C_DESC_OREP = "<repo_name> - open repo in new terminal for manual fixes"
    C_DESC_OALL = "open all repos in new terminal for manual fixes"
    C_DESC_COMMIT = "open editor for commit message, then add git commit -m in all repos (tested editors: atom, nano)"
    C_DESC_DOCKER = "open docker environment according to readme.md (press 'exit' to exit in docker).\
                    Please use the link to set docker without root \
                    https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user"
    
    parser = ARGP.ArgumentParser(C_DESCRIPTION)
    parser.add_argument(GC_ARG_INIT, action="store_true", help=C_DESC_INIT)
    parser.add_argument(GC_ARG_CHECKOUT_B, action="store", type=str, default=None, help=C_DESC_CHECKOUT_B)
    parser.add_argument(GC_ARG_CHECKOUT, action="store", type=str, default=None, help=C_DESC_CHECKOUT)
    parser.add_argument(GC_ARG_CFG_BRANCH, action="store", type=str, default=None, help=C_DESC_CFG_BRANCH)
    parser.add_argument(GC_ARG_FETCH, action="store_true", help=C_DESC_FETCH)
    parser.add_argument(GC_ARG_PULL, action="store_true", help=C_DESC_PULL)
    parser.add_argument(GC_ARG_PUSH, action="store_true", help=C_DESC_PUSH)
    parser.add_argument(GC_ARG_STATUS, action="store_true", help=C_DESC_STATUS)
    parser.add_argument(GC_ARG_SHOW_REPOS, action="store_true", help=C_DESC_SHOW_REPOS)
    parser.add_argument(GC_ARG_CLEAR, action="store_true", help=C_DESC_CLEAR)
    parser.add_argument(GC_ARG_EDIT, action="store_true", help=C_DESC_EDIT)
    parser.add_argument(GC_ARG_SYNC, action="store_true", help=C_DESC_SYNC)
    parser.add_argument(GC_ARG_PROFILE, action="store", type=str, default=None, help=C_DESC_PROFILE)
    parser.add_argument(GC_ARG_ADD, action="store_true", help=C_DESC_ADD)
    parser.add_argument(GC_ARG_OREP, action="store", type=str, default=None, help=C_DESC_OREP)
    parser.add_argument(GC_ARG_OALL, action="store_true", help=C_DESC_OALL)
    parser.add_argument(GC_ARG_COMMIT, action="store_true", help=C_DESC_COMMIT)
    parser.add_argument(GC_ARG_DOCKER, action="store_true", help=C_DESC_DOCKER)
    
    args = parser.parse_args()
    return args


def __get_profile():
    return gp_profile


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
    if not __ch_str(branch_name):
        print("Please specify 'branch_name' in " + GC_VCS_P_CFG + \
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
        repo_path = OS.path.join(GC_SRC_PATH, repo_folder_name)
        repos_paths.append(repo_path)
    
    isValid = len(repos_paths) != 0
    if not isValid:
        print("Please specify repo names in " + GC_VCS_P_CFG + \
                "\n or run --init command and specify it in " + GC_VCS_P_CFG + \
                "\nAborting command...")
        return False

    return isValid, repos_paths


def get_check_repos_names():
    profile = __get_profile()
    repos_names = Copy.deepcopy(profile["repos"])
        
    isValid = len(repos_names) != 0
    if not isValid:
        print("Please specify repo names in " + GC_VCS_P_CFG + \
                "\n or run --init command and specify it in " + GC_VCS_P_CFG + \
                "\nAborting command...")
        return False

    return isValid, repos_names


def __save_cfg_file():
    with open(GC_VCS_P_CFG, 'w+') as f:
        JSON.dump(G_CFG, f, indent=4)


def __switch_branch_cfg(branch):
    if not __ch_str(branch):
        print("Bad branch name (string supposed): " + str(branch) + \
                "\n Please run --init command or specify it manually in " + GC_VCS_P_CFG + \
                "\nAborting command...")
        return False
    
    profile = __get_profile()
    profile["branch_name"] = branch    
    __save_cfg_file()    
    return True


def init_repos_json():
    if not OS.path.exists(GC_VCS_P_CFG):
        print("cannot find config file, please use " + GC_ARG_INIT)
        return False

    global G_CFG
    if len(G_CFG["repos"]) != 0:
        print("skipping auto initialization of " + GC_VCS_P_CFG)
        return False

    try: 
        with open(GC_VCS_P_CFG, 'r') as f:
            G_CFG = JSON.load(f)
    except ValueError as ve:
        print("Error during JSON parsing: " + GC_VCS_P_CFG + "\
            \n Message: " + str(ve))
        return False

    if G_CFG == None:
        print("Error: cannot load config " + G_CFG)
        return False

    global gp_profile
    gp_profile = G_CFG["profiles"][G_CFG["profile"]]

    print("\nactive profile: " + gp_profile["branch_name"] + "\n" + str(gp_profile))
    return True


def __add_profile(profile_name):
    repos = G_CFG["repos"]
    profiles = G_CFG["profiles"]

    profile = {}
    profile["branch_name"] = GC_DEFAULT_BRANCH_NAME
    profile["repos"] = repos

    profiles[profile_name] = profile
    G_CFG["profiles"] = profiles


def work_init():
    if not OS.path.exists(GC_SRC_PATH) :
        OS.mkdir(GC_SRC_PATH)
    
    cmd = "vcs import " + GC_SRC_PATH + " < " + GC_REPOS_NAME
    OS.system(cmd)

    repos = []
    entries = OS.scandir(GC_SRC_PATH)
    for entry in entries:
        ename = entry.name      
        if not ename.startswith('.') and not entry.is_file():            
            repos.append(ename)
            print ("adding: " + ename + " ...")
    
    G_CFG["repos"] = repos
    __add_profile(GC_DEFAULT_PROFILE_NAME)
    __save_cfg_file()


def work_show_repos():
    isValid, repo_paths = get_check_repos_paths()
    if not isValid:
        print("Error: cannot load repos paths!" /
            "Please check profiles/<active_profile>/repos in " + str(GC_VCS_P_CFG))
        return
    
    isValid, repo_names = get_check_repos_names()
    if not isValid:
        print("Error: cannot load repos names!" /
            "Please check profiles/<active_profile>/repos in " + str(GC_VCS_P_CFG))
        return

    print("repo paths:")
    for r in repo_paths:
        print(r)

    print("\nrepo names:")
    for r in repo_names:
        print(r)



def work_status():
    isValid, repos_paths = get_check_repos_paths()
    if not isValid:
        return

    repos_str = __build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args status"
    OS.system(cmd)
    return


def work_add_profile(profile):
    __add_profile(profile)
    print("New profile has been added: " + profile +"\
        \nCheck it in editor")
    __save_cfg_file()


def work_checkoutb(branch):
    isValid, repos_paths = get_check_repos_paths()
    if not isValid:
        return

    __switch_branch_cfg(branch)
    repos_str = __build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args checkout -b " + branch
    OS.system(cmd)


def work_checkout(branch):
    isValid, repos_paths = get_check_repos_paths()
    if not isValid:
        return

    __switch_branch_cfg(branch)
    repos_str = __build_repos_str(repos_paths)

    cmd = "vcs custom --git --repos " + repos_str + " --args checkout " + branch
    OS.system(cmd)


def work_fetch():
    isValid, repos_paths = get_check_repos_paths()
    if not isValid:
        return

    repos_str = __build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args fetch"
    OS.system(cmd)


def work_pull():
    isValid, branch_name, _ , repos_paths = get_check_meta_info()
    if not isValid:
        return


    repos_str = __build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args pull origin " + branch_name
    OS.system(cmd)


def work_push():
    isValid, branch_name, _ , repos_paths = get_check_meta_info()
    if not isValid:
        return

    repos_str = __build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args push -u origin " + branch_name
    OS.system(cmd)


def work_clear():
    entries = OS.scandir(GC_SRC_PATH)
    for entry in entries:
        ename = entry.name
        if not ename.startswith('.') and not entry.is_file():
            dir_path = OS.path.join(GC_SRC_PATH, ename)
            Shutil.rmtree(dir_path)
            print ("deleted: " + ename + " ...")
    
    vcs_cfg_path = OS.path.join(GC_FOLDER_PATH, GC_VCS_P_CFG)
    if not OS.path.exists(vcs_cfg_path):
        print ("cannot find config: " + vcs_cfg_path)
    else:
        OS.remove(vcs_cfg_path)
        print ("config is deleted: " + vcs_cfg_path)
    return


def work_sync():
    work_checkout(gp_profile["branch_name"])
    return


def work_orep(repo):
    isValid, repos_names = get_check_repos_names()
    if not isValid:
        return

    if repo not in repos_names:
        print("Bad repo name (string supposed): " + str(repo) + \
                "\nCheck repo name in active profile in " + GC_VCS_P_CFG + \
                "\nor use " + str(GC_ARG_SHOW_REPOS) + " to show" + \
                "\nActual repos: " + str(repos_names)
                )
        return

    cmd = "gnome-terminal --working-directory=$(pwd)/src/" + repo
    OS.system(cmd)
    return


def work_oallrepos():
    isValid, repos_paths = get_check_repos_paths()
    if not isValid:
        return

    for repo in repos_paths:
        cmd = "gnome-terminal --working-directory=" + repo
        OS.system(cmd)        
    
    return


def work_add():
    isValid, repos_names = get_check_repos_paths()
    if not isValid:
        return

    repos_str = __build_repos_str(repos_names)
    cmd = "vcs custom --git --repos " + repos_str + " --args add ."
    OS.system(cmd)


def __commit_default_editor(commit_file_path):
    cmd = GC_EDITOR_COMMIT_DEFAULT + " " + commit_file_path
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


def work_commit():
    isValid, branch_name, _, repos_paths = get_check_meta_info()
    if not isValid:
        return

    with open(GC_COMMIT_FILE_NAME, 'w+') as f:
        f.close()
    
    commit_file_path = OS.path.join(GC_FOLDER_PATH, GC_COMMIT_FILE_NAME)
    if G_CFG["editor_commit"] == GC_EDITOR_COMMIT_DEFAULT:
        __commit_default_editor(commit_file_path)
    else:
        __commit_alternative_editor(commit_file_path)
    
    commit_message = ""
    with open(GC_COMMIT_FILE_NAME, 'r') as f:
        commit_message = f.read()

    if not __ch_str(commit_message):
        print("Please specify commit message in opened editor\n"\
                "Error: Cannot find a commit message\n"\
                "Check: \" " + G_CFG["editor_commit"] + "\" field in main JSON: " + GC_VCS_P_CFG
                )
        return

    commit_message += "\n On branch " + branch_name + \
                        " \n pm-Development: " + G_CFG["autor"]
    
    repos_str = __build_repos_str(repos_paths)
    cmd = "vcs custom --git --repos " + repos_str + " --args commit -m \"" + commit_message + "\""
    OS.system(cmd)

    OS.remove(commit_file_path)
    return


def work_docker_open():     
    OS.system(GC_DOCKER_OPEN_CMD)
    

def parse_work():
    args = parse_args()

    if args.clear:
        work_clear()
        
    if args.init:
        work_init()        

    if not init_repos_json():
        return

    print("\nSync started... \n\n")
    work_sync()
    print("\nSync completed! Working on direct command... \n\n")

    if __ch_str(args.orep):
        work_orep(args.orep)

    if args.oallrepos:
        work_oallrepos()

    if __ch_str(args.profile):
        work_add_profile(args.profile)

    if __ch_str(args.checkoutb):
        work_checkoutb(args.checkoutb)      

    if __ch_str(args.checkout):
        work_checkout(args.checkout)

    if __ch_str(args.cfgb):
        __switch_branch_cfg(args.cfgb)

    if args.show_repos:
        work_show_repos()

    if args.fetch:
        work_fetch()

    if args.status:
        work_status()

    if args.pull:
        work_pull()

    if args.push:
        work_push()

    if args.sync:
        work_sync()

    if args.add:
        work_add()

    if args.commit:
        work_commit()


parse_work()
exit(0)