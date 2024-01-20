from commands.base import new_command
from models.chat import Chat, Message
from uuid import uuid4
import datetime as dt
from datetime import datetime
import asyncio
import sanic
import json 

from commands.helper import send_message_to_user

clients = {}
admins = {}
app = sanic.Sanic.get_app("CoffeeChat")

async def clean_closed_connections(connections):
    for cID in list(connections.keys()).copy():
        try:
            await connections[cID].ping()
        except sanic.exceptions.WebsocketClosed:
            del connections[cID]


async def clean_closed_clients_all():
    await asyncio.sleep(5)
    print(admins)
    print(clients)
    print('Removing closed connections....')
    await clean_closed_connections(clients)
    await clean_closed_connections(admins)
    app.add_task(clean_closed_clients_all())

app.add_task(clean_closed_clients_all())


@new_command
async def get_chat(ws, data):
    if data["chat_id"] is None:
        chat_data = {
            "session_token": str(uuid4()),
            "created_at": dt.datetime.now(),
            "messages": [
                {"text": "سلام. به سایت ما خوش اومدی. چجوری میتونم کمکت کنم؟", "ts": dt.datetime.now(), "from_user": False},
            ]
        }
        chat = Chat.from_dict(chat_data)
        await chat.insert_one()
    else:
        chat = await Chat.get_by_token(data["chat_id"])
    clients[chat.session_token] = ws

    return chat.to_dict()

@new_command
async def new_user_message(ws, data):
    chat = await Chat.get_by_token(data["chat_id"])
    if data["chat_id"] in admins:
        await send_message_to_user(admins[data["chat_id"]], "new_user_message", data["message"])
    await chat.add_message(Message(data["message"], datetime.now(), True))

@new_command
async def new_admin_message(ws, data):
    chat = await Chat.get_by_token(data["chat_id"])
    await chat.add_message(Message(data["message"], datetime.now(), False))
    if data["chat_id"] in clients:
        await send_message_to_user(clients[data["chat_id"]], "new_admin_message", data["message"])
        return {}

@new_command
async def register_admin(ws, data):
    admins[data["chat_id"]] = ws
