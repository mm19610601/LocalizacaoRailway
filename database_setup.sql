-- Database setup script for Railway PostgreSQL
-- Run this script to create the required tables if they don't exist

-- Create utilizadores table
CREATE TABLE IF NOT EXISTS utilizadores (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    nome_completo TEXT,
    funcao TEXT,
    telemovel TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create localizacoes table
CREATE TABLE IF NOT EXISTS localizacoes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    latitude NUMERIC(10, 6) NOT NULL,
    longitude NUMERIC(10, 6) NOT NULL,
    precisao NUMERIC(5, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES utilizadores(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_localizacoes_user_id ON localizacoes(user_id);
CREATE INDEX IF NOT EXISTS idx_localizacoes_timestamp ON localizacoes(timestamp);
CREATE INDEX IF NOT EXISTS idx_localizacoes_coordinates ON localizacoes(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_utilizadores_username ON utilizadores(username);

-- Insert sample data (optional - remove if not needed)
INSERT INTO utilizadores (username, password, nome_completo, funcao, telemovel) 
VALUES 
    ('admin', 'admin123', 'Administrador', 'Admin', '969081497'),
    ('mmonteiro', '19610601-mM', 'Eng° Miguel Monteiro', 'Admin', NULL)
ON CONFLICT (username) DO NOTHING;

-- Add some sample locations (optional - remove if not needed)
DO $$
DECLARE
    admin_id INTEGER;
    mmonteiro_id INTEGER;
BEGIN
    SELECT id INTO admin_id FROM utilizadores WHERE username = 'admin';
    SELECT id INTO mmonteiro_id FROM utilizadores WHERE username = 'mmonteiro';
    
    IF admin_id IS NOT NULL THEN
        INSERT INTO localizacoes (user_id, latitude, longitude, precisao, timestamp) 
        VALUES 
            (admin_id, 39.500000, -8.700000, 9.00, '2025-07-21 13:18:50'),
            (admin_id, 39.600000, -8.700000, 9.00, '2025-07-21 13:18:54'),
            (admin_id, 39.700000, -8.700000, 9.00, '2025-07-21 13:18:58')
        ON CONFLICT DO NOTHING;
    END IF;
END $$;

-- Grant necessary permissions (adjust as needed for your Railway setup)
-- Note: These might not be necessary depending on your Railway configuration
-- GRANT ALL PRIVILEGES ON TABLE utilizadores TO your_app_user;
-- GRANT ALL PRIVILEGES ON TABLE localizacoes TO your_app_user;
-- GRANT ALL PRIVILEGES ON SEQUENCE utilizadores_id_seq TO your_app_user;
-- GRANT ALL PRIVILEGES ON SEQUENCE localizacoes_id_seq TO your_app_user;

-- Create a view for location statistics (optional)
CREATE OR REPLACE VIEW location_stats AS
SELECT 
    u.id as user_id,
    u.username,
    u.nome_completo,
    COUNT(l.id) as total_locations,
    MIN(l.timestamp) as first_location,
    MAX(l.timestamp) as last_location,
    AVG(l.precisao) as avg_precision
FROM utilizadores u
LEFT JOIN localizacoes l ON u.id = l.user_id
GROUP BY u.id, u.username, u.nome_completo;

-- Create a function to clean old locations (older than 1 year)
CREATE OR REPLACE FUNCTION cleanup_old_locations()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM localizacoes 
    WHERE timestamp < NOW() - INTERVAL '1 year';
    
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Optional: Create a trigger to automatically update a last_updated timestamp
ALTER TABLE utilizadores ADD COLUMN IF NOT EXISTS last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

CREATE OR REPLACE FUNCTION update_utilizador_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_utilizador_update ON utilizadores;
CREATE TRIGGER trigger_utilizador_update
    BEFORE UPDATE ON utilizadores
    FOR EACH ROW
    EXECUTE FUNCTION update_utilizador_timestamp();

-- Show table structure for verification
\d utilizadores;
\d localizacoes;

-- Show sample data counts
SELECT 'utilizadores' as table_name, COUNT(*) as record_count FROM utilizadores
UNION ALL
SELECT 'localizacoes' as table_name, COUNT(*) as record_count FROM localizacoes;
