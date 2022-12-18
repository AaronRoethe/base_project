import os
import json
import subprocess
import base64
import logging
from datetime import datetime

def rootDirectory():
    project_root = os.path.dirname(os.path.dirname(__file__))
    return project_root

def log(args):
    handlers = [ logging.StreamHandler() ]
    fileName = f'logs/{datetime.now():%Y%m%d_%H%M%S}-{args.file[:-5]}.log'

    if not args.dryrun: 
        handlers += [ logging.FileHandler(fileName) ]

    logging.basicConfig(
        level=logging.ERROR,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
    logger=logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    return logger

def is_installed(name):
    """Checks if a program is installed on the machine executing this script"""
    if os.name == 'nt':
        process = subprocess.Popen(['where', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(['/usr/bin/which', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process.communicate()
    return process.returncode == 0

def checkInstalledPackages():
    """Confirms required packages are installed."""
    installList = read_json('configs/install.json')
    packages_missing = [msg for package, msg in installList.items() if not is_installed(package)]

    if packages_missing:
        msg = f"""
        Required Packages:

            {f'{os.linesep}'.join(packages_missing)}
        """
        print(msg)
        raise SystemExit

def removeEmptyLines(file):
    output=""
    with open(file) as f:
        output = ''.join(line for line in f if not line.isspace())
                
    with open(file,"w") as f:
        f.write(output)

def write_file(file, text):
    with open(file, "w") as f:
        f.write(text)

def read_raw(file):
    with open(file, 'r') as data:
        return data.read()

def read_json(relativePath):
    with open(relativePath, 'r') as f:
        return json.load(f)

def convertB64(stringVar):
    return base64.b64encode(stringVar.encode('utf-8'))
