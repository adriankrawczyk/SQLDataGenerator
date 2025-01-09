import random

# Parse the existing translator-language assignments
translator_languages = {}

# Read the file and parse assignments
with open('./users/insert_translator_language.sql', 'r') as f:
    for line in f:
        if line.strip():
            # Extract translator_id and language_id using string manipulation
            parts = line.split('VALUES (')[1].strip(');\n').split(', ')
            translator_id = int(parts[0])
            language_id = int(parts[1])
            
            # Add to dictionary of translator languages
            if translator_id not in translator_languages:
                translator_languages[translator_id] = []
            translator_languages[translator_id].append(language_id)

# Generate 1000 random translations
with open('insert_translations.sql', 'w') as f:
    for i in range(1000):
        # Randomly select a translator
        translator_id = random.choice(list(translator_languages.keys()))
        # Randomly select one of their known languages
        language_id = random.choice(translator_languages[translator_id])
        
        insert_statement = f"INSERT INTO translations(translator_id, language_id) VALUES ({translator_id}, {language_id});\n"
        f.write(insert_statement)

print("Generated 1000 INSERT statements and saved them to insert_translations.sql")
print(f"Each translation uses a random translator with one of their known languages")