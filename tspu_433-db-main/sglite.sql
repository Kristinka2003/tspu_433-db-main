SELECT first_name, last_name FROM employees WHERE gender = 'M';
SELECT * FROM employees WHERE hire_date > '1986-01-01';
SELECT last_name, salary FROM employees JOIN salaries ON employees.emp_no = salaries.emp_no ORDER BY salary DESC LIMIT 30;
SELECT gender, COUNT(*) AS employee_count FROM employees GROUP BY gender;
SELECT * FROM employees WHERE first_name LIKE 'S%';
SELECT * FROM employees WHERE emp_no IN (SELECT emp_no FROM salaries WHERE salary > (SELECT 100000 FROM salaries));