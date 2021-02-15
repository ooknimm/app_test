import pymysql


def get_connection(database):
    connection = pymysql.connect(
        host=database['host'],
        user=database['user'],
        password=database['password'],
        db=database['name'],
        charset=database['charset']
    )

    return connection
