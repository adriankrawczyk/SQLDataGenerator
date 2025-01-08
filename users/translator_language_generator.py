import random

# List of translator IDs
translator_ids = [1, 8, 11, 12, 16, 19, 21, 22, 24, 25, 27, 29, 30, 32, 33, 
                 38, 40, 41, 43, 45, 47, 48, 49, 50, 53, 54, 55, 56, 58, 60]

# Open the file to write INSERT statements
with open('insert_translator_language.sql', 'w') as f:
    # First ensure each translator has at least one language
    assignments = []
    
    # Assign one random language to each translator
    for translator_id in translator_ids:
        language_id = random.randint(1, 20)
        insert_statement = f"INSERT INTO translator_languages(translator_id, language_id) VALUES ({translator_id}, {language_id});\n"
        assignments.append((translator_id, language_id))
        f.write(insert_statement)
    
    # Generate remaining random assignments
    remaining_assignments = 120 - len(translator_ids)
    for _ in range(remaining_assignments):
        translator_id = random.choice(translator_ids)
        language_id = random.randint(1, 20)
        # Avoid duplicate assignments for same translator-language pair
        while (translator_id, language_id) in assignments:
            translator_id = random.choice(translator_ids)
            language_id = random.randint(1, 20)
        
        insert_statement = f"INSERT INTO translator_languages(translator_id, language_id) VALUES ({translator_id}, {language_id});\n"
        assignments.append((translator_id, language_id))
        f.write(insert_statement)

print(f"Generated {len(assignments)} INSERT statements and saved them to insert_translations.sql")
print(f"Each translator has at least 1 language assigned")