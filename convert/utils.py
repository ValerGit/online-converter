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


def get_attrs_by_table(conn, table):
    cur = conn.cursor()
    cur.execute("SHOW columns FROM " + table)
    columns = []
    for row in cur.fetchall():
        columns.append(row[0])
    return columns