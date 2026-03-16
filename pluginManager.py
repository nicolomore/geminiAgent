from pathlib import Path
import importlib
import agent
import os
import inspect
def loadPlugins(agente : agent.Agent):
    folderPath = Path(__file__).parent / "plugins"
    listTools = []
    for item in os.listdir(folderPath):
        module = importlib.import_module(f"plugins.{item}.{item}")
        for name, obj in inspect.getmembers(module):
            if hasattr(obj, "isTool"):
                listTools.append(obj)
    
    agente.addTools(listTools)