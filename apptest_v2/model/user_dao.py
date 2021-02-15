import pymysql

from utils.custom_exceptions import DatabaseException
from utils.enums import PermissionTypeEnum


class UserDao:
    """
        유저앱 Dao
    """

    def login_id_duplicate_check(self, login_id, connection):
        """
            로그인 아이디 중복 체크

        Args:
            login_id: 로그인 아이디
            connection: 데이터베이스 연결 객체

        Returns:
            0 혹은 1
        """

        sql = """
            SELECT 
                EXISTS
                    (
                        SELECT 
                            id
                        FROM
                            accounts
                        WHERE
                            login_id = %s
                            AND is_deleted = 0
                    )
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, login_id)
                result = cursor.fetchone()[0]
                return result

        except Exception as e:
            raise e

    def email_duplicate_check(self, email, connection):
        """
            이메일 중복 체크

        Args:
            email: 이메일
            connection: 데이터베이스 중복 체크

        Returns:
            0 혹은 1
        """

        sql = """
            SELECT 
                EXISTS
                    (
                        SELECT 
                            account_id
                        FROM
                            users
                        WHERE
                            email = %s
                            AND is_deleted = 0
                    )
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, email)
                result = cursor.fetchone()[0]
                return result
        except Exception as e:
            raise e

    def create_account(self, data, connection):
        """
            account 생성

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            account_id
        """

        sql = """
            INSERT INTO accounts (
                login_id
                , password
                , permission_type_id
            ) VALUES (
                %(login_id)s
                , %(password)s
                , %(permission_type_id)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DatabaseException('ACCOUNT_CREATE_FAIL')
                return cursor.lastrowid

        except Exception as e:
            raise e

    def create_user(self, data, connection):
        """
            유저 생성

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        sql = """
            INSERT INTO users (
                account_id
                , name
                , email
                , birth_date
                , memo
            ) VALUES (
                %(account_id)s
                , %(name)s
                , %(email)s
                , %(birth_date)s
                , %(memo)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DatabaseException('USER_CREATE_FAIL')

        except Exception as e:
            raise e

    def create_admin(self, data, connection):
        """
            어드민 생성

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        sql = """
            INSERT INTO admins (
                account_id
                , name
                , memo
            ) VALUES (
                %(account_id)s
                , %(name)s
                , %(memo)s
            );
        """

        try:
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    raise DatabaseException('ADMIN_CREATE_FAIL')

        except Exception as e:
            raise e

    def get_login_user_information(self, login_id, connection):
        """
            유저 id, password, permission_type_id 조호;

        Args:
            login_id: 로그인 아이디
            connection: 데이터베이스 연결 객체

        Returns:
            유저 정보 객체
        """

        sql = """
            SELECT
                id
                , password
                , permission_type_id
            FROM
                accounts
            WHERE
                login_id = %s
                AND is_deleted = 0;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, login_id)
                result = cursor.fetchone()
                return result

        except Exception as e:
            raise e

    def get_user_list(self, data, connection):
        """
            유저 목록 조회

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            [유저객체]
        """

        user_sql = """
            SELECT
                permission_types.permission_type AS permission_type
                , accounts.login_id AS login_id
                , users.name AS name
                , users.email AS email
                , users.birth_date AS birth_date
                , users.memo AS memo
                , users.created_at AS created_at
            FROM
                users
                INNER JOIN accounts
                    ON accounts.id = users.account_id
                INNER JOIN permission_types
                    ON accounts.permission_type_id = permission_types.id
            WHERE
                accounts.is_deleted = 0
                AND users.is_deleted = 0
            LIMIT 
                %(offset)s, %(limit)s;
        """

        admin_sql = """
            SELECT
                permission_types.permission_type AS permission_type
                , accounts.login_id AS login_id
                , admins.name AS name
                , admins.memo AS memo
                , admins.created_at AS created_at
            FROM
                accounts
                INNER JOIN admins
                    ON accounts.id = admins.account_id
                INNER JOIN permission_types
                    ON accounts.permission_type_id = permission_types.id
            WHERE
                accounts.is_deleted = 0
                AND admins.is_deleted = 0
            LIMIT 
                %(offset)s, %(limit)s;
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                if data['permission'] == PermissionTypeEnum.admin.name:
                    cursor.execute(admin_sql, data)
                elif data['permission'] == PermissionTypeEnum.user.name:
                    cursor.execute(user_sql, data)
                result = cursor.fetchall()
                return result

        except Exception as e:
            raise e

    def get_user_information(self, data, connection):
        """
            유저 정보 조회

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            유저 객체
        """

        user_sql = """
            SELECT
                permission_types.permission_type AS permission_type
                , accounts.login_id AS login_id
                , users.name AS name
                , users.email AS email
                , users.birth_date AS birth_date
                , users.memo AS memo
                , users.created_at AS created_at
            FROM
                accounts
                INNER JOIN users
                    ON accounts.id = users.account_id
                INNER JOIN permission_types
                    ON accounts.permission_type_id = permission_types.id
            WHERE
                accounts.id = %(account_id)s
                AND accounts.is_deleted = 0
                AND users.is_deleted = 0
        """

        admin_sql = """
            SELECT
                permission_types.permission_type AS permission_type
                , accounts.login_id AS login_id
                , admins.name AS name
                , admins.memo AS memo
                , admins.created_at AS created_at
            FROM
                accounts
                INNER JOIN admins
                    ON accounts.id = admins.account_id
                INNER JOIN permission_types
                    ON accounts.permission_type_id = permission_types.id
            WHERE
                accounts.id = %(account_id)s
                AND accounts.is_deleted = 0
                AND admins.is_deleted = 0
        """

        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                if data['permission_type_id'] == PermissionTypeEnum.admin.value:
                    cursor.execute(admin_sql, data)
                elif data['permission_type_id'] == PermissionTypeEnum.user.value:
                    cursor.execute(user_sql, data)
                result = cursor.fetchone()
                return result

        except Exception as e:
            raise e

    def update_exist_check(self, data, connection):
        """
            기존 유저 정보와 업데이트 정보가 동일한지 검사

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            0 혹은 1
        """

        user_sql = """
            SELECT
                EXISTS
                    (
                        SELECT
                            account_id
                        FROM
                            users
                        WHERE
                            account_id = %(account_id)s
                            AND name = %(name)s
                            AND email = %(email)s
        """

        admin_sql = """
            SELECT
                EXISTS
                    (
                        SELECT
                            account_id
                        FROM
                            admins
                        WHERE
                            account_id = %(account_id)s
                            AND name = %(name)s
        """

        try:
            with connection.cursor() as cursor:
                if data['permission_type_id'] == PermissionTypeEnum.user.value:
                    if data['birth_date']:
                        user_sql += """
                            AND birth_date = %(birth_date)s                        
                        """

                    if data['memo']:
                        user_sql += """
                            AND memo = %(memo)s                        
                        """

                    user_sql += """
                    )
                AS user_exist;                    
                    """
                    cursor.execute(user_sql, data)

                elif data['permission_type_id'] == PermissionTypeEnum.admin.value:
                    if data['memo']:
                        admin_sql += """
                            AND memo = %(memo)s                        
                        """
                    admin_sql += """
                    )
                AS user_exist;                    
                    """
                    cursor.execute(admin_sql, data)

                result = cursor.fetchone()[0]
                return result

        except Exception as e:
            raise e

    def put_email_duplicate_check(self, data, connection):
        """
            이메일 중복 검사

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            0 혹은 1
        """

        sql = """
            SELECT 
                EXISTS
                    (
                        SELECT 
                            account_id
                        FROM
                            users
                        WHERE
                            account_id != %(account_id)s
                            AND email = %(email)s
                            AND is_deleted = 0
                    )
                AS user_exist;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result
        except Exception as e:
            raise e

    def put_user_information(self, data, connection):
        """
            유저 정보 수정

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        user_sql = """
            UPDATE
                users
            SET
                name = %(name)s
                , email = %(email)s
                , birth_date = %(birth_date)s 
                , memo = %(memo)s
            WHERE
                account_id = %(account_id)s
        """

        admin_sql = """
            UPDATE
                admins
            SET
                name = %(name)s
                , memo = %(memo)s
            WHERE
                account_id = %(account_id)s
        """

        try:
            with connection.cursor() as cursor:
                if data['permission_type_id'] == PermissionTypeEnum.user.value:
                    result = cursor.execute(user_sql, data)
                elif data['permission_type_id'] == PermissionTypeEnum.admin.value:
                    result = cursor.execute(admin_sql, data)

                if not result:
                    raise DatabaseException('USER_INFORMATION_UPDATE_FAIL')

        except Exception as e:
            raise e

    def account_exist_check(self, data, connection):
        """
            account 중복 체크

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            0 혹은 1
        """

        sql = """
            SELECT
                EXISTS
                    (
                        SELECT
                            id
                        FROM
                            accounts
                        WHERE
                            id = %(account_id)s
                            AND is_deleted = 0
                    )
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result

        except Exception as e:
            raise e

    def admin_exist_check(self, data, connection):
        """
            어드민 중복 체크

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            0 혹은 1
        """

        sql = """
            SELECT
                EXISTS
                    (
                        SELECT
                            account_id
                        FROM
                            admins
                        WHERE
                            account_id = %(account_id)s
                            AND is_deleted = 0
                    )
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result

        except Exception as e:
            raise e

    def user_exist_check(self, data, connection):
        """
            유저 중복 체크

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            0 혹은 1
        """

        sql = """
            SELECT
                EXISTS
                    (
                        SELECT
                            account_id
                        FROM
                            users
                        WHERE
                            account_id = %(account_id)s
                            AND is_deleted = 0
                    )
                AS user_exist;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                result = cursor.fetchone()[0]
                return result

        except Exception as e:
            raise e

    def delete_user(self, data, connection):
        """
            유저 삭제

            논리 삭제

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        sql = """
            UPDATE
                accounts
            SET
                is_deleted = 1
            WHERE
                id = %(account_id)s;
        """

        user_sql = """
            UPDATE
                users
            SET
                is_deleted = 1
            WHERE
                account_id = %(account_id)s;
        """

        admin_sql = """
            UPDATE
                admins
            SET
                is_deleted = 1
            WHERE
                account_id = %(account_id)s;
        """

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                if data['permission_type_id'] == PermissionTypeEnum.admin.value:
                    cursor.execute(admin_sql, data)
                elif data['permission_type_id'] == PermissionTypeEnum.user.value:
                    cursor.execute(user_sql, data)

        except Exception as e:
            raise e
