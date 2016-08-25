INSERT INTO courses (course_id, course_name, code) VALUES
  (1,	'Python-Base', 'P012345'),
  (2,	'Python-Database',	'P234567'),
  (3, 'HTML',	'H345678'),
  (4,	'Java-Base',	'J456789'),
  (5,	'JavaScript-Base', 'JS43210');


INSERT INTO users (user_id, user_name, email, status, phone, m_phone) VALUES
  (1,	'Stas Savchuk',	'stas@savchuk.me',	TRUE,	'+380505015275',	'+380505015275'),
  (2,	'Marko Savchuk',	'makro@savchuk.me',	FALSE,	'+380506070703',	'+380506070703'),
  (3,	'Andrii Dvoiak',	'andrii@dvoiak.me',	TRUE,	'+380505050505', NULL),
  (4,	'Taras Kurus',	'kurus@gmail.com',	FALSE,	NULL, NULL);


INSERT INTO records (rec_id, user_id, course_id) VALUES
  (1,	1,	1),
  (2,	1,	2),
  (3,	4,  1),
  (4,	2,	5);