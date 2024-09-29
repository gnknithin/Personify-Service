import asyncio
import tornado
from tornado.httpserver import HTTPServer
from tornado.web import Application

class MainHandler(tornado.web.RequestHandler):
    async def get(self) -> None:
        _: None = self.write(chunk="Hello, world")

def make_app() -> Application:
    return tornado.web.Application(handlers=[
        (r"/", MainHandler),
    ])

async def main() -> None:
    app: Application = make_app()
    _: HTTPServer = app.listen(port=8888)
    _ = await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main=main())