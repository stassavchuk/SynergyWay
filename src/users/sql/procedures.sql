-- This file contains procedures that are already work

--------------------------------------------------------------------------
--                           SELECT FUNCTIONS                           --
--------------------------------------------------------------------------

-- Select all users
CREATE OR REPLACE FUNCTION all_users()
  RETURNS TABLE (
    user_id   INTEGER,
    user_name   VARCHAR (64),
    email VARCHAR (128),
    status BOOLEAN) AS
$func$
BEGIN
   RETURN QUERY
   SELECT users.user_id, users.user_name, users.email, users.status
   FROM  users
   ORDER  BY users.user_id DESC;
END
$func$  LANGUAGE plpgsql;

-- To select all users run the next:
SELECT * FROM all_users()

-----------------------------------------------------------------------

-- Select one user data
CREATE OR REPLACE FUNCTION user_data(u_id INTEGER)
  RETURNS TABLE (
    user_id   INTEGER,
    user_name   VARCHAR (64),
    email VARCHAR (128),
    status BOOLEAN,
    phone VARCHAR(16),
    m_phone VARCHAR(16)
  ) AS
$func$
BEGIN
   RETURN QUERY
   SELECT * FROM  users
   WHERE users.user_id = u_id;
END
$func$  LANGUAGE plpgsql;

-- To select user data of needed ID, run the next:
SELECT * FROM user_data(1)

---------------------------------------------------------------------

-- Select one user courses
CREATE OR REPLACE FUNCTION user_courses(u_id INTEGER)
  RETURNS TABLE (
    course_name   VARCHAR (64)
  ) AS
$func$
BEGIN
   RETURN QUERY
   SELECT courses.course_name FROM records, courses
   WHERE records.user_id = u_id AND records.course_id = courses.course_id;
END
$func$  LANGUAGE plpgsql;

-- To select user courses, run the next:
SELECT * FROM user_courses(1);

--------------------------------------------------------------------

-- Select all courses
CREATE OR REPLACE FUNCTION all_courses()
  RETURNS TABLE (
    course_id INTEGER,
    course_name   VARCHAR (64),
    code VARCHAR(8)
  ) AS
$func$
BEGIN
   RETURN QUERY
   SELECT * FROM courses;
END
$func$  LANGUAGE plpgsql;

-- To execute, tun the following:
SELECT * FROM all_courses()

-------------------------------------------------------------------