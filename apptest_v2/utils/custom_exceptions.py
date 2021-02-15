class CustomException(Exception):
    """
        커스텀 에러

        status_code와 message를 관리합니다.
        모든 커스텀 에러는 이 클래스를 상속받습니다.
        이 클래스를 상속받음으로 인해 error_handler의 handle_custom_exception 함수 하나로 에러 메시지 전달이 관리가 됩니다.
        상속 받는 자식 클래스들은 super().__init__을 사용해서 status_code와 message를 오버라이딩합니다.
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


class UserAlreadyExist(CustomException):
    """
        중복 유저 에러
    """

    def __init__(self, message):
        status_code = 400
        message = message
        super().__init__(status_code, message)


class DatabaseException(CustomException):
    """
        데이터베이스 에러
    """

    def __init__(self, message):
        status_code = 500
        message = message
        super().__init__(status_code, message)


class UserDoesNotExist(CustomException):
    """
        해당 유저 없음
    """

    def __init__(self, message):
        status_code = 404
        message = message
        super().__init__(status_code, message)


class LoginException(CustomException):
    """
        로그인 실패 에러
    """

    def __init__(self, message):
        status_code = 401
        message = message
        super().__init__(status_code, message)


class PermissionDeniedError(CustomException):
    """
        권한이 아님
    """

    def __init__(self, message):
        status_code = 403
        message = message
        super().__init__(status_code, message)


class PutUserInformationError(CustomException):
    """
        정보 수정 실패 에러
    """

    def __init__(self, message):
        status_code = 400
        message = message
        super().__init__(status_code, message)
