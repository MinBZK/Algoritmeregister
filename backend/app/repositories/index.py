from abc import ABC, abstractmethod
from sqlalchemy.orm import Session


class IRepository(ABC):
    @abstractmethod
    def __init__(self, session: Session):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def add(self, item):
        raise NotImplementedError
