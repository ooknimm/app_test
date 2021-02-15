DROP DATABASE IF EXISTS apptest_v1;
create database apptest_v1;
use apptest_v1;

CREATE TABLE users (
	id int NOT NULL AUTO_INCREMENT
    , login_id varchar(30) NOT NULL COMMENT '유저 아이디'
    , password varchar(80) NOT NULL COMMENT '비밀번호'
    , `name` varchar(30) NOT NULL COMMENT '성명'
    , email varchar(411) NOT NULL COMMENT '이메일'
    , birth_date date NULL COMMENT '생년월일'
    , memo varchar(500) NULL COMMENT '회원 관리 메모'
    , PRIMARY KEY(id)
) COMMENT '유저 관리 테이블';


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