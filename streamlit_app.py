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

# --- FASE 1: DADOS E METEOROLOGIA ---
elif fase_selecionada == "Fase 1: Dados & Meteo":
    st.header("🌦️ Fase 1: Base Inicial e Meteorologia")
    
    st.subheader("1.1 Integração API Meteorológica (Simulação)")
    # Simulação de chamada de API
    if st.button("Atualizar Dados Meteorológicos"):
        with st.spinner('Consultando API Externa...'):
            time.sleep(1)
            st.success("Dados recebidos com sucesso!")
            
            # Dados fictícios
            clima_data = {
                'Dia': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'],
                'Temp (°C)': [28, 27, 30, 32, 29],
                'Umidade (%)': [60, 65, 55, 50, 62],
                'Precipitação (mm)': [0, 2, 0, 0, 5]
            }
            df_clima = pd.DataFrame(clima_data)
            st.dataframe(df_clima, use_container_width=True)
            
            st.subheader("1.2 Análise Estatística (R integration simulation)")
            st.line_chart(df_clima.set_index('Dia')['Temp (°C)'])

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
