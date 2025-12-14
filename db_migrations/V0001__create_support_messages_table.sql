CREATE TABLE IF NOT EXISTS support_messages (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    sender VARCHAR(50) NOT NULL CHECK (sender IN ('user', 'support', 'admin')),
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_support_messages_timestamp ON support_messages(timestamp DESC);
CREATE INDEX idx_support_messages_sender ON support_messages(sender);