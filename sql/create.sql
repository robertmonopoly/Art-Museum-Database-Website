CREATE TYPE User_Role AS ENUM ('USER','ADMIN');
CREATE TYPE Sex AS ENUM ('FEMALE', 'MALE', 'OTHER');
CREATE TYPE MembershipType AS ENUM ('NONE','BASIC', 'SILVER','GOLD');

CREATE TABLE images (
    image_id UUID PRIMARY KEY,
    bytes BYTEA NOT NULL
);

CREATE TABLE artworks (
    object_number VARCHAR PRIMARY KEY,
    artist TEXT NOT NULL,
    artwork_title VARCHAR (256) UNIQUE NOT NULL,
    made_on DATE NOT NULL,
    object_type TEXT NOT NULL,
    image_id UUID UNIQUE NOT NULL REFERENCES images(image_id)
);

CREATE TABLE user_account (
    user_id UUID PRIMARY KEY,
    first_name VARCHAR (60) NOT NULL, 
    last_name VARCHAR (60) NOT NULL,
    email VARCHAR (100) NOT NULL UNIQUE,
    date_of_birth DATE NOT NULL,
    membership MembershipType NOT NULL,
    account_status VARCHAR(2) NOT NULL
);

CREATE TABLE user_login (
    user_id UUID PRIMARY KEY REFERENCES user_account(user_id),
    user_role User_Role NOT NULL,
    user_name TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL UNIQUE
);

CREATE TABLE gift_shop_item (
    gift_SKU TEXT PRIMARY KEY,
    gift_name TEXT NOT NULL UNIQUE,
    gift_type TEXT NOT NULL,
    gift_price MONEY NOT NULL
);

CREATE TABLE gift_shop_sales (
    gift_transaction_id UUID PRIMARY KEY,
    gift_SKU TEXT NOT NULL,
    gift_transaction_at TIMESTAMP NOT NULL,
    user_id UUID NOT NULL REFERENCES user_account(user_id)
);

CREATE TABLE gift_shop_item_inventory (
    gift_serial_number UUID PRIMARY KEY,
    gift_SKU TEXT NOT NULL REFERENCES gift_shop_item(gift_SKU),
    gift_transaction_id UUID REFERENCES gift_shop_sales(gift_transaction_id)
);

CREATE TABLE employees (
    employee_id UUID PRIMARY KEY,
    employee_membership MembershipType NOT NULL,
    employee_first_name VARCHAR (60) NOT NULL,  
    employee_last_name VARCHAR (60) NOT NULL,
    employee_email VARCHAR (100) NOT NULL UNIQUE,
    employee_ssn TEXT NOT NULL,
    employee_phone_number TEXT NOT NULL,
    employee_date_of_birth DATE NOT NULL,
    salary MONEY NOT NULL
);

CREATE TABLE exhibitions (
    exhib_id UUID PRIMARY KEY,
    exhib_at TIMESTAMP NOT NULL,
    exhib_ticket_price MONEY NOT NULL,
    exhib_gallery TEXT NOT NULL,
    exhib_title TEXT NOT NULL,
    curator TEXT NOT NULL,
    exhib_artists TEXT NOT NULL
);

CREATE TABLE ticket_sales(
    event_transac_id UUID PRIMARY KEY, 
    user_id UUID NOT NULL REFERENCES user_account(user_id), 
    transact_at DATE NOT NULL,
    event_id UUID NOT NULL,
    event_name TEXT NOT NULL,
    num_tickets INTEGER NOT NULL,
    user_price MONEY NOT NULL
);

CREATE TABLE films (
    film_id UUID PRIMARY KEY,
    viewing_at TIMESTAMP NOT NULL,
    film_title TEXT NOT NULL,
    film_ticket_price MONEY NOT NULL,
    duration_min INTEGER NOT NULL,
    film_director TEXT NOT NULL,
    film_rating TEXT NOT NULL,
    image_id UUID UNIQUE NOT NULL REFERENCES images(image_id)
);

CREATE TABLE donation (
    donation_transaction_id UUID PRIMARY KEY,
    donator_email VARCHAR (100) NOT NULL,
    donation_on DATE NOT NULL,
    donation_amount MONEY NOT NULL
);

CREATE TABLE notifs (
    event_id UUID PRIMARY KEY,
    event_title TEXT NOT NULL,
    event_at TIMESTAMP NOT NULL
);

CREATE OR REPLACE FUNCTION exhibit_insert_trigger_fnc()
  RETURNS trigger AS
$$
BEGIN
    INSERT INTO notifs (event_id, event_title ,event_at)
        VALUES (NEW.exhib_id, NEW.exhib_title, NEW.exhib_at);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER new_exhib
    AFTER INSERT 
    ON "exhibitions"
    FOR EACH ROW
    EXECUTE PROCEDURE exhibit_insert_trigger_fnc();

-- CREATE TRIGGER new_film
--         AFTER INSERT
        -- ON "films"
--         FOR EACH ROW
--         EXECUTE FUNCTION film_insert_trigger_fnc();

CREATE OR REPLACE FUNCTION update_member_ticket_price()
  RETURNS trigger AS
$$
BEGIN
    IF (user_account.membership = 'BASIC') 
    WHERE user_account.user_id = ticket_sales.user_id THEN
        -- apply 10% discount 
        UPDATE "ticket_sales" SET NEW.user_price = user_price * 0.9;
        SELECT CONCAT('Your discount is 10%. Your new price is $', NEW.user_price) AS message;
    END IF;
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER exhib_discount_mem
    AFTER INSERT
    ON "ticket_sales"
    FOR EACH ROW
    EXECUTE PROCEDURE update_member_ticket_price();

CREATE TRIGGER film_discount_mem
    AFTER INSERT
    ON "ticket_sales"
    FOR EACH ROW
    EXECUTE PROCEDURE update_member_ticket_price();