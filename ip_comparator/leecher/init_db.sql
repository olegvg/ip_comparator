CREATE TYPE d_state AS ENUM
  ('dirty', 'clean');

CREATE TABLE iptable
  (
    user_id integer,
    ip_address inet,
    t_date timestamp with time zone NOT NULL,
    CONSTRAINT iptable_pkey PRIMARY KEY (t_date),
    CONSTRAINT user_ip_cst UNIQUE (user_id, ip_address)
  );

CREATE TABLE date_marker
  (
    id bigserial NOT NULL,
    end_marker timestamp with time zone,
    state d_state,
    CONSTRAINT date_marker_pkey PRIMARY KEY (id)
  );

CREATE OR REPLACE FUNCTION seek_window()
  RETURNS TABLE(interval_id bigint, user_id integer, ip_address inet, t_date timestamp with time zone) AS
  $BODY$
    DECLARE
      last_timestamp timestamp with time zone;
      end_marker timestamp with time zone;
      rec_id bigint;
    BEGIN
      SELECT max(td.t_date) INTO last_timestamp FROM iptable as td;
      IF last_timestamp IS NULL THEN
        RAISE NOTICE 'iptable has not filled yet';
        RETURN;
      END IF;
      SELECT max(dm.end_marker) INTO end_marker FROM date_marker as dm;
      IF end_marker IS NULL THEN
        RAISE NOTICE 'date_marker is empty, start with epoch';
        end_marker = to_timestamp(0);
      END IF;
      IF end_marker = last_timestamp THEN
        RETURN;
      END IF;
        INSERT INTO date_marker(end_marker, state) VALUES(last_timestamp, 'dirty') RETURNING id INTO rec_id;
        RETURN QUERY SELECT rec_id as interval_id, it.user_id, it.ip_address, it.t_date FROM iptable as it WHERE it.t_date > end_marker;
    END;
  $BODY$
  LANGUAGE plpgsql;

