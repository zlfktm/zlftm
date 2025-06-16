-- PM 직책을 가진 모든 직원의 연봉을 10% 인상한 후 그 결과를 확인
update employees set salary = salary * 1.1 where position = 'PM';
select * from employees where position = 'PM';