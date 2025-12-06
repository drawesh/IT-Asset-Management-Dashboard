CREATE TABLE assets (
    asset_id SERIAL PRIMARY KEY,
    asset_name VARCHAR(100),
    asset_type VARCHAR(50),
    status VARCHAR(50),
    purchase_date DATE,
    warranty_expiry DATE,
    assigned_to VARCHAR(100),
    cost NUMERIC,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
