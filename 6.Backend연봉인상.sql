-- Backend 직책을 가진 모든 직원의 연봉을 5% 인상
update employees set salary = salary * 1.05 where position = 'Backend';