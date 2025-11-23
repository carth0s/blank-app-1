import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# Configuração da Página
st.set_page_config(page_title="Sistema Integrado Agro 4.0", layout="wide", page_icon="🌱")

# CSS para estilizar
st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO E BARRA LATERAL ---
st.sidebar.title("🚜 Menu de Navegação")
st.sidebar.info("Fase 7: Consolidação do Sistema")
fase_selecionada = st.sidebar.radio("Escolha a Fase para Gerenciar:", 
    ["Home", 
     "Fase 1: Dados & Meteo", 
     "Fase 2: Banco de Dados", 
     "Fase 3: IoT & Sensores", 
     "Fase 4: ML & Decisão", 
     "Fase 5: Cloud AWS", 
     "Fase 6: Visão Computacional"])

st.title("🌱 Sistema de Gestão Agrícola Integrado")
st.markdown("---")

# --- LÓGICA DAS FASES ---

# --- HOME ---
if fase_selecionada == "Home":
    st.header("Bem-vindo ao Painel de Controle")
    st.write("Este dashboard centraliza todas as etapas do projeto, desde a coleta de dados até a inteligência artificial.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Status do Sistema", "Online", delta="Normal")
    col2.metric("Cloud AWS", "Conectado", delta="US-EAST-1")
    col3.metric("Dispositivos IoT", "4 Ativos", delta="+1")
    
    st.image("https://streamlit.io/images/brand/streamlit-mark-color.png", width=100)
    st.info("Selecione uma fase no menu lateral para interagir com os módulos específicos.")

# ... (início do código anterior permanece igual)

# --- FASE 1: DADOS E METEOROLOGIA ---
elif fase_selecionada == "Fase 1: Dados & Meteo":
    st.header("🌦️ Fase 1: Gestão Inicial & Análise")
    st.markdown("Integração dos scripts de Gestão Agrícola (Python) e Cálculo de Custos (Lógica R).")

    # Criando abas para separar os dois códigos que você mandou
    tab_gestao, tab_analise = st.tabs(["🌱 Gestão Agrícola (CRUD)", "📊 Análise Financeira (R)"])

    # --- TAB 1: O CÓDIGO PYTHON ---
    with tab_gestao:
        st.subheader("Gestão Agrícola FarmTech 2025®")
        
        # Inicializando o banco de dados na memória do navegador 
        if 'fazenda' not in st.session_state:
            st.session_state.fazenda = pd.DataFrame(columns=['Cultura', 'Area_m2', 'Insumo', 'Aplicacao_L'])

        # Formulário de Cadastro 
        with st.expander("📝 Cadastrar Nova Cultura", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                cultura_opt = st.selectbox("Selecione a Cultura:", ["Arroz", "Feijão"])
                insumo_opt = st.selectbox("Insumo:", ["Fertilizante", "Pesticida"])
            
            with col2:
                tipo_geo = st.selectbox("Formato da Área:", ["Retângulo", "Círculo", "Trapézio"])
                
                # Inputs dinâmicos baseados na geometria
                area_calc = 0.0
                if tipo_geo == "Retângulo":
                    l = st.number_input("Largura (m)", min_value=0.0)
                    c = st.number_input("Comprimento (m)", min_value=0.0)
                    area_calc = l * c
                elif tipo_geo == "Círculo":
                    r = st.number_input("Raio (m)", min_value=0.0)
                    area_calc = math.pi * (r ** 2)
                elif tipo_geo == "Trapézio":
                    B = st.number_input("Base Maior (m)", min_value=0.0)
                    b = st.number_input("Base Menor (m)", min_value=0.0)
                    h = st.number_input("Altura (m)", min_value=0.0)
                    area_calc = ((B + b) * h) / 2
            
            st.info(f"Área Calculada: {area_calc:.2f} m²")

            if st.button("Salvar Registro"):
                if area_calc > 0:
                    # Lógica de Aplicação
                    taxa = 500 if insumo_opt == "Fertilizante" else 250
                    total_aplicacao = area_calc * taxa
                    
                    # Adicionando ao DataFrame na sessão
                    novo_dado = pd.DataFrame([{
                        'Cultura': cultura_opt,
                        'Area_m2': area_calc,
                        'Insumo': insumo_opt,
                        'Aplicacao_L': total_aplicacao / 1000  # Convertendo para Litros
                    }])
                    st.session_state.fazenda = pd.concat([st.session_state.fazenda, novo_dado], ignore_index=True)
                    st.success(f"{cultura_opt} cadastrado com sucesso!")
                    time.sleep(1) 
                    st.rerun()
                else:
                    st.error("A área deve ser maior que zero.")

        # Visualização e Exclusão 
        st.divider()
        st.subheader("📋 Culturas Cadastradas")
        
        if not st.session_state.fazenda.empty:
            st.dataframe(st.session_state.fazenda, use_container_width=True)
            
            # Botão para limpar tudo 
            if st.button("🗑️ Excluir Todos os Dados"):
                st.session_state.fazenda = pd.DataFrame(columns=['Cultura', 'Area_m2', 'Insumo', 'Aplicacao_L'])
                st.rerun()
        else:
            st.warning("Nenhuma cultura cadastrada.")

    # --- TAB 2: O CÓDIGO R  ---
    with tab_analise:
        st.subheader("Cálculo de Gastos e Estatística (Lógica R)")
        st.caption("Implementação da lógica estatística definida no script R da Fase 1.")
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            r_cultura = st.radio("Cultura (R):", ["Arroz", "Feijão"], horizontal=True)
            r_insumo = st.radio("Insumo (R):", ["Fertilizante", "Pesticida"], horizontal=True)
        
        with col_r2:
            r_litros_txt = st.text_area("Digite os valores de consumo de litros (separados por espaço):", "10 20 15 30 12")
        
        if st.button("Calcular Estatísticas"):
            try:
                # 1. Parsing dos Inputs 
                litros = [float(x) for x in r_litros_txt.split()]
                
                # 2. Definição das constantes 
                if r_cultura == "Arroz":
                    fator = 2.607142857142857
                    ciclo = 140
                else:
                    fator = 4.5625
                    ciclo = 80
                
                if r_insumo == "Fertilizante":
                    custo_litro = 47
                else:
                    custo_litro = 389
                
                # 3. Cálculos Vetoriais 
                litros_anuais = np.array(litros) * fator
                media = math.floor(np.mean(litros_anuais))
                excedente = np.sum(litros_anuais - media)
                gasto_total = np.sum(litros_anuais) * custo_litro
                
                # 4. Exibição dos Resultados 
                st.divider()
                st.markdown(f"### 📑 Resultados para {r_cultura}")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Ciclo de Plantio", f"{ciclo} dias")
                m2.metric("Média Anual", f"{media} L")
                m3.metric("Custo Total", f"R$ {gasto_total:,.2f}")
                
                st.info(f"**Desvio (Excedente):** {excedente:.2f} litros além da média.")
                
                # Gráfico extra 
                st.bar_chart(litros_anuais)
                st.caption("Distribuição dos Litros Anuais Calculados")

            except ValueError:
                st.error("Erro na entrada de dados! Certifique-se de usar apenas números separados por espaço.")

# --- FASE 2: BANCO DE DADOS ---
elif fase_selecionada == "Fase 2: Banco de Dados":
    st.header("🗄️ Fase 2: Banco de Dados Estruturado")
    st.markdown("Visualização das tabelas do MER/DER consolidadas.")
    
    tab1, tab2 = st.tabs(["Tabela Sensores", "Tabela Produção"])
    
    with tab1:
        # Simulação de dados vindos do SQL
        st.write("**Tabela: TB_IOT_LEITURAS**")
        df_db = pd.DataFrame({
            'ID_LEITURA': range(1001, 1006),
            'TIMESTAMP': pd.date_range(start='now', periods=5, freq='min'),
            'SENSOR_TYPE': ['DHT22', 'DHT22', 'LDR', 'PH_METER', 'DHT22'],
            'VALOR': [24.5, 24.6, 800, 7.2, 24.7]
        })
        st.dataframe(df_db, use_container_width=True)
        st.caption("Dados carregados do PostgreSQL (Simulado).")

    with tab2:
        st.write("**Tabela: TB_PLANTIO**")
        st.dataframe(pd.DataFrame({
            'CULTURA': ['Soja', 'Milho', 'Café'],
            'AREA_HA': [150, 200, 80],
            'STATUS': ['Crescimento', 'Colheita', 'Florada']
        }))

# --- FASE 3: IOT E AUTOMAÇÃO ---
elif fase_selecionada == "Fase 3: IoT & Sensores":
    st.header("📡 Fase 3: IoT e Controle em Tempo Real")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Monitoramento em Tempo Real (ESP32)")
        # Simulação de valores de sensores
        temp = random.uniform(20.0, 35.0)
        umid = random.uniform(40.0, 80.0)
        solo = random.randint(300, 800) # Leitura analógica simulada
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Temperatura (DHT22)", f"{temp:.1f} °C")
        m2.metric("Umidade Ar", f"{umid:.1f} %")
        m3.metric("Umidade Solo (LDR/Cap)", f"{solo}")
        
    with col2:
        st.subheader("Atuadores")
        st.write("Controle de Irrigação")
        irrigacao = st.toggle("Ativar Bomba de Água")
        if irrigacao:
            st.warning("⚠️ BOMBA LIGADA - Enviando comando ao ESP32...")
        else:
            st.success("Bomba Desligada - Economia de energia.")

# --- FASE 4: MACHINE LEARNING ---
elif fase_selecionada == "Fase 4: ML & Decisão":
    st.header("🤖 Fase 4: Dashboard Preditivo (Scikit-Learn)")
    
    st.write("Previsão de necessidade de irrigação baseada em dados históricos.")
    
    # Inputs para o modelo
    col_in1, col_in2 = st.columns(2)
    input_temp = col_in1.slider("Temperatura Atual", 10, 45, 30)
    input_umid = col_in2.slider("Umidade do Solo (0-1000)", 0, 1000, 450)
    
    if st.button("Rodar Modelo Preditivo"):
        # Simulação simples de lógica de ML
        # Em produção, aqui você carregaria: model = joblib.load('modelo_agro.pkl')
        chance_irrigacao = 0
        if input_temp > 30 or input_umid < 400:
            prediction = "IRRIGAR AGORA"
            cor = "error" # vermelho
        else:
            prediction = "AGUARDAR"
            cor = "success" # verde
            
        st.subheader("Resultado da IA:")
        st.markdown(f"Ação Recomendada: :{cor}[**{prediction}**]")
        
        # Gráfico simples de dispersão
        st.caption("Dispersão dos dados de treino (Visualização)")
        chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['Temp', 'Umidade'])
        st.scatter_chart(chart_data)

# --- FASE 5: CLOUD COMPUTING ---
elif fase_selecionada == "Fase 5: Cloud AWS":
    st.header("☁️ Fase 5: Infraestrutura Cloud & Segurança")
    
    st.markdown("### Monitoramento de Segurança (ISO 27001)")
    
    col1, col2, col3 = st.columns(3)
    col1.success("Encryption at Rest: **ATIVO**")
    col2.success("Firewall WAF: **ATIVO**")
    col3.success("Backup Automático: **02:00 AM**")
    
    st.markdown("### Logs de Acesso (Audit Trail)")
    logs = pd.DataFrame({
        'User': ['admin', 'sistema_iot', 'gestor_agro'],
        'Action': ['LOGIN', 'POST_DATA', 'VIEW_DASHBOARD'],
        'IP': ['192.168.1.10', '10.0.0.55', '189.32.11.4'],
        'Status': ['Allow', 'Allow', 'Allow']
    })
    st.table(logs)

# --- FASE 6: VISÃO COMPUTACIONAL ---
elif fase_selecionada == "Fase 6: Visão Computacional":
    st.header("👁️ Fase 6: Detecção de Pragas (YOLO)")
    
    st.write("Upload de imagem da plantação para análise de saúde.")
    
    uploaded_file = st.file_uploader("Escolha uma imagem da lavoura...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption='Imagem Carregada', width=400)
        
        if st.button("Processar Imagem com YOLO"):
            with st.spinner('Rede Neural analisando pixels...'):
                time.sleep(2) # Simula processamento pesado
                
                # Aqui entraria a chamada real: results = model(imagem)
                
                st.subheader("Resultados da Análise:")
                st.error("⚠️ DETECÇÃO: Ferrugem Asiática (Confiança: 92%)")
                st.success("✅ CRESCIMENTO: Normal nas demais áreas")
                
                st.progress(92, text="Nível de Confiança da IA")

# --- RODAPÉ ---
st.sidebar.markdown("---")
st.sidebar.caption("FIAP - Projeto Fase 7 Consolidação")
