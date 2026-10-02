INSERT INTO employees (
    name, department, role, hire_date, salary, active
) VALUES
    ('Ana Martins', 'Engenharia', 'Backend Developer', '2022-03-14', 8500.00, TRUE),
    ('Bruno Ferreira', 'Vendas', 'Account Executive', '2023-01-09', 6500.00, TRUE),
    ('Carla Souza', 'Vendas', 'Account Executive', '2024-05-06', 6200.00, TRUE),
    ('Diego Almeida', 'Marketing', 'Growth Analyst', '2021-11-22', 7000.00, TRUE),
    ('Eva Lima', 'Vendas', 'Sales Development Representative', '2022-08-17', 4800.00, FALSE),
    ('Fabio Rocha', 'Financeiro', 'Financial Analyst', '2023-07-03', 6800.00, TRUE),
    ('Gabriela Nunes', 'Produto', 'Product Manager', '2022-02-10', 9200.00, TRUE),
    ('Henrique Costa', 'Suporte', 'Support Analyst', '2024-01-08', 5200.00, TRUE),
    ('Isabela Mendes', 'RH', 'People Analyst', '2021-06-21', 6100.00, TRUE),
    ('Joao Ribeiro', 'Operacoes', 'Operations Analyst', '2023-09-18', 5900.00, TRUE);

-- Factory em massa: produz mais 40 funcionarios deterministicos.
INSERT INTO employees (
    name, department, role, hire_date, salary, active
)
SELECT
    'Funcionario ' || LPAD(factory_number::TEXT, 2, '0'),
    (ARRAY[
        'Engenharia', 'Vendas', 'Marketing',
        'Financeiro', 'Produto', 'Suporte'
    ])[1 + ((factory_number - 1) % 6)],
    (ARRAY[
        'Analyst', 'Specialist', 'Coordinator',
        'Developer', 'Consultant', 'Assistant'
    ])[1 + ((factory_number - 1) % 6)],
    DATE '2020-01-01' + ((factory_number * 47) % 1800),
    3500.00 + ((factory_number * 317) % 8500),
    factory_number % 11 <> 0
FROM generate_series(11, 50) AS factory_number;

INSERT INTO sales (
    employee_id, sold_at, amount, status
)
SELECT
    1 + ((factory_number - 1) % 50),
    DATE '2026-01-01' + ((factory_number * 17) % 365),
    250.00 + ((factory_number * 137) % 9750),
    CASE
        WHEN factory_number % 15 = 0 THEN 'cancelled'
        ELSE 'completed'
    END
FROM generate_series(1, 600) AS factory_number;
