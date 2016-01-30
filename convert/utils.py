import MySQLdb
import MySQLdb.cursors


def check_mysql_connection(host, user, password, db):
    try:
        conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=db
        )
    except MySQLdb.Error:
        return False
    return conn


def get_table_names_by_connection(conn):
    cur = conn.cursor()
    cur.execute("SHOW TABLES")
    return cur.fetchall()