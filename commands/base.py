commands = {}

def new_command(func):
    global commands
    async def wrapper(company_id, ws, data):
        print(1)
        print(company_id)
        response = await func(company_id, ws, data)
        return {
            "command": func.__name__,
            "data": response
        }
    commands[func.__name__] = wrapper

async def execute_command(company_id, ws, command, data):
    return await commands[command](company_id, ws, data)
