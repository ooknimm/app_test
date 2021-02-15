import re
from datetime import date, datetime


def login_id_validator(login_id, connection):
    """
        로그인 아이디 유효성 검사

        회원가입시 로그인 아이디에 대한 유효성을 검사합니다. (중복 검사도 실시)
        6~30글자의 영어 소문자, 숫자

    Args:
        login_id: 로그인 아이디
        connection: 데이터베이스 연결 객체

    Returns:
        ''
    """

    pattern = '^[a-z0-9]{6,30}$'
    regex = re.compile(pattern)
    result = regex.match(login_id)
    if not result:
        return 'LOGIN_ID_IS_NOT_VALID '

    sql = """
        SELECT
            EXISTS
                (
                    SELECT
                        id
                    FROM 
                        users 
                    WHERE 
                    login_id = %s
                )
            AS user_exist;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, login_id)
            result = cursor.fetchone()[0]
        if result:
            return 'LOGIN_ID_ALREADY_EXISTS '
        return ''

    except Exception as e:
        raise e


def name_validator(name):
    """
        이름 유효성 검사

        회원 가입, 정보 수정 시 사용자의 이름에 대한 유효성 검사를 합니다.
        2~30글자의 한글

    Args:
        name: 사용자 이름

    Returns:
        ''
    """

    pattern = '^[가-힣]{2,30}$'
    regex = re.compile(pattern)
    result = regex.match(name)
    if not result:
        return 'NAME_IS_NOT_VALID '
    return ''


def email_validator(email, connection):
    """
        이메일 유효성 검사

        회원 가입시 이메일에 대한 유효성 검사를 합니다. (중복 검사도 실시)
        이메일 주소 규격 준수

    Args:
        email: 이메일 주소
        connection: 데이터베이스 연결 객체

    Returns:
        ''
    """

    pattern = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
    regex = re.compile(pattern)
    result = regex.match(email)
    if not result:
        return 'EMAIL_IS_NOT_VALID '

    sql = """
        SELECT
            EXISTS
                (
                    SELECT
                        id 
                    FROM 
                        users 
                    WHERE 
                        email = %s
                )
            AS user_exist;
    """

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, email)
            result = cursor.fetchone()[0]
        if result:
            return 'EMAIL_ALREADY_EXISTS '
        return ''

    except Exception as e:
        raise e


def password_validator(password):
    """
        비밀번호 유효성 검사

        회원가입시 비밀번호에 대한 유효성을 검사합니다.
        6~20글자의 영어 대소문자, 숫자

    Args:
        password: 비밀번호

    Returns:
        ''
    """

    pattern = '^[a-zA-Z0-9]{6,20}$'
    regex = re.compile(pattern)
    result = regex.match(password)
    if not result:
        return 'PASSWORD_IS_NOT_VALID '
    return ''


def birth_date_validator(birth_date):
    """
        생년월일 유효성 검사

        회원가입, 정보 수정시 생년월일에 대한 유효성 검사를 합니다.
        YYYY-MM-DD 형식이어야 합니다.

    Args:
        birth_date: 생년월일

    Returns:
        ''
    """
    try:
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
        if birth_date.strftime("%Y-%m-%d") > date.today().strftime("%Y-%m-%d"):
            raise ValueError
        return ''

    except ValueError:
        return 'INVALID_BIRTH_DATE '


def update_exist_check(data, connection):
    """
        정보 일치 확인

        유저 정보 수정시 바뀐 정보가 있는지를 체크합니다.

    Args:
        data: 유저 정보가 담긴 딕셔너리 객체
        connection: 데이터베이스 연결 객체

    Returns:
        1 혹은 0
    """

    sql = """
        SELECT
            EXISTS
                (
                    SELECT 
                        id
                    FROM
                        users
                    WHERE 
                        email = %(email)s 
                        AND name = %(name)s  
    """

    try:
        if data['birth_date']:
            sql += """
                        AND birth_date = %(birth_date)s
            """

        if data['memo']:
            sql += """
                        AND memo = %(memo)s
            """

        sql += """
                ) 
            AS user_exist;
        """

        with connection.cursor() as cursor:
            cursor.execute(sql, data)
            result = cursor.fetchone()[0]
        return result

    except Exception as e:
        raise e


def update_email_validator(email):
    """
        이메일 유효성 검사

        회원 정보 수정시 이메일에 대한 유효성 검사를 실시합니다.

    Args:
        email: 이메일

    Returns:
        ''
    """

    pattern = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
    regex = re.compile(pattern)
    invalid_result = regex.match(email)
    if not invalid_result:
        return 'EMAIL_IS_NOT_VALID '
    return ''
