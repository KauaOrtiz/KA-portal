import psycopg2

def bd_conn():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            database = "ka",
            host = "localhost",
            user = "postgres",
            password = "postgres",
            port = "5432"
        )
        print(conn.info)
        cur = conn.cursor()
        return cur

    except Exception as error:
        print(error)
        return None

    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()