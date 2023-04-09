DROP TABLE IF EXISTS user_login;

DROP TABLE IF EXISTS donation;

DROP TABLE IF EXISTS calendar;

DROP TABLE IF EXISTS film_ticket_sales;

DROP TABLE IF EXISTS films;

DROP TABLE IF EXISTS exhib_ticket_sales;

DROP TABLE IF EXISTS exhibitions;

DROP TABLE IF EXISTS employees;

DROP TABLE IF EXISTS gift_shop_item_inventory;

DROP TABLE IF EXISTS gift_shop_sales;

DROP TABLE IF EXISTS gift_shop_item;

DROP TABLE IF EXISTS user_account;

DROP TABLE IF EXISTS artworks;

DROP TABLE IF EXISTS images;

DROP TYPE MembershipType;

DROP TYPE Sex;

DROP TYPE User_Role;

DROP TYPE User_Address;

DROP TYPE US_State;

DROP TRIGGER IF EXISTS insert_exhibition_trigger ON exhibitions;


DROP TRIGGER IF EXISTS insert_films_trigger ON films;

