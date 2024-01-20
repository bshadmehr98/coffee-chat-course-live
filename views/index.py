from sanic_motor import BaseModel
from sanic import Sanic, Websocket
from sanic.response import text
from models.chat import Chat, Message
from uuid import uuid4
from datetime import datetime
from pprint import pprint
from asyncio import sleep, wait
import json
from commands.base import execute_command
from libs import datetime_handler


app = Sanic.get_app("CoffeeChat")


@app.get("/")
@app.ext.template("admin/chat_list.html")
async def admin_chat_list(request):
    chats = await Chat.get_unread_chats()
    return {"chats": chats}

@app.get("/admin/chats/<token:str>")
@app.ext.template("admin/chat_single.html")
async def admin_single_chat(request, token):
    chat = await Chat.get_by_token(token)
    return {"chat": chat}

@app.websocket("/feed")
async def feed(request, ws: Websocket):
    async for msg in ws:
        message = json.loads(msg)
        response = await execute_command(ws, message["command"], message["data"])
        await ws.send(json.dumps(response, default=datetime_handler))
