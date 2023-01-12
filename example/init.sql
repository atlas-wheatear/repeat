CREATE TABLE users (
   username VARCHAR NOT NULL UNIQUE,
   password VARCHAR NOT NULL
);

INSERT INTO users VALUES
    ('admin', 'FLAG{th1s_41nt-g0oD-c0d3}');
