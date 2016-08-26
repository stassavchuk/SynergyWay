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
