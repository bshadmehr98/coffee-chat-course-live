from sanic import Sanic
from sanic.response import text
from sanic_motor import BaseModel
from sanic_jwt import initialize
from auth import authenticate, retrieve_user
import os
from sanic import Sanic
from sanic.response import json
import etcd3
import os
import uuid
import asyncio

app = Sanic("CoffeeChat")
etcd = etcd3.client()

app.config.CORS_ORIGINS = "*"

settings = dict(
    MOTOR_URI='mongodb://coffeechat:coffeechat@127.0.0.1:27017/coffeechat?authSource=coffeechat',
    PORT=os.environ.get("PORT"),
    ETCD_LEASE_TTL=10,
    ETCD_LEADER_KEY="coffeechat/leader"
)


async def elect_leader():
    while True:
        try:
            lease = etcd.lease(app.config.get("ETCD_LEASE_TTL", 10))
            success, _ = etcd.transaction(
                compare=[
                    etcd.transactions.version(app.config.get("ETCD_LEADER_KEY")) == 0
                ],
                success=[
                    etcd.transactions.put(app.config.get("ETCD_LEADER_KEY"), app.config.get("PORT"), lease)
                ],
                failure=[]
            )

            if success:
                print(f"I am the leader ({app.config.get('PORT')})")
                # As long as we're the leader, keep refreshing the lease.
                while True:
                    await asyncio.sleep(app.config.get("ETCD_LEASE_TTL", 10) / 2)
                    lease.refresh()
            else:
                print(f"I am a follower ({app.config.get('PORT')})")
                await asyncio.sleep(app.config.get("ETCD_LEASE_TTL", 10))
        except Exception as e:
            print(f"Error during election: {e}")
            await asyncio.sleep(app.config.get("ETCD_LEASE_TTL", 10))


app.add_task(elect_leader())

app.config.update(settings)
app.static('/static', './static')

BaseModel.init_app(app)

initialize(app, authenticate, retrieve_user=retrieve_user)

