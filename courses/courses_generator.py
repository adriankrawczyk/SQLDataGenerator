import random
from datetime import datetime, timedelta
from typing import List, TextIO

class CourseDataGenerator:
    COURSE_NAMES: List[str] = [
        'Python Programming', 'Java Development', 'Web Technologies',
        'Data Science Fundamentals', 'Machine Learning Basics', 'Cloud Computing',
        'Network Security', 'Database Management', 'Software Architecture',
        'Mobile App Development', 'DevOps Practices', 'Artificial Intelligence',
        'Business Analytics', 'UI/UX Design', 'Project Management',
        'Quality Assurance', 'Agile Methodologies', 'Blockchain Development',
        'Internet of Things', 'Data Analytics'
    ]

    CLASS_NAMES: List[str] = [
        'Introduction to {course}', 'Advanced {course}', 'Applied {course}',
        'Practical {course}', '{course} Workshop', '{course} Lab',
        '{course} Seminar', '{course} Project', 'Special Topics in {course}',
        '{course} Case Studies'
    ]

    def __init__(self, num_courses: int = 50):
        self.num_courses = num_courses
        self.current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.base_date = datetime.now() - timedelta(days=365)

    def generate_datetime(self, start_offset_days: int = 0, end_offset_days: int = 365) -> datetime:
        """Generate a random datetime within the given range."""
        start_date = self.base_date + timedelta(days=start_offset_days)
        end_date = start_date + timedelta(days=max(1, end_offset_days))
        days_between = (end_date - start_date).days
        random_days = random.randint(0, max(1, days_between))
        random_seconds = random.randint(0, 86399)
        return start_date + timedelta(days=random_days, seconds=random_seconds)

    def write_header(self, file: TextIO) -> None:
        """Write the header comment to a file."""
        file.write(f"-- Generated on {self.current_time}\n")
        file.write("-- COMMIT EVERY 1000 ROWS\n\n")
        file.write("SET FOREIGN_KEY_CHECKS=0;\n\n")

    def generate_courses(self, file: TextIO) -> List[int]:
        """Generate and write course data."""
        course_ids = []
        for course_id in range(1, self.num_courses + 1):
            name = random.choice(self.COURSE_NAMES)
            maxpeopl = random.randint(20, 100)
            price = round(random.uniform(500, 3000), 2)
            
            file.write(
                f"INSERT INTO course ( name, maxpeople, price) "
                f"VALUES ( '{name}', {maxpeopl}, {price});\n"
            )
            course_ids.append(course_id)

        return course_ids

    def generate_course_classes(self, course_ids: List[int], file: TextIO) -> List[tuple]:
        """Generate and write course class data."""
        class_records = []
        class_id = 1
        
        for course_id in course_ids:
            num_classes = random.randint(3, 8)
            course_name = random.choice(self.COURSE_NAMES)
            
            for _ in range(num_classes):
                class_name = random.choice(self.CLASS_NAMES).format(course=course_name)
                
                file.write(
                    f"INSERT INTO course_class ( name, course_id) "
                    f"VALUES ( '{class_name}', {course_id});\n"
                )
                
                class_records.append((class_id, course_id))
                class_id += 1

        
        return class_records

    def generate_course_meetings(self, class_records: List[tuple], file: TextIO) -> List[int]:
        """Generate and write course meeting data."""
        activity_ids = []
        activity_id = 1
        
        for class_id, _ in class_records:
            num_meetings = random.randint(10, 30)
            
            for _ in range(num_meetings):
                time_start = self.generate_datetime()
                time_end = time_start + timedelta(hours=random.randint(1, 4))
                
                file.write(
                    f"INSERT INTO course_meeting (time_start, time_end, class_id) "
                    f"VALUES ( '{time_start}', '{time_end}', {class_id});\n"
                )
                
                activity_ids.append(activity_id)
                activity_id += 1

        
        return activity_ids

    def generate_course_attendants(self, course_ids: List[int], file: TextIO) -> None:
        """Generate and write course attendant data."""
        study_id = 1
        
        for course_id in course_ids:
            num_students = random.randint(10, 50)
            
            for _ in range(num_students):
                student_id = random.randint(1, 935) 
                
                file.write(
                    f"INSERT INTO course_attendant (study_id, student_id, course_id) "
                    f"VALUES ({study_id}, {student_id}, {course_id});\n"
                )
                
                study_id += 1


    def generate_data(self) -> None:
        """Generate all course-related data."""
        with open('insert_course.sql', 'w', encoding='utf-8') as course_file, \
             open('insert_course_class.sql', 'w', encoding='utf-8') as class_file, \
             open('insert_course_meeting.sql', 'w', encoding='utf-8') as meeting_file, \
             open('insert_course_attendant.sql', 'w', encoding='utf-8') as attendant_file:

            # Write headers
            for file in [course_file, class_file, meeting_file, attendant_file]:
                self.write_header(file)

            # Generate course data and get IDs
            course_ids = self.generate_courses(course_file)
            
            # Generate course classes and get records
            class_records = self.generate_course_classes(course_ids, class_file)
            
            # Generate course meetings
            self.generate_course_meetings(class_records, meeting_file)
            
            # Generate course attendants
            self.generate_course_attendants(course_ids, attendant_file)


if __name__ == "__main__":
    generator = CourseDataGenerator()
    generator.generate_data()