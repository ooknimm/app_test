from flask import jsonify

from flask_request_validator.exceptions import InvalidRequestError
from flask_request_validator.error_formatter import demo_error_formatter

from .custom_exceptions import CustomException


def error_handle(app):
    """
        에러 메시지 전달을 관리합니다.
        flask의 errorhandler 데코레이터를 사용합니다.

    Args:
        app: Flask 객체

    """

    @app.errorhandler(Exception)
    def handle_internal_server_error(e):
        return jsonify({'message': format(e)}), 500

    @app.errorhandler(KeyError)
    def handle_key_error(e):
        return jsonify({'message': 'INVALID_KEY ' + format(e)}), 400

    @app.errorhandler(InvalidRequestError)
    def handle_invalid_request_error(e):
        return jsonify({'message': demo_error_formatter(e)}), 400

    @app.errorhandler(CustomException)
    def handle_custom_exception(e):
        """
            커스텀 에러의 메시지 전달을 관리합니다.
        """

        return jsonify({'message': format(e)}), e.status_code

