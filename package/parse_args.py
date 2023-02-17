import argparse as ARGP
import config_args as ca


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
                     \nAdditional information is in CONFIG FILE: " + ca.GC_VCS_P_CFG + "\
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
