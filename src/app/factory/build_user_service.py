from app.user_service import UserService
from bootstrap import ApplicationBootstrap
from domain.user_model import UserModel
from infra.data.unit_of_work.factory.build_postgres_uow import PostgresUnitOfWorkFactory


class UserServiceFactory():
    def __init__(self, bootstrap: ApplicationBootstrap) -> None:
        self._bootstrap = bootstrap

    def build(self, scope: str) -> UserService:

        _postgres_uow = PostgresUnitOfWorkFactory(bootstrap=self._bootstrap).build(
            model_type=UserModel,
            scope=scope
        )

        user_service = UserService(
            logger=self._bootstrap.logger,
            uow=_postgres_uow,
            model_type=UserModel

        )
        return user_service
