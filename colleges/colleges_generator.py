import random
from datetime import datetime, timedelta
from typing import List, TextIO

class CollegeDataGenerator:
    COLLEGE_NAMES: List[str] = [
        'School of Computer Science', 'School of Business', 'School of Engineering',
        'School of Arts', 'School of Medicine', 'School of Law', 'School of Design',
        'School of Mathematics', 'School of Physics', 'School of Chemistry',
        'School of Economics', 'School of Psychology', 'School of Architecture',
        'School of Biology', 'School of Chemistry', 'School of Environmental Science',
        'School of History', 'School of Literature', 'School of Philosophy',
        'School of Political Science'
    ]

    CLASS_NAMES: List[str] = [
        'Introduction to Programming', 'Data Structures', 'Algorithms',
        'Database Systems', 'Web Development', 'Machine Learning',
        'Artificial Intelligence', 'Computer Networks', 'Operating Systems',
        'Software Engineering', 'Digital Marketing', 'Business Analytics',
        'Advanced Mathematics', 'Statistical Analysis', 'Project Management',
        'System Design', 'Cloud Computing', 'Mobile Development',
        'Cybersecurity Fundamentals', 'Data Mining', 'Natural Language Processing',
        'Computer Graphics', 'Quantum Computing', 'Blockchain Technology',
        'Internet of Things', 'Robotics', 'Game Development',
        'Computer Architecture', 'Parallel Computing', 'Embedded Systems'
    ]

    def __init__(self, num_colleges: int = 50):
        self.num_colleges = num_colleges
        self.current_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.base_date = datetime.now() - timedelta(days=365)  # Start from 1 year ago

    def generate_datetime(self, start_offset_days: int = 0, end_offset_days: int = 365) -> datetime:
        """Generate a random datetime within the given range."""
        start_date = self.base_date + timedelta(days=start_offset_days)
        end_date = start_date + timedelta(days=max(1, end_offset_days))  # Ensure at least 1 day difference
        days_between = (end_date - start_date).days
        random_days = random.randint(0, max(1, days_between))  # Use randint instead of randrange
        random_seconds = random.randint(0, 86399)  # Seconds in a day (0-86399)
        return start_date + timedelta(days=random_days, seconds=random_seconds)

    def write_header(self, file: TextIO) -> None:
        """Write the header comment to a file."""
        file.write(f"-- Generated on {self.current_time}\n")
        file.write("-- COMMIT EVERY 1000 ROWS\n\n")
        file.write("SET FOREIGN_KEY_CHECKS=0;\n\n")

    def generate_college(self, college_id: int, file: TextIO) -> None:
        """Generate and write college data."""
        name = f"{random.choice(self.COLLEGE_NAMES)} {college_id}"
        product_id = random.randint(1, 100)
        max_allocation = random.randint(100, 500)
        price = round(random.uniform(2000, 10000), 2)
        admission_fee = round(random.uniform(100, 500), 2)

        file.write(
            f"INSERT INTO college (college_id, name, product_id, max_allocation, price, admission_fee) "
            f"VALUES ({college_id}, '{name}', {product_id}, {max_allocation}, {price}, {admission_fee});\n"
        )
        if college_id % 1000 == 0:
            file.write("COMMIT;\n")

    def generate_class(self, class_id: int, college_id: int, file: TextIO) -> int:
        """Generate and write class data. Returns the class ID."""
        semester = random.randint(1, 8)
        class_name = random.choice(self.CLASS_NAMES)
        actual_class_id = (college_id-1)*20 + class_id  # Increased multiplier for more classes
        
        file.write(
            f"INSERT INTO college_class (class_id, name, college_id, semester) "
            f"VALUES ({actual_class_id}, '{class_name}', {college_id}, {semester});\n"
        )
        if actual_class_id % 1000 == 0:
            file.write("COMMIT;\n")
        return actual_class_id

    def generate_meeting(self, meeting_id: int, class_id: int, college_id: int, file: TextIO) -> int:
        """Generate and write meeting data. Returns the activity ID."""
        time_start = self.generate_datetime()
        time_end = time_start + timedelta(hours=random.randint(1, 4))
        price_students = round(random.uniform(30, 150), 2)
        price_others = round(random.uniform(60, 300), 2)
        activity_id = class_id * 10 + meeting_id

        file.write(
            f"INSERT INTO college_meeting (activity_id, name, time_start, time_end, "
            f"class_id, price_for_students, price_for_others) VALUES "
            f"({activity_id}, 'Meeting {meeting_id}', '{time_start}', '{time_end}', "
            f"{class_id}, {price_students}, {price_others});\n"
        )
        if activity_id % 1000 == 0:
            file.write("COMMIT;\n")
        return activity_id

    def generate_data(self) -> None:
        """Generate all college-related data and write to files."""
        with open('insert_college.sql', 'w', encoding='utf-8') as college_file, \
             open('insert_college_class.sql', 'w', encoding='utf-8') as class_file, \
             open('insert_college_meeting.sql', 'w', encoding='utf-8') as meeting_file, \
             open('insert_practices.sql', 'w', encoding='utf-8') as practices_file, \
             open('insert_practice_presence.sql', 'w', encoding='utf-8') as presence_file, \
             open('insert_college_attendant.sql', 'w', encoding='utf-8') as attendant_file, \
             open('insert_schedule_details.sql', 'w', encoding='utf-8') as schedule_file:

            # Write headers
            for file in [college_file, class_file, meeting_file, practices_file, 
                        presence_file, attendant_file, schedule_file]:
                self.write_header(file)

            # Generate data for each college
            for college_id in range(1, self.num_colleges + 1):
                self.generate_college(college_id, college_file)

                # Generate classes
                num_classes = random.randint(8, 15)
                for class_id in range(1, num_classes + 1):
                    actual_class_id = self.generate_class(class_id, college_id, class_file)

                    # Generate meetings
                    num_meetings = random.randint(3, 8)
                    for meeting_id in range(1, num_meetings + 1):
                        activity_id = self.generate_meeting(meeting_id, actual_class_id, college_id, meeting_file)

                        # Generate practices
                        for practice_offset in range(0, random.randint(5, 10)):
                            practice_id = activity_id * 100 + practice_offset
                            practice_date = self.generate_datetime().strftime('%Y-%m-%d')  # Format date without milliseconds
                            practices_file.write(
                                f"INSERT INTO practices (practice_id, college_id, date) "
                                f"VALUES ({practice_id}, {college_id}, '{practice_date}');\n"
                            )
                            if practice_id % 1000 == 0:
                                practices_file.write("COMMIT;\n")

                            # Generate practice presence
                            num_students = random.randint(15, 40)
                            for student_id in range(1, num_students + 1):
                                present = random.choice([0, 1])
                                presence_file.write(
                                    f"INSERT INTO practice_presence (practice_id, student_id, present) "
                                    f"VALUES ({practice_id}, {student_id}, {present});\n"
                                )
                            if student_id % 1000 == 0:
                                presence_file.write("COMMIT;\n")

                # Generate attendants
                num_attendants = random.randint(30, 80)
                for i in range(num_attendants):
                    study_id = (college_id-1)*1000 + i
                    student_id = random.randint(1, 5000)
                    semester = random.randint(1, 8)
                    
                    attendant_file.write(
                        f"INSERT INTO college_attendant (study_id, student_id, college_id, semester) "
                        f"VALUES ({study_id}, {student_id}, {college_id}, {semester});\n"
                    )
                    if study_id % 1000 == 0:
                        attendant_file.write("COMMIT;\n")

                    start_date = self.generate_datetime(-180, -30).date().strftime('%Y-%m-%d')  # Only date component
                    end_date = self.generate_datetime(30, 365).date().strftime('%Y-%m-%d')  
                    grade = random.choice([2.0, 3.0, 3.5, 4.0, 4.5, 5.0])
                    passed = 1 if grade >= 3.0 else 0
                    
                    schedule_file.write(
                        f"INSERT INTO schedule_details (study_id, class_id, start_date, end_date, grade, passed) VALUES "
                        f"({student_id}, {actual_class_id}, '{start_date}', '{end_date}', {grade}, {passed});\n"
                    )
                    if i % 1000 == 0:
                        schedule_file.write("COMMIT;\n")

            # Write final commits
            for file in [college_file, class_file, meeting_file, practices_file, 
                        presence_file, attendant_file, schedule_file]:
                file.write("\nCOMMIT;\n")
                file.write("\nSET FOREIGN_KEY_CHECKS=1;\n")



if __name__ == "__main__":
    generator = CollegeDataGenerator()
    generator.generate_data()