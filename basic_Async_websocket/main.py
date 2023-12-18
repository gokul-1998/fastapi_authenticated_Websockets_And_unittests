import asyncio
from functools import lru_cache

from fastapi import FastAPI, WebSocket, Depends
from fastapi.testclient import TestClient
# from pydantic import BaseSettings
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()

reports_queue = asyncio.Queue()
reports_queue.put_nowait(3123213)


class Settings(BaseSettings):
    run: bool = True


@lru_cache()
def get_settings():
    return Settings()


@app.get('/')
async def get(settings: Settings = Depends(get_settings)):
    settings.run = True


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket, settings: Settings = Depends(get_settings)):
    await websocket.accept()
    while settings.run:
        await websocket.send_json(await reports_queue.get())


def test_websocket():
    client = TestClient(app)
    get_settings().run = False
    with client.websocket_connect('/ws') as websocket:
        pass
    
# to run the above test case use the following command:
# `python -m pytest basic_Async_websocket/main.py`