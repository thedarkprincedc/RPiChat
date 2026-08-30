
import json
import pytest
import websockets


@pytest.mark.asyncio
async def test_websocket_control_and_telemetry():
    uri = "ws://localhost:8080/ws/control"

    async with websockets.connect(uri) as ws:

        # Verify connection
        assert ws.open

        # Send control
        await ws.send(json.dumps({
            "type": "control",
            "throttle": 0.5,
            "steering": 0.2,
        }))

        # Receive response
        message = await ws.recv()
        data = json.loads(message)

        assert data["type"] == "control_ack"
        assert data["success"] is True