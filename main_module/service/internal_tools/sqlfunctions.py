import sys

import psycopg2
import pandas as pd

# Here you want to change your database, username & password according to your own values
param_dic = {
    "host": "localhost",
    "port": 5432,
    "database": "zhassbala",
    "user": "zhassbala",
    "password": "87787003431",
}


def connect(params_dic):
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params_dic)
        # print('Connected to the PostgreSQL database...')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    return conn


def single_insert(conn, insert_req):
    """Execute a single INSERT request"""
    cursor = conn.cursor()
    try:
        # print('Inserting to the PostgreSQL database...')
        cursor.execute(insert_req)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()


def execute_many(conn: psycopg2.connection, df: pd.DataFrame, table: str):
    """
    Using cursor.executemany() to insert the dataframe
    """
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    print(tuples, list(df.columns))
    # Comma-separated dataframe columns
    cols = ",".join(list(df.columns))
    col_cnt = len(df.columns)
    # SQL quert to execute
    query = "INSERT INTO %s(%s) VALUES(%s)" % (
        table,
        cols,
        "%s," * (col_cnt - 1) + "%s",
    )

    return
    cursor = conn.cursor()
    try:
        # print('Inserting to the PostgreSQL database...')
        cursor.executemany(query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    cursor.close()


def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1

    # Naturally we get a list of tupples
    tupples = cursor.fetchall()
    cursor.close()

    # We just need to turn it into a pandas dataframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


def select_last_values(conn, tableName, columns_, dateCol):
    query_cols = ",".join(columns_)
    select_query = """
        SELECT t1.cryptocompare_id, %s
        FROM %s t1
            INNER JOIN (SELECT cryptocompare_id, max(%s) AS day
                        FROM %s
                        GROUP BY cryptocompare_id) AS max_day
                        ON t1.cryptocompare_id=max_day.cryptocompare_id
                            AND t1.%s=max_day.day;
        """ % (
        query_cols,
        tableName,
        dateCol,
        tableName,
        dateCol,
    )
    column_names = ["cryptocompare_id"] + columns_
    df = postgresql_to_dataframe(conn, select_query, column_names)

    return df
