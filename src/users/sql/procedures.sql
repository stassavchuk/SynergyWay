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
SELECT * FROM all_users();

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
SELECT * FROM user_data(1);

---------------------------------------------------------------------

-- Select one user courses
CREATE OR REPLACE FUNCTION user_courses(u_id INTEGER)
  RETURNS TABLE (
    course_id INTEGER,
    course_name   VARCHAR (64)
  ) AS
$func$
BEGIN
   RETURN QUERY
   SELECT courses.course_id, courses.course_name FROM records, courses
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
SELECT * FROM all_courses();

-------------------------------------------------------------------


--------------------------------------------------------------------------
--                        APPEND/DELETE FUNCTIONS                       --
--------------------------------------------------------------------------


-- Should be tested.  !!!!!
-- Cause buds if some data is already stored in DB. Starts default value from 1, even if 1 is booked
CREATE OR REPLACE FUNCTION add_user(u_id INTEGER, u_name VARCHAR(64), u_email VARCHAR(128), u_status BOOLEAN, u_phone VARCHAR(16), u_m_phone VARCHAR(16))
  RETURNS void AS
  $func$
      BEGIN
        INSERT INTO users(user_id, user_name, email, status, phone, m_phone)
        VALUES(DEFAULT, u_name, u_email, u_status, u_phone, u_m_phone);
      END;
  $func$ LANGUAGE plpgsql;

SELECT add_user('new user', 'user@email.com', FALSE, '+000000000000', '+000000000000');

SELECT * FROM all_users();

-----------------------------------------------------------------------------------------------------------------------

-- Delete user
CREATE OR REPLACE FUNCTION delete_user(u_id INTEGER)
  RETURNS void AS
  $func$
      BEGIN
        DELETE FROM users WHERE users.user_id = u_id;
        -- DELETE FROM records WHERE records.user_id = u_id;
      END;
  $func$ LANGUAGE plpgsql;

SELECT delete_user(40);

SELECT * FROM all_users();

-------------------------------------------------------------------------------------------------------------------------

-- Update user

CREATE OR REPLACE FUNCTION update_user(u_id INTEGER, u_name VARCHAR(64), u_email VARCHAR(128), u_status BOOLEAN, u_phone VARCHAR(16), u_m_phone VARCHAR(16))
  RETURNS void AS
  $func$
      BEGIN
        UPDATE users SET (user_name, email, status, phone, m_phone) = (u_name, u_email, u_status, u_phone, u_m_phone)
        WHERE users.user_id = u_id;
      END;
  $func$ LANGUAGE plpgsql;

SELECT update_user(5, 'Stas Savchuk', 'stas@email.com', TRUE, '+000000000000', '+000000000000');

-----------------------------------------------------------------------------------------

-- Add course to user

CREATE OR REPLACE FUNCTION add_record(u_id INTEGER, c_id INTEGER)
  RETURNS void AS
  $func$
      BEGIN
        IF exists(SELECT 1 FROM records WHERE records.user_id = u_id AND records.course_id = c_id) THEN
        ELSE
          INSERT INTO records (rec_id, user_id, course_id) VALUES (DEFAULT,	u_id,	c_id);
        END IF;
      END;
  $func$ LANGUAGE plpgsql;

SELECT add_record(5, 2);

--------------------------------------------------------------------------------------

-- Delete all courses of user

CREATE OR REPLACE FUNCTION delete_all_records(u_id INTEGER)
  RETURNS void AS
  $func$
      BEGIN
        DELETE FROM records WHERE records.user_id = u_id;
      END;
  $func$ LANGUAGE plpgsql;

SELECT delete_all_records(5);

-------------------------------------------------------

-- Update records
--- !!!
--- Doesn't work with array[], to delete all record use delete_all_records()
--- Has the same problem with INSERT as add_user

CREATE OR REPLACE FUNCTION update_records(u_id INTEGER, course_list INTEGER[])
  RETURNS void AS
  $func$
      DECLARE
        c_id INTEGER;
      BEGIN
        DELETE FROM records WHERE records.user_id = u_id;

        FOREACH c_id IN ARRAY course_list LOOP
          INSERT INTO records (rec_id, user_id, course_id) VALUES (DEFAULT,	u_id,	c_id);
        END LOOP;
      END;
  $func$ LANGUAGE plpgsql;

SELECT update_records(5, array[1]);


-------------------------------------------------------------------------------------

--------------------------------------------------------------------------
--                        CREATING DATABASE/TABLES                      --
--------------------------------------------------------------------------

-- Important extension
CREATE EXTENSION dblink;

CREATE OR REPLACE FUNCTION create_db(db_name VARCHAR(32))
  RETURNS void AS
  $func$
      BEGIN
        IF exists(SELECT 1 FROM pg_database WHERE datname = db_name) THEN
        ELSE
          PERFORM dblink_exec('dbname=' || current_database()   -- current db
                     , 'CREATE DATABASE ' || quote_ident(db_name));
        END IF;
      END;
  $func$ LANGUAGE plpgsql;


SELECT create_db('newDB');

----------------------------------------------------------
CREATE OR REPLACE FUNCTION create_db_with_tables(db_name VARCHAR(32))
  RETURNS void AS
  $func$
      BEGIN
        IF exists(SELECT 1 FROM pg_database WHERE datname = db_name) THEN
        ELSE
          PERFORM dblink_exec('dbname=' || current_database()   -- current db
                     , 'CREATE DATABASE ' || quote_ident(db_name));

          PERFORM dblink_exec('dbname=' || db_name,
            ' -- Table "user"
              CREATE TABLE IF NOT EXISTS "users" (
                  user_id     SERIAL        PRIMARY KEY,
                  user_name   VARCHAR (64)  NOT NULL,
                  email       VARCHAR (128) NOT NULL,
                  status      BOOLEAN       NOT NULL      DEFAULT FALSE,
                  phone       VARCHAR (16),
                  m_phone     VARCHAR (16)
              );

              -- Table "courses"
              CREATE TABLE IF NOT EXISTS "courses" (
                  course_id   SERIAL        PRIMARY KEY,
                  course_name VARCHAR (64)  NOT NULL,
                  code        VARCHAR (8)   NOT NULL
              );

              -- Table "records", the table aimed to connect user and courses as many-to-many
              CREATE TABLE IF NOT EXISTS "records" (
                  rec_id      SERIAL        PRIMARY KEY,
                  user_id     INTEGER       NOT NULL      REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
                  course_id   INTEGER       NOT NULL      REFERENCES courses (course_id) ON UPDATE CASCADE ON DELETE CASCADE
              );'
          );
        END IF;
      END;
  $func$ LANGUAGE plpgsql;

SELECT create_db_with_tables('dbWithTables');

------------------------------------------------------------------------------



---------------------------------------------------------------------------------
--                          ONE SCRIPT FOR EVERYTHING                          --
---------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION create_db_with_tables(db_name VARCHAR(32))
  RETURNS void AS
  $mainfunc$
      BEGIN
        IF exists(SELECT 1 FROM pg_database WHERE datname = db_name) THEN
        ELSE
          PERFORM dblink_exec('dbname=' || current_database()   -- current db
                     , 'CREATE DATABASE ' || quote_ident(db_name));

          PERFORM dblink_exec('dbname=' || db_name,
            ' -- Table "user"
              CREATE TABLE IF NOT EXISTS "users" (
                  user_id     SERIAL        PRIMARY KEY,
                  user_name   VARCHAR (64)  NOT NULL,
                  email       VARCHAR (128) NOT NULL,
                  status      BOOLEAN       NOT NULL      DEFAULT FALSE,
                  phone       VARCHAR (16),
                  m_phone     VARCHAR (16)
              );

              -- Table "courses"
              CREATE TABLE IF NOT EXISTS "courses" (
                  course_id   SERIAL        PRIMARY KEY,
                  course_name VARCHAR (64)  NOT NULL,
                  code        VARCHAR (8)   NOT NULL
              );

              -- Table "records", the table aimed to connect user and courses as many-to-many
              CREATE TABLE IF NOT EXISTS "records" (
                  rec_id      SERIAL        PRIMARY KEY,
                  user_id     INTEGER       NOT NULL      REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
                  course_id   INTEGER       NOT NULL      REFERENCES courses (course_id) ON UPDATE CASCADE ON DELETE CASCADE
              );

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

              -- Select one user courses
              CREATE OR REPLACE FUNCTION user_courses(u_id INTEGER)
                RETURNS TABLE (
                  course_id INTEGER,
                  course_name   VARCHAR (64)
                ) AS
              $func$
              BEGIN
                 RETURN QUERY
                 SELECT courses.course_id, courses.course_name FROM records, courses
                 WHERE records.user_id = u_id AND records.course_id = courses.course_id;
              END
              $func$  LANGUAGE plpgsql;

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

              -- Create user
              CREATE OR REPLACE FUNCTION add_user(u_id INTEGER, u_name VARCHAR(64), u_email VARCHAR(128), u_status BOOLEAN, u_phone VARCHAR(16), u_m_phone VARCHAR(16))
              RETURNS void AS
              $func$
                  BEGIN
                    INSERT INTO users(user_id, user_name, email, status, phone, m_phone)
                    VALUES(DEFAULT, u_name, u_email, u_status, u_phone, u_m_phone);
                  END;
              $func$ LANGUAGE plpgsql;

              -- Delete user
              CREATE OR REPLACE FUNCTION delete_user(u_id INTEGER)
                RETURNS void AS
                $func$
                    BEGIN
                      DELETE FROM users WHERE users.user_id = u_id;
                      -- DELETE FROM records WHERE records.user_id = u_id;
                    END;
                $func$ LANGUAGE plpgsql;

              CREATE OR REPLACE FUNCTION update_user(u_id INTEGER, u_name VARCHAR(64), u_email VARCHAR(128), u_status BOOLEAN, u_phone VARCHAR(16), u_m_phone VARCHAR(16))
              RETURNS void AS
              $func$
                  BEGIN
                    UPDATE users SET (user_name, email, status, phone, m_phone) = (u_name, u_email, u_status, u_phone, u_m_phone)
                    WHERE users.user_id = u_id;
                  END;
              $func$ LANGUAGE plpgsql;


              CREATE OR REPLACE FUNCTION update_records(u_id INTEGER, course_list INTEGER[])
                RETURNS void AS
                $func$
                    DECLARE
                      c_id INTEGER;
                    BEGIN
                      DELETE FROM records WHERE records.user_id = u_id;

                      FOREACH c_id IN ARRAY course_list LOOP
                        INSERT INTO records (rec_id, user_id, course_id) VALUES (DEFAULT,	u_id,	c_id);
                      END LOOP;
                    END;
                $func$ LANGUAGE plpgsql;
          '
          );
        END IF;
      END;
  $mainfunc$ LANGUAGE plpgsql;

SELECT create_db_with_tables('awesomeDB');