import re

# Read employee IDs from the insert_employee_assign_type.sql file
employee_ids = []

# Open and read the insert_employee_assign_type.sql file
with open("./users/insert_employee_assign_type.sql", "r") as file:
    # Use regex to find all employee_id values in the INSERT statements
    for line in file:
        match = re.search(r"VALUES \((\d+), 1\);", line)
        if match:
            employee_ids.append(int(match.group(1)))

# Create INSERT INTO statements for the tutors table
tutor_statements = [f"INSERT INTO tutors (tutor_id) VALUES ({emp_id});" for emp_id in sorted(employee_ids)]

# Write the tutor_statements to the insert_tutors.sql file
with open("insert_tutors.sql", "w") as file:
    for statement in tutor_statements:
        file.write(statement + "\n")

print("SQL file created: insert_tutors.sql")
