"""Base pipeline class for data processing."""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Any

import pandas as pd
from django.db import transaction

from main_module.data_processing.internal_tools.sqlfunctions import (
    connect,
    execute_batch,
)

logger = logging.getLogger(__name__)


class BasePipeline(ABC):
    """Base class for all data processing pipelines."""

    def __init__(self, name: str):
        """
        Initialize pipeline.

        Args:
            name: Human-readable name for the pipeline
        """
        self.name = name
        self._conn = None

    @property
    def conn(self):
        """Lazy database connection."""
        if self._conn is None:
            self._conn = connect()
        return self._conn

    def close(self) -> None:
        """Close database connection."""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @abstractmethod
    def extract(self) -> Any:
        """
        Extract data from source.

        Returns:
            Extracted data in any format
        """
        pass

    @abstractmethod
    def transform(self, data: Any) -> pd.DataFrame:
        """
        Transform extracted data.

        Args:
            data: Data from extract step

        Returns:
            Transformed DataFrame ready for loading
        """
        pass

    @abstractmethod
    def load(self, df: pd.DataFrame) -> None:
        """
        Load transformed data.

        Args:
            df: DataFrame to load
        """
        pass

    def execute(self) -> None:
        """Execute the pipeline."""
        try:
            # Extract
            logger.info(f"{self.name}: Starting extraction")
            data = self.extract()
            logger.info(f"{self.name}: Extraction complete")

            # Transform
            logger.info(f"{self.name}: Starting transformation")
            df = self.transform(data)
            logger.info(f"{self.name}: Transformation complete")

            # Load
            logger.info(f"{self.name}: Starting load")
            with transaction.atomic():
                self.load(df)
            logger.info(f"{self.name}: Load complete")

        except Exception as e:
            logger.error(f"{self.name}: Pipeline failed", exc_info=True)
            raise
        finally:
            self.close()

    def batch_insert(
        self, df: pd.DataFrame, table: str, chunk_size: int = 1000
    ) -> None:
        """
        Helper method to insert DataFrame in batches.

        Args:
            df: DataFrame to insert
            table: Target table name
            chunk_size: Number of records per batch
        """
        if df.empty:
            logger.warning(f"{self.name}: Empty DataFrame, skipping insert")
            return

        logger.info(f"{self.name}: Inserting {len(df)} records into {table}")
        execute_batch(self.conn, df, table, chunk_size)
        logger.info(f"{self.name}: Insert complete")
