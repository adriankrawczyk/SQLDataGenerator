import re

def fix_datetime_format(datetime_str):
    return datetime_str.split('.')[0] + "'"
with open('./courses/insert_course_meeting.sql', 'r') as input_file:
    with open('./courses/insert_course_meeting_fixed.sql', 'w') as output_file:
        for line in input_file:
            fixed_line = line
            datetime_values = re.findall(r"'[\d-]+ [\d:]+\.[\d]+'", line)
            for dt in datetime_values:
                fixed_dt = fix_datetime_format(dt)
                fixed_line = fixed_line.replace(dt, fixed_dt)
            output_file.write(fixed_line)
print("Created insert_course_meeting_fixed.sql with corrected datetime format")