import json


async def send_message_to_user(ws, command, message):
    response = {
                "data": message,
                "command": command
                }
    await ws.send(json.dumps(response))
