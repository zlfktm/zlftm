-- 모든 직원을 position 별로 그룹화하여 각 직책의 평균 연봉을 계산
select position, avg(salary) as average_salary from employees group by position;