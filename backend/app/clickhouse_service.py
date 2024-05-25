# clickhouse_service.py

import clickhouse_connect

def get_clickhouse_connection():
    conn = clickhouse_connect.get_client(
        host='clickhouse', 
        port=8123,
        username='default', 
        password=''
    )
    return conn

def execute_query(query):
    conn = get_clickhouse_connection()
    result = conn.query(query)
    return result.result_rows