from app import app  # noqa
from views import *  # noqa
from commands import *


if __name__ == "__main__":
    app.run(port=int(app.config.get("PORT")))
