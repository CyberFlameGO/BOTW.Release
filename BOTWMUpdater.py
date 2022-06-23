import requests
from requests.structures import CaseInsensitiveDict
import zipfile
import uuid
import os
from distutils.dir_util import copy_tree
from distutils.dir_util import remove_tree
import base64

print("Downloading latest version...")

Headers = CaseInsensitiveDict()
Headers["Authorization"] = "token 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"
URL = "https://api.github.com/repos/edgarcantuco/BOTW.Release/zipball/main"
# URL = "https://api.github.com/repos/edgarcantuco/BOTW.Release/contents/version.txt"

r = requests.get(URL, headers=Headers)

# data = r.json()

# print(data)

# content = data['content']
# encoding = data.get('encoding')

# if encoding == "base64":
#     print(base64.b64decode(content).decode())
# exit()

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

    os.remove(zipname)
    os.remove(".gitignore")
    os.remove("README.md")
    remove_tree(foldername)