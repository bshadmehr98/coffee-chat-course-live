from commands.base import new_command
from models.chat import Chat, Message
from uuid import uuid4
import datetime as dt
from datetime import datetime
import asyncio
import sanic

clients = {}
app = sanic.Sanic.get_app("CoffeeChat")



async def clean_closed_clients():
    await asyncio.sleep(60)
    print('Removing closed connections....')
    for cID in list(clients.keys()).copy():
        try:
            await clients[cID].ping()
        except sanic.exceptions.WebsocketClosed:
            del clients[cID]
    app.add_task(clean_closed_clients())

app.add_task(clean_closed_clients())


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
    await chat.add_message(Message(data["message"], datetime.now(), True))



