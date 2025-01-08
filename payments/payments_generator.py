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
        random_number_of_seconds = random.randrange(86400)  # Seconds in a day
        random_date = start_date + timedelta(days=random_number_of_days, seconds=random_number_of_seconds)
        return random_date.strftime('%Y-%m-%d %H:%M:%S')

    # Open files for each table
    with open('insert_orders.sql', 'w', encoding='utf-8') as orders_file, \
         open('insert_order_details.sql', 'w', encoding='utf-8') as details_file, \
         open('insert_order_college_meeting.sql', 'w', encoding='utf-8') as college_meeting_file, \
         open('insert_payments.sql', 'w', encoding='utf-8') as payments_file:

        # Write headers
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for file in [orders_file, details_file, college_meeting_file, payments_file]:
            file.write(f"-- Generated on {current_time}\n\n")

        # Generate orders and related data
        for order_id in range(1, num_orders + 1):
            # Generate order
            student_id = random.randint(1, 1000)  # Assuming 1000 students
            order_date = generate_datetime()
            
            # Generate 1-3 order details for each order
            num_details = random.randint(1, 3)
            total_price = 0
            
            # Store order details for this order
            order_details = []
            for detail_id in range(1, num_details + 1):
                product_id = random.randint(1, 50)  # Assuming 50 products
                price = round(random.uniform(50, 500), 2)
                paid = round(random.uniform(0, price), 2)  # Some might be partially paid
                payment_id = random.randint(1, num_orders * 2)  # Allowing multiple payments
                
                total_price += price
                order_details.append({
                    'detail_id': (order_id - 1) * 3 + detail_id,  # Ensure unique detail_ids
                    'product_id': product_id,
                    'price': price,
                    'paid': paid,
                    'payment_id': payment_id
                })

            # Write order record
            orders_file.write(
                f"INSERT INTO orders (order_id, total_price, student_id, order_date) "
                f"VALUES ({order_id}, {total_price}, {student_id}, '{order_date}');\n"
            )

            # Write order details records
            for detail in order_details:
                details_file.write(
                    f"INSERT INTO order_details (order_details_id, order_id, product_id, price, paid, payment_id) "
                    f"VALUES ({detail['detail_id']}, {order_id}, {detail['product_id']}, "
                    f"{detail['price']}, {detail['paid']}, {detail['payment_id']});\n"
                )

                # Generate college meeting record (for some orders)
                if random.random() < 0.7:  # 70% chance of having a college meeting
                    college_id = random.randint(1, 20)  # Assuming 20 colleges
                    college_meeting_file.write(
                        f"INSERT INTO order_college_meeting (order_details_id, meeting_id, college_id) "
                        f"VALUES ({detail['detail_id']}, {random.randint(1, 100)}, {college_id});\n"
                    )

            # Generate payment records
            for detail in order_details:
                payment_url = generate_payment_url()
                payment_status = random.choice([0, 1])  # 0 for pending, 1 for completed
                
                payments_file.write(
                    f"INSERT INTO payments (payment_id, payment_url, payment_status) "
                    f"VALUES ({detail['payment_id']}, '{payment_url}', {payment_status});\n"
                )

if __name__ == "__main__":
    generate_order_data()