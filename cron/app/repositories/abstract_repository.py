from abc import ABC, abstractmethod
from typing import Iterable, Any
from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    """
    Base repository interface for bulk persistence operations.
    """

    @abstractmethod
    def bulk_upsert(self, db: Session, rows: Iterable[dict[str, Any]]):
        """
        Sets and performs a bulk upsert operation for the given rows.
        """
        pass
