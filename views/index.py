from sanic_motor import BaseModel
from sanic import Sanic, Websocket
from sanic.response import text
from models.chat import Chat, Message
from uuid import uuid4
from datetime import datetime
from pprint import pprint
from asyncio import sleep
import json
from commands.base import execute_command
from libs import datetime_handler


app = Sanic.get_app("CoffeeChat")


@app.get("/")
async def hello_world(request):
    # chat_data = {
    #     "session_token": str(uuid4()),
    #     "created_at": datetime.now(),
    #     "messages": [
    #         {"text": "salam", "ts": datetime.now(), "from_user": True},
    #         {"text": "salam", "ts": datetime.now(), "from_user": False},
    #         {"text": "Khobi?", "ts": datetime.now(), "from_user": True},
    #         {"text": "Are", "ts": datetime.now(), "from_user": False},
    #     ]
    # }
    # chat  = Chat.from_dict(chat_data)
    chat = await Chat.get_by_token("4beeebd8-71e0-4b3a-bdb5-f726f5b3f5c8")
    await chat.add_message(Message("Salam", datetime.now(), True))
    pprint(chat)
    # await chat.insert_one()
    return text("Hello, world.")

@app.websocket("/feed")
async def feed(request, ws: Websocket):
    async for msg in ws:
        message = json.loads(msg)
        response = await execute_command(message["command"], message["data"])
        await ws.send(json.dumps(response, default=datetime_handler))