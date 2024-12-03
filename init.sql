CREATE SCHEMA IF NOT EXISTS service_identity;

-- Criar sequência para tabela customers
CREATE SEQUENCE customers_id_seq;

-- Criar tabela customers
CREATE TABLE customers (
    id INTEGER PRIMARY KEY DEFAULT nextval('customers_id_seq'),
    name VARCHAR(120) NULL,
    email VARCHAR(80) NULL,
    national_id VARCHAR(11) UNIQUE NOT NULL,
    registration_status int2 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);


INSERT INTO customers (id, name, email, national_id, registration_status, created_at, updated_at)
VALUES (nextval('customers_id_seq'), '', '', '00000000000', 2, NOW(), NULL);

INSERT INTO customers (id, name, email, national_id, registration_status, created_at, updated_at)
VALUES (nextval('customers_id_seq'), 'João Oliveira', 'joao@example.com', '11111111111', 1, NOW(), NULL);


-- Criar tabela customers
CREATE TABLE customers (
    id INTEGER PRIMARY KEY DEFAULT nextval('customers_id_seq'),
    name VARCHAR(120) NULL,
    email VARCHAR(80) NULL,
    national_id VARCHAR(11) UNIQUE NOT NULL,
    registration_status int2 NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);