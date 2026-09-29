-- ===================================================================
-- CASE 1: AI WorkShift 2030 - Consultas Analíticas Avançadas (SQL)
-- Foco: Insights Estratégicos para Storytelling em Portfólio
-- ===================================================================

-- -------------------------------------------------------------------
-- QUERY 1: Análise de Elevação da Escolaridade por Setor
-- Objetivo: Identificar quais indústrias estão exigindo maior qualificação
-- formal e onde a barreira de entrada educacional mais aumentou.
-- -------------------------------------------------------------------
WITH analise_educacao AS (
    SELECT 
        s.industry AS setor,
        f.education_shift_type,
        COUNT(*) AS total_posicoes,
        ROUND(AVG(f.ai_exposure_index), 3) AS media_exposicao_ia,
        ROUND(AVG(f.salary_growth_pct), 2) AS media_crescimento_salarial_pct
    FROM fato_ai_job_impact f
    JOIN dim_setor s ON f.setor_id = s.setor_id
    GROUP BY s.industry, f.education_shift_type
)
SELECT 
    setor,
    education_shift_type,
    total_posicoes,
    ROUND(total_posicoes * 100.0 / SUM(total_posicoes) OVER(PARTITION BY setor), 2) AS pct_do_setor,
    media_exposicao_ia,
    media_crescimento_salarial_pct
FROM analise_educacao
ORDER BY setor, pct_do_setor DESC;


-- -------------------------------------------------------------------
-- QUERY 2: Impacto Salarial e de Volume de Vagas por Categoria de Risco
-- Objetivo: Confrontar o período Pré-IA (2020) com a projeção Pós-IA (2030)
-- -------------------------------------------------------------------
SELECT 
    f.risk_category,
    COUNT(*) AS total_amostras,
    ROUND(AVG(f.salary_pre_ai_usd), 2) AS salario_medio_pre_ia,
    ROUND(AVG(f.salary_post_ai_usd), 2) AS salario_medio_pos_ia,
    ROUND(AVG(f.salary_growth_pct), 2) AS variacao_salarial_media_pct,
    SUM(f.job_volume_pre_ai_k) AS volume_vagas_pre_k,
    SUM(f.job_volume_2030_k) AS volume_vagas_2030_k,
    ROUND(
        (SUM(f.job_volume_2030_k) - SUM(f.job_volume_pre_ai_k)) * 100.0 / SUM(f.job_volume_pre_ai_k), 
        2
    ) AS saldo_liquido_vagas_pct
FROM fato_ai_job_impact f
GROUP BY f.risk_category
ORDER BY variacao_salarial_media_pct DESC;


-- -------------------------------------------------------------------
-- QUERY 3: Ranking dos Top 5 Cargos Vencedores vs. Top 5 Cargos Vulneráveis
-- Objetivo: Identificar as profissões com maior valorização salarial vs. compressão
-- -------------------------------------------------------------------
WITH ranking_cargos AS (
    SELECT 
        c.job_title,
        c.industry,
        c.primary_emerging_skill,
        ROUND(AVG(f.automation_probability_2030), 2) AS prob_automacao,
        ROUND(AVG(f.salary_pre_ai_usd), 0) AS sal_pre,
        ROUND(AVG(f.salary_post_ai_usd), 0) AS sal_pos,
        ROUND(AVG(f.salary_growth_pct), 2) AS ganho_salarial_pct,
        ROUND(AVG(f.job_volume_growth_pct), 2) AS expansao_vagas_pct,
        ROW_NUMBER() OVER(ORDER BY AVG(f.salary_growth_pct) DESC) AS rank_vencedores,
        ROW_NUMBER() OVER(ORDER BY AVG(f.salary_growth_pct) ASC) AS rank_vulneraveis
    FROM fato_ai_job_impact f
    JOIN dim_cargo c ON f.cargo_id = c.cargo_id
    GROUP BY c.job_title, c.industry, c.primary_emerging_skill
)
SELECT 
    'Top Vencedores (High Augmentation)' AS grupo,
    rank_vencedores AS posicao,
    job_title,
    industry,
    primary_emerging_skill,
    ganho_salarial_pct,
    expansao_vagas_pct,
    prob_automacao
FROM ranking_cargos
WHERE rank_vencedores <= 5

UNION ALL

SELECT 
    'Top Vulneráveis (Displacement Risk)' AS grupo,
    rank_vulneraveis AS posicao,
    job_title,
    industry,
    primary_emerging_skill,
    ganho_salarial_pct,
    expansao_vagas_pct,
    prob_automacao
FROM ranking_cargos
WHERE rank_vulneraveis <= 5
ORDER BY grupo, posicao;


-- -------------------------------------------------------------------
-- QUERY 4: Análise por Quartis de Exposição à IA (NTILE)
-- Objetivo: Demonstrar se maior exposição à IA é sempre destrutiva ou não.
-- -------------------------------------------------------------------
WITH quartis_ia AS (
    SELECT 
        f.job_record_id,
        f.ai_exposure_index,
        f.automation_probability_2030,
        f.salary_growth_pct,
        f.job_volume_growth_pct,
        NTILE(4) OVER (ORDER BY f.ai_exposure_index) AS quartil_exposicao_ia
    FROM fato_ai_job_impact f
)
SELECT 
    CASE quartil_exposicao_ia
        WHEN 1 THEN 'Q1 - Baixa Exposição (0.05 - 0.65)'
        WHEN 2 THEN 'Q2 - Média-Baixa Exposição (0.65 - 0.80)'
        WHEN 3 THEN 'Q3 - Média-Alta Exposição (0.80 - 0.90)'
        WHEN 4 THEN 'Q4 - Altíssima Exposição (0.90 - 1.00)'
    END AS faixa_exposicao,
    COUNT(*) AS total_postos,
    ROUND(AVG(automation_probability_2030), 3) AS media_prob_automacao,
    ROUND(AVG(salary_growth_pct), 2) AS media_ganho_salarial_pct,
    ROUND(AVG(job_volume_growth_pct), 2) AS media_crescimento_vagas_pct
FROM quartis_ia
GROUP BY quartil_exposicao_ia
ORDER BY quartil_exposicao_ia;
