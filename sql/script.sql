START TRANSACTION;
-- you can see that the queries are related to each other by the same user_uuid (first value in the column)

-- admin with no membership
INSERT INTO user_account VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'mich', 'nguyen', 'mich@gmail.com', '02-20-2003', 'NONE', '1');
INSERT INTO user_login VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'ADMIN', 'mich@gmail.com','$2b$12$fpXMLIw1ALlrjxuAJD8xquon54dBCWPmXP5t7WeTRAk9/2eKIo3x2');
-- user with no membership
INSERT INTO user_account VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'joe','mom','someone@gmail.com', '02-13-1996', 'NONE', '1');
INSERT INTO user_login VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'USER', 'someone@gmail.com','$2b$12$CriXFp4IvckRl4UdaDmadu5UTLiTGG/aYjHXbQJfG.A8r9mqwrcWO');
-- user with silver membership
INSERT INTO user_account VALUES ('6be41a29-8fd3-407e-9b37-784a30492237', 'alex','homer', 'other@gmail.com', '06-13-1998', 'SILVER', '1');
INSERT INTO user_login VALUES ('6be41a29-8fd3-407e-9b37-784a30492237', 'USER', 'other@gmail.com','$2b$12$PFACfUxSzEbglUTMopXx4u1w52RcaJa8zelcqGLdJm5dlMwbR91KK');
-- user with basic membership
INSERT INTO user_account VALUES ('c8304586-5661-4db7-8e75-4dd44b4f7648', 'yves','chu', 'her@gmail.com', '12-11-2002', 'BASIC', '1');
INSERT INTO user_login VALUES ('c8304586-5661-4db7-8e75-4dd44b4f7648', 'USER', 'her@gmail.com','$2b$12$WhzUm6vuWEG/0tDXneCHuuZljGnH.wQcCidwqz0yM9WGbp8cN5sru');

-- these are for the report generation of how many of a certain item was sold in an interval
INSERT INTO gift_shop_item VALUES ('toteb-art2', 'totebag','accessories','13.99');
INSERT INTO gift_shop_item VALUES ('toteb-art3', 'totebag','accessories','11.99');
INSERT INTO gift_shop_item VALUES ('toteb-art4', 'totebag','accessories','12.99');
INSERT INTO gift_shop_item VALUES ('toteb-art1', 'totebag','accessories','15.99');

INSERT INTO gift_shop_item VALUES ('mugs-art1', 'mug','living','9.99');
INSERT INTO gift_shop_item VALUES ('mugs-art3', 'mug','living','18.99');
INSERT INTO gift_shop_item VALUES ('mugs-art2', 'mug','living','12.99');
INSERT INTO gift_shop_item VALUES ('mugs-art6', 'mug','living','10.99');

INSERT INTO gift_shop_item VALUES ('pai-ang-bla', 'paintbrush','supplies','9.99');

INSERT INTO gift_shop_sales VALUES ('3457ab7b-9ecb-48e2-a8d0-2b921fe12747', 'toteb-art2', '2023-03-27 10:36:01','e3a9dd72-cad1-11ed-afa1-0242ac120002');
INSERT INTO gift_shop_sales VALUES ('b6cbac88-cb79-11ed-afa1-0242ac120002', 'toteb-art1', '2023-04-10 11:36:01','e3a9dd72-cad1-11ed-afa1-0242ac120002');
INSERT INTO gift_shop_sales VALUES ('ceca31ea-cc16-11ed-afa1-0242ac120002', 'toteb-art4', '2023-04-11 11:36:01','e3a9dd72-cad1-11ed-afa1-0242ac120002');
INSERT INTO gift_shop_sales VALUES ('1437c24c-cc17-11ed-afa1-0242ac120002', 'toteb-art3', '2023-04-13 11:36:01','e3a9dd72-cad1-11ed-afa1-0242ac120002');

INSERT INTO gift_shop_sales VALUES ('c7974efc-cb45-11ed-afa1-0242ac120002', 'mugs-art1', '2023-04-10 13:00:58', '6be41a29-8fd3-407e-9b37-784a30492237');
INSERT INTO gift_shop_sales VALUES ('b6cbb0b6-cb79-11ed-afa1-0242ac120002', 'mugs-art2', '2023-04-11 12:00:58', '6be41a29-8fd3-407e-9b37-784a30492237');
INSERT INTO gift_shop_sales VALUES ('d113ed03-2b3b-46a1-b0a5-1f8a234f3288', 'mugs-art6', '2023-04-12 11:00:58', '6be41a29-8fd3-407e-9b37-784a30492237');

INSERT INTO gift_shop_sales VALUES ('dc4f2f5e-cb45-11ed-afa1-0242ac120002', 'pai-ang-bla', '2023-04-14 14:08:52', 'c8304586-5661-4db7-8e75-4dd44b4f7648');
INSERT INTO gift_shop_sales VALUES ('ceca2fa6-cc16-11ed-afa1-0242ac120002', 'pai-cir-bla', '2023-04-15 14:08:52', 'c8304586-5661-4db7-8e75-4dd44b4f7648');
INSERT INTO gift_shop_sales VALUES ('f4db3386-27a0-4dfb-814b-e2e4e12ee98b', 'pai-cir-wht', '2023-04-11 14:08:52', 'e3a9dc6e-cad1-11ed-afa1-0242ac120002');

INSERT INTO donation VALUES ('b6cbb3e0-cb79-11ed-afa1-0242ac120002', 'mich@gmail.com', '2023-12-13 05:48:06', 5.05);

-- these are for the report generation of how many of a certain item was sold in a day
/*INSERT INTO exhibitions VALUES ('b6cbb3e0-cb79-11ed-afa1-0242ac120002', '2004-12-13 05:48:06', '5.99','gallery name','Exhibit: Flower', 'some curator', 'an artist');
INSERT INTO exhibitions VALUES ('b6cbb3e0-cb79-11ed-afa1-0242ac120002', '2004-12-13 05:48:06', '5.99','gallery name','Exhibit: Flower', 'some curator', 'an artist');
INSERT INTO exhib_ticket_sales VALUES ('f91e597a-cb90-11ed-afa1-0242ac120002', 'c8304586-5661-4db7-8e75-4dd44b4f7648', 'b6cbb3e0-cb79-11ed-afa1-0242ac120002', '2023-03-02 20:35:06');

INSERT INTO exhibitions VALUES ('f91e5c22-cb90-11ed-afa1-0242ac120002', '2013-05-09 02:01:37', '6.99','def name','Exhibit: Painting', 'another curator', 'some artist');
INSERT INTO exhib_ticket_sales VALUES ('cad242c1-fbcc-4d53-917c-e2c561d2df1c', 'c8304586-5661-4db7-8e75-4dd44b4f7648', 'f91e5c22-cb90-11ed-afa1-0242ac120002', '2023-04-10 20:35:06');

INSERT INTO films VALUES ('d88e557c-cb8e-11ed-afa1-0242ac120002', '2004-12-13 05:48:06', 'Film: Interstellar', '4.99', '124','some director', '5');
INSERT INTO film_ticket_sales VALUES ('f91e5ad8-cb90-11ed-afa1-0242ac120002', '6be41a29-8fd3-407e-9b37-784a30492237', 'd88e557c-cb8e-11ed-afa1-0242ac120002', '2023-03-02 20:35:06');

INSERT INTO films VALUES ('23382a5a-cb97-11ed-afa1-0242ac120002', '2013-08-19 06:36:03', 'Film: Matrix', '3.99', '121','some director', '4');
INSERT INTO film_ticket_sales VALUES ('233831f8-cb97-11ed-afa1-0242ac120002', '6be41a29-8fd3-407e-9b37-784a30492237', '23382a5a-cb97-11ed-afa1-0242ac120002', '2023-04-10 20:35:06');
*/

COMMIT;
