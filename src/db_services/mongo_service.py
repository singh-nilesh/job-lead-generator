from pymongo import MongoClient
from pymongo.errors import PyMongoError, ConnectionFailure, ConfigurationError
from src.core.logger import db_logger as logger
from src.core.exception import CustomException
from .base import BaseDatabaseService
import sys

class MongoDBService(BaseDatabaseService):
    def __init__(self,
                 db_name,
                 collection_name,
                 user_name,
                 password,
                 task_id=None,
                 service="mongo",
                 port="27017"):
        super().__init__()
        self.task_id = task_id
        self.uri = f"mongodb://{user_name}:{password}@{service}:{port}/{db_name}"
        self.collection_name = collection_name
        self.client = None
        self.collection = None

    def _ensure_connection(self):
        if self.client is None or not self._connected:
            self.connect()

    def connect(self):
        if self._connected:
            return
        try:
            logger.info(f"[task={self.task_id}] Connecting to MongoDB (collection={self.collection_name})")
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            
            self.client.admin.command("ping")
            db = self.client.get_default_database()
            if db is None:
                raise ConfigurationError("No database specified in Mongo URI.")
            
            self.collection = db[self.collection_name]
            self._connected = True
            logger.info(f"[task={self.task_id}] MongoDB connection established")
        
        except (ConnectionFailure, ConfigurationError) as e:
            logger.error(f"[task={self.task_id}] MongoDB connection error: {e}")
            raise CustomException(f"MongoDB connection failed: {str(e)}", sys)
        
        except Exception as e:
            logger.error(f"[task={self.task_id}] Unexpected MongoDB connection error: {e}")
            raise CustomException(f"Unexpected MongoDB connection error: {str(e)}", sys)


    def close(self):
        if self.client:
            try:
                self.client.close()
                logger.info(f"[task={self.task_id}] MongoDB connection closed")
            except Exception as e:
                logger.error(f"[task={self.task_id}] Error closing MongoDB connection: {e}", exc_info=True)
                raise CustomException(f"Error closing MongoDB connection: {e}") from e
            finally:
                self._connected = False


    def insert(self, doc: list[dict]):
        """
        Insert multiple documents.
        Args: doc: list of data dictonary
        Returns: list of inserted ObjectIds.
        """
        self._ensure_connection()

        if not isinstance(doc, list) or not doc:
            raise CustomException("Parameter 'doc' must be a non-empty list of dicts.")
        if not all(isinstance(d, dict) for d in doc):
            raise CustomException("All items in 'doc' must be dicts.")
        if self.collection is None:
            raise CustomException("Mongo collection is not initialized.")

        try:
            result = self.collection.insert_many(doc, ordered=False)
            return list(result.inserted_ids)
        
        except PyMongoError as e:
            logger.error(f"[task={self.task_id}] insert_many failed: {e} | docs_count={len(doc)}")
            raise CustomException(f"MongoDB insert_many failed: {e}") from e
        except Exception as e:
            logger.error(f"[task={self.task_id}] Unexpected insert error: {e}", exc_info=True)
            raise CustomException(f"Unexpected MongoDB insert error: {e}") from e


    def find(self, filter_query:dict = {} , row_limit:int = 0) -> list[dict]:
        """
        Fetch documents.
        Args:
            filter_query (dict): Mongo filter. None -> {}.
            row_limit (int): Max docs to return (0 = no limit).
        Returns:
            list[dict]: List of documents (ObjectId stringified).
        """
        self._ensure_connection()
        if self.collection is None:
            raise CustomException("Mongo collection is not initialized.")
        
        try:
            cursor = self.collection.find(filter_query)
            if row_limit > 0:
                cursor = cursor.limit(row_limit)

            docs = []
            for doc in cursor:
                # Convert ObjectId to string for JSON friendliness
                _id = doc.get("_id")
                if _id is not None:
                    doc["_id"] = str(_id)
                docs.append(doc)
            return docs

        except PyMongoError as e:
            logger.error(f"[task={self.task_id}] find failed: {e} | query={filter_query}")
            raise CustomException(f"MongoDB find failed: {e}") from e
        except Exception as e:
            logger.error(f"[task={self.task_id}] Unexpected find error: {e}", exc_info=True)
            raise CustomException(f"Unexpected MongoDB find error: {e}") from e