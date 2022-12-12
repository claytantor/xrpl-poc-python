-- INSERT INTO wallet (wallet_id,seed,private_key,public_key,classic_address,created_at,updated_at,fiat_i8n_currency) VALUES
-- 	 (8,NULL,NULL,NULL,'rhcEvK2vuWNw5mvm3JQotG6siMw1iGde1Y','2021-12-22 19:10:25.000','2021-12-22 19:10:25.000','USD');
-- INSERT INTO xumm_payload (xumm_payload_id,body,webhook_body,created_at,updated_at,payload_uuidv4,wallet_id,payment_item_id,is_signed,txid) VALUES
-- 	 (62,'{"uuid": "ebfd5cd6-462b-46e1-9eeb-4e9ad2e37884", "next": {"always": "https://xumm.app/sign/ebfd5cd6-462b-46e1-9eeb-4e9ad2e37884"}, "refs": {"qr_png": "https://xumm.app/sign/ebfd5cd6-462b-46e1-9eeb-4e9ad2e37884_q.png", "qr_matrix": "https://xumm.app/sign/ebfd5cd6-462b-46e1-9eeb-4e9ad2e37884_q.json", "qr_uri_quality_opts": ["m", "q", "h"], "websocket_status": "wss://xumm.app/sign/ebfd5cd6-462b-46e1-9eeb-4e9ad2e37884"}, "pushed": false}',NULL,'2022-12-06 19:24:29.045517','2022-12-06 19:24:29.045524','ebfd5cd6-462b-46e1-9eeb-4e9ad2e37884',8,NULL,0,NULL),
-- 	 (63,'{"uuid": "ee7937df-46c5-49ed-96bb-f3af9244de0d", "next": {"always": "https://xumm.app/sign/ee7937df-46c5-49ed-96bb-f3af9244de0d"}, "refs": {"qr_png": "https://xumm.app/sign/ee7937df-46c5-49ed-96bb-f3af9244de0d_q.png", "qr_matrix": "https://xumm.app/sign/ee7937df-46c5-49ed-96bb-f3af9244de0d_q.json", "qr_uri_quality_opts": ["m", "q", "h"], "websocket_status": "wss://xumm.app/sign/ee7937df-46c5-49ed-96bb-f3af9244de0d"}, "pushed": false}',NULL,'2022-12-06 19:28:03.487779','2022-12-06 19:28:03.487785','ee7937df-46c5-49ed-96bb-f3af9244de0d',8,NULL,0,NULL),
-- 	 (64,'{"uuid": "22af42a9-8f62-4246-8000-9ff84f00d2c6", "next": {"always": "https://xumm.app/sign/22af42a9-8f62-4246-8000-9ff84f00d2c6"}, "refs": {"qr_png": "https://xumm.app/sign/22af42a9-8f62-4246-8000-9ff84f00d2c6_q.png", "qr_matrix": "https://xumm.app/sign/22af42a9-8f62-4246-8000-9ff84f00d2c6_q.json", "qr_uri_quality_opts": ["m", "q", "h"], "websocket_status": "wss://xumm.app/sign/22af42a9-8f62-4246-8000-9ff84f00d2c6"}, "pushed": false}',NULL,'2022-12-06 19:34:27.074418','2022-12-06 19:34:27.074426','22af42a9-8f62-4246-8000-9ff84f00d2c6',8,NULL,0,NULL),
-- 	 (65,'{"uuid": "ad0a3b30-d9f8-4f48-9940-9487543e9461", "next": {"always": "https://xumm.app/sign/ad0a3b30-d9f8-4f48-9940-9487543e9461"}, "refs": {"qr_png": "https://xumm.app/sign/ad0a3b30-d9f8-4f48-9940-9487543e9461_q.png", "qr_matrix": "https://xumm.app/sign/ad0a3b30-d9f8-4f48-9940-9487543e9461_q.json", "qr_uri_quality_opts": ["m", "q", "h"], "websocket_status": "wss://xumm.app/sign/ad0a3b30-d9f8-4f48-9940-9487543e9461"}, "pushed": false}',NULL,'2022-12-06 20:03:16.357684','2022-12-06 20:03:16.357691','ad0a3b30-d9f8-4f48-9940-9487543e9461',8,NULL,1,'2A733238491F6BCACD00A2C1FBF2CB14FC527A3EEEAD1F81FC87B90C80AE8737'),
-- 	 (66,'{"uuid": "fc631445-63df-4d98-b387-592119de819a", "next": {"always": "https://xumm.app/sign/fc631445-63df-4d98-b387-592119de819a"}, "refs": {"qr_png": "https://xumm.app/sign/fc631445-63df-4d98-b387-592119de819a_q.png", "qr_matrix": "https://xumm.app/sign/fc631445-63df-4d98-b387-592119de819a_q.json", "qr_uri_quality_opts": ["m", "q", "h"], "websocket_status": "wss://xumm.app/sign/fc631445-63df-4d98-b387-592119de819a"}, "pushed": false}',NULL,'2022-12-06 20:28:37.749548','2022-12-06 20:28:37.749555','fc631445-63df-4d98-b387-592119de819a',8,NULL,1,'0D6534513E1A179B53183BACAB67A23A65A7788FABB4339EE8C823FC0B4D1F1F');     
-- INSERT INTO payment_item (payment_item_id,fiat_i8n_currency,fiat_i8n_price,wallet_id,name,description,sku_id,created_at,updated_at) VALUES
-- 	 (3,'USD',0.21,8,'Tootsie Roll Chocolate Midgees','Tootsie Roll Chocolatey Twist Midgees Resealable Standup Bag, Peanut Free, Gluten Free original, Allergy Friendly, Mini Midgees','bd209ac51b','2022-11-14 17:25:12.317136','2022-11-14 17:25:12.317142'),
-- 	 (4,'USD',0.16,8,'Atomic Fireball Jawbdreaker - Single Wrapped','Red hot flavor: Atomic Fireballs are the original super intense cinnamon jawbreaker candy that will leave you wanting more; Exhilarate your taste buds with their seriously fiery cinnamon sweetness
-- ','033ac306b6','2022-11-22 15:47:21.344198','2022-11-22 15:47:21.344205'),
-- 	 (5,'USD',0.21,8,'A Special Pony','The cute pink pony ran down the road looking slightly uncomfortable. She gave her hand a shake of an uncertain look.','KhiHwJNo4Vts','2022-12-08 17:46:47.805462','2022-12-08 17:46:47.805469');
INSERT INTO file_uploads (id,"type",file_path,file_name,file_size,original_name,created_at,updated_at,payment_item_id) VALUES
	 (3,'PaymentItemImage','https://s3.us-west-2.amazonaws.com/dev.xurlpay.org/uploaded_images/65c74114-c2c9-444b-9c6f-a579123fa77e.png','65c74114-c2c9-444b-9c6f-a579123fa77e.png',0,'65c74114-c2c9-444b-9c6f-a579123fa77e.png','2022-11-15 01:25:13.182871','2022-11-15 01:25:13.182878',3),
	 (7,'PaymentItemImage','https://s3.us-west-2.amazonaws.com/dev.xurlpay.org/uploaded_images/4217f5c3-d8e1-49e4-a955-803cc35ca8c2.png','4217f5c3-d8e1-49e4-a955-803cc35ca8c2.png',0,'4217f5c3-d8e1-49e4-a955-803cc35ca8c2.png','2022-12-09 01:19:37.063060','2022-12-09 01:19:37.063063',4),
	 (9,'PaymentItemImage','https://s3.us-west-2.amazonaws.com/dev.xurlpay.org/uploaded_images/aeaa66aa-48f3-491f-8595-722c5555f3e5.png','aeaa66aa-48f3-491f-8595-722c5555f3e5.png',0,'aeaa66aa-48f3-491f-8595-722c5555f3e5.png','2022-12-09 01:46:48.420462','2022-12-09 01:46:48.420468',5);