import random
from datetime import datetime

countries = ['Poland', 'Germany', 'France', 'Belgium', 'Netherlands', 'Czech Republic', 'Slovakia', 'Hungary', 'Austria', 'Switzerland', 'Italy', 'Sweden', 'Denmark', 'Finland', 'Norway']
country_ids = ['PL', 'DE', 'FR', 'BE', 'NL', 'CZ', 'SK', 'HU', 'AT', 'CH', 'IT', 'SE', 'DK', 'FI', 'NO']
places_file_path = "./data/places.txt"
men_first_names_path = "./data/men_first_names.txt"
women_first_names_path = "./data/women_first_names.txt"
men_last_names_path = "./data/men_last_names.txt"
women_last_names_path = "./data/women_last_names.txt"
students_sql_path = "insert_students.sql"
    
COUNTRIES_WITH_IDS = {
        'Poland': 1,
        'Germany': 2,
        'France': 3,
        'Belgium': 4,
        'Netherlands': 5,
        'Czech Republic': 6,
        'Slovakia': 7,
        'Hungary': 8,
        'Austria': 9,
        'Switzerland': 10,
        'Italy': 11,
        'Sweden': 12,
        'Denmark': 13,
        'Finland': 14,
        'Norway': 15
    }
CITIES_WITH_IDS = {
    'Warsaw': 1,
    'Kraków': 2,
    'Łódź': 3,
    'Berlin': 4,
    'Munich': 5,
    'Hamburg': 6,
    'Paris': 7,
    'Marseille': 8,
    'Lyon': 9,
    'Brussels': 10,
    'Antwerp': 11,
    'Ghent': 12,
    'Amsterdam': 13,
    'Rotterdam': 14,
    'The Hague': 15,
    'Prague': 16,
    'Brno': 17,
    'Ostrava': 18,
    'Bratislava': 19,
    'Košice': 20,
    'Nitra': 21,
    'Budapest': 22
}

    # Email domain lists
email_domains = [
        "gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com",
        "protonmail.com", "aol.com", "mail.com", "zoho.com", "yandex.com"
    ]

    # Country phone prefixes
country_prefixes = {
        'Poland': '48',
        'Germany': '49',
        'France': '33',
        'Belgium': '32',
        'Netherlands': '31',
        'Czech Republic': '420',
        'Slovakia': '421',
        'Hungary': '36',
        'Austria': '43',
        'Switzerland': '41',
        'Italy': '39',
        'Sweden': '46',
        'Denmark': '45',
        'Finland': '358',
        'Norway': '47'
    }

countries = {}
with open(places_file_path, "r", encoding="utf-8") as places_file:
    for line in places_file:
        country_name, city_name, street, zip_code = line.strip().split(";")
        if country_name not in countries:
            countries[country_name] = []
        countries[country_name].append((city_name, street, zip_code))

def load_names(file_path):
    names = {}
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            country_name, name = line.strip().split(";")
            if country_name not in names:
                names[country_name] = []
            names[country_name].append(name)
    return names

def generate_email(first_name, last_name):
    email_formats = [
        f"{first_name.lower()}.{last_name.lower()}",
        f"{first_name.lower()}{last_name.lower()}",
        f"{first_name[0].lower()}{last_name.lower()}",
        f"{last_name.lower()}{first_name[0].lower()}",
        f"{first_name.lower()}{random.randint(1, 999)}",
        f"{first_name.lower()}{last_name.lower()}{random.randint(1, 99)}"
    ]
        
    email_prefix = random.choice(email_formats)
    domain = random.choice(email_domains)
    return f"{email_prefix}@{domain}"

def generate_phone(country_name):
    prefix = country_prefixes.get(country_name, '48')  # Default to Poland if country not found
        # Generate exactly 9 digits
    number = ''.join([str(random.randint(0, 9)) for _ in range(9)])
        # Format as XXX-XXX-XXX
    return f"+{prefix} {number[:3]}-{number[3:6]}-{number[6:]}"

men_first_names = load_names(men_first_names_path)
women_first_names = load_names(women_first_names_path)
men_last_names = load_names(men_last_names_path)
women_last_names = load_names(women_last_names_path)

def insert_countries():
    with open("insert_countries.sql", "w", encoding="utf-8") as file:
        for country_id, country in zip(country_ids, countries):
            file.write(f"INSERT INTO countries (name) VALUES ('{country}');\n")

def insert_cities():
    city_file_path = "./data/places.txt"
    cities_sql_path = "insert_cities.sql"
    
    # Lista krajów z przypisanymi indeksami (1-based index)
    countries = [
        "Poland", "Germany", "France", "Belgium", "Netherlands",
        "Czech Republic", "Slovakia", "Hungary", "Austria", "Switzerland",
        "Italy", "Sweden", "Denmark", "Finland", "Norway"
    ]
    
    unique_cities = set()
    
    with open(city_file_path, "r", encoding="utf-8") as places_file, open(cities_sql_path, "w", encoding="utf-8") as cities_file:
        cities_file.write("-- SQL script to insert unique cities into the 'cities' table\n\n")
        
        for line in places_file:
            country_name, city_name, _, _ = line.strip().split(";")
            
            if country_name in countries:
                country_id = countries.index(country_name) + 1  # Indeksowanie od 1
                entry_key = (country_id, city_name)
                
                if entry_key not in unique_cities:
                    unique_cities.add(entry_key)
                    cities_file.write(f"INSERT INTO cities (country_id, name) VALUES ({country_id}, '{city_name}');\n")





def generate_students():
    with open(students_sql_path, "w", encoding="utf-8") as students_file:
        students_file.write("-- SQL script to insert students into the 'students' table\n")
        students_file.write(f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        student_id = 1

        for country_name, places in countries.items():
            country_id = COUNTRIES_WITH_IDS.get(country_name)
            if country_id is None:
                continue  # Skip if the country is not in the predefined list
            
            # Skip if names are unavailable for this country
            if (
                country_name not in men_first_names or 
                country_name not in women_first_names or 
                country_name not in men_last_names or 
                country_name not in women_last_names
            ):
                continue

            for city_name, street, zip_code in places:
                city_id = CITIES_WITH_IDS.get(city_name)
                if city_id is None:
                    continue  # Skip if the city is not in the predefined list

                # Generate a random number of students for this street
                num_students = random.randint(1, 8)
                
                for _ in range(num_students):
                    gender = random.choice(["male", "female"])
                    if gender == "male":
                        first_name = random.choice(men_first_names[country_name])
                        last_name = random.choice(men_last_names[country_name])
                    else:
                        first_name = random.choice(women_first_names[country_name])
                        last_name = random.choice(women_last_names[country_name])

                    email = generate_email(first_name, last_name)
                    phone = generate_phone(country_name)

                    # Escape special characters in SQL
                    street_escaped = street.replace("'", "''")
                    city_name_escaped = city_name.replace("'", "''")
                    first_name_escaped = first_name.replace("'", "''")
                    last_name_escaped = last_name.replace("'", "''")

                    # Write the INSERT statement
                    students_file.write(
                        f"INSERT INTO students (street, zip, city_id, first_name, last_name, email, phone) "
                        f"VALUES ('{street_escaped}', '{zip_code}', {city_id}, '{first_name_escaped}', "
                        f"'{last_name_escaped}', '{email}', '{phone}');\n"
                    )
                    student_id += 1


def generate_employees():
    employee_count = 200
    with open("insert_employees.sql", "w", encoding="utf-8") as employees_file:
        employees_file.write("-- SQL script to insert employees into the 'employee' table\n")
        employees_file.write(f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Filter countries that have names data
        valid_countries = [
            country for country in countries
            if country in men_first_names and country in women_first_names and
            country in men_last_names and country in women_last_names
        ]

        if not valid_countries:
            raise ValueError("No countries with complete name data found")

        for employee_id in range(1, employee_count):
            country = random.choice(valid_countries)
            gender = random.choice(["male", "female"])
            
            if gender == "male":
                first_name = random.choice(men_first_names[country])
                last_name = random.choice(men_last_names[country])
            else:
                first_name = random.choice(women_first_names[country])
                last_name = random.choice(women_last_names[country])

            email = generate_email(first_name, last_name)
            phone = generate_phone(country)
            is_active = random.choice([0, 1])

            # Escape special characters
            first_name = first_name.replace("'", "''")
            last_name = last_name.replace("'", "''")

            employees_file.write(
                f"INSERT INTO employee ( first_name, last_name, email, phone, is_active) "
                f"VALUES ( '{first_name}', '{last_name}', '{email}', '{phone}', {is_active});\n"
            )


# 206 students, 199 employees
generate_students()