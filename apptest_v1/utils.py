from datetime import datetime, timedelta
from functools import wraps

import jwt

from flask import current_app, request, g, jsonify


def token_generator(id):
    """
        토큰 발행 함수

    Args:
        id: int
    Returns:
        token
    """

    payload = {
        'id': id,
        'exp': datetime.utcnow() + timedelta(hours=48)
    }

    token = jwt.encode(
        payload,
        current_app.config['JWT_SECRET_KEY'],
        algorithm=current_app.config['JWT_ALGORITHM']
    )

    return token


def login_decorator(func):
    """
        로그인 데코레이터

        로그인 확인 작업을 수행합니다.

    Args:
        func: 타겟 함수

    Returns:
        타겟 함수
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers.get('Authorization')
            payload = jwt.decode(
                token,
                current_app.config['JWT_SECRET_KEY'],
                algorithms=current_app.config['JWT_ALGORITHM']
            )

            g.id = payload['id']

        except jwt.InvalidTokenError:
            return jsonify({'message': 'INVALID_USER'}), 401

        return func(*args, **kwargs)
    return wrapper
