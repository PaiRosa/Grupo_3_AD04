# 📊 Especificação Técnica e Guia do Dashboard Power BI
## Case: AI WorkShift 2030 — O Impacto da IA no Mercado de Trabalho

---

## 1. 🏗️ Modelo de Dados (Star Schema no Power BI)

Conecte os arquivos CSV gerados na pasta `data/` via Power Query:
- `fato_ai_job_impact.csv`
- `dim_cargo.csv`
- `dim_setor.csv`
- `dim_escolaridade.csv`

### Relacionamentos (Diagram View)
| Tabela Fato | Coluna Fato | Tabela Dimensão | Coluna Dimensão | Cardinalidade | Direção Filtro |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `fato_ai_job_impact` | `Cargo_ID` | `dim_cargo` | `Cargo_ID` | N : 1 | Única (Dim -> Fato) |
| `fato_ai_job_impact` | `Setor_ID` | `dim_setor` | `Setor_ID` | N : 1 | Única (Dim -> Fato) |
| `fato_ai_job_impact` | `Escolaridade_Pre_ID` | `dim_escolaridade` | `Escolaridade_ID` | N : 1 | Única (Dim -> Fato) |
| `fato_ai_job_impact` | `Escolaridade_Pos_ID` | `dim_escolaridade` | `Escolaridade_ID` | N : 1 (Inativo) | Única (Dim -> Fato) |

> **Nota:** O relacionamento com `Escolaridade_Pos_ID` pode ser mantido inativo ou ativado via função DAX `USERELATIONSHIP()` para comparar perfis antes e depois da IA na mesma dimensão.

---

## 2. 📐 Dicionário de Medidas DAX (Tabela `_Medidas`)

Crie uma tabela vazia chamada `_Medidas` e insira as seguintes fórmulas:

### Métricas de Volume de Vagas
```dax
// Total de Vagas Pré-IA (2020) em milhares
Total_Vagas_Pre_IA = 
SUM(fato_ai_job_impact[Job_Volume_Pre_AI_k])

// Total de Vagas Projetadas Pós-IA (2030) em milhares
Total_Vagas_Pos_IA = 
SUM(fato_ai_job_impact[Job_Volume_2030_k])

// Saldo Líquido de Vagas (Volume Absoluto)
Saldo_Vagas_Liquido_k = 
[Total_Vagas_Pos_IA] - [Total_Vagas_Pre_IA]

// Variação Percentual do Volume de Vagas
Variacao_Vagas_% = 
DIVIDE([Saldo_Vagas_Liquido_k], [Total_Vagas_Pre_IA], 0)
```

### Métricas Salariais
```dax
// Salário Médio Pré-IA (USD)
Salario_Medio_Pre_IA = 
AVERAGE(fato_ai_job_impact[Salary_Pre_AI_USD])

// Salário Médio Projetado Pós-IA (USD)
Salario_Medio_Pos_IA = 
AVERAGE(fato_ai_job_impact[Salary_Post_AI_USD])

// Ganho Salarial Percentual
Variacao_Salarial_% = 
DIVIDE(
    [Salario_Medio_Pos_IA] - [Salario_Medio_Pre_IA],
    [Salario_Medio_Pre_IA],
    0
)

// Gap Salarial Absoluto (USD)
Gap_Salarial_USD = 
[Salario_Medio_Pos_IA] - [Salario_Medio_Pre_IA]
```

### Métricas de Exposição e Risco de IA
```dax
// Índice Médio de Exposição à IA
Indice_Medio_Exposicao = 
AVERAGE(fato_ai_job_impact[AI_Exposure_Index])

// Probabilidade Média de Automação
Probabilidade_Media_Automacao = 
AVERAGE(fato_ai_job_impact[Automation_Probability_2030])

// % de Vagas sob Alto Risco de Automação
Pct_Vagas_Alto_Risco = 
DIVIDE(
    CALCULATE([Total_Vagas_Pos_IA], fato_ai_job_impact[Risk_Category] = "Alto Risco de Automação"),
    [Total_Vagas_Pos_IA],
    0
)

// Taxa de Elevação de Escolaridade
Taxa_Elevacao_Escolaridade = 
DIVIDE(
    CALCULATE(COUNTROWS(fato_ai_job_impact), fato_ai_job_impact[Education_Shift_Type] = "Exigência Elevada (Upgraded)"),
    COUNTROWS(fato_ai_job_impact),
    0
)
```

### Medida Dinâmica de Cor Hexadecimal para Formatação Condicional
```dax
Cor_Variacao_Salarial = 
SWITCH(
    TRUE(),
    [Variacao_Salarial_%] > 0.15, "#10B981",  -- Verde esmeralda (Crescimento Forte)
    [Variacao_Salarial_%] >= 0,   "#0EA5E9",  -- Azul ciano (Estabilidade / Ganho Moderado)
    [Variacao_Salarial_%] < -0.05, "#EF4444", -- Vermelho coral (Queda Acentuada)
    "#F59E0B"                                 -- Laranja âmbar (Leve retração)
)
```

---

## 3. 🖥️ Layout e Estrutura das Páginas do Dashboard

### 🎨 Paleta de Cores Recomendada (Design Moderno & Acessível)
- **Background Principal:** `#F8FAFC` (Cinza neutro ultra-claro) ou `#0F172A` (Dark mode)
- **Cards & Containers:** `#FFFFFF` (com sombra suave `rgba(0,0,0,0.05)`)
- **Azul Primário (Tech/Institucional):** `#0284C7`
- **Verde Sucesso (Amplificação/Ganho):** `#10B981`
- **Vermelho Alerta (Automação/Compressão):** `#EF4444`
- **Tipografia:** Segoe UI ou Inter, títulos semibold.

---

### Página 1: Visão Executiva — O Balanço Líquido da IA
*Objetivo: Apresentar a visão macroeconômica de ganhadores e perdedores na era da IA.*
- **Faixa Superior (KPI Cards):**
  1. `Total_Vagas_Pos_IA` (com subtítulo indicando `[Saldo_Vagas_Liquido_k]` e ícone de seta).
  2. `Salario_Medio_Pos_IA` (formatado em `$#,##0`, com indicador de `[Variacao_Salarial_%]`).
  3. `Indice_Medio_Exposicao` (percentual com barra de progresso).
  4. `Pct_Vagas_Alto_Risco` (cartão com alerta visual).
- **Visual Principal (Esquerda - 60% da tela):**
  - *Gráfico de Barras Divergentes (Tornado Chart):* Setor Econômico vs. `[Variacao_Vagas_%]`. Mostra claramente setores em expansão líquida (Tecnologia, Saúde, Manufatura Avançada) vs. setores em encolhimento de postos (Varejo operacional, Apoio Bancário, Mídia tradicional).
- **Visual Secundário (Direita - 40% da tela):**
  - *Gráfico de Rosca (Donut Chart):* Distribuição de vagas por `Risk_Category`.
  - *Tabela Top 5 Vencedores & Top 5 Vulneráveis:* Exibindo Cargo, Habilidade Emergente e Variação Salarial com barra de dados colorida.
- **Filtros Globais (Slicers):** Setor, Modelo de Trabalho (Remoto/Híbrido/Presencial), Região Global.

---

### Página 2: O Novo Filtro Educacional — Escolaridade & Skills
*Objetivo: Responder à pergunta de negócio sobre exigência de qualificação formal pré vs. pós-IA.*
- **KPI Cards de Apoio:**
  - `Taxa_Elevacao_Escolaridade` (39.3% das posições passaram a exigir credenciais formais mais altas).
  - Escolaridade com maior bônus salarial médio.
- **Visual 1 (Gráfico de Barras 100% Empilhadas):**
  - Eixo X = Categoria de Risco de Automação.
  - Eixo Y = % de Distribuição por Nível de Ensino.
  - *Insight visível:* Cargos de alto risco estão concentrados em ensino médio e cursos de curta duração; funções de baixa probabilidade de automação exigem graduação e pós-graduação.
- **Visual 2 (Matriz Cruzada):**
  - Linhas = Escolaridade Pré-IA; Colunas = Escolaridade Pós-IA; Valores = Contagem de Ocupações.
  - Identifica o fenômeno do "Degree Escalation" (cargos migrando de High School -> Associate, e Bachelor -> Master's).
- **Visual 3 (Treemap de Competências):**
  - Tamanho = Volume de Vagas; Cor = Ganho Salarial Médio.
  - Destaque para *LLM Fine-tuning*, *Agentic AI Supervision*, *In-Silico Trials*, e *Digital Twin Engineering*.

---

### Página 3: Matriz de Disrupção Salarial & Risco (Scatter Plot)
*Objetivo: A visualização mais impressionante do portfólio — Quadrantes de Gartner da Força de Trabalho.*
- **Visual Central (Gráfico de Dispersão Quadrante 2x2):**
  - **Eixo X:** `Probabilidade_Media_Automacao` (0% a 100%).
  - **Eixo Y:** `Variacao_Salarial_%` (-30% a +50%).
  - **Tamanho da Bolha:** `Total_Vagas_Pos_IA`.
  - **Cor da Bolha:** Setor Econômico.
  - **Linhas Constantes de Referência:**
    - Linha X constante em 50% de Probabilidade de Automação.
    - Linha Y constante em 0% de Variação Salarial.
- **Os 4 Quadrantes Analíticos:**
  1. *Superior Esquerdo (Baixa Automação, Alto Ganho):* **Super-Trabalhadores Amplificados** (ex: ML Engineers, Cientistas Biomédicos, Gestores Quantitativos).
  2. *Superior Direito (Alta Automação, Ganho Positivo):* **Especialistas em Requalificação** (ex: Técnicos em Automação que operam sistemas autônomos).
  3. *Inferior Esquerdo (Baixa Automação, Baixo Ganho):* **Funções de Cuidado & Presenciais Estáveis** (salários com crescimento moderado, baixa perda de vagas).
  4. *Inferior Direito (Alta Automação, Perda Salarial):* **Área Crítica de Deslocamento** (ex: Atendentes de Banco, Digitadores de Laudos, Redatores operacionais).

---

### Página 4: Simulador de Carreira e Upskilling (What-If Parameters)
*Objetivo: Interatividade avançada com parâmetros DAX.*
- O usuário seleciona o cargo atual e simula:
  1. *"E se eu investir em uma certificação de IA (+15% produtividade)?"*
  2. *"Qual o gap salarial em relação à média do setor?"*
- Exibe a trajetória recomendada de capacitação técnica.
