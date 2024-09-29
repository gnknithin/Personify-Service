from tornado.web import RequestHandler


class AdminRequestHandler(RequestHandler):
    async def get(self) -> None:
        return await self.render(template_name="templates/admin.html")
