from functools import wraps

import jwt

from flask import request, current_app, g, jsonify


def login_decorator(func):
    """
        로그인 데코레이터

        로그인 확인 작업을 합니다.
        g객체를 활용해서 account_id와 permission_type_id를 전달합니다.

    Args:
        func: 타겟 함수

    Returns:
        타겟 함수
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:

            token = request.headers.get('Authorization')

            user = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=current_app.config['JWT_ALGORITHM']
            )

            g.account_id = user['account_id']
            g.permission_type_id = user['permission_type_id']

        except jwt.exceptions.InvalidTokenError:
            return jsonify({'message': 'INVALID_USER'}), 401

        return func(*args, **kwargs)
    return wrapper
