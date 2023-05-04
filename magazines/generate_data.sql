-- Populate Author table
INSERT INTO myapp_author (first_name, last_name, birth_date, email, website)
SELECT
  substr(md5(random()::text), 1, 10),
  substr(md5(random()::text), 1, 10),
  date_trunc('day', now() - interval '70 years') + (random() * interval '70 years'),
  substr(md5(random()::text), 1, 10) || '@example.com',
  'http://www.' || substr(md5(random()::text), 1, 10) || '.com'
FROM generate_series(1, 1000000);

-- Populate Publisher table
INSERT INTO myapp_publisher (name, address, city, country, website, age)
SELECT
  substr(md5(random()::text), 1, 10),
  substr(md5(random()::text), 1, 20),
  substr(md5(random()::text), 1, 10),
  substr(md5(random()::text), 1, 10),
  'http://www.' || substr(md5(random()::text), 1, 10) || '.com',
  floor(random() * 100) + 20
FROM generate_series(1, 1000000);

-- Populate Buyer table
INSERT INTO myapp_buyer (name, email)
SELECT
  substr(md5(random()::text), 1, 10),
  substr(md5(random()::text), 1, 10) || '@example.com'
FROM generate_series(1, 1000000);

-- Populate BuyerSubscription table
INSERT INTO myapp_buyersubscription (buyer_id, start_date, end_date)
SELECT
  id,
  date_trunc('day', now() - interval '1 year') + (random() * interval '6 months'),
  date_trunc('day', now() + interval '1 year') - (random() * interval '6 months')
FROM myapp_buyer
LIMIT 1000000;

-- Populate Magazine table
INSERT INTO myapp_magazine (title, number_of_pages, publish_date, quantity, ibn, author_id, publisher_id, price)
SELECT
  substr(md5(random()::text), 1, 10),
  floor(random() * 1000) + 1,
  date_trunc('day', now() - interval '20 years') + (random() * interval '20 years'),
  floor(random() * 100) + 1,
  (SELECT id FROM myapp_author ORDER BY random() LIMIT 1),
  (SELECT id FROM myapp_publisher ORDER BY random() LIMIT 1),
  floor(random() * 9999) + 1
FROM generate_series(1, 1000000);

-- Populate Purchase table
INSERT INTO myapp_purchase (magazine_id, buyer_id, price, timestamp)
SELECT
  (SELECT id FROM myapp_magazine ORDER BY random() LIMIT 1),
  (SELECT id FROM myapp_buyer ORDER BY random() LIMIT 1),
  floor(random() * 9999) + 1,
  date_trunc('day', now() - interval '1 year') + (random() * interval '1 year')
FROM generate_series(1, 1000000);

-- Populate MagazineBuyers (many-to-many intermediate table)
INSERT INTO myapp_magazine_buyers (magazine_id, buyer_id)
SELECT
(SELECT id FROM myapp_magazine ORDER BY random() LIMIT 1),
(SELECT id FROM myapp_buyer ORDER BY random() LIMIT 1)
FROM
generate_series(1, 10000000);