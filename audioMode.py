from contextlib import contextmanager
from dotenv import load_dotenv
from google import genai
from strumenti import *
import pyaudio
import asyncio
import sys
import os

@contextmanager
def ignoreErrors():
    devnull = os.open(os.devnull, os.O_WRONLY)
    oldStderr =os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(oldStderr, 2)
        os.close(oldStderr)

load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
chunk = 2048
client = genai.Client()
tools = [createFolder, googleSearch,deleteFromMemory, folderTree,readMemory, updateMemory,youtubeDownloader,
         createFile, launchCommands, getSystemInfo, readFile, getCurrentWorkingDirectory, getFolderContent, findFolderOrFile]

async def call():
    with ignoreErrors():
        audioManager = pyaudio.PyAudio()
    microphoneStream = audioManager.open(format=pyaudio.paInt16, channels=1, rate=24000, input=True, frames_per_buffer=chunk)
    audioStream = audioManager.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True, frames_per_buffer=chunk)

    async with client.aio.live.connect(model="gemini-2.5-flash-native-audio-preview-12-2025", config= {"temperature" : 0.7, "response_modalities": ["AUDIO"], "tools" : tools}) as session:
        print("In linea")
        async def send():
            while True:
                data = await asyncio.to_thread(microphoneStream.read, chunk, exception_on_overflow=False)
                await session.send_realtime_input(audio={"data" : data, "mime_type": "audio/pcm"})
        async def receive():
            async for message in session.receive():
                if message.server_content:
                    model_turn = message.server_content.model_turn
                    if model_turn:
                        for part in model_turn.parts:
                            if part.inline_data:
                                await asyncio.to_thread(audioStream.write, part.inline_data.data)
                if message.tool_call:
                    functionResponce = []
                    for call in message.tool_call.function_calls:
                        function = globals().get(call.name)
                        if function:
                            print(f'Eseguo {call.name}')
                            try:
                                output = await asyncio.to_thread(function, **call.args)
                                functionResponce.append({
                                    "name" : call.name,
                                    "id": call.id,
                                    "response" : {"result": output}
                                })
                            except Exception as e:
                                print(e)
                    await session.send_tool_response(function_responses=functionResponce)

        try:
            await asyncio.gather(send(), receive())
        except Exception as e:
            print(e)
        finally:
            microphoneStream.stop_stream()
            microphoneStream.close()
            audioStream.stop_stream()
            audioStream.close()
            audioManager.terminate()
            
asyncio.run(call())