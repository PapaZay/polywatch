
CREATE EXTENSION IF NOT EXISTS timescaledb;


CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


SELECT extname, extversion FROM pg_extension WHERE extname = 'timescaledb';