import random
employee_ids = random.sample(range(200), 100)
insert_statements = [f"INSERT INTO employee_assign_type (employee_id, type_id) VALUES ({emp_id}, 1);" for emp_id in sorted(employee_ids)]
for statement in insert_statements:
    print(statement)
