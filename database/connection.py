"""
database/connection.py
MongoDB Atlas connection manager with connection pooling.
"""
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    """Singleton MongoDB connection manager."""

    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def connect(self):
        """Establish connection to MongoDB Atlas."""
        if self._client is not None:
            return self._db

        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB_NAME", "nexora_ai")

        if not mongo_uri:
            raise ValueError("MONGO_URI environment variable is not set")

        try:
            self._client = MongoClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=30000,
                connectTimeoutMS=5000,
                socketTimeoutMS=30000,
                retryWrites=True,
            )
            # Verify connection
            self._client.admin.command("ping")
            self._db = self._client[db_name]
            print(f"Connected to MongoDB: {db_name}")
            return self._db

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"MongoDB connection failed: {e}")
            raise

    def get_db(self):
        """Get the database instance, connecting if necessary."""
        if self._db is None:
            self.connect()
        return self._db

    def get_collection(self, name: str):
        """Get a specific collection by name."""
        return self.get_db()[name]

    def close(self):
        """Close the MongoDB connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            print("MongoDB connection closed")


# Singleton instance
db_connection = DatabaseConnection()


def get_db():
    """Helper function to get database instance."""
    return db_connection.get_db()


def get_collection(name: str):
    """Helper function to get a collection."""
    return db_connection.get_collection(name)
