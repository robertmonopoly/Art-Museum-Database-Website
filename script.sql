START TRANSACTION;
-- you can see that the queries are related to each other by the same user_uuid (first value in the column)

-- admin with no membership
INSERT INTO user_account VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'mich', 'nguyen','(410 cedar point,league city,TX,77573)', 'mich@gmail.com','832-853-9706', 'FEMALE', '02-20-2003', 'NONE');
INSERT INTO user_login VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'ADMIN', 'mich@gmail.com','$2b$12$fpXMLIw1ALlrjxuAJD8xquon54dBCWPmXP5t7WeTRAk9/2eKIo3x2','2023-02-01 20:56:31');
-- user with no membership
INSERT INTO user_account VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'joe','mom', '(324 oak forest,poop island,CA,34325)', 'someone@gmail.com', '432-433-3244', 'MALE', '02-13-1996', 'NONE');
INSERT INTO user_login VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'USER', 'someone@gmail.com','$2b$12$CriXFp4IvckRl4UdaDmadu5UTLiTGG/aYjHXbQJfG.A8r9mqwrcWO','2023-11-04 07:22:02');
-- user with silver membership
INSERT INTO user_account VALUES ('6be41a29-8fd3-407e-9b37-784a30492237', 'alex','homer', '(123 cedar fork,sten island,TX,12325)', 'other@gmail.com', '332-456-3244', 'FEMALE', '06-13-1998', 'SILVER');
INSERT INTO user_login VALUES ('6be41a29-8fd3-407e-9b37-784a30492237', 'USER', 'other@gmail.com','$2b$12$PFACfUxSzEbglUTMopXx4u1w52RcaJa8zelcqGLdJm5dlMwbR91KK','2023-12-14 04:30:02');
-- user with basic membership
INSERT INTO user_account VALUES ('c8304586-5661-4db7-8e75-4dd44b4f7648', 'yves','chu', '(861 country side,spoon island,FL,324225)', 'her@gmail.com', '112-426-3265', 'FEMALE', '12-11-2002', 'BASIC');
INSERT INTO user_login VALUES ('c8304586-5661-4db7-8e75-4dd44b4f7648', 'USER', 'her@gmail.com','$2b$12$WhzUm6vuWEG/0tDXneCHuuZljGnH.wQcCidwqz0yM9WGbp8cN5sru','2023-05-04 07:22:02');

-- these are for the report generation of how many of a certain item was sold in a day
INSERT INTO gift_shop_item VALUES ('toteb-art2', 'totebag','accessories','13.99');

INSERT INTO gift_shop_item VALUES ('mugs-art1', 'mug','living','10.99');

INSERT INTO gift_shop_item VALUES ('pai-ang-bla', 'paintbrush','supplies','9.99');

INSERT INTO gift_shop_sales VALUES ('3457ab7b-9ecb-48e2-a8d0-2b921fe12747', 'toteb-art2', '2023-03-27 10:36:01','e3a9dd72-cad1-11ed-afa1-0242ac120002');

INSERT INTO gift_shop_sales VALUES ('6be41a29-8fd3-407e-9b37-784a30492237', 'mugs-art1', '2023-03-27 13:00:58', '')
-- CREATE TABLE gift_shop_item (
--     gift_SKU TEXT PRIMARY KEY,
--     gift_name TEXT NOT NULL,
--     gift_type TEXT NOT NULL,
--     gift_price MONEY NOT NULL
-- );

-- CREATE TABLE gift_shop_sales (
--     gift_transaction_id UUID PRIMARY KEY,
--     gift_SKU TEXT NOT NULL,
--     gift_transaction_at TIMESTAMP NOT NULL,
--     user_id UUID NOT NULL REFERENCES user_account(user_id)
-- );
COMMIT;