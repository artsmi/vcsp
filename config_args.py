import pathlib as Pathlib
import os as OS

GC_VCS_P_CFG = "vcs_p.json"
GC_SRC_NAME = "src"
GC_REPOS_NAME = ".repos"
GC_DEFAULT_BRANCH_NAME = "master"
GC_DEFAULT_PROFILE_NAME = "default"
GC_COMMIT_FILE_NAME = "_commit.vcs_p"
GC_EDITOR_COMMIT_DEFAULT = "nano"
GC_DOCKER_OPEN_CMD = "docker run --rm -it -v $(pwd):/ws -w /ws 192.168.89.202:5000/promobot/pm_meta:latest"

G_CFG = {"repos": [], "profile": "default", "profiles": {}}

gp_profile = None

GC_FOLDER_PATH = Pathlib.Path(__file__).parent.resolve()
GC_REPOS_PATH = OS.path.join(GC_FOLDER_PATH, GC_REPOS_NAME)
GC_SRC_PATH = OS.path.join(GC_FOLDER_PATH, GC_SRC_NAME)