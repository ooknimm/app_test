import json
import traceback

from flask import Flask, jsonify, request, g

import bcrypt
import pymysql

from connection import get_connection
from validator import (
                    login_id_validator,
                    name_validator,
                    email_validator,
                    password_validator,
                    update_email_validator,
                    update_exist_check,
                    birth_date_validator
                )
from utils import token_generator, login_decorator


def create_app():
    """
        Flask 앱 생성

    Returns:
        app

    """

    app = Flask(__name__)
    app.debug = True
    app.config.from_pyfile('config.py')
    database = app.config['DB']

    @app.route('/users', methods=['GET'])
    def get_user_list():
        """
            유저 리스트 조회

            전체 유저를 조회합니다.

        Returns:
            {'data': result}, 200
        """

        connection = None
        try:
            connection = get_connection(database)
            sql = """
                SELECT
                    id
                    , login_id
                FROM    
                    users
            """

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()

            return jsonify({'data': result}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({'message': e.__str__()}), 500

        finally:
            connection.close()

    @app.route('/sign-up', methods=['POST'])
    def sign_up():
        """
            회원가입

            필수 항목 : login_id, email, name, password
            선택 항목 : birth_date, memo

        Returns:
            {'message': 'SUCCESS'}, 200
        """

        connection = None
        try:
            data = json.loads(request.data)

            connection = get_connection(database)

            login_id_check = login_id_validator(data['login_id'], connection)
            email_check = email_validator(data['email'], connection)
            name_check = name_validator(data['name'])
            password_check = password_validator(data['password'])
            data['birth_date'] = data.get('birth_date')

            birth_date_check = ''
            if data['birth_date']:
                birth_date_check = birth_date_validator(data['birth_date'])
            data['memo'] = data.get('memo')

            if login_id_check or name_check or email_check or password_check or birth_date_check:
                return jsonify(
                    {
                        'message': ', '.join((
                            login_id_check +
                            name_check +
                            email_check +
                            password_check +
                            birth_date_check).split())
                    }
                ), 400

            data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            sql = """
                INSERT INTO users (
                    login_id
                    , password
                    , name
                    , email
                    , birth_date
                    , memo
                ) VALUES (
                    %(login_id)s
                    , %(password)s
                    , %(name)s
                    , %(email)s
                    , %(birth_date)s
                    , %(memo)s
                );
            """
            with connection.cursor() as cursor:
                result = cursor.execute(sql, data)
                if not result:
                    return jsonify({'message': 'USER_CREATE_FAIL'}), 500

            connection.commit()

            return jsonify({'message': 'SUCCESS'}), 200

        except KeyError:
            return jsonify({'message': 'KEY_ERROR'}), 400

        except Exception as e:
            if connection:
                connection.rollback()
            traceback.print_exc()
            return jsonify({'message': e.__str__()}), 500

        finally:
            if connection:
                connection.close()

    @app.route('/users/<int:user_id>', methods=['GET'])
    def get_user_information(user_id):
        """
            유저 상세 조회

            한 명의 유저에 대한 정보를 조회합니다.
            path parameter를 사용해서 유저 아이디를 받습니다.

        Args:
            user_id: int

        Returns:
            {'data': result}, 200
        """

        connection = None
        try:
            connection = get_connection(database)
            sql = """
                SELECT
                    login_id
                    , name
                    , email
                    , birth_date
                    , memo
                FROM    
                    users
                WHERE
                    id = %s
            """

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(sql, user_id)
                result = cursor.fetchone()
                if not result:
                    return jsonify({'message': 'USER_DOES_NOT_EXISTS'}), 404
                result['birth_date'] = result['birth_date'].strftime('%Y-%m-%d')

            return jsonify({'data': result}), 200

        except Exception as e:
            traceback.print_exc()
            return jsonify({'message': e.__str__()}), 500

        finally:
            if connection:
                connection.close()

    @app.route('/login', methods=['POST'])
    def login():
        """
            유저 로그인

            토큰 방식 로그인입니다.

        Returns:
            {'token': token}, 200
        """

        connection = None
        try:
            data = json.loads(request.data)
            login_id = data['login_id']
            password = data['password']
            connection = get_connection(database)
            sql = """
                SELECT
                    id
                    , login_id
                    , password
                FROM
                    users
                WHERE
                    login_id = %s
            """

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                result = cursor.execute(sql, login_id)
                if not result:
                    return jsonify({'message': 'INVALID_LOGIN_ID'}), 400

                user = cursor.fetchone()
                if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    return jsonify({'message': 'INVALID_PASSWORD'}), 401

                token = token_generator(user['id'])
                return jsonify({'token': token}), 200

        except KeyError:
            return jsonify({'message': 'KEY_ERROR'}), 400

        except Exception as e:
            traceback.print_exc()
            return jsonify({'message': e.__str__()}), 500

        finally:
            if connection:
                connection.close()

    @app.route('/my-page', methods=['PUT'])
    @login_decorator
    def put_user_information():
        """
            유저 정보 수정

            유저 본인의 정보만 수정 가능합니다.

            필수 항목 : email, name
            선택 항목 : memo, birth_date

        Returns:
            {'message': 'SUCCESS'}, 200
        """

        connection = None
        try:
            connection = get_connection(database)
            data = json.loads(request.data)
            data['user_id'] = g.id
            data['memo'] = data.get('memo')
            data['birth_date'] = data.get('birth_date')
            update_check = update_exist_check(data, connection)

            if not update_check:
                name_check = name_validator(data['name'])
                email_check = update_email_validator(data['email'])

                birth_date_check = ''
                if data['birth_date']:
                    birth_date_check = birth_date_validator(data['birth_date'])

                if name_check or email_check or birth_date_check:
                    return jsonify(
                        {
                            'message': ', '.join((
                                name_check +
                                email_check +
                                birth_date_check).split())
                        }
                    ), 400

                sql = """
                    UPDATE 
                        users 
                    SET
                        name = %(name)s
                        , email = %(email)s
                        , birth_date = %(birth_date)s
                        , memo = %(memo)s
                    WHERE
                        id = %(user_id)s;
                """

                with connection.cursor() as cursor:
                    result = cursor.execute(sql, data)
                    if not result:
                        return jsonify({'message': 'USER_INFORMATION_UPDATE_FAIL'}), 500
                    connection.commit()

            return jsonify({'message': 'SUCCESS'}), 200

        except KeyError:
            return jsonify({'message': 'KEY_ERROR'}), 400

        except Exception as e:
            if connection:
                connection.rollback()
            traceback.print_exc()
            return jsonify({'message': e.__str__()}), 500

        finally:
            if connection:
                connection.close()

    @app.route('/my-page', methods=['DELETE'])
    @login_decorator
    def delete_user():
        """
            회원 삭제
            
            유저 본인만 가능합니다.
            물리 삭제입니다.
        
        Returns:
            {'message': 'SUCCESS'}, 200
        """

        connection = None
        try:
            connection = get_connection(database)
            user_id = g.id
            sql = """
                DELETE FROM
                    users
                WHERE
                    id = %s
            """

            with connection.cursor() as cursor:
                result = cursor.execute(sql, user_id)
                if not result:
                    return jsonify({'message': 'USER_DELETE_FAIL'}), 500
            connection.commit()
            return jsonify({'message': 'SUCCESS'}), 200

        except Exception as e:
            if connection:
                connection.rollback()
            traceback.print_exc()
            return jsonify({'message': e.__str__()}), 500

        finally:
            if connection:
                connection.close()

    return app
