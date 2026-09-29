-- ===================================================================
-- CASE 1: AI WorkShift 2030 - Modelagem Dimensional (Star Schema)
-- Compatibilidade: PostgreSQL, DuckDB, SQLite, MySQL
-- ===================================================================

-- 1. Tabela Dimensão: Cargo (dim_cargo)
DROP TABLE IF EXISTS dim_cargo;
CREATE TABLE dim_cargo (
    cargo_id VARCHAR(10) PRIMARY KEY,
    job_title VARCHAR(100) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    primary_emerging_skill VARCHAR(150) NOT NULL
);

-- 2. Tabela Dimensão: Setor Econômico (dim_setor)
DROP TABLE IF EXISTS dim_setor;
CREATE TABLE dim_setor (
    setor_id VARCHAR(10) PRIMARY KEY,
    industry VARCHAR(100) NOT NULL
);

-- 3. Tabela Dimensão: Escolaridade (dim_escolaridade)
DROP TABLE IF EXISTS dim_escolaridade;
CREATE TABLE dim_escolaridade (
    escolaridade_id VARCHAR(10) PRIMARY KEY,
    nivel_escolaridade VARCHAR(50) NOT NULL,
    grau_hierarquico INT NOT NULL
);

-- 4. Tabela Fato: Impacto da IA nas Ocupações (fato_ai_job_impact)
DROP TABLE IF EXISTS fato_ai_job_impact;
CREATE TABLE fato_ai_job_impact (
    job_record_id VARCHAR(20) PRIMARY KEY,
    cargo_id VARCHAR(10) REFERENCES dim_cargo(cargo_id),
    setor_id VARCHAR(10) REFERENCES dim_setor(setor_id),
    escolaridade_pre_id VARCHAR(10) REFERENCES dim_escolaridade(escolaridade_id),
    escolaridade_pos_id VARCHAR(10) REFERENCES dim_escolaridade(escolaridade_id),
    experience_level VARCHAR(30) NOT NULL,
    work_model VARCHAR(30) NOT NULL,
    region VARCHAR(50) NOT NULL,
    education_shift_type VARCHAR(100) NOT NULL,
    ai_exposure_index NUMERIC(5,3) NOT NULL,
    automation_probability_2030 NUMERIC(5,3) NOT NULL,
    risk_category VARCHAR(50) NOT NULL,
    job_volume_pre_ai_k INT NOT NULL,
    job_volume_2030_k INT NOT NULL,
    job_volume_growth_pct NUMERIC(6,2) NOT NULL,
    salary_pre_ai_usd INT NOT NULL,
    salary_post_ai_usd INT NOT NULL,
    salary_growth_pct NUMERIC(6,2) NOT NULL
);

-- Índices para otimização de consultas analíticas
CREATE INDEX idx_fato_cargo ON fato_ai_job_impact(cargo_id);
CREATE INDEX idx_fato_setor ON fato_ai_job_impact(setor_id);
CREATE INDEX idx_fato_risco ON fato_ai_job_impact(risk_category);
