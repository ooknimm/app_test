import re
from datetime import datetime, date

from flask_request_validator import AbstractRule
from flask_request_validator.exceptions import RuleError


class LoginIdRule(AbstractRule):
    def validate(self, value):
        pattern = '^[a-z0-9]{6,30}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        if not result:
            raise RuleError('INVALID_ID')
        return value


class NameRule(AbstractRule):
    def validate(self, value):
        pattern = '^[가-힣]{2,30}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        if not result:
            raise RuleError('INVALID_NAME')
        return value


class EmailRule(AbstractRule):
    def validate(self, value):
        pattern = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        if not result:
            raise RuleError('INVALID_EMAIL')
        return value


class PutEmailRule(AbstractRule):
    def validate(self, value):
        if value == 'None':
            return None

        pattern = '^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
        regex = re.compile(pattern)
        result = regex.match(value)
        if not result:
            raise RuleError('INVALID_EMAIL')
        return value


class PasswordRule(AbstractRule):
    """
        비밀번호 규칙

        6~20글자의 영어 대소문자, 숫자
    """

    def validate(self, value):
        pattern = '^[a-zA-Z0-9]{6,20}$'
        regex = re.compile(pattern)
        result = regex.match(value)
        if not result:
            raise RuleError('INVALID_PASSWORD')
        return value


class BirthDateRule(AbstractRule):
    """
        생년월일 규칙

        YYYY-MM-DD 형식의 날짜
    """

    def validate(self, value):
        if value == 'None':
            return None
        birth_date = datetime.strptime(value, "%Y-%m-%d")
        if birth_date.strftime("%Y-%m-%d") > date.today().strftime("%Y-%m-%d"):
            raise RuleError('INVALID_BIRTH_DATE')
        return value


class MemoRule(AbstractRule):
    """
        메모 규칙

        flask_request_validator의 오류로 인해 작성
        기본 값이 None일 때 발생하는 오류
    """

    def validate(self, value):
        if value == 'None':
            return None
        return value


class ZeroRule(AbstractRule):
    """
        0 규칙

        flask_request_validator의 오류로 인해 작성
        기본 값이 0일 때 발생하는 오류
    """

    def validate(self, value):
        if value == '0':
            return 0
        return int(value)
