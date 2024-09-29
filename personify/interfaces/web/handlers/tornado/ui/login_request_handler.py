from tornado.web import RequestHandler


class LoginRequestHandler(RequestHandler):
    async def get(self) -> None:
        return await self.render(template_name="templates/login.html")
