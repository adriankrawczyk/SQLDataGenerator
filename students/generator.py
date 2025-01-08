countries = ['Poland', 'Germany', 'France', 'Belgium', 'Netherlands', 'Czech Republic', 'Slovakia', 'Hungary', 'Austria', 'Switzerland', 'Italy', 'Sweden', 'Denmark', 'Finland', 'Norway']
country_ids = ['PL', 'DE', 'FR', 'BE', 'NL', 'CZ', 'SK', 'HU', 'AT', 'CH', 'IT', 'SE', 'DK', 'FI', 'NO']


def insert_countries():
    with open("insert_countries.sql", "w", encoding="utf-8") as file:
        for country_id, country in zip(country_ids, countries):
            file.write(f"INSERT INTO countries (country_id, name) VALUES ('{country_id}', '{country}');\n")

def insert_cities():
    city_file_path = "./data/places.txt"
    cities_sql_path = "insert_cities.sql"
    unique_entries = set()
    with open(city_file_path, "r", encoding="utf-8") as places_file, open(cities_sql_path, "w", encoding="utf-8") as cities_file:
        cities_file.write("-- SQL script to insert cities into the 'cities' table\n\n")
        city_id = 1
        for line in places_file:
            country_name, city_name, street = line.strip().split(";")
            entry_key = (country_name, city_name, street)
            if entry_key not in unique_entries and country_name in countries:
                unique_entries.add(entry_key)
                country_id = country_ids[countries.index(country_name)]
                cities_file.write(f"INSERT INTO cities (city_id, country_id, name) VALUES ({city_id}, '{country_id}', '{city_name} ({street})');\n")
                city_id += 1
                
insert_cities()