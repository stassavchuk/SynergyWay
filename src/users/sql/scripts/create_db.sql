CREATE OR REPLACE FUNCTION create_db(db_name VARCHAR(32))
  RETURNS void AS
  $func$
      BEGIN
        IF exists(SELECT 1 FROM pg_database WHERE datname = db_name) THEN
        ELSE
          PERFORM dblink_exec('dbname=' || current_database(), 'CREATE DATABASE ' || quote_ident(db_name));
        END IF;
      END;
  $func$ LANGUAGE plpgsql;

