import asyncio
from functools import lru_cache

from fastapi import FastAPI, WebSocket, Depends
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings

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
        # Receive data from the client
        data = await websocket.receive_text()
        print(f"Received data: {data}")

        # Send data to the client
        await websocket.send_json({"message": "Hello, client!"})


import asyncio
from fastapi.testclient import TestClient
 # Replace 'your_module' with the actual name of your module

async def test_websocket():
    client = TestClient(app)
    settings = app.dependency_overrides[get_settings]
    settings.run = False

    async with client.websocket_connect('/ws') as websocket:
        # Send data to the server
        await websocket.send_text("Hello, server!")

        # Receive data from the server
        data = await websocket.receive_json()
        assert data == {"message": "Hello, client!"}

# Run the test
asyncio.run(test_websocket())
