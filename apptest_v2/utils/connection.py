import pymysql


def get_connection(database):
    """
        mysql 연결 함수

    Args:
        database: 데이터베이스 정보

    Returns:
        데이터베이스 연결 객체
    """
    connection = pymysql.connect(
        host=database['host'],
        user=database['user'],
        password=database['password'],
        db=database['name'],
        charset=database['charset']
    )

    return connection
