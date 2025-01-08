import random
from datetime import datetime, timedelta
from typing import List, TextIO
from enum import Enum

class MeetingType(Enum):
    SYNC = 'sync'
    ASYNC = 'async'
    STATIONARY = 'stationary'

class MeetingDataGenerator:
    ROOM_NAMES: List[str] = [
        'Main Auditorium', 'Lecture Hall A', 'Lecture Hall B', 'Seminar Room 1',
        'Conference Room 101', 'Lab 201', 'Study Hall', 'Meeting Room A',
        'Classroom 301', 'Workshop Space', 'Distance Learning Center',
        'Virtual Room 1', 'Collaboration Space', 'Research Lab'
    ]

    def __init__(self, num_meetings: int = 1000):
        self.num_meetings = num_meetings
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

    def generate_rooms(self, file: TextIO, num_rooms: int = 50) -> List[int]:
        """Generate and write room data."""
        room_ids = []
        for room_id in range(1, num_rooms + 1):
            name = f"{random.choice(self.ROOM_NAMES)} {room_id}"
            place_km = random.randint(0, 100)
            file.write(
                f"INSERT INTO rooms (room_id, name, place_km) "
                f"VALUES ({room_id}, '{name}', {place_km});\n"
            )
            room_ids.append(room_id)
            if room_id % 1000 == 0:
                file.write("COMMIT;\n")
        return room_ids

    def generate_meetings(self, file: TextIO) -> List[int]:
        """Generate and write base meeting data."""
        meeting_ids = []
        for meeting_id in range(1, self.num_meetings + 1):
            tutor_id = random.randint(1, 200)
            translation_id = random.randint(1, 50) if random.random() < 0.3 else None
            
            file.write(
                f"INSERT INTO meeting (id, tutor_id, translation_id) VALUES "
                f"({meeting_id}, {tutor_id}, {translation_id if translation_id else 'NULL'});\n"
            )
            meeting_ids.append(meeting_id)
            if meeting_id % 1000 == 0:
                file.write("COMMIT;\n")
        return meeting_ids

    def generate_meeting_types(self, meeting_ids: List[int], room_ids: List[int]) -> None:
        """Generate different types of meetings and their specific data."""
        with open('insert_online_sync_meeting.sql', 'w', encoding='utf-8') as sync_file, \
             open('insert_online_async_meeting.sql', 'w', encoding='utf-8') as async_file, \
             open('insert_stationary_meetings.sql', 'w', encoding='utf-8') as stationary_file:

            for file in [sync_file, async_file, stationary_file]:
                self.write_header(file)

            for meeting_id in meeting_ids:
                meeting_type = random.choice(list(MeetingType))
                meeting_url = f"https://meeting.example.com/{meeting_id}"
                recording_url = f"https://recording.example.com/{meeting_id}"

                if meeting_type == MeetingType.SYNC:
                    sync_file.write(
                        f"INSERT INTO online_sync_meeting (meeting_id, meeting_url, recording_url) "
                        f"VALUES ({meeting_id}, '{meeting_url}', '{recording_url}');\n"
                    )
                elif meeting_type == MeetingType.ASYNC:
                    async_file.write(
                        f"INSERT INTO online_async_meeting (meeting_id, recording_url) "
                        f"VALUES ({meeting_id}, '{recording_url}');\n"
                    )
                else:  # STATIONARY
                    room_id = random.choice(room_ids)
                    stationary_file.write(
                        f"INSERT INTO stationary_meetings (meeting_id, room_id) "
                        f"VALUES ({meeting_id}, {room_id});\n"
                    )

                if meeting_id % 1000 == 0:
                    for file in [sync_file, async_file, stationary_file]:
                        file.write("COMMIT;\n")

    def generate_attendant_presence(self, meeting_ids: List[int]) -> None:
        """Generate attendance data for both college and course attendants."""
        with open('insert_college_attendant_presence.sql', 'w', encoding='utf-8') as college_file, \
             open('insert_course_attendant_presence.sql', 'w', encoding='utf-8') as course_file:

            for file in [college_file, course_file]:
                self.write_header(file)

            for meeting_id in meeting_ids:
                # Generate college attendant presence
                num_college_students = random.randint(10, 30)
                for student_id in range(1, num_college_students + 1):
                    present = random.choice([0, 1])
                    college_file.write(
                        f"INSERT INTO college_attendant_presence (student_id, meeting_id, present) "
                        f"VALUES ({student_id}, {meeting_id}, {present});\n"
                    )

                # Generate course attendant presence
                num_course_students = random.randint(10, 30)
                for student_id in range(1, num_course_students + 1):
                    present = random.choice([0, 1])
                    course_file.write(
                        f"INSERT INTO course_attendant_presence (student_id, meeting_id, present) "
                        f"VALUES ({student_id}, {meeting_id}, {present});\n"
                    )

                if meeting_id % 1000 == 0:
                    college_file.write("COMMIT;\n")
                    course_file.write("COMMIT;\n")

    def generate_data(self) -> None:
        """Generate all meeting-related data."""
        with open('insert_rooms.sql', 'w', encoding='utf-8') as rooms_file, \
             open('insert_meeting.sql', 'w', encoding='utf-8') as meeting_file:

            self.write_header(rooms_file)
            self.write_header(meeting_file)

            # Generate base data
            room_ids = self.generate_rooms(rooms_file)
            meeting_ids = self.generate_meetings(meeting_file)

            # Generate specific meeting types and attendance
            self.generate_meeting_types(meeting_ids, room_ids)
            self.generate_attendant_presence(meeting_ids)

            # Write final commits
            for file in [rooms_file, meeting_file]:
                file.write("\nCOMMIT;\n")
                file.write("\nSET FOREIGN_KEY_CHECKS=1;\n")

if __name__ == "__main__":
    generator = MeetingDataGenerator()
    generator.generate_data()