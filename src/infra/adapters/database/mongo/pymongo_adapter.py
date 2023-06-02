import logging
from typing import Any, Dict, List, Optional, Union

from bson import ObjectId
from infra.adapters.database.base_database_adapter import BaseDatabaseAdapter
from infra.builders.database.mongo_connection_string import (
    MongoDbConnectionStringBuilder,
)
from infra.validators.database.mongo_connection_string import (
    MongoConnectionStringValidator,
)
from pymongo import MongoClient, ReturnDocument
from pymongo.results import DeleteResult, InsertManyResult, InsertOneResult


class PyMongoAdapter(BaseDatabaseAdapter):
    def __init__(
        self,
        logger: logging.Logger,
        connection_string: str
    ) -> None:
        '''
        Mongo Database Adapter
        '''
        super().__init__(logger=logger)
        self._connection_string = connection_string
        self._client: Any = MongoClient(self._connection_string)

    @classmethod
    def from_connection_string(
        cls,
        logger: logging.Logger,
        connection_string: str
    ) -> 'PyMongoAdapter':
        if not MongoConnectionStringValidator.is_valid(
            connection_string=connection_string
        ):
            raise ValueError

        return cls(logger, connection_string)

    @classmethod
    def from_dict(
        cls,
        logger: logging.Logger,
        **connection_info: Dict[Any, Any]
    ) -> 'PyMongoAdapter':
        return cls(
            logger,
            MongoDbConnectionStringBuilder(
                **connection_info).get_connection_string()
        )

    @property
    def client(self):
        return self._client

    def check_availability(self) -> bool:
        '''
        Check availability

        # Return

        bool
        '''
        ping = self._client.admin.command("ping")

        return ping["ok"] == 1

    def __string_to_object_id(self, value: str):
        object_id = ObjectId(value)
        if ObjectId.is_valid(object_id):
            return object_id
        else:
            return None

    def insert_one(
        self, db_name: str, collection_name: str, data: Dict[Any, Any]
    ) -> Union[InsertOneResult, None]:
        collection = self._client[db_name][collection_name]
        with self._client.start_session() as session:
            result = collection.insert_one(
                document=data,
                session=session
            )
        return result

    def delete_one(
        self, db_name: str, collection_name: str, key: str
    ) -> Union[DeleteResult, None]:
        collection = self._client[db_name][collection_name]
        _apply_filter = {'_id': self.__string_to_object_id(key)}
        with self._client.start_session() as session:
            result = collection.delete_one(_apply_filter, session=session)
        return result

    def find_one(
        self, db_name: str, collection_name: str, key: str
    ) -> Union[Dict[Any, Any], None]:
        collection = self._client[db_name][collection_name]
        result = collection.find_one({"_id": self.__string_to_object_id(key)})

        return result

    def find_one_and_update(
        self,
        db_name: str,
        collection_name: str,
        key: str,
        data: Dict[Any, Any]
    ) -> Union[Dict[Any, Any], None]:
        collection = self._client[db_name][collection_name]
        _apply_filter = {'_id': self.__string_to_object_id(key)}
        _update_data = {'$set': data}
        with self._client.start_session() as session:
            result = collection.find_one_and_update(
                filter=_apply_filter,
                update=_update_data,
                upsert=False,
                return_document=ReturnDocument.AFTER,
                session=session
            )

        return result

    def insert_many(
        self,
        db_name: str,
        collection_name: str,
        data: List[Dict[Any, Any]]
    ) -> InsertManyResult:
        collection = self._client[db_name][collection_name]
        with self._client.start_session() as session:
            result = collection.insert_many(data, session=session)
        return result

    def find(
            self,
            db_name: str,
            collection_name: str,
            filter_by: Optional[Dict[Any, Any]] = None,
            skip_to: int = 0,
            limit_by: int = 0
    ) -> List[Dict[Any, Any]]:
        collection = self._client[db_name][collection_name]
        result = collection.find(
            filter=filter_by, skip=skip_to, limit=limit_by
        )
        return list(result)

    def delete_many(
        self,
        db_name: str,
        collection_name: str,
        keys: List[str],
    ) -> DeleteResult:
        collection = self._client[db_name][collection_name]
        _apply_filter = {'_id': {'$in': keys}}
        with self._client.start_session() as session:
            result = collection.delete_many(
                filter=_apply_filter,
                session=session
            )

        return result

    def count(self, db_name: str, collection_name: str) -> int:
        collection = self._client[db_name][collection_name]
        result = collection.count_documents({})
        return result
