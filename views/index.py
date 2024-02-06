from sanic_motor import BaseModel
from sanic import Sanic, Websocket
from sanic.response import text
from models.chat import Chat, Message
from models.company import CompanyModel, Company

from uuid import uuid4
from datetime import datetime
from pprint import pprint
from asyncio import sleep, wait
import json
from commands.base import execute_command
from libs import datetime_handler
from sanic.exceptions import SanicException


app = Sanic.get_app("CoffeeChat")


@app.get("/sample")
async def admin_chat_list(request):
    c = Company(phone_no="163516516510", password="46546846854", created_at=datetime.now())
    await c.insert_one()
    return text("Hello")


@app.post("/company/signup")
async def company_signup(request):
    print(request.json)
    print(await Company.get_by_phone(request.json["phone_no"]))
    if await Company.get_by_phone(request.json["phone_no"]) is not None:
        raise SanicException("User alredy exists", status_code=403)
    c = Company(phone_no=request.json["phone_no"], password=request.json["password"], created_at=datetime.now())
    await c.insert_one()
    return text("Hello")



@app.get("/")
@app.ext.template("admin/chat_list.html")
async def sample(request):
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
