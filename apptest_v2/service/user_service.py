import bcrypt
import jwt

from model import UserDao
from utils.custom_exceptions import UserAlreadyExist, UserDoesNotExist, LoginException, PutUserInformationError
from utils.enums import PermissionTypeEnum


class UserService:
    """
        유저앱 service
    """

    def __init__(self, config):
        self.config = config
        self.user_dao = UserDao()

    def sign_up_logic(self, data, connection):
        """
            회원가입 로직

            login_id, email의 중복 검사를 실시
            bcrypt로 비밀번호 암호화
            account 먼저 생성하고 user를 생성

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        login_id_check = self.user_dao.login_id_duplicate_check(data['login_id'], connection)
        email_check = self.user_dao.email_duplicate_check(data['email'], connection)

        if login_id_check or email_check:
            raise UserAlreadyExist(
                ', '.join((
                    login_id_check * ' login_id' +
                    email_check * ' email'
                ).split()) + ' ALREADY EXISTS'
            )

        data['permission_type_id'] = PermissionTypeEnum.user.value
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        account_id = self.user_dao.create_account(data, connection)

        data['account_id'] = account_id
        self.user_dao.create_user(data, connection)

    def admin_sign_up_logic(self, data, connection):
        """
            어드민 가입 로직

            login_id 중복 검사 실시
            bcrypt로 비밀번호 암호화
            account를 먼저 생성하고 admin 생성

        Args:
            data: 어드민 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        login_id_check = self.user_dao.login_id_duplicate_check(data['login_id'], connection)

        if login_id_check:
            raise UserAlreadyExist('login_id ALREADY EXISTS')

        data['permission_type_id'] = PermissionTypeEnum.admin.value
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        account_id = self.user_dao.create_account(data, connection)

        data['account_id'] = account_id
        self.user_dao.create_admin(data, connection)

    def token_generator(self, user):
        """
            토큰 발행 함수

        Args:
            user: 유저 정보

        Returns:
            token
        """

        payload = {
            'account_id': user['id'],
            'permission_type_id': user['permission_type_id']
        }

        token = jwt.encode(
            payload,
            self.config['JWT_SECRET_KEY'],
            algorithm=self.config['JWT_ALGORITHM']
        )

        return token

    def login_logic(self, data, connection):
        """
            로그인 로직

            비밀번호 일치 여부를 검사
            일치하면 토큰 전달

        Args:
            data:
            connection:

        Returns:
            token
        """

        user = self.user_dao.get_login_user_information(data['login_id'], connection)
        if not user:
            raise UserDoesNotExist('USER_DOES_NOT_EXIST')

        if not bcrypt.checkpw(data['password'].encode('utf-8'), user['password'].encode('utf-8')):
            raise LoginException('INVALID_PASSWORD')

        token = self.token_generator(user)

        return token

    def get_user_list_logic(self, data, connection):
        """
            유저 목록 조회 로직

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            [user 객체]
        """

        return self.user_dao.get_user_list(data, connection)

    def get_user_information_logic(self, data, connection):
        """
            유저 상세 정보 조회 로직

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            user 객체
        """

        return self.user_dao.get_user_information(data, connection)

    def put_user_information_logic(self, data, connection):
        """
            유저 정보 수정 로직

            유저 정보가 동일한지 체크
            이메일 중복 검사를 실시

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        update_check = self.user_dao.update_exist_check(data, connection)
        if update_check:
            return

        if data['permission_type_id'] == PermissionTypeEnum.user.value:
            email_check = self.user_dao.put_email_duplicate_check(data, connection)
            if email_check:
                raise PutUserInformationError('EMAIL_ALREADY_EXIST')

        self.user_dao.put_user_information(data, connection)

    def delete_user_logic(self, data, connection):
        """
            유저 삭제 로직

        Args:
            data: 유저 정보
            connection: 데이터베이스 연결 객체

        Returns:
            None
        """

        account_check = self.user_dao.account_exist_check(data, connection)
        if data['permission_type_id'] == PermissionTypeEnum.admin.value:
            any_check = self.user_dao.admin_exist_check(data, connection)
        elif data['permission_type_id'] == PermissionTypeEnum.user.value:
            any_check = self.user_dao.user_exist_check(data, connection)

        if not account_check or not any_check:
            raise UserDoesNotExist('USER_DOES_NOT_EXIST')

        self.user_dao.delete_user(data, connection)
