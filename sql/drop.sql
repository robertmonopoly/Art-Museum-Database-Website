DROP TRIGGER IF EXISTS film_discount_mem ON ticket_sales CASCADE;

DROP TRIGGER IF EXISTS exhib_discount_mem ON ticket_sales CASCADE;

DROP FUNCTION IF EXISTS update_member_ticket_price CASCADE;

DROP TRIGGER IF EXISTS new_film ON films CASCADE;

DROP TRIGGER IF EXISTS new_exhib ON exhibitions CASCADE;

DROP FUNCTION IF EXISTS exhibit_insert_trigger_fnc CASCADE;

DROP TABLE IF EXISTS notifs CASCADE;

DROP TABLE IF EXISTS donation CASCADE;

DROP TABLE IF EXISTS films CASCADE;

DROP TABLE IF EXISTS ticket_sales CASCADE;

DROP TABLE IF EXISTS exhibitions CASCADE;

DROP TABLE IF EXISTS employees CASCADE;

DROP TABLE IF EXISTS gift_shop_item_inventory CASCADE;

DROP TABLE IF EXISTS gift_shop_sales CASCADE;

DROP TABLE IF EXISTS gift_shop_item CASCADE;

DROP TABLE IF EXISTS user_login CASCADE;

DROP TABLE IF EXISTS user_account CASCADE;

DROP TABLE IF EXISTS artworks CASCADE;

DROP TABLE IF EXISTS images CASCADE;

DROP TYPE MembershipType CASCADE;

DROP TYPE Sex CASCADE;

DROP TYPE User_Role;

