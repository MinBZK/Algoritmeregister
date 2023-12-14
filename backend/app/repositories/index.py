from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class IRepository(ABC):
    @abstractmethod
    def __init__(self, session: Session):
        raise NotImplementedError

    # @abstractmethod
    # def __del__(self):
    #     raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def add(self, item):
        raise NotImplementedError

    # @abstractmethod
    # def get_by_id(self, id: int):
    #     raise NotImplementedError

    # @abstractmethod
    # def update(self, item, id: int):
    #     raise NotImplementedError

    # @abstractmethod
    # def remove_by_id(self, id: int):
    #     raise NotImplementedError
