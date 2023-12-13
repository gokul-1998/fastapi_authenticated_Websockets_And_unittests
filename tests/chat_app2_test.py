from fastapi import WebSocketDisconnect
from fastapi.testclient import TestClient
import pytest
from chat_app2.main import app

client = TestClient(app)
# def test_websocket():
    
#     with client.websocket_connect("/ws") as websocket:
#         data = websocket.receive_json()
#         assert data == {"msg": "Hello WebSocket"}



def test_read_main():
    response = client.get("/a")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_websocket_endpoint():
    client = TestClient(app)
    
    # Mock WebSocket connection
    with client.websocket_connect("/ws/1") as websocket:
        websocket.send_text("Hello")
        response = websocket.receive_text()
        assert response == "You: Hello"
        
        # Simulate client disconnect
        with pytest.raises(WebSocketDisconnect):
            websocket.close()

        # Ensure disconnection is handled
        response =  websocket.receive_text()
        assert response == "Client #1 left the chat"