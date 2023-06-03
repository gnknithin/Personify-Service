import logging
from typing import Any, Dict, Generic, List, Optional, Type, Union

from infra.adapters.database.mongo.pymongo_adapter import PyMongoAdapter
from infra.constants._type import TEntityModel
from infra.data.repositories.abstract_repository import AbstractRepository


class MongoRepository(AbstractRepository, Generic[TEntityModel]):
    '''
    A Base Class for all MongoDB Repositories Using PyMongo Package
    '''

    def __init__(
        self,
        logger: logging.Logger,
        db_adapter: PyMongoAdapter,
        database_name: str,
        collection_name: str,
        model_type: Type[TEntityModel]
    ) -> None:
        super().__init__(logger=logger)
        self._context = db_adapter
        self._model_type = model_type
        self._database_name = database_name
        self._collection_name = collection_name

    @property
    def context(self) -> PyMongoAdapter:
        return self._context

    @property
    def database(self) -> str:
        return self._database_name

    @property
    def collection(self) -> str:
        return self._collection_name

    def add(self, data: TEntityModel) -> Union[str, None]:
        return self.context.insert_one(
            db_name=self.database, collection_name=self.collection,
            data=self._model_type().dump(obj=data)
        )

    def get_by_key(self, key: str) -> Union[TEntityModel, None]:
        _result = self.context.find_one(
            db_name=self.database, collection_name=self.collection, key=key
        )
        return self._model_type().load(data=_result) if _result is not None else None

    def get(
        self,
        filter_by: Optional[Dict[Any, Any]] = None,
        skip_to: Optional[int] = 0,
        limit_by: Optional[int] = 0
    ) -> List[TEntityModel]:
        _result = self.context.find(
            db_name=self.database, collection_name=self.collection,
            filter_by=filter_by, skip_to=skip_to, limit_by=limit_by
        )
        return self._model_type(many=True).load(data=_result)

    def update(self, key: str, data: TEntityModel) -> Union[TEntityModel, None]:
        _result = self.context.find_one_and_update(
            db_name=self.database, collection_name=self.collection, key=key,
            data=self._model_type().dump(obj=data)
        )
        return self._model_type().load(data=_result) if _result is not None else None

    def remove(self, key: str) -> bool:
        return self.context.delete_one(
            db_name=self.database, collection_name=self.collection, key=key
        )
