commands = {}

def new_command(func):
    global commands
    async def wrapper(ws, data):
        response = await func(ws, data)
        return {
            "command": func.__name__,
            "data": response
        }
    commands[func.__name__] = wrapper

async def execute_command(ws, command, data):
    return await commands[command](ws, data)
