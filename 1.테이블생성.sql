-- employees 테이블을 생성해주세요
-- 속성명 id의 자료형은 INT입니다. 추가로 자동으로 1씩 증가하도록 설정하고 기본키로 지정합니다.
-- 속성명 name의 자료형은 VARCHAR(100)입니다.
-- 속성명 position의 자료형은 VARCHAR(100)입니다.
-- 속성명 salary의 자료형은 DECIMAL(10, 2)입니다.
create table employees (
id int auto_increment primary key,
name varchar(100),
position varchar(100),
salary decimal(10, 2)
);