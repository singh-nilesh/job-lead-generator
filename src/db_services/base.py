from abc import ABC, abstractmethod

class BaseDatabaseService(ABC):
    def __init__(self):
        self._connected = False

    def __enter__(self):
        if not self._connected:
            self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def insert(self, data):
        pass

    @abstractmethod
    def find(self, query):
        pass