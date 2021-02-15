DROP DATABASE IF EXISTS apptest_v2;
CREATE DATABASE apptest_v2;
USE apptest_v2;

CREATE TABLE permission_types (
	id INT NOT NULL
    , permission_type VARCHAR(20) NOT NULL COMMENT '권한 종류'
    , PRIMARY KEY(id)
) COMMENT '권한 관리 테이블';

CREATE TABLE accounts (
	id INT NOT NULL AUTO_INCREMENT
    , login_id VARCHAR(30) NOT NULL COMMENT '아이디'
    , password VARCHAR(80) NOT NULL COMMENT '비밀번호'
    , permission_type_id INT NOT NULL COMMENT '권한 타입 아이디'
    , created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일'
    , updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일'
    , is_deleted INT NOT NULL DEFAULT 0 COMMENT '삭제 여부'
    , PRIMARY KEY(id)
    , CONSTRAINT FK_accounts_permission_type_id_permission_types_id
		FOREIGN KEY (permission_type_id) REFERENCES permission_types (id)
		ON DELETE RESTRICT ON UPDATE RESTRICT
) COMMENT '어카운트 정보 테이블';
    
    
CREATE TABLE users (
	account_id INT NOT NULL COMMENT '어카운트 아이디'
    , name VARCHAR(30) NOT NULL COMMENT '성명'
    , email VARCHAR(411) NOT NULL COMMENT '이메일'
    , birth_date DATE NULL COMMENT '생년월일'
    , memo TEXT NULL COMMENT '회원 관리 메모'
    , created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일'
    , updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일'
    , is_deleted INT NOT NULL DEFAULT 0 COMMENT '삭제 여부'
    , PRIMARY KEY (account_id)
    , CONSTRAINT FK_users_accunts_id_accounts_id
		FOREIGN KEY (account_id) REFERENCES accounts (id)
		ON DELETE RESTRICT ON UPDATE RESTRICT
) COMMENT '유저 정보 테이블';

CREATE TABLE admins (
	account_id INT NOT NULL COMMENT '어카운트 아이디'
    , name VARCHAR(30) NOT NULL COMMENT '성명'
    , memo TEXT NULL COMMENT '회원 관리 메모'
    , created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성일'
    , updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정일'
    , is_deleted INT NOT NULL DEFAULT 0 COMMENT '삭제 여부'
    , PRIMARY KEY (account_id)
    , CONSTRAINT FK_admins_accunts_id_accounts_id
		FOREIGN KEY (account_id) REFERENCES accounts (id)
		ON DELETE RESTRICT ON UPDATE RESTRICT
) COMMENT '어드민 정보 테이블';


INSERT INTO permission_types (
	id
    , permission_type
) VALUES (
	1
    , 'admin'
);

INSERT INTO permission_types (
	id
    , permission_type
) VALUES (
	2
    , 'user'
);


delimiter $$
drop procedure if exists account_data $$
create procedure account_data()
begin
	declare i int default 1;
    while i < 30 DO
		INSERT INTO accounts (
			login_id, password, permission_type_id
		) VALUES (
			concat('testuser', i), '1q2w3e', 2
		);
		set i = i + 1;
	end while;
end $$ 
call account_data(); $$ 


delimiter $$
drop procedure if exists user_data $$
create procedure user_data()
begin
	declare i int default 1;
    while i < 30 DO
		INSERT INTO users (
			login_id, password, name, email, birth_date, memo
		) VALUES (
			concat('testuser', i), '1q2w3e', concat('유저', i), concat('testuser', i, '@naver.com'), '2009-01-01', concat(i, '번째 테스트 유저입니다.')
		);
		set i = i + 1;
	end while;
end $$ 
call user_data(); $$ 
