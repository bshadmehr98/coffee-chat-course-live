from sanic_jwt import exceptions
from models.company import Company
import bcrypt

def hash_password(password):
    # Convert the password to bytes, then hash
    print(password)
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode()

def check_password(password, hashed):
    # Convert the password to bytes and check against the hashed password
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

async def authenticate(request, *args, **kwargs):
    username = request.json.get("phone_no", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = await Company.get_by_phone(username)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if check_password(password, user.password):
        raise exceptions.AuthenticationFailed("Password is incorrect.")
    return user
