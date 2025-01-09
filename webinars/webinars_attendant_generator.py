import random

# Keep track of unique combinations to avoid duplicates
attendances = set()

# Open file to write INSERT statements
with open('insert_webinar_attendant.sql', 'w') as f:
    # Generate 10,000 unique attendances
    while len(attendances) < 10000:
        student_id = random.randint(1, 934)
        webinar_id = random.randint(1, 100)
        
        # Only add if this combination doesn't exist yet
        combination = (student_id, webinar_id)
        if combination not in attendances:
            attendances.add(combination)
            insert_statement = f"INSERT INTO webinar_attendant (student_id, webinar_id) VALUES ({student_id}, {webinar_id});\n"
            f.write(insert_statement)

print(f"Generated {len(attendances)} unique webinar attendances and saved them to insert_webinar_attendant.sql")