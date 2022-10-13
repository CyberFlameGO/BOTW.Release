import requests
from requests.structures import CaseInsensitiveDict
import zipfile
import uuid
import os
from distutils.dir_util import copy_tree, remove_tree
import sys
import json

def download(branch = "main"):

    print(f"Downloading latest version of branch {branch}...")

    Headers = CaseInsensitiveDict()
    Headers["Authorization"] = "token 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"
    URL = "https://api.github.com/repos/edgarcantuco/BOTW.Release/zipball/" + branch

    r = requests.get(URL, headers=Headers)

    zipname = uuid.uuid4().hex + ".zip"
    foldername = uuid.uuid4().hex

    if r.status_code == 200:
        with open(zipname, 'wb') as file:
            file.write(r.content)

        with zipfile.ZipFile(zipname, 'r') as zip_ref:
            zip_ref.extractall(foldername)

        file.close()
        zip_ref.close()

        InsideFolder = os.listdir(os.getcwd() + "/" + foldername)[0]

        copy_tree(os.getcwd() + "/" + foldername + "/" + InsideFolder, os.getcwd())

        with open("Branch.txt", "w") as file:
            file.write(branch)

        os.remove(zipname)
        os.remove(".gitignore")
        remove_tree(foldername)

def getBranches():

    Headers = CaseInsensitiveDict()
    Headers["Authorization"] = "token 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"
    URL = "https://api.github.com/repos/edgarcantuco/BOTW.Release/branches"

    r = requests.get(URL, headers=Headers)

    if r.status_code == 200:
        r = json.loads(r.content)
        branches = {}

        for branch in r:
            branches[branch["name"].lower()] = branch["name"]

        return branches

    else:

        return json.loads(r.content)["message"]


if __name__ == "__main__":
    arguments = sys.argv

    if len(arguments) == 1:
        download()

    elif len(arguments) > 1:
        
        branches = getBranches()
        if arguments[1].lower() in ["branch", "b", "branches"]:
            for branch in branches.values():
                print(branch)
        else:
            if arguments[1].lower() in branches.keys():
                download(branches[arguments[1].lower()])
            else:
                input(f"Branch with name {arguments[1]} doesn't exist. Press enter to finish.")
