from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from rich.console import Group, Console
from email.message import EmailMessage
from readability import readability
from serpapi import GoogleSearch
from dotenv import load_dotenv
from questionary import select
from rich.style import Style
from rich.panel import Panel
from pathlib import Path
from manager import *
import google.auth
import subprocess
import py_compile
import html2text
import mimetypes
import platform
import requests
import yt_dlp
import base64
import shutil
import json
import ast
import os

class AstAnalyzer(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.report = []
        self.indent = 0

    def visit_Import(self, node):
        string = "**📦 libreria:**"
        for name in node.names:
            string += f" {name.name},"
        string = string[:-1]
        self.report.append(string)

    def visit_ImportFrom(self, node):
        string = "**📦 modulo:**"
        string += f" {node.module if node.module else '.'} ->"
        for name in node.names:
            string += f" {name.name},"
        string = string[:-1]
        self.report.append(string)

    def visit_ClassDef(self, node):
        indentString = "    " * self.indent
        self.report.append(f"{indentString}- **📦 class {node.name}**:")
        self.indent += 1
        indentString = "    " * self.indent
        if node.bases:
            basi = [ast.unparse(b) for b in node.bases]
            self.report.append(f"{indentString}- **📦 genitori: {', '.join(basi)}**:")
        if ast.get_docstring(node):
            self.report.append(f"{indentString}- '{ast.get_docstring(node)}'")
        for dec in node.decorator_list:
            self.report.append(f"{indentString}- 🏷️ @{ast.unparse(dec)}")
        self.generic_visit(node)
        self.indent -= 1

    def visit_FunctionDef(self, node):
        indentString = "    " * self.indent
        string = f"{indentString}- **⚡ def {node.name}**("
        args = []
        for arg in node.args.args:
            if(arg.annotation):
                args.append(f"{arg.arg}: {ast.unparse(arg.annotation)}")
            else:
                args.append( f"{arg.arg}")
        string +=  ", ".join(args) + ")"
        if node.returns:
            string += f" -> {ast.unparse(node.returns)}"
        self.report.append(string)
        self.indent += 1
        indentString = "    " * self.indent
        if ast.get_docstring(node):
            self.report.append(f"{indentString}'{ast.get_docstring(node)}'")
        for dec in node.decorator_list:
            self.report.append(f"{indentString}- 🏷️ @{ast.unparse(dec)}")
        self.indent -= 1
    
    def visit_AsyncFunctionDef(self, node):
        indentString = "    " * self.indent
        string = f"{indentString}- **⚡ async def {node.name}**("
        args = []
        for arg in node.args.args:
            if(arg.annotation):
                args.append(f"{arg.arg}: {ast.unparse(arg.annotation)}")
            else:
                args.append( f"{arg.arg}")
        string +=  ", ".join(args) + ")"
        if node.returns:
            string += f" -> {ast.unparse(node.returns)}"
        self.report.append(string)
        self.indent += 1
        indentString = "    " * self.indent
        if ast.get_docstring(node):
            self.report.append(f"{indentString}'{ast.get_docstring(node)}'")
        for dec in node.decorator_list:
            self.report.append(f"{indentString}- 🏷️ @{ast.unparse(dec)}")
        self.indent -= 1

    def finish(self):
        finalReport = ""
        for riga in self.report:
            finalReport += riga + "\n"
        return finalReport


@tool
def createFile(name: str, content: str):
    """Create or override a file with a specified content."""
    with open(file = name, mode = "w") as file:
        file.write(content)

@tool
def createFolder(path: str):
    """Create a folder given its path, if they don't exist, it also creates the parents of the folder"""
    folder = Path(path)
    folder.mkdir(parents=True, exist_ok=True)

@tool
def findFolderOrFile(name: str, startingFolder : str = "/home"):
    """find a folder or a file by its name and a starting path (default is /home), it returns the absolute path. its useful if you don't know where is a file or a folder specified by user"""
    results = []
    for root, folders, files in os.walk(startingFolder):
        if name in folders:
            results.append(os.path.join(root, name))
        if name in files:
            results.append(os.path.join(root, name))
    return results

@tool
def readFile(path: str):
    """Read the content of a file."""
    with open(file = path, mode = "r") as file:
        return file.read()

@tool
def readAllFolderFiles(path: str):
    """read all the files in a folder giving you a dictionary with all the files content, the key is the file name"""
    content = {}
    for item in os.listdir(path=path):
        if not os.path.isdir(os.path.join(path, item)):
            try:
                with open(os.path.join(path, item), "r") as file:
                    content["item"] = file.read()
            except:
                content += f"\n[{item}]\n[not readable]"
    return content

@tool
def getCurrentWorkingDirectory():
    """gives you the absolute path of the folder you are in"""
    return os.getcwd()

@tool
def getFolderContent(path: str):
    """gives you a list of the files and folders contained in a folder"""
    return os.listdir(path=path)

@tool
def folderTree(path: str):
    """return you a recursive tree of the content of a folder"""
    tree = {"name" : os.path.basename(path), "type" : "folder","path": path, "children" : []}
    try:
        for item in os.listdir(path=path):
            itemPath = os.path.join(path, item)
            if os.path.isdir(itemPath):
                tree["children"].append(folderTree(itemPath))
            else:
                tree["children"].append(
                    {
                        "name" : os.path.basename(itemPath), "type" : "file", "path": itemPath
                    }
                )
    except:
        tree["children"].append({"name": "permesso negato", "type": "errore"})
    return tree

def launchCommands(commands : list[list[str]]):
    """launch commands in the terminal giving a list of commands, every command is a list with command and argument for subprocess. you can use the terminal for doing actions. the function returns a list of tuples with output and errors of every command in order"""
    outputs = []
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        outputs.append((result.stdout, result.stderr))
    return outputs
    
@tool
def getSystemInfo():
    """gives informations and context about the OS in use"""
    osName = platform.system()
    architecture = platform.machine()
    version = platform.version()
    release = platform.release()
    node = platform.node()
    systemInfo = {
        "name" : osName,
        "architecture" :architecture,
        "version" : version,
        "release" : release,
        "node": node,
    }
    if osName == "Linux" :
        distroInfo = platform.freedesktop_os_release()
        systemInfo["distro name"] = distroInfo.get("NAME", "N/A")
        systemInfo["distro ID"] = distroInfo.get("ID", "N/A")
    return systemInfo

@tool
def youtubeDownloader(videoName : str, onlyAudio : bool = True, folder : str = ""):
    """download audio or video from youtube in a folder given given the youtube title. default folder is the home folder"""
    research = f'ytsearch1: {videoName}'
    format = ""
    filename = os.path.join(folder,f'{videoName}.%(ext)s')
    postprocessors = []
    if onlyAudio:
        format = 'bestaudio/best'
        postprocessors = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        format = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]'
    
    options = {
        'format': format,
        'outtmpl': filename,
        'postprocessors': postprocessors,
        'default_search': 'ytsearch',
        'quiet': True,
        'noprogress': True,
        'noplaylist': True,
        'logger': None,
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.extract_info(research, download=True)

@tool
def updateMemory(informations: dict):
    """saves something you need or want to remember in your memory or updates previously memorized data. if you want to update your memory, the keys of the updated values you pass should be the same of the old datas in the memory"""
    jsonString = ""
    thisFolderPath = os.path.dirname(os.path.abspath(__file__))
    memoryPath = os.path.join(thisFolderPath, "memory/memory.json")
    with open(memoryPath, "r") as file:
        jsonString = file.read()
    memory = json.loads(jsonString)
    memory = memory | informations
    with open(memoryPath, "w") as file:
        json.dump(memory, file, indent=4)

@tool
def readMemory():
    """read your memory if you need some informations"""
    jsonString = ""
    thisFolderPath = os.path.dirname(os.path.abspath(__file__))
    memoryPath = os.path.join(thisFolderPath, "memory/memory.json")
    with open(memoryPath, "r") as file:
        jsonString = file.read()
    return jsonString

@tool
def deleteFromMemory(keyList : list[str]):
    """delete something saved in memory by giving his key in a list (you can give a list of multiple keys)"""
    jsonString = ""
    thisFolderPath = os.path.dirname(os.path.abspath(__file__))
    memoryPath = os.path.join(thisFolderPath, "memory/memory.json")
    with open(memoryPath, "r") as file:
        jsonString = file.read()
    memory = json.loads(jsonString)
    for key in keyList:
        del memory[key]
    with open(memoryPath, "w") as file:
        json.dump(memory, file, indent=4)

@tool
def googleSearch(query : str):
    """search a query on google, useful for up to date informations"""
    load_dotenv()
    apiKey = os.getenv("SERP_API_KEY")
    config = {
        "engine": "google",
        "q": query,
        "hl" : "it",
        "gl": "it",
        "num": 5,
        "api_key": apiKey
    }
    search = GoogleSearch(config)
    results = search.get_dict()
    organicResults = results.get("organic_results", [])
    cleanedResults = []
    for organicResult in organicResults:
        cleanedResults.append({"title": organicResult.get("title"), "link": organicResult.get("link"), "snippet": organicResult.get("snippet")})
    print("\n[searched]")
    return cleanedResults

@tool
def siteContent(link: str):
    """return the content of a site given his link in a dictionary where the key is the title"""
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }
    html = requests.post(url=link, headers=headers)
    documento = readability.Document(html.text)
    titolo = documento.title()
    body = documento.summary()
    markdown = html2text.html2text(body)
    return {titolo: markdown}

@tool
def analyzePythonProject(path: str):
    """return an analysis written in markdown made with ast of a python project"""
    blacklist = [
        "venv", 
        ".venv", 
        "env", 
        "bin", 
        "lib", 
        "lib64", 
        "include", 
        "share",
        ".git", 
        ".svn", 
        ".hg",
        "__pycache__", 
        ".pytest_cache", 
        ".mypy_cache", 
        ".ipynb_checkpoints", 
        ".ruff_cache",
        ".vscode", 
        ".idea", 
        ".project",
        "build", 
        "dist", 
        "egg-info", 
        "htmlcov"
    ]
    trees = {}
    for root, folders, files in os.walk(path):
        folders[:] = list(filter(lambda folder: not folder in blacklist, folders))
        for filename in files:
            if filename.endswith(".py"):
                fullPath = os.path.join(root, filename)
                try:
                    with open(fullPath, "r") as file:
                        trees[fullPath] = ast.parse(file.read())
                except SyntaxError:
                    continue
                except UnicodeError:
                    continue
    markdown = ""
    for path in trees.keys():
        markdown += f"### {path}\n"
        analyzer = AstAnalyzer()
        analyzer.visit(trees[path])
        markdown += analyzer.finish() + "\n"
    with open("mark.md", "w") as file:
        file.write(markdown)
    
    return markdown

@tool
def replaceInFile(filePath : str, oldStr : str, newStr : str):
    """replace a string in a file with a new one"""
    content = ""
    with open(filePath, "r") as file:
        content = file.read()
    content = content.replace(oldStr, newStr)
    with open(filePath, "w") as file:
        file.write(content)
    
    
@tool
def manageTask(task : str):
    """you can write here a TODO list for completing a task in markdown"""
    path = os.path.join(os.getcwd(), "task/task.md")
    os.makedirs(os.path.join(os.getcwd(), "task"), exist_ok=True)
    with open(path, "w") as file:
        file.write(task)
    return "task memorizzata"

@tool
def readTask():
    """giver you the TODO list for completing a task in markdown"""
    path = os.path.join(os.getcwd(), "task/task.md")
    if not os.path.exists(path):
        return "nessuna task attiva"
    with open(path, "r") as file:
        return file.read()
    
@tool
def testPythonCode(path : str):
    """simply executes a python file and gives you output and errors"""
    commandArgs = ["python3", path]
    result = subprocess.run(commandArgs, capture_output=True, text=True)
    if result.returncode == 0:
        return f"esecuzione perfetta, output:\n{result.stdout}"
    else:
        return f"ERRORE (return code {result.returncode}, TRACEBACK:\n{result.stderr})"

@tool
def checkPythonSyntax(path : str):
    """you can use this function to check any syntax errors in a python file without running it"""
    try:
        py_compile.compile(path, doraise=True)
        return "tutto ok"
    except py_compile.PyCompileError as e:
        return f"errore di sintassi : {e.msg}"
    
@tool
def backupFile(filePath: str):
    """backup a file given his path, it puts the backup in the filepath with the .backup extension"""
    if(os.path.exists(filePath)):
        shutil.copy2(filePath, f"{filePath}.backup")
        return "backup completato"
    return "file non esistente"

@tool
def restoreFile(filePath: str):
    """restores the backup of a file given his path"""
    if(os.path.exists(f"{filePath}.backup")):
        shutil.copy2(f"{filePath}.backup", filePath)
        return "ripristino avvenuto con successo"
    return "bakup non esistente"

@tool
def sendMail(destinationAddress: str, object : str, content: str, attachmentPath : str = None):
    """"sends an email to a destination address with content, an object and if you want an attachment"""
    SCOPES = ['https://mail.google.com/']
    tokenPath = "/home/batman/progetti/agenteV2/token.json"
    credenziali = Credentials.from_authorized_user_file(tokenPath, SCOPES)
    service = build("gmail", "v1", credentials=credenziali)
    messaggio = EmailMessage()
    messaggio.set_content(content)
    messaggio["To"] = destinationAddress
    messaggio["From"] = "nicolomorelli06@gmail.com"
    messaggio["Subject"] = object
    if attachmentPath is not None:
        ctype, encoding = mimetypes.guess_type(attachmentPath)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split("/", 1)
        with open(attachmentPath, "rb") as file:
            messaggio.add_attachment(file.read(), maintype= maintype, subtype = subtype, filename = os.path.basename(attachmentPath))
    codificato = base64.urlsafe_b64encode(messaggio.as_bytes()).decode()
    createMessage = {"raw": codificato}
    send = (service.users().messages().send(userId= "me", body = createMessage).execute())
