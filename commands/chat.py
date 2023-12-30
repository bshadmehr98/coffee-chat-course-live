from commands.base import new_command
from models.chat import Chat
from uuid import uuid4
import datetime as dt


@new_command
async def get_chat(data):
    print(data)
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
    return chat.to_dict()