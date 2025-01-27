import psycopg
import psycopg.rows
from psycopg_pool import ConnectionPool

from iaEditais.config import Settings


class Connection:
    def __init__(self, conninfo, **kwargs):
        self.pool = ConnectionPool(conninfo=conninfo, open=True, **kwargs)

    def exec(self, query, params=None):
        try:
            with self.pool.connection() as conn:
                with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                    cur.execute(query, params)
                    conn.commit()
                    return cur.rowcount
        except Exception as e:
            print(f'Error executing query: {query}')
            print(f'With parameters: {params}')
            print(f'Error: {e}')
            raise

    def select(self, query, params=None) -> list:
        try:
            with self.pool.connection() as conn:
                with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                    cur.execute(query, params)
                    return cur.fetchall()
        except Exception as e:
            print(f'Error executing query: {query}')
            print(f'With parameters: {params}')
            print(f'Error: {e}')
            raise

    def close(self):
        self.pool.close()


conn = Connection(Settings().get_connection_string())