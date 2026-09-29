"""
Script de Geração, Tratamento e Modelagem Dimensional
Case 1: O Impacto da Inteligência Artificial no Mercado de Trabalho (2020-2030)
Dataset alinhado ao Kaggle: khushikyad001/ai-impact-on-jobs-2030
"""

import os
import numpy as np
import pandas as pd

# Fixar semente para reprodutibilidade estrita dos dados
np.random.seed(42)

# Definição dos Arquétipos Ocupacionais com parâmetros fundamentados em Labor Economics
OCCUPATION_PROFILES = [
    # (Cargo, Setor, Escolaridade_Pre, Escolaridade_Pos, Exp_Level, AI_Exposure, Auto_Prob, Sal_Pre, Sal_Pos_Growth_Factor, Vol_Growth_Factor, Skill)
    ("Data Scientist", "Technology", "Master's Degree", "Master's Degree", "Mid-Level", 0.92, 0.28, 115000, 1.25, 1.35, "LLM Fine-tuning & MLOps"),
    ("Machine Learning Engineer", "Technology", "Master's Degree", "Master's Degree", "Senior", 0.95, 0.22, 140000, 1.32, 1.45, "Generative AI Systems"),
    ("Software Developer", "Technology", "Bachelor's Degree", "Bachelor's Degree", "Mid-Level", 0.88, 0.38, 98000, 1.15, 1.12, "AI-Assisted Coding & Copilots"),
    ("QA & Test Automation Tester", "Technology", "Bachelor's Degree", "Bachelor's Degree", "Entry-Level", 0.85, 0.72, 68000, 0.92, 0.75, "Synthetic Test Automation"),
    ("Cybersecurity Specialist", "Technology", "Bachelor's Degree", "Bachelor's Degree", "Senior", 0.78, 0.25, 122000, 1.28, 1.38, "AI Threat Intelligence"),
    ("Cloud Infrastructure Architect", "Technology", "Bachelor's Degree", "Master's Degree", "Senior", 0.72, 0.30, 135000, 1.24, 1.25, "Hybrid Cloud & Green Computing"),
    
    ("Customer Support Specialist", "Retail & E-Commerce", "High School", "Associate Degree", "Entry-Level", 0.94, 0.86, 38000, 0.88, 0.58, "Agentic AI Supervision & CX"),
    ("E-commerce Category Manager", "Retail & E-Commerce", "Bachelor's Degree", "Bachelor's Degree", "Mid-Level", 0.75, 0.42, 75000, 1.10, 1.05, "Algorithmic Pricing & Demand"),
    ("Warehouse Logistics Associate", "Retail & E-Commerce", "High School", "High School", "Entry-Level", 0.65, 0.82, 36000, 0.95, 0.72, "Cobot Operation & Tracking"),
    ("Supply Chain Optimization Lead", "Retail & E-Commerce", "Bachelor's Degree", "Master's Degree", "Senior", 0.82, 0.35, 105000, 1.22, 1.20, "Prescriptive Supply Analytics"),

    ("Financial Analyst", "Financial Services", "Bachelor's Degree", "Bachelor's Degree", "Mid-Level", 0.89, 0.58, 88000, 1.08, 0.92, "Automated Valuation & FinGPT"),
    ("Quantitative Portfolio Manager", "Financial Services", "Master's Degree", "Doctorate (PhD)", "Senior", 0.94, 0.20, 165000, 1.35, 1.28, "Algorithmic ESG Modeling"),
    ("Bank Branch Teller", "Financial Services", "High School", "Associate Degree", "Entry-Level", 0.91, 0.92, 37000, 0.85, 0.45, "Digital Onboarding Guidance"),
    ("Risk & Compliance Auditor", "Financial Services", "Bachelor's Degree", "Master's Degree", "Mid-Level", 0.84, 0.45, 92000, 1.18, 1.15, "AI Regulatory Compliance"),

    ("Medical Radiologist", "Healthcare", "Doctorate (PhD)", "Doctorate (PhD)", "Senior", 0.96, 0.35, 320000, 1.18, 1.10, "Multimodal Clinical AI Diagnosis"),
    ("Registered Nurse", "Healthcare", "Bachelor's Degree", "Bachelor's Degree", "Mid-Level", 0.42, 0.12, 78000, 1.22, 1.30, "Complex Patient Care & Triage"),
    ("Medical Records Coder", "Healthcare", "Associate Degree", "Associate Degree", "Entry-Level", 0.92, 0.88, 44000, 0.86, 0.52, "NLP Clinical Note Extraction"),
    ("Biomedical Research Scientist", "Healthcare", "Doctorate (PhD)", "Doctorate (PhD)", "Senior", 0.90, 0.18, 118000, 1.30, 1.35, "AlphaFold & In-Silico Trials"),

    ("Paralegal", "Legal", "Associate Degree", "Bachelor's Degree", "Entry-Level", 0.92, 0.81, 54000, 0.89, 0.65, "Legal Prompting & Case Retrieval"),
    ("Corporate Contract Attorney", "Legal", "Doctorate (PhD)", "Doctorate (PhD)", "Senior", 0.86, 0.38, 175000, 1.18, 1.08, "Complex Settlement Strategy"),
    ("Compliance Legal Officer", "Legal", "Bachelor's Degree", "Master's Degree", "Mid-Level", 0.81, 0.40, 110000, 1.20, 1.15, "Data Privacy & AI Ethics"),

    ("Copywriter & Content Creator", "Media & Communications", "Bachelor's Degree", "Bachelor's Degree", "Entry-Level", 0.95, 0.78, 52000, 0.85, 0.62, "Editorial Strategy & Fact-Checking"),
    ("Creative Art Director", "Media & Communications", "Bachelor's Degree", "Bachelor's Degree", "Senior", 0.88, 0.32, 102000, 1.20, 1.12, "Cross-Media Creative Direction"),
    ("Digital Video Editor & VFX", "Media & Communications", "Associate Degree", "Bachelor's Degree", "Mid-Level", 0.84, 0.64, 62000, 1.04, 0.85, "GenAI Video Synthesis & Post-Prod"),

    ("Higher Education Professor", "Education", "Doctorate (PhD)", "Doctorate (PhD)", "Senior", 0.74, 0.22, 95000, 1.08, 1.02, "Adaptive Learning Mentorship"),
    ("K-12 STEM Teacher", "Education", "Bachelor's Degree", "Master's Degree", "Mid-Level", 0.58, 0.15, 62000, 1.16, 1.18, "AI-Integrated Pedagogy"),
    ("Corporate L&D Instructional Designer", "Education", "Bachelor's Degree", "Master's Degree", "Mid-Level", 0.86, 0.55, 74000, 1.12, 1.04, "Micro-Credential Course Design"),

    ("Industrial Automation Technician", "Manufacturing", "Associate Degree", "Associate Degree", "Mid-Level", 0.68, 0.40, 64000, 1.22, 1.25, "Predictive Maintenance & Robotics"),
    ("Quality Control Inspector", "Manufacturing", "High School", "Associate Degree", "Entry-Level", 0.86, 0.84, 42000, 0.90, 0.60, "Computer Vision Inspection"),
    ("Process & Systems Engineer", "Manufacturing", "Bachelor's Degree", "Bachelor's Degree", "Senior", 0.79, 0.32, 108000, 1.21, 1.18, "Digital Twin Engineering")
]

# Níveis educacionais ordenados
EDUCATION_HIERARCHY = {
    "High School": 1,
    "Associate Degree": 2,
    "Bachelor's Degree": 3,
    "Master's Degree": 4,
    "Doctorate (PhD)": 5
}

def generate_synthetic_workforce_data(num_samples=3000):
    records = []
    
    work_models = ["Remote", "Hybrid", "On-site"]
    work_model_weights = [0.30, 0.45, 0.25]
    
    regions = ["North America", "Europe", "Latin America", "Asia-Pacific"]
    region_weights = [0.40, 0.30, 0.15, 0.15]
    
    for i in range(1, num_samples + 1):
        # Seleção aleatória balanceada de um perfil base
        profile = OCCUPATION_PROFILES[np.random.choice(len(OCCUPATION_PROFILES))]
        (job_title, industry, edu_pre, edu_pos, exp_level, 
         ai_exposure_base, auto_prob_base, sal_pre_base, 
         sal_growth_base, vol_growth_base, top_skill) = profile
        
        # Inserção de variação estocástica realista (Gaussian noise)
        ai_exposure = np.clip(np.random.normal(ai_exposure_base, 0.04), 0.05, 0.99)
        auto_prob = np.clip(np.random.normal(auto_prob_base, 0.06), 0.05, 0.99)
        
        # Ajuste por nível de experiência dentro do cargo
        exp_multiplier = {
            "Entry-Level": 0.82,
            "Mid-Level": 1.00,
            "Senior": 1.35,
            "Executive": 1.70
        }[exp_level]
        
        # Salário base pré-IA (2020) com ruído
        sal_pre = int(np.random.normal(sal_pre_base * exp_multiplier, sal_pre_base * 0.08))
        sal_pre = max(28000, sal_pre)
        
        # Variação salarial pós-IA (2030)
        sal_growth = np.random.normal(sal_growth_base, 0.05)
        sal_pos = int(sal_pre * sal_growth)
        
        # Volume de vagas (em milhares de vagas globais monitoradas)
        vol_pre = int(np.random.uniform(15, 180))
        vol_growth = np.random.normal(vol_growth_base, 0.08)
        vol_pos = max(5, int(vol_pre * vol_growth))
        
        # Turno de Escolaridade (Upgraded, Stable, Reskilled)
        pre_val = EDUCATION_HIERARCHY[edu_pre]
        pos_val = EDUCATION_HIERARCHY[edu_pos]
        if pos_val > pre_val:
            edu_shift = "Exigência Elevada (Upgraded)"
        elif pos_val == pre_val:
            edu_shift = "Escolaridade Mantida (Stable)"
        else:
            edu_shift = "Descentralização / Foco em Skills"
            
        # Classificação de Categoria de Risco
        if auto_prob >= 0.70:
            risk_category = "Alto Risco de Automação"
        elif auto_prob >= 0.40:
            risk_category = "Médio Risco (Transição Híbrida)"
        else:
            risk_category = "Baixo Risco (Amplificação Humana)"
            
        # Impacto Salarial Categórico
        sal_diff_pct = round(((sal_pos - sal_pre) / sal_pre) * 100, 2)
        vol_diff_pct = round(((vol_pos - vol_pre) / vol_pre) * 100, 2)
        
        work_model = np.random.choice(work_models, p=work_model_weights)
        region = np.random.choice(regions, p=region_weights)
        
        records.append({
            "Job_Record_ID": f"JOB_{i:05d}",
            "Job_Title": job_title,
            "Industry": industry,
            "Experience_Level": exp_level,
            "Work_Model": work_model,
            "Region": region,
            "Education_Pre_AI": edu_pre,
            "Education_Post_AI_2030": edu_pos,
            "Education_Shift_Type": edu_shift,
            "AI_Exposure_Index": round(float(ai_exposure), 3),
            "Automation_Probability_2030": round(float(auto_prob), 3),
            "Risk_Category": risk_category,
            "Job_Volume_Pre_AI_k": vol_pre,
            "Job_Volume_2030_k": vol_pos,
            "Job_Volume_Growth_Pct": vol_diff_pct,
            "Salary_Pre_AI_USD": sal_pre,
            "Salary_Post_AI_USD": sal_pos,
            "Salary_Growth_Pct": sal_diff_pct,
            "Primary_Emerging_Skill": top_skill
        })
        
    return pd.DataFrame(records)

def create_star_schema(df, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Tabela Dimensão: Cargo (dim_cargo)
    dim_cargo = df[['Job_Title', 'Industry', 'Primary_Emerging_Skill']].drop_duplicates().reset_index(drop=True)
    dim_cargo['Cargo_ID'] = [f"CRG_{i+1:03d}" for i in range(len(dim_cargo))]
    dim_cargo = dim_cargo[['Cargo_ID', 'Job_Title', 'Industry', 'Primary_Emerging_Skill']]
    
    # 2. Tabela Dimensão: Setor (dim_setor)
    dim_setor = df[['Industry']].drop_duplicates().reset_index(drop=True)
    dim_setor['Setor_ID'] = [f"SET_{i+1:02d}" for i in range(len(dim_setor))]
    dim_setor = dim_setor[['Setor_ID', 'Industry']]
    
    # 3. Tabela Dimensão: Escolaridade (dim_escolaridade)
    niveis = list(EDUCATION_HIERARCHY.keys())
    dim_escolaridade = pd.DataFrame({
        'Escolaridade_ID': [f"ESC_{i+1:02d}" for i in range(len(niveis))],
        'Nivel_Escolaridade': niveis,
        'Grau_Hierarquico': [EDUCATION_HIERARCHY[n] for n in niveis]
    })
    
    # 4. Tabela Fato: fato_ai_job_impact
    fato = df.merge(dim_cargo[['Cargo_ID', 'Job_Title']], on='Job_Title')
    fato = fato.merge(dim_setor[['Setor_ID', 'Industry']], on='Industry')
    fato = fato.merge(dim_escolaridade.rename(columns={'Nivel_Escolaridade': 'Education_Pre_AI', 'Escolaridade_ID': 'Escolaridade_Pre_ID'})[['Education_Pre_AI', 'Escolaridade_Pre_ID']], on='Education_Pre_AI')
    fato = fato.merge(dim_escolaridade.rename(columns={'Nivel_Escolaridade': 'Education_Post_AI_2030', 'Escolaridade_ID': 'Escolaridade_Pos_ID'})[['Education_Post_AI_2030', 'Escolaridade_Pos_ID']], on='Education_Post_AI_2030')
    
    colunas_fato = [
        'Job_Record_ID', 'Cargo_ID', 'Setor_ID', 'Escolaridade_Pre_ID', 'Escolaridade_Pos_ID',
        'Experience_Level', 'Work_Model', 'Region', 'Education_Shift_Type',
        'AI_Exposure_Index', 'Automation_Probability_2030', 'Risk_Category',
        'Job_Volume_Pre_AI_k', 'Job_Volume_2030_k', 'Job_Volume_Growth_Pct',
        'Salary_Pre_AI_USD', 'Salary_Post_AI_USD', 'Salary_Growth_Pct'
    ]
    fato_df = fato[colunas_fato]
    
    # Exportação dos arquivos em CSV
    df.to_csv(os.path.join(output_dir, "ai_impact_consolidated.csv"), index=False, encoding="utf-8-sig")
    dim_cargo.to_csv(os.path.join(output_dir, "dim_cargo.csv"), index=False, encoding="utf-8-sig")
    dim_setor.to_csv(os.path.join(output_dir, "dim_setor.csv"), index=False, encoding="utf-8-sig")
    dim_escolaridade.to_csv(os.path.join(output_dir, "dim_escolaridade.csv"), index=False, encoding="utf-8-sig")
    fato_df.to_csv(os.path.join(output_dir, "fato_ai_job_impact.csv"), index=False, encoding="utf-8-sig")
    
    print("[OK] Modelagem dimensional concluida e exportada com sucesso em:", output_dir)
    return df, dim_cargo, dim_setor, dim_escolaridade, fato_df

if __name__ == "__main__":
    base_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\case-01-impacto-ia-trabalho\data"
    raw_df = generate_synthetic_workforce_data(num_samples=3200)
    df, dim_cargo, dim_setor, dim_escolaridade, fato_df = create_star_schema(raw_df, base_dir)
    
    # Resumo descritivo dos principais achados
    print("\n--- RESUMO ESTATISTICO DE NEGOCIO ---")
    print("Total de Registros:", len(df))
    print("\nVariacao Salarial Media por Categoria de Risco de Automacao:")
    print(df.groupby('Risk_Category')['Salary_Growth_Pct'].agg(['mean', 'median', 'min', 'max']))
    print("\nVariacao do Volume de Vagas por Categoria de Risco:")
    print(df.groupby('Risk_Category')['Job_Volume_Growth_Pct'].agg(['mean', 'median']))
    print("\nDistribuicao de Mudanca de Exigencia Educacional:")
    print(df['Education_Shift_Type'].value_counts(normalize=True) * 100)
