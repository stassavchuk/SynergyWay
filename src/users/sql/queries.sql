-- SELECT user_name, email, status FROM users

-- SELECT course_name, code FROM courses


-- OPTION #1
-- SELECT users.user_name, users.email, users.phone, users.m_phone, users.status, courses.course_name
-- FROM users, courses, records
-- WHERE users.user_id = 1 AND users.user_id = records.user_id AND records.course_id = courses.course_id

-- OPTION #2
SELECT * FROM users
WHERE user_id = 1

SELECT course_name FROM records, courses
WHERE records.user_id = 1 AND records.course_id = courses.course_id