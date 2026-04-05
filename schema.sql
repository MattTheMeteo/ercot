CREATE TABLE IF NOT EXISTS price_locations (
    id SERIAL PRIMARY KEY,
    iso TEXT NOT NULL,
    location_type TEXT NOT NULL,
    location TEXT NOT NULL,
    market TEXT NOT NULL,
    resolution TEXT NOT NULL,
    UNIQUE(iso, location, market)
);

CREATE TABLE IF NOT EXISTS price_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    price NUMERIC NOT NULL,
    location_id INTEGER NOT NULL REFERENCES price_locations(id),
    UNIQUE(timestamp, location_id)
);

CREATE INDEX IF NOT EXISTS idx_price_data_timestamp ON price_data(timestamp);
CREATE INDEX IF NOT EXISTS idx_price_data_location_id ON price_data(location_id);
