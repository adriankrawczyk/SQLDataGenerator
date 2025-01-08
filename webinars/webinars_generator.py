import random
from datetime import datetime, timedelta

def generate_webinars(count=100):
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
            # Select random topic and description
            topic = random.choice(list(TOPICS.keys()))
            description = random.choice(TOPICS[topic])
            
            # Generate other fields
            meeting_url = generate_meeting_url()
            product_id = random.randint(1, 20)  # Assuming 20 different products
            tutor_id = random.randint(1, 50)    # Assuming 50 different tutors
            organization_id = random.randint(1, 10)  # Assuming 10 different organizations
            price = generate_price()
            webinar_date = generate_date()
            admission_fee = generate_admission_fee()

            # Create webinar name by combining topic with a type
            webinar_types = ['Masterclass', 'Workshop', 'Bootcamp', 'Training', 'Seminar']
            name = f"{topic} {random.choice(webinar_types)}"

            # Escape special characters
            name = name.replace("'", "''")
            description = description.replace("'", "''")
            meeting_url = meeting_url.replace("'", "''")

            # Write SQL insert statement
            file.write(
                f"INSERT INTO webinar (activity_id, name, description, meeting_url, product_id, "
                f"tutor_id, organization_id, price, webinar_date, admission_fee) VALUES "
                f"({activity_id}, '{name}', '{description}', '{meeting_url}', {product_id}, "
                f"{tutor_id}, {organization_id}, {price}, '{webinar_date}', {admission_fee});\n"
            )

if __name__ == "__main__":
    generate_webinars()