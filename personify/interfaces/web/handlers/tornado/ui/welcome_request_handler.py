from tornado.web import RequestHandler


class WelcomeRequestHandler(RequestHandler):
    async def get(self) -> None:
        return await self.render(template_name="templates/welcome.html")
