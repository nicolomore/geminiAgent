from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from functools import wraps
from pathlib import Path
import inspect
import os.path

instance = None

def tool(function):
    if inspect.iscoroutinefunction(function):
        @wraps(function)
        async def asyncToolCall(*args, **kwargs):
            try:
                output = await function(*args, **kwargs)
                if  instance:
                    instance.onToolCall( function.__name__, args, kwargs, output)
                return output
            except Exception as e:
                return str(e)

        return asyncToolCall
    else:
        @wraps(function)
        def syncToolCall(*args, **kwargs):
            try:
                output = function(*args, **kwargs)
                if  instance:
                    instance.call_from_thread(instance.onToolCall, function.__name__, args, kwargs, output)
                return output
            except Exception as e:
                return str(e)

        return syncToolCall


def initGmail():
    SCOPES = ['https://mail.google.com/']
    credenziali = None
    tokenPath = Path(__file__).resolve().parent / "token.json"
    if os.path.exists(tokenPath):
        credenziali = Credentials.from_authorized_user_file(tokenPath, SCOPES)
    if not credenziali or not credenziali.valid:
        if credenziali and credenziali.expired and credenziali.refresh_token:
            credenziali.refresh(Request())
        else:
            credPath = "/home/batman/progetti/agenteV2/credentials.json"
            flow = InstalledAppFlow.from_client_secrets_file(credPath, SCOPES)
            credenziali = flow.run_local_server(port=0)
            with open(tokenPath, "w") as file:
                file.write(credenziali.to_json())
    build("gmail", "v1", credentials=credenziali)
