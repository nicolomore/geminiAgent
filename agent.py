from dotenv import load_dotenv
from google.genai import types
from google import genai
from baseTools import *
import os

class Agent:
    def __init__(self):
        load_dotenv()
        self.apiKey = os.getenv("GOOGLE_API_KEY")
        self.client = genai.Client(api_key=self.apiKey)
        self.tools = [createFolder, googleSearch,deleteFromMemory, 
                    folderTree,readMemory, updateMemory,youtubeDownloader,
                    createFile, launchCommands, getSystemInfo, 
                    readFile, getCurrentWorkingDirectory, getFolderContent, 
                    findFolderOrFile, siteContent, analyzePythonProject,
                    manageTask, readTask, replaceInFile,
                    testPythonCode, checkPythonSyntax, backupFile,
                    restoreFile, sendMail, testAsync]
        self.config = types.GenerateContentConfig(temperature=0.7, tools=self.tools)
        self.chat = None
        self.history = []
        self.systemPrompt = ""

    def start(self):
        self.chat = self.client.aio.chats.create(model = "gemini-3.1-flash-lite-preview", config=self.config, history=self.history)

    def setSystemPrompt(self, prompt: str):
        self.systemPrompt = prompt
        self.config = types.GenerateContentConfig(temperature=0.7, tools=self.tools, system_instruction= self.systemPrompt)
        if self.chat:
            self.chat = self.client.aio.chats.create(model = "gemini-3.1-flash-lite-preview", config=self.config, history=self.history)
    
    def addTools(self, tools: list):
        for tool in tools:
            self.tools.append(tool)
        self.config = types.GenerateContentConfig(temperature=0.7, tools=self.tools, system_instruction= self.systemPrompt)
        if self.chat:
            self.chat = self.client.aio.chats.create(model = "gemini-3.1-flash-lite-preview", config=self.config, history=self.history)
    async def answer(self, prompt: str):
        try:
            response = await self.chat.send_message([prompt])
            self.history = self.chat.get_history()
            return response
        except Exception as e:
            return e
    

