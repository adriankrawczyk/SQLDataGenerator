import random
from datetime import datetime, timedelta

def generate_order_data(num_orders=100):
    # Payment URLs for different payment providers
    PAYMENT_PROVIDERS = [
        'https://stripe.com/pay/',
        'https://paypal.com/checkout/',
        'https://square.com/pay/',
        'https://wise.com/pay/'
    ]

    def generate_payment_url():
        provider = random.choice(PAYMENT_PROVIDERS)
        transaction_id = ''.join(random.choices('0123456789abcdef', k=16))
        return f"{provider}{transaction_id}"

    def generate_datetime(start_date=None):
        if start_date is None:
            start_date = datetime.now() - timedelta(days=180)  # Start from 6 months ago
        end_date = datetime.now()
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        # Round to nearest minute instead of second for cleaner timestamps
        random_number_of_minutes = random.randrange(1440)  # Minutes in a day
        random_date = start_date + timedelta(days=random_number_of_days, minutes=random_number_of_minutes)
        return random_date.strftime('%Y-%m-%d %H:%M:00')  # Set seconds to 00

    def round_price(price):
        # Round to nearest .99 or .50 for more realistic pricing
        base = round(price)
        if random.random() < 0.7:  # 70% chance of .99
            return base - 0.01
        return base - 0.50

    # Open files for each table
    with open('insert_orders.sql', 'w', encoding='utf-8') as orders_file, \
         open('insert_order_details.sql', 'w', encoding='utf-8') as details_file, \
         open('insert_order_college.sql', 'w', encoding='utf-8') as college_file, \
         open('insert_order_college_meeting.sql', 'w', encoding='utf-8') as college_meeting_file, \
         open('insert_order_course.sql', 'w', encoding='utf-8') as course_file, \
         open('insert_order_webinar.sql', 'w', encoding='utf-8') as webinar_file, \
         open('insert_payments.sql', 'w', encoding='utf-8') as payments_file:

        # Write headers
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        for file in [orders_file, details_file, college_file, college_meeting_file, 
                    course_file, webinar_file, payments_file]:
            file.write(f"-- Generated on {current_time}\n\n")

        # Generate orders and related data
        for order_id in range(1, num_orders + 1):
            # Generate order
            student_id = random.randint(1, 934)
            order_date = generate_datetime()
            payment_date = generate_datetime(datetime.strptime(order_date, '%Y-%m-%d %H:%M:00'))
            
            # Generate 1-3 order details for each order
            num_details = random.randint(1, 3)
            total_price = 0
            
            # Store order details for this order
            order_details = []
            for detail_id in range(1, num_details + 1):
                product_id = random.randint(1, 50)
                base_price = round_price(random.uniform(50, 500))
                price = round(base_price, 2)
                # Make paid amount either full price, half price, or zero
                paid_ratio = random.choice([0, 0.5, 1])
                paid = round(price * paid_ratio, 2)
                payment_id = random.randint(1, num_orders * 2)
                
                total_price += price
                detail_unique_id = (order_id - 1) * 3 + detail_id
                
                order_details.append({
                    'detail_id': detail_unique_id,
                    'product_id': product_id,
                    'price': price,
                    'paid': paid,
                    'payment_id': payment_id
                })

            # Round total price to 2 decimal places
            total_price = round(total_price, 2)

            # Write order record
            orders_file.write(
                f"INSERT INTO orders (total_price, student_id, order_date, payment_date) "
                f"VALUES ({total_price:.2f}, {student_id}, '{order_date}', '{payment_date}');\n"
            )

            # Write order details records
            for detail in order_details:
                details_file.write(
                    f"INSERT INTO order_details (order_id, product_id, price, paid, payment_id) "
                    f"VALUES ({order_id}, {detail['product_id']}, "
                    f"{detail['price']:.2f}, {detail['paid']:.2f}, {detail['payment_id']});\n"
                )

                # Generate related records with probabilities
                if random.random() < 0.3:  # 30% chance of college
                    college_id = random.randint(1, 20)
                    college_file.write(
                        f"INSERT INTO order_college (order_details_id, college_id) "
                        f"VALUES ({detail['detail_id']}, {college_id});\n"
                    )

                if random.random() < 0.4:  # 40% chance of college meeting
                    meeting_id = random.randint(1, 100)
                    college_meeting_file.write(
                        f"INSERT INTO order_college_meeting (order_details_id, meeting_id) "
                        f"VALUES ({detail['detail_id']}, {meeting_id});\n"
                    )

                if random.random() < 0.5:  # 50% chance of course
                    course_id = random.randint(1, 30)
                    course_file.write(
                        f"INSERT INTO order_course (order_details_id, course_id) "
                        f"VALUES ({detail['detail_id']}, {course_id});\n"
                    )

                if random.random() < 0.4:  # 40% chance of webinar
                    webinar_id = random.randint(1, 100)
                    access_start = generate_datetime()
                    webinar_file.write(
                        f"INSERT INTO order_webinar (order_details_id, webinar_id, access_start_date) "
                        f"VALUES ({detail['detail_id']}, {webinar_id}, '{access_start}');\n"
                    )

                # Generate payment record
                payment_url = generate_payment_url()
                payment_status = random.choice([0, 1])
                payment_date = generate_datetime()
                
                payments_file.write(
                    f"INSERT INTO payments (payment_url, payment_status, payment_date) "
                    f"VALUES ('{payment_url}', {payment_status}, '{payment_date}');\n"
                )

if __name__ == "__main__":
    generate_order_data(1000)  # Generate 100 orders