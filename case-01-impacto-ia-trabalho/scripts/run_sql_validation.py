"""
Validação e Execução das Consultas SQL via SQLite (Standard Library)
"""

import sqlite3
import pandas as pd
import os

db_path = r"C:\Users\lenovo\.gemini\antigravity\scratch\case-01-impacto-ia-trabalho\data\ai_impact.db"
data_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\case-01-impacto-ia-trabalho\data"
sql_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\case-01-impacto-ia-trabalho\sql"

# Conectar e criar banco SQLite local
conn = sqlite3.connect(db_path)

# Carregar tabelas a partir dos CSVs
dim_cargo = pd.read_csv(os.path.join(data_dir, "dim_cargo.csv"))
dim_setor = pd.read_csv(os.path.join(data_dir, "dim_setor.csv"))
dim_escolaridade = pd.read_csv(os.path.join(data_dir, "dim_escolaridade.csv"))
fato = pd.read_csv(os.path.join(data_dir, "fato_ai_job_impact.csv"))

# Salvar no SQLite com nomes padronizados minúsculos
dim_cargo.to_sql("dim_cargo", conn, if_exists="replace", index=False)
dim_setor.to_sql("dim_setor", conn, if_exists="replace", index=False)
dim_escolaridade.to_sql("dim_escolaridade", conn, if_exists="replace", index=False)
fato.to_sql("fato_ai_job_impact", conn, if_exists="replace", index=False)

print("[OK] Banco de dados SQLite criado e tabelas carregadas com sucesso.")

# Executar consultas analíticas
queries = [
    ("1. Impacto Salarial e de Vagas por Risco de Automação", """
    SELECT 
        risk_category,
        COUNT(*) AS total_amostras,
        ROUND(AVG(salary_pre_ai_usd), 0) AS sal_medio_pre,
        ROUND(AVG(salary_post_ai_usd), 0) AS sal_medio_pos,
        ROUND(AVG(salary_growth_pct), 2) AS var_salarial_pct,
        SUM(job_volume_pre_ai_k) AS vagas_pre_k,
        SUM(job_volume_2030_k) AS vagas_pos_k,
        ROUND((SUM(job_volume_2030_k) - SUM(job_volume_pre_ai_k)) * 100.0 / SUM(job_volume_pre_ai_k), 2) AS saldo_vagas_pct
    FROM fato_ai_job_impact
    GROUP BY risk_category
    ORDER BY var_salarial_pct DESC;
    """),
    
    ("2. Top 5 Profissões com Maior Aceleração Salarial (Augmentation)", """
    SELECT 
        c.Job_Title,
        c.Industry,
        c.Primary_Emerging_Skill,
        ROUND(AVG(f.Salary_Growth_Pct), 2) AS ganho_salarial_pct,
        ROUND(AVG(f.Job_Volume_Growth_Pct), 2) AS saldo_vagas_pct,
        ROUND(AVG(f.Automation_Probability_2030), 2) AS prob_automacao
    FROM fato_ai_job_impact f
    JOIN dim_cargo c ON f.Cargo_ID = c.Cargo_ID
    GROUP BY c.Job_Title, c.Industry, c.Primary_Emerging_Skill
    ORDER BY ganho_salarial_pct DESC
    LIMIT 5;
    """),
    
    ("3. Top 5 Profissões com Maior Compressão e Risco de Deslocamento", """
    SELECT 
        c.Job_Title,
        c.Industry,
        c.Primary_Emerging_Skill,
        ROUND(AVG(f.Salary_Growth_Pct), 2) AS ganho_salarial_pct,
        ROUND(AVG(f.Job_Volume_Growth_Pct), 2) AS saldo_vagas_pct,
        ROUND(AVG(f.Automation_Probability_2030), 2) AS prob_automacao
    FROM fato_ai_job_impact f
    JOIN dim_cargo c ON f.Cargo_ID = c.Cargo_ID
    GROUP BY c.Job_Title, c.Industry, c.Primary_Emerging_Skill
    ORDER BY ganho_salarial_pct ASC
    LIMIT 5;
    """)
]

for title, q in queries:
    print(f"\n==========================================")
    print(f"-> {title}")
    print(f"==========================================")
    res_df = pd.read_sql_query(q, conn)
    print(res_df.to_string(index=False))

conn.close()
