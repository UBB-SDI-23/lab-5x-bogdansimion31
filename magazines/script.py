import timedelta as timedelta
from django.contrib.auth import get_user_model
from faker import Faker
import psycopg2
import random

# Connect to the PostgreSQL database
from magazines.magazine_api.models import BuyerSubscription

conn = psycopg2.connect(
    host="localhost",
    database="bogdansimion",
    user="bogdansimion",
    password="password"
)

# Create a cursor object
cur = conn.cursor()

# Create a Faker instance
fake = Faker()

# Generate and insert 1,000,000 Author records
# for i in range(1000000):
#     first_name = fake.first_name()
#     last_name = fake.last_name()
#     birth_date = fake.date_of_birth()
#     email = fake.email()
#     website = fake.url()
#
#     # SQL query to insert an Author record
#     query = "INSERT INTO magazine_api_author (first_name, last_name, birth_date, email, website) VALUES (%s, %s, %s, %s, %s)"
#     values = (first_name, last_name, birth_date, email, website)
#
#     # Execute the SQL query
#     cur.execute(query, values)
#
#     # Commit the changes to the database
#     if i % 1000 == 0:
#         conn.commit()
#
# print("Authors generated")
#
#
# # Generate and insert 1,000,000 Publisher records
# for i in range(1000000):
#     name = fake.company()
#     address = fake.address()
#     city = fake.city()
#     country = fake.country()
#     website = fake.url()
#     age = random.randint(20, 80)
#
#     # SQL query to insert a Publisher record
#     query = "INSERT INTO magazine_api_publisher (name, address, city, country, website, age) VALUES (%s, %s, %s, %s, %s, %s)"
#     values = (name, address, city, country, website, age)
#
#     # Execute the SQL query
#     cur.execute(query, values)
#
#     # Commit the changes to the database
#     if i % 1000 == 0:
#         conn.commit()
#
# print("Publishers generated")

# Generate and insert 1,000,000 Buyer records
# for i in range(1000000):
#     name = fake.name()
#     email = fake.email()
#     text = fake.sentence(nb_words=3)
#
#     # SQL query to insert a Buyer record
#     query = "INSERT INTO magazine_api_buyer (name, email, text) VALUES (%s, %s, %s)"
#     values = (name, email, text)
#
#     # Execute the SQL query
#     cur.execute(query, values)
#
#     # Commit the changes to the database
#     if i % 1000 == 0:
#         conn.commit()
#
# print("Buyers generated")

# # Generate and insert 10,000,000 Magazine records
# for i in range(10000000):
#     title = fake.text(max_nb_chars=100)
#     number_of_pages = random.randint(1, 1000)
#     publish_date = fake.date_between(start_date='-20y', end_date='today')
#     quantity = random.randint(1, 100)
#     ibn = random.randint(10000, 99999)
#     price = random.randint(1, 9999)
#
#     # SQL query to insert a Magazine record
#     query = "INSERT INTO magazine_api_magazine (title, number_of_pages, publish_date, quantity, ibn, price) VALUES (%s, %s, %s, %s, %s, %s)"
#     values = (title, number_of_pages, publish_date, quantity, ibn, price)
#
#     # Execute the SQL query
#     cur.execute(query, values)
#
#     # Commit the changes to the database
#     if i % 1000 == 0:
#         conn.commit()
#
# print("Magazines generated")

User = get_user_model()
# Get all buyers from the database
buyers = User.objects.filter(is_staff=False)

# Generate and insert BuyerSubscription records for each buyer
for buyer in buyers:
    # Generate a random start and end date
    start_date = fake.date_between(start_date='-5y', end_date='today')
    end_date = start_date + timedelta(days=random.randint(30, 365))

    # Create a new BuyerSubscription object
    subscription = BuyerSubscription(buyer=buyer, start_date=start_date, end_date=end_date)

    # Save the BuyerSubscription to the database
    subscription.save()

print("BuyerSubscriptions generated")

# Get the IDs of all Authors and Publishers
cur.execute("SELECT id FROM magazine_api_author")
author_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT id FROM magazine_api_publisher")
publisher_ids = [row[0] for row in cur.fetchall()]

# Generate and insert 1,000 Magazine records
for i in range(1000000):
    title = fake.sentence(nb_words=3)
    number_of_pages = random.randint(1, 1000)
    publish_date = fake.date_between(start_date="-10y", end_date="today")
    quantity = random.randint(1, 100)
    ibn = random.randint(10000, 99999)
    author_id = random.choice(author_ids)
    publisher_id = random.choice(publisher_ids)
    price = random.randint(10, 100)

    # SQL query to insert a Magazine record
    query = "INSERT INTO magazine_api_magazine (title, number_of_pages, publish_date, quantity, ibn, author_id, publisher_id, price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
    values = (title, number_of_pages, publish_date, quantity, ibn, author_id, publisher_id, price)

    try:
        # Execute the SQL query
        cur.execute(query, values)

        # Get the ID of the inserted Magazine record
        magazine_id = cur.fetchone()[0]

        # Generate and insert 1-5 Buyer records for the Magazine
        for j in range(random.randint(1, 5)):
            name = fake.name()
            email = fake.email()

            # SQL query to insert a Buyer record
            query = "INSERT INTO magazine_api_buyer (name, email) VALUES (%s, %s) RETURNING id"
            values = (name, email)

            try:
                # Execute the SQL query
                cur.execute(query, values)

                # Get the ID of the inserted Buyer record
                buyer_id = cur.fetchone()[0]

                # SQL query to insert a record into the MagazineBuyers table
                query = "INSERT INTO magazine_api_magazine_buyers (magazine_id, buyer_id) VALUES (%s, %s)"
                values = (magazine_id, buyer_id)

                # Execute the SQL query
                cur.execute(query, values)

            except psycopg2.Error as e:
                print(f"Error inserting Buyer record: {e}")
                conn.rollback()

        # Commit the changes to the database
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error inserting Magazine record: {e}")
        conn.rollback()

cur.execute("SELECT id FROM magazine_api_magazine")
magazines = cur.fetchall()

cur.execute("SELECT id FROM magazine_api_buyer")
buyers = cur.fetchall()
from datetime import datetime, timedelta

for i in range(1000000):
    magazine_id = random.choice(magazines)[0]
    buyer_id = random.choice(buyers)[0]
    price = random.randint(1, 100)
    timestamp = datetime.now() - timedelta(days=random.randint(1, 365))
    query = "INSERT INTO magazine_api_purchase (magazine_id, buyer_id, price, timestamp) VALUES (%s, %s, %s, %s)"
    values = (magazine_id, buyer_id, price, timestamp)
    try:
        cur.execute(query, values)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

# Close the cursor and connection
cur.close()
conn.close()

#trebuie adaugat un field de text la un model