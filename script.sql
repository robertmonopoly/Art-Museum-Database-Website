START TRANSACTION;

INSERT INTO user_account VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'mich', 'nguyen','(410 cedar point,league city,TX,77573)', 'mich@gmail.com','832-853-9706', 'FEMALE', '02-20-2003', 'BASIC');

INSERT INTO user_account VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'joe','ng', '(324 oak forest,poop island,CA,34325)', 'deeznuts@gmail.com', '432-433-3244', 'MALE', '02-13-1996', 'NONE');

INSERT INTO user_login VALUES ('e3a9dc6e-cad1-11ed-afa1-0242ac120002', 'ADMIN', 'mich@gmail.com','$2b$12$wtVgUvQfX5AuuIP8d7eIk./68GBDkYd6sOVG5eWsxBsC94b0pyFTS','2027-02-01 20:56:31');

INSERT INTO user_login VALUES ('e3a9dd72-cad1-11ed-afa1-0242ac120002', 'USER', 'deeznuts@gmail.com','$2b$12$CriXFp4IvckRl4UdaDmadu5UTLiTGG/aYjHXbQJfG.A8r9mqwrcWO','2004-11-04 07:22:02');

COMMIT;