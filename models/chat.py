from sanic_motor import BaseModel
import dataclasses
from models.base import BaseDataClass
from typing import Optional, List
import datetime as dt

class ChatModel(BaseModel):
    __coll__ = 'chats'
    __unique_fields__ = ['session_token']


@dataclasses.dataclass
class Message(BaseDataClass):
    text: str
    ts: dt.datetime
    from_user: bool


@dataclasses.dataclass
class Chat(BaseDataClass):
    session_token: str
    created_at: Optional[dt.datetime]
    messages: Optional[List[Message]]
    
    MODEL = ChatModel
    
    @classmethod
    async def get_by_token(cls, token):
        res = await Chat.MODEL.find_one({"session_token": token})
        return Chat.to_object(res)
    
    
    @classmethod
    def to_object(cls, data):
        chat = Chat(
            session_token=data.session_token,
            created_at=data.created_at,
            messages=[]
        )
        if data.messages:
            chat.messages = [Message(**m) for m in data.messages]
        return chat
    
    async def add_message(self, message):
        await Chat.MODEL.update_one({"session_token": self.session_token}, {"$push": {"messages": message.to_dict()}})