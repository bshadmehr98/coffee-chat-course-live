from sanic_motor import BaseModel
from bson import ObjectId
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
    company_id: str
    
    MODEL = ChatModel


    def to_dict(self):
        data = super().to_dict()
        return data

    def to_mongo(self):
        data = super().to_dict()
        data["company_id"] = ObjectId(data["company_id"])
        return data

    
    @classmethod
    async def get_by_token(cls, token):
        res = await Chat.MODEL.find_one({"session_token": token})
        return Chat.to_object(res)
    
    
    @classmethod
    def to_object(cls, data):
        chat = Chat(
            company_id=str(data.company_id),
            session_token=data.session_token,
            created_at=data.created_at,
            messages=[]
        )
        if data.messages:
            chat.messages = [Message(**m) for m in data.messages]
        return chat
    
    async def add_message(self, message):
        await Chat.MODEL.update_one({"session_token": self.session_token}, {"$push": {"messages": message.to_dict()}})

    @classmethod
    async def get_unread_chats(cls, company_id):
        chats_raw = await Chat.MODEL.find({})
        chats = [Chat.to_object(c) for c in chats_raw.objects]
        return chats

