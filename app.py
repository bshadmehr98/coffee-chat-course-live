from sanic import Sanic
from sanic.response import text
from sanic_motor import BaseModel

app = Sanic("CoffeeChat")

app.config.CORS_ORIGINS = "*"

settings = dict(
    MOTOR_URI='mongodb://coffeechat:coffeechat@127.0.0.1:27017/coffeechat?authSource=coffeechat'
)

app.config.update(settings)
app.static('/static', './static')

BaseModel.init_app(app)

