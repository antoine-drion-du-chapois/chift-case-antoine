from abc import ABC, abstractmethod
from typing import Iterable, Any
from datetime import datetime
from sqlalchemy.orm import Session


class AbstractRepository(ABC):
    """
    Generic repository interface for bulk synchronization operations.
    """

    @abstractmethod
    def bulk_upsert(
        self,
        db: Session,
        rows: Iterable[dict[str, Any]],
    ) -> None:
        """
        Perform bulk upsert
        """
        pass
