import logging
import os

from aiohttp import web

import sockjs


CHAT_FILE = open(
    os.path.join(os.path.dirname(__file__), 'chat.html'), 'rb').read()


async def chat_msg_handler(msg, session):
    if session.manager is None:
        return
    if msg.type == sockjs.MSG_OPEN:
        session.manager.broadcast("Someone joined.")
    elif msg.type == sockjs.MSG_MESSAGE:
        session.manager.broadcast(msg.data)
    elif msg.type == sockjs.MSG_CLOSED:
        session.manager.broadcast("Someone left.")


def index(request):
    return web.Response(body=CHAT_FILE, content_type='text/html')


if __name__ == '__main__':
    """Simple sockjs chat."""
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    app = web.Application()
    app.router.add_route('GET', '/', index)
    sockjs.add_endpoint(app, chat_msg_handler, name='chat', prefix='/sockjs/')

    web.run_app(app)
