""" 
fastapi_example.py 
starlette / fastapi / sanic asgi + websocket + mounted apps demo 

run: 
$ uvicorn --reload fastapi_example:app

then visit / for websocket demo

"""

from asyncio import sleep
from datetime import datetime

# fastapi deps
from fastapi import FastAPI

# starlette deps
from starlette.staticfiles import StaticFiles
from starlette.responses import PlainTextResponse
from starlette.routing import Route, WebSocketRoute, Mount
from starlette.websockets import WebSocket
from starlette.background import BackgroundTask

from starlette.middleware.trustedhost import TrustedHostMiddleware

# sanic deps
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import text

# sanic class-based view
class SanicView(HTTPMethodView):
    async def get(self, request):
        return text('I am a Sanic get method :D')

sanic_app = Sanic('test-app')
sanic_app.add_route(SanicView.as_view(), '/sanic-api/test')

# starlette StaticFiles app 
starlette_static_files = StaticFiles(directory="./frontend/dist/", html=True)

# starlette functional websocket endpoint
async def websocket_endpoint(websocket):    
    await websocket.accept()

    while True:
        now = datetime.now()
        now_str = now.strftime("%m/%d/%Y, %H:%M:%S")

        try:
            await websocket.send_text(now_str)
        except:
            break;

        await sleep(2)

    await websocket.close()

# starlette bg task 
async def background_task(message):
    # send mail, hash a pw, time consuming stuff like that 
    await sleep(5)
    print(message)

# starlette functional endpoint
async def test(request):
    task = BackgroundTask(background_task, message="testing background task!")
    return PlainTextResponse("Testing Starlette functional endpoint with a bg task!", background=task)

# fastapi routes 
routes = [
    Mount("/sanic-api", sanic_app),
    WebSocketRoute("/ws", websocket_endpoint), 
    Route('/test', endpoint=test),
    Mount("/", starlette_static_files),
]

app = FastAPI(routes=routes)

# uncomment this to enable the trusted host middleware 

#app.add_middleware(
#    TrustedHostMiddleware, 
#    allowed_hosts=['example.com', '*.example.com']
#)

