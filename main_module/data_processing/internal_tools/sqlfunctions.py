"""Database utility functions for data processing."""

import logging
import sys
from typing import Optional, List, Any

import psycopg2
import pandas as pd
from django.conf import settings

logger = logging.getLogger(__name__)


def get_db_params() -> dict:
    """
    Get database connection parameters from Django settings.

    Returns:
        Dictionary with database connection parameters
    """
    return {
        "host": settings.DATABASES["default"]["HOST"],
        "port": settings.DATABASES["default"]["PORT"],
        "database": settings.DATABASES["default"]["NAME"],
        "user": settings.DATABASES["default"]["USER"],
        "password": settings.DATABASES["default"]["PASSWORD"],
    }


def connect(
    params_dic: Optional[dict] = None,
) -> Optional[psycopg2.extensions.connection]:
    """
    Connect to the PostgreSQL database server.

    Args:
        params_dic: Optional connection parameters. If None, uses Django settings.

    Returns:
        Database connection object or None if connection fails

    Raises:
        psycopg2.Error: If connection fails
    """
    if params_dic is None:
        params_dic = get_db_params()

    try:
        conn = psycopg2.connect(**params_dic)
        logger.debug("Connected to PostgreSQL database")
        return conn
    except psycopg2.Error as error:
        logger.error(f"Failed to connect to database: {str(error)}")
        raise


def execute_query(
    conn: psycopg2.extensions.connection, query: str, params: Optional[tuple] = None
) -> bool:
    """
    Execute a single SQL query.

    Args:
        conn: Database connection
        query: SQL query to execute
        params: Query parameters

    Returns:
        True if successful, False otherwise
    """
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
        return True
    except psycopg2.Error as error:
        logger.error(f"Query execution failed: {str(error)}")
        conn.rollback()
        return False
    finally:
        cursor.close()


def execute_batch(
    conn: psycopg2.extensions.connection,
    df: pd.DataFrame,
    table: str,
    chunk_size: int = 1000,
) -> bool:
    """
    Insert DataFrame records in batches.

    Args:
        conn: Database connection
        df: DataFrame to insert
        table: Target table name
        chunk_size: Number of records per batch

    Returns:
        True if successful, False otherwise
    """
    if df.empty:
        logger.warning("Empty DataFrame provided")
        return True

    cursor = conn.cursor()
    try:
        # Create placeholders for SQL query
        columns = list(df.columns)
        placeholders = ",".join(["%s"] * len(columns))
        query = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

        # Convert DataFrame to list of tuples
        records = [tuple(x) for x in df.to_numpy()]

        # Execute in chunks
        for i in range(0, len(records), chunk_size):
            chunk = records[i : i + chunk_size]
            cursor.executemany(query, chunk)
            conn.commit()
            logger.debug(f"Inserted chunk {i//chunk_size + 1}")

        return True
    except psycopg2.Error as error:
        logger.error(f"Batch execution failed: {str(error)}")
        conn.rollback()
        return False
    finally:
        cursor.close()


def fetch_query(
    conn: psycopg2.extensions.connection, query: str, params: Optional[tuple] = None
) -> List[Any]:
    """
    Execute a query and fetch results.

    Args:
        conn: Database connection
        query: SQL query to execute
        params: Query parameters

    Returns:
        List of query results
    """
    cursor = conn.cursor()
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except psycopg2.Error as error:
        logger.error(f"Query fetch failed: {str(error)}")
        return []
    finally:
        cursor.close()
