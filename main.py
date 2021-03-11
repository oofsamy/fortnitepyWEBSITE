import fortnitepy
import json
import os
import codecs
import sanic
from sanic.response import file

from fortnitepy.ext import commands


email = ''
password = ''
filename = 'device_auths.json'
description = 'Sanic/fortnitepy bot made by oofsamy#2714'

def get_device_auth_details():
    if os.path.isfile(filename):
        with open(filename, 'r') as fp:
            return json.load(fp)
    return {}

def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open(filename, 'w') as fp:
        json.dump(existing, fp)


device_auth_details = get_device_auth_details().get(email, {})
bot = commands.Bot(
    command_prefix='!',
    auth=fortnitepy.AdvancedAuth(
        email=email,
        password=password,
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details
    )
)

sanic_app = sanic.Sanic(__name__)
server = None

sanic_app.static('/static', './static')

@bot.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)

@sanic_app.route('/friends', methods=['GET'])
async def get_friends_handler(request):
    friends = [friend.id for friend in bot.friends]
    return sanic.response.json(friends)

@sanic_app.route('/index', methods=['GET'])
async def get_friends_handler(request):
    friends = [friend.id for friend in bot.friends]
    return sanic.response.html("index.html")

@sanic_app.route('/html')
async def handle_request(request):
    return await file('test.html')

@sanic_app.route('/')
async def index(request):
    return await file('main.html')

@sanic_app.websocket('/feed')
async def feed(request, ws):
    while True:
        data = await ws.recv()
        if data == "renegaderaider":
            await bot.party.me.set_outfit(asset="CID_028_Athena_Commando_F")
        elif data == "ghoultrooper":
            await bot.party.me.set_outfit(asset="CID_029_Athena_Commando_F_Halloween")
        elif data == "jonesy":
            await bot.party.me.set_outfit(asset="CID_005_Athena_Commando_M_Default")
        elif data == "blackknight":
            await bot.party.me.set_outfit(asset="CID_035_Athena_Commando_M_Medieval")
@bot.event
async def event_ready():
    global server
    print('----------------')
    print('Bot ready as')
    print(bot.user.display_name)
    print(bot.user.id)
    print('----------------')

    coro = sanic_app.create_server(
        host='localhost',
        port=6969,
        return_asyncio_server=True,
    )
    server = await coro

@bot.event
async def event_before_close():
    global server

    if server is not None:
        await server.close()

@bot.event
async def event_friend_request(request):
    await request.accept()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run()