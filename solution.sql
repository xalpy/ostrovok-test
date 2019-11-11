SELECT emp1.* FROM employee emp1 WHERE emp1.salary = ( SELECT max(salary) from employee emp2 WHERE emp2.department = emp1.department)
