from google import genai
import os
from dotenv import load_dotenv
from google.genai import types
import sys
from strumenti import *
from rich.console import Console
from rich.markdown import Markdown
from rich.console import Group
from rich.panel import Panel
from rich.padding import Padding
import questionary
from prompt_toolkit.styles import Style

load_dotenv()

apiKey = os.getenv("GOOGLE_API_KEY")
customStyle = Style([('question', 'bold'), ('answer', 'italic'), ('placeholder', 'fg:#6c757d italic')])
client = genai.Client()
console = Console()

config = types.GenerateContentConfig(
            temperature=0.7,
            tools= [createFolder, googleSearch,deleteFromMemory, 
                    folderTree,readMemory, updateMemory,youtubeDownloader,
                    createFile, launchCommands, getSystemInfo, 
                    readFile, getCurrentWorkingDirectory, getFolderContent, 
                    findFolderOrFile, siteContent, analyzePythonProject,
                    manageTask, readTask, replaceInFile,
                    testPythonCode, checkPythonSyntax, backupFile,
                    restoreFile, sendMail]
        )

chat = client.chats.create(model = "gemini-3.1-flash-lite-preview", config=config)

async def answer(prompt: str):
    try:
        response = chat.send_message([prompt])
        return response
    except Exception as e:
        return e


