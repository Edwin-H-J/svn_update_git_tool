import git,json,sys,os,subprocess
import xml.etree.ElementTree as ET
os.environ['PYTHONIOENCODING'] = 'utf-8'
def load_cfg_json():
    os.getcwd()
    jsonPath = os.path.join(os.getcwd(),'config.json')
    if not os.path.exists(jsonPath):
        jsonPath = os.path.join(os.path.dirname(sys.argv[0]),'config.json')
    if not os.path.exists(jsonPath):
        print("Config file not found")
        return None,None
    cfg = json.load(open(jsonPath))
    return cfg['repo_path'],cfg['main_branch']
def load_cfg_args():
    return os.getcwd(),sys.argv[1]

def check_main_branch(repo,main_branch):
    return repo.active_branch.name == main_branch

def get_now_branch(repo):
    return repo.active_branch.name

def stash(repo):
    repo.git.stash('push')
def checkout(repo,branch):
    repo.git.checkout(branch)

def stashAndCheckout(repo,branch):
    stash(repo)
    checkout(repo,branch)

def addAll(repo):
    repo.git.add('--all')

def commit(repo):
    repo.git.commit('-a','-m','auto commit')

def commitAndCheckout(repo,branch):
    addAll(repo)
    checkout(repo,branch)

def getPostUpdateInfo():
    return {
        "path":sys.argv[1],
        "depth":sys.argv[2],
        "revision":sys.argv[3],
        "error":sys.argv[4],
        "cwd":sys.argv[5],
        "resultpath":sys.argv[6]
    }

def getSVNStatusXML(path):
    process = subprocess.Popen(['svn', 'status', '-q','--xml',path], stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error != None:
        print(error)
        return None
    return ET.XML(output.decode('utf-8'))

def recursiveHandleXML(node,func):
    func(node)
    for child in node:
        recursiveHandleXML(child,func)
def checkIsConflict(node):
    if node.tag == 'entry':
        status = node.find('wc-status')
        if status != None:
            return status.attrib['item'] == 'conflicted'
    return False

def checkHaveConflictRecursive(node):
    if checkIsConflict(node):
        return True
    for child in node:
        if checkHaveConflictRecursive(child):
            return True
    return False

def checkSVNHadConflict(path):
    xml = getSVNStatusXML(path)
    if xml == None:
        return True
    return checkHaveConflictRecursive(xml)