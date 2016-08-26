CREATE OR REPLACE FUNCTION construct_db()
  RETURNS void AS
  $mainfunc$
      BEGIN
      -- Table "user"
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
      END;
$mainfunc$ LANGUAGE plpgsql;