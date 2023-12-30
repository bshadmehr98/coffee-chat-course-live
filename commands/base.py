commands = {}

def new_command(func):
    global commands
    async def wrapper(data):
        response = await func(data)
        return {
            "command": func.__name__,
            "data": response
        }
    commands[func.__name__] = wrapper

async def execute_command(command, data):
    print(commands)
    return await commands[command](data)