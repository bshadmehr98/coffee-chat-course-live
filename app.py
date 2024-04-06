from sanic import Sanic
from sanic.response import text
from sanic_motor import BaseModel
from sanic_jwt import initialize
from auth import authenticate, retrieve_user

app = Sanic("CoffeeChat")

app.config.CORS_ORIGINS = "*"

settings = dict(
    MOTOR_URI='mongodb://coffeechat:coffeechat@127.0.0.1:27017/coffeechat?authSource=coffeechat'
)

app.config.update(settings)
app.static('/static', './static')

BaseModel.init_app(app)

initialize(app, authenticate, retrieve_user=retrieve_user)

