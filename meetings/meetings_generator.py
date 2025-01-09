import random
from datetime import datetime, timedelta
from typing import List, TextIO, Tuple
from enum import Enum
import string
import uuid

# Define tutor and translator IDs
tutor_ids = [2, 3, 4, 5, 6, 7, 9, 10, 13, 14, 15, 17, 18, 20, 23, 26, 28, 31, 34, 35, 36, 37, 39, 42, 44, 46, 51, 52, 57, 59, 62, 63, 64, 66, 69, 72, 73, 75, 76, 78, 79, 80, 81, 82, 83, 86, 87, 89, 92, 96, 98, 101, 102, 104, 105, 106, 107, 112, 114, 115, 116, 117, 118, 120, 121, 123, 125, 126, 129, 132, 134, 136, 137, 139, 140, 143, 144, 148, 152, 153, 156, 159, 161, 162, 163, 164, 166, 167, 175, 176, 178, 180, 185, 186, 187, 189, 193, 194, 197, 199]

translator_ids = [1, 8, 11, 12, 16, 19, 21, 22, 24, 25, 27, 29, 30, 32, 33, 38, 40, 41, 43, 45, 47, 48, 49, 50, 53, 54, 55, 56, 58, 60]

class RoomNameGenerator:
    ADJECTIVES = [
    'Algorithmic', 'Computational', 'Data-Driven', 'Neural', 'Cognitive',
    'Semantic', 'Virtual', 'Cloud', 'Cyber', 'Encrypted',
    'Optimized', 'Logical', 'Binary', 'Dynamic', 'Syntactic',
    'Parallel', 'Quantum', 'Digital', 'Scalable', 'Modular',
    'Autonomous', 'Decentralized', 'Analytical', 'Smart', 'Intelligent'
]


    ROOM_TYPES = [
        'Hub', 'Lab', 'Room',
        'Center', 'Suite',  'Chamber', 'Hall', 'Facility'
    ]

    SPECIALTIES = [
        'Research', 'Design', 'Learning', 'Innovation', 'Technology',
        'Science', 'Arts', 'Media', 'Computing', 'Engineering',
        'Analytics', 'Development', 'Virtual', 'Projects', 'Robotics'
    ]

    @classmethod
    def generate_name(cls) -> str:
        name_patterns = [
            lambda: f"The {random.choice(cls.ADJECTIVES)} {random.choice(cls.ROOM_TYPES)}",
            lambda: f"{random.choice(cls.ADJECTIVES)} {random.choice(cls.SPECIALTIES)} {random.choice(cls.ROOM_TYPES)}",
            lambda: f"{random.choice(cls.SPECIALTIES)} {random.choice(cls.ROOM_TYPES)}",
            lambda: f"{random.choice(cls.ADJECTIVES)} {random.choice(cls.ROOM_TYPES)} {random.randint(100, 999)}"
        ]
        return random.choice(name_patterns)()

class MeetingType(Enum):
    SYNC = 'sync'
    ASYNC = 'async'
    STATIONARY = 'stationary'

class URLGenerator:
    MEETING_DOMAINS = [
        'meet.eduspace.io',
        'virtual.learnhub.com',
        'classroom.educato.net',
        'conference.learnsync.io',
        'room.academix.com',
        'meet.scholarly.net',
        'classes.instructure.com',
        'virtual.teachspace.io'
    ]
    
    RECORDING_DOMAINS = [
        'recordings.eduspace.io',
        'media.learnhub.com',
        'archive.educato.net',
        'replay.learnsync.io',
        'stream.academix.com',
        'watch.scholarly.net',
        'video.instructure.com',
        'playback.teachspace.io'
    ]
    
    URL_PATTERNS = [
        lambda id_str: f"/{id_str}",
        lambda id_str: f"/m/{id_str}",
        lambda id_str: f"/room/{id_str}",
        lambda id_str: f"/join/{id_str}",
        lambda id_str: f"/session/{id_str}"
    ]
    
    RECORDING_PATTERNS = [
        lambda id_str: f"/recording/{id_str}",
        lambda id_str: f"/replay/{id_str}",
        lambda id_str: f"/watch/{id_str}",
        lambda id_str: f"/video/{id_str}"
    ]

    @staticmethod
    def generate_meeting_id() -> str:
        """Generate a realistic meeting ID using various formats."""
        formats = [
            lambda: str(uuid.uuid4()),
            lambda: ''.join(random.choices(string.digits, k=10)),
            lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
            lambda: '-'.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=3)) for _ in range(3))
        ]
        return random.choice(formats)()

    @classmethod
    def generate_urls(cls) -> Tuple[str, str]:
        """Generate both meeting and recording URLs."""
        meeting_domain = random.choice(cls.MEETING_DOMAINS)
        recording_domain = random.choice(cls.RECORDING_DOMAINS)
        
        meeting_unique_id = cls.generate_meeting_id()
        recording_unique_id = cls.generate_meeting_id()
        
        meeting_pattern = random.choice(cls.URL_PATTERNS)
        recording_pattern = random.choice(cls.RECORDING_PATTERNS)
        
        meeting_url = f"https://{meeting_domain}{meeting_pattern(meeting_unique_id)}"
        recording_url = f"https://{recording_domain}{recording_pattern(recording_unique_id)}"
        
        return meeting_url, recording_url

class MeetingDataGenerator:
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
        """Write SQL file header with timestamp."""
        file.write(f"-- Generated on {self.current_time}\n\n")

    def generate_rooms(self, file: TextIO, num_rooms: int = 50) -> None:
        """Generate and write room data."""
        for _ in range(num_rooms):
            name = RoomNameGenerator.generate_name()
            place_limit = random.randint(10, 100)
            file.write(
                f"INSERT INTO rooms (name, place_limit) "
                f"VALUES ('{name}', {place_limit});\n"
            )

    def generate_meetings(self, file: TextIO) -> None:
        """Generate and write base meeting data."""
        for _ in range(self.num_meetings):
            tutor_id = random.choice(tutor_ids)
            translation_id = random.randint(31,1031) if random.random() < 0.8 else None
            meeting_date = self.generate_datetime().strftime('%Y-%m-%d %H:%M:%S')
            
            file.write(
                f"INSERT INTO meeting (tutor_id, translation_id) VALUES "
                f"({tutor_id}, {translation_id if translation_id else 'NULL'});\n"
            )

    def generate_meeting_types(self) -> None:
        """Generate different types of meetings and their specific data."""
        url_generator = URLGenerator()
        
        with open('insert_online_sync_meeting.sql', 'w', encoding='utf-8') as sync_file, \
             open('insert_online_async_meeting.sql', 'w', encoding='utf-8') as async_file, \
             open('insert_stationary_meetings.sql', 'w', encoding='utf-8') as stationary_file:

            for file in [sync_file, async_file, stationary_file]:
                self.write_header(file)

            for _ in range(self.num_meetings):
                meeting_type = random.choice(list(MeetingType))
                meeting_url, recording_url = url_generator.generate_urls()

                if meeting_type == MeetingType.SYNC:
                    sync_file.write(
                        f"INSERT INTO online_sync_meeting (meeting_id,meeting_url, recording_url) "
                        f"VALUES ({random.randint(1,2000)}, '{meeting_url}', '{recording_url}');\n"
                    )
                elif meeting_type == MeetingType.ASYNC:
                    async_file.write(
                        f"INSERT INTO online_async_meeting (recording_url) "
                        f"VALUES ('{recording_url}');\n"
                    )
                else:  # STATIONARY
                    room_id = random.randint(1, 50)  # Assuming 50 rooms
                    stationary_file.write(
                        f"INSERT INTO stationary_meetings (room_id) "
                        f"VALUES ({room_id});\n"
                    )

    def generate_attendant_presence(self) -> None:
        """Generate attendance data for both college and course attendants."""
        with open('insert_college_attendant_presence.sql', 'w', encoding='utf-8') as college_file, \
             open('insert_course_attendant_presence.sql', 'w', encoding='utf-8') as course_file:

            for file in [college_file, course_file]:
                self.write_header(file)

            for meeting_number in range(self.num_meetings):
                # Generate college attendant presence
                num_college_students = random.randint(10, 30)
                for _ in range(num_college_students):
                    student_id = random.randint(1, 935)
                    present = random.choice([0, 1])
                    college_file.write(
                        f"INSERT INTO college_attendant_presence (student_id, meeting_id, present) "
                        f"VALUES ({student_id}, {meeting_number + 1}, {present});\n"
                    )

                # Generate course attendant presence
                num_course_students = random.randint(10, 30)
                for _ in range(num_course_students):
                    student_id = random.randint(1, 935)
                    present = random.choice([0, 1])
                    course_file.write(
                        f"INSERT INTO course_attendant_presence (student_id, meeting_id, present) "
                        f"VALUES ({student_id}, {meeting_number + 1}, {present});\n"
                    )

    def generate_data(self) -> None:
        """Generate all meeting-related data."""
        with open('insert_rooms.sql', 'w', encoding='utf-8') as rooms_file, \
             open('insert_meeting.sql', 'w', encoding='utf-8') as meeting_file:

            # Generate base data
            self.generate_rooms(rooms_file)
            self.generate_meetings(meeting_file)

            # Generate specific meeting types and attendance
            self.generate_meeting_types()
            self.generate_attendant_presence()

if __name__ == "__main__":
    generator = MeetingDataGenerator(num_meetings=1000)
    generator.generate_data()