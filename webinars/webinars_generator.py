import random
from datetime import datetime, timedelta

def generate_webinars(count=100):
    tutor_ids = [2, 3, 4, 5, 6, 7, 9, 10, 13, 14, 15, 17, 18, 20, 23, 26, 28, 31, 34, 35, 36, 37, 39, 42, 44, 46, 51, 52, 57, 59, 62, 63, 64, 66, 69, 72, 73, 75, 76, 78, 79, 80, 81, 82, 83, 86, 87, 89, 92, 96, 98, 101, 102, 104, 105, 106, 107, 112, 114, 115, 116, 117, 118, 120, 121, 123, 125, 126, 129, 132, 134, 136, 137, 139, 140, 143, 144, 148, 152, 153, 156, 159, 161, 162, 163, 164, 166, 167, 175, 176, 178, 180, 185, 186, 187, 189, 193, 194, 197, 199]

    TOPICS = {
        'Python Programming': [
            'Introduction to Python basics and syntax',
            'Advanced Python concepts and best practices',
            'Building web applications with Django',
            'Data analysis with Pandas and NumPy',
            'Machine Learning with Python'
        ],
        'Data Science': [
            'Statistical analysis fundamentals',
            'Big Data processing techniques',
            'Data visualization masterclass',
            'Predictive modeling essentials',
            'Deep learning fundamentals'
        ],
        'Web Development': [
            'Frontend development with React',
            'Backend development with Node.js',
            'Full-stack web development bootcamp',
            'Modern CSS frameworks and tools',
            'RESTful API design principles'
        ],
        'Cloud Computing': [
            'AWS certification preparation',
            'Cloud architecture fundamentals',
            'DevOps practices and tools',
            'Microservices architecture',
            'Container orchestration with Kubernetes'
        ],
        'Digital Marketing': [
            'Social media marketing strategies',
            'SEO optimization techniques',
            'Content marketing masterclass',
            'Email marketing campaigns',
            'Digital advertising fundamentals'
        ]
    }

    PLATFORMS = [
        'https://zoom.us/j/',
        'https://meet.google.com/',
        'https://teams.microsoft.com/l/meetup-join/',
        'https://webex.com/meet/'
    ]

    def generate_meeting_url():
        platform = random.choice(PLATFORMS)
        meeting_id = ''.join(random.choices('0123456789abcdef', k=12))
        return f"{platform}{meeting_id}"

    def generate_price():
        # Generate prices between $50 and $500
        return round(random.uniform(50, 500), 2)

    def generate_admission_fee():
        # Generate admission fees between $10 and $50
        return round(random.uniform(10, 50), 2)

    def generate_date():
        # Generate dates from today up to 6 months in the future
        start_date = datetime.now()
        end_date = start_date + timedelta(days=180)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + timedelta(days=random_number_of_days)
        return random_date.strftime('%Y-%m-%d')

    # Generate SQL file
    with open('insert_webinars.sql', 'w', encoding='utf-8') as file:
        file.write("-- SQL script to insert webinars into the 'webinar' table\n")
        file.write(f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        for activity_id in range(1, count + 1):
            topic = random.choice(list(TOPICS.keys()))
            description = random.choice(TOPICS[topic])
            meeting_url = generate_meeting_url()
            tutor_id = random.choice(tutor_ids) 
            price = generate_price()
            webinar_date = generate_date()
            admission_fee = generate_admission_fee()
            translation_id = random.randint(0,1030)
            # Create webinar name by combining topic with a type
            webinar_types = ['Masterclass', 'Workshop', 'Bootcamp', 'Training', 'Seminar']
            name = f"{topic} {random.choice(webinar_types)}"

            # Escape special characters
            name = name.replace("'", "''")
            description = description.replace("'", "''")
            meeting_url = meeting_url.replace("'", "''")

            # Write SQL insert statement
            file.write(
                f"INSERT INTO webinar ( name, description, meeting_url, "
                f"tutor_id, translation_id, price, webinar_date, admission_fee) VALUES "
                f"('{name}', '{description}', '{meeting_url}', "
                f"{tutor_id}, {translation_id} ,{price}, '{webinar_date}', {admission_fee});\n"
            )

if __name__ == "__main__":
    generate_webinars()