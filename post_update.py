import json,git,os,sys

from base import *

if __name__ == '__main__':
    repo_path,cfgMainBranch = load_cfg_json()
    if not os.path.exists(repo_path):
        sys.stderr.write("Repo path not found")
        exit(1)
    if cfgMainBranch == None or cfgMainBranch == "":
        sys.stderr.write("Main branch not found")
        exit(1)
    repo = git.Repo(repo_path)
    if not check_main_branch(repo,cfgMainBranch):
        exit(1)
    if checkSVNHadConflict(repo_path):
        sys.stderr.write("SVN had conflict,stop auto commit")
        exit(1)
    try:
        addAll(repo)
        commit(repo)
    except git.GitCommandError as e:
        if str(e.stdout).find("nothing to commit, working tree clean") == -1:
            sys.stderr.write(e)
            exit(1)
    exit(0)
