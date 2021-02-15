import traceback

from flask import jsonify, g
from flask.views import MethodView

from flask_request_validator import (
    validate_params,
    Param,
    JSON,
    GET,
    Enum
)

from utils.rules import EmailRule, LoginIdRule, PasswordRule, BirthDateRule, NameRule, MemoRule, ZeroRule, PutEmailRule
from utils.connection import get_connection
from utils.decorator import login_decorator
from utils.enums import PermissionTypeEnum
from utils.custom_exceptions import PermissionDeniedError, PutUserInformationError


class UserSignUpView(MethodView):
    """
        유저 회원가입 뷰
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
        self.database = database

    @validate_params(
        Param('login_id', JSON, str, rules=[LoginIdRule()]),
        Param('password', JSON, str, rules=[PasswordRule()]),
        Param('name', JSON, str, rules=[NameRule()]),
        Param('email', JSON, str, rules=[EmailRule()]),
        Param('birth_date', JSON, str, required=False, rules=[BirthDateRule()]),
        Param('memo', JSON, str, required=False, rules=[MemoRule()])
    )
    def post(self, valid):
        """
            회원가입 (유저)

        Args:
            valid:
                login_id = 영어 소문자, 숫자 6-30글자
                name = 한글 2-30글자
                email = 도메인 규격 준수
                password = 영어 대소문자, 숫자 6-20글자
                birth_date = YYYY-MM-DD (필수아님)
                memo = 제약 없음 (필수아님)

        Returns:
            {'message': 'SUCCESS'}, 200
        """

        connection = None
        try:
            data = valid.get_json()
            connection = get_connection(self.database)
            self.user_service.sign_up_logic(data, connection)
            connection.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            traceback.print_exc()
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()


class AdminSignUpView(MethodView):
    """
        어드민 회원가입 뷰
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
        self.database = database

    @validate_params(
        Param('login_id', JSON, str, rules=[LoginIdRule()]),
        Param('password', JSON, str, rules=[PasswordRule()]),
        Param('name', JSON, str, rules=[NameRule()]),
        Param('memo', JSON, str, required=False, rules=[MemoRule()])
    )
    def post(self, valid):
        """
            회원가입 (어드민)

        Args:
            valid:
                login_id = 영어 소문자, 숫자 6-30글자
                name = 한글 2-30글자
                password = 영어 대소문자, 숫자 6-20글자

        Returns:
            {'message': 'SUCCESS'}, 200
        """

        connection = None
        try:
            data = valid.get_json()
            connection = get_connection(self.database)
            self.user_service.admin_sign_up_logic(data, connection)
            connection.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            traceback.print_exc()
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()


class UserLoginView(MethodView):
    """
        유저 로그인 뷰
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
        self.database = database

    @validate_params(
        Param('login_id', JSON, str, rules=[LoginIdRule()]),
        Param('password', JSON, str, rules=[PasswordRule()])
    )
    def post(self, valid):
        """
            로그인 (어드민, 유저)

        Args:
            valid:
                login_id,
                password

        Returns:
            {'message': 'SUCCESS', 'token': token}, 200
        """

        connection = None
        try:
            data = valid.get_json()
            connection = get_connection(self.database)
            token = self.user_service.login_logic(data, connection)
            return jsonify({'message': 'SUCCESS', 'token': token}), 200

        except Exception as e:
            traceback.print_exc()
            raise e

        finally:
            if connection:
                connection.close()


class UserListView(MethodView):
    """
        유저 목록 조회 뷰
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
        self.database = database

    @login_decorator
    @validate_params(
        Param('permission', GET, str, required=False, default='user', rules=[Enum('user', 'admin')]),
        Param('offset', GET, str, required=False, default='0', rules=[ZeroRule()]),
        Param('limit', GET, int, required=False, default=10)
    )
    def get(self, valid):
        """
            유저 목록 조회

            어드민만 사용 가능
            페이지네이션 구현

        Args:
            valid:
                permission = user 혹은 admin / 기본값 user
                offset = str(라이브러리 기본값 에러로 인해) / 기본값 0
                limit = int / 기본값 10

        Returns:
            {'message': 'SUCCESS', 'data': user_list}, 200
        """

        connection = None
        try:
            permission_type_id = g.permission_type_id

            if permission_type_id != PermissionTypeEnum.admin.value:
                raise PermissionDeniedError('PERMISSION_DENIED')

            data = valid.get_params()
            connection = get_connection(self.database)
            user_list = self.user_service.get_user_list_logic(data, connection)

            return jsonify({'message': 'SUCCESS', 'data': user_list}), 200

        except Exception as e:
            traceback.print_exc()
            raise e

        finally:
            if connection:
                connection.close()


class UserDetailView(MethodView):
    """
        유저 디테일 뷰
    """

    def __init__(self, services, database):
        self.user_service = services.user_service
        self.database = database

    @login_decorator
    def get(self):
        """
            유저 상세 조회

            유저, 어드민 모두 가능

        Returns:
            {'message': 'SUCCESS', 'data': user_info}, 200
        """

        connection = None
        try:
            connection = get_connection(self.database)
            data = {
                'account_id': g.account_id,
                'permission_type_id': g.permission_type_id
            }
            user_info = self.user_service.get_user_information_logic(data, connection)
            return jsonify({'message': 'SUCCESS', 'data': user_info}), 200

        except Exception as e:
            traceback.print_exc()
            raise e

        finally:
            if connection:
                connection.close()

    @login_decorator
    @validate_params(
        Param('name', JSON, str, rules=[NameRule()]),
        Param('email', JSON, str, required=False, rules=[PutEmailRule()]),
        Param('birth_date', JSON, str, required=False, rules=[BirthDateRule()]),
        Param('memo', JSON, str, required=False, rules=[MemoRule()])
    )
    def put(self, valid):
        """
            유저 정보 수정

            유저, 어드민 모두 가능

        Args:
            valid:
                name = 한글 2-30글자
                memo = 제약 없음 (필수아님)
                (유저일시 필수) email = 도메인 규격 준수
                (유저일시 선택) birth_date = YYYY-MM-DD
        Returns:
            {'message': 'SUCCESS'}, 200
        """

        connection = None
        try:
            data = valid.get_json()
            data['account_id'] = g.account_id
            data['permission_type_id'] = g.permission_type_id

            if data['permission_type_id'] == PermissionTypeEnum.user.value and not data['email']:
                raise PutUserInformationError('EMAIL_IS_REQUIRED')

            connection = get_connection(self.database)
            self.user_service.put_user_information_logic(data, connection)
            connection.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            traceback.print_exc()
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()

    @login_decorator
    def delete(self):
        """
            유저, 어드민 삭제

            논리 삭제

        Returns:
            {'message': 'SUCCESS'}, 200
        """

        connection = None
        try:
            data = {
                'account_id': g.account_id,
                'permission_type_id': g.permission_type_id
            }
            connection = get_connection(self.database)
            self.user_service.delete_user_logic(data, connection)
            connection.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            traceback.print_exc()
            if connection:
                connection.rollback()
            raise e

        finally:
            if connection:
                connection.close()
