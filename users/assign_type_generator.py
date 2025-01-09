import random

# Generate 100 unique random employee_ids between 0 and 199
employee_ids = random.sample(range(200), 100)

# Create INSERT INTO statements
insert_statements = [f"INSERT INTO employee_assign_type (employee_id, type_id) VALUES ({emp_id}, 1);" for emp_id in sorted(employee_ids)]

# Print the statements
for statement in insert_statements:
    print(statement)
