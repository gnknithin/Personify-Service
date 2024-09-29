from tornado.web import RequestHandler


class RegisterRequestHandler(RequestHandler):
    async def get(self) -> None:
        return await self.render(template_name="templates/register.html")
