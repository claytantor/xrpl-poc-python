# Single-database configuration for Flask.


ALTER TABLE wallet ADD COLUMN created_at DATETIME;
ALTER TABLE wallet ADD COLUMN updated_at DATETIME;
ALTER TABLE wallet ADD COLUMN fiat_i8n_currency VARCHAR(3);
UPDATE wallet SET fiat_i8n_currency='USD';

