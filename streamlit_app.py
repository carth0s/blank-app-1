import streamlit as st
import pandas as pd
import numpy as np
import math
import time
import random
import sqlite3
from datetime import datetime

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

# --- FASE 2: BANCO DE DADOS (SQLite) ---
elif fase_selecionada == "Fase 2: Banco de Dados":
    st.header("🗄️ Fase 2: Banco de Dados Estruturado (SQLite)")
    st.markdown("Gerenciamento de Sensores e Leituras com persistência de dados em arquivo `.db`.")

    # --- CONFIGURAÇÃO DO BANCO (Backend) ---
    def get_db_connection():
        # check_same_thread=False é necessário no Streamlit para evitar erros de thread
        conn = sqlite3.connect("sensores.db", check_same_thread=False)
        return conn

    def init_db():
        conn = get_db_connection()
        cursor = conn.cursor()
        # Criação da tabela T_SENSOR
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS T_SENSOR (
            ID_SENSOR INTEGER PRIMARY KEY AUTOINCREMENT,
            TIPO TEXT NOT NULL,
            STATUS TEXT,
            DATA_INSTALACAO TIMESTAMP,
            ID_PLANTACAO INTEGER
        )
        ''')
        # Criação da tabela T_LEITURA_SENSOR
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS T_LEITURA_SENSOR (
            ID_LEITURA INTEGER PRIMARY KEY AUTOINCREMENT,
            DATA_HORA TIMESTAMP,
            VALOR DOUBLE,
            TIPO_MEDICAO TEXT,
            ID_SENSOR INTEGER,
            FOREIGN KEY(ID_SENSOR) REFERENCES T_SENSOR(ID_SENSOR)
        )
        ''')
        conn.commit()
        conn.close()

    # Garante que as tabelas existem ao carregar a página
    init_db()

    # --- INTERFACE (Frontend) ---
    tab_sensores, tab_leituras = st.tabs(["📡 Gerenciar Sensores", "📈 Gerenciar Leituras"])

    # === ABA 1: SENSORES ===
    with tab_sensores:
        st.subheader("Cadastro de Sensores")
        
        with st.form("form_sensor"):
            col1, col2 = st.columns(2)
            input_tipo = col1.selectbox("Tipo do Sensor", ["Umidade (DHT22)", "Temperatura (DHT22)", "Nutrientes (NPK)", "pH Solo"])
            input_status = col2.selectbox("Status", ["Ativo", "Inativo", "Manutenção"])
            input_plantacao = st.number_input("ID da Plantação", min_value=1, value=101)
            
            btn_sensor = st.form_submit_button("Inserir Sensor")
            
            if btn_sensor:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO T_SENSOR (TIPO, STATUS, DATA_INSTALACAO, ID_PLANTACAO)
                    VALUES (?, ?, ?, ?)
                ''', (input_tipo, input_status, datetime.now(), input_plantacao))
                conn.commit()
                conn.close()
                st.success("Sensor inserido com sucesso!")
                st.rerun()

        st.divider()
        st.subheader("Sensores Cadastrados")
        conn = get_db_connection()
        df_sensores = pd.read_sql("SELECT * FROM T_SENSOR", conn)
        conn.close()
        st.dataframe(df_sensores, use_container_width=True)

    # === ABA 2: LEITURAS (CRUD) ===
    with tab_leituras:
        st.subheader("Operações de Leitura (CRUD)")
        
        # Carregar IDs de sensores existentes para o selectbox
        conn = get_db_connection()
        df_ids = pd.read_sql("SELECT ID_SENSOR FROM T_SENSOR", conn)
        conn.close()
        
        lista_ids = df_ids['ID_SENSOR'].tolist() if not df_ids.empty else []

        col_crud1, col_crud2 = st.columns([1, 2])

        # Coluna da Esquerda: Formulários de Ação
        with col_crud1:
            acao = st.radio("Escolha a Operação:", ["Inserir Nova Leitura", "Atualizar Valor", "Deletar Leitura"])
            
            if acao == "Inserir Nova Leitura":
                if not lista_ids:
                    st.warning("Cadastre um sensor primeiro!")
                else:
                    sel_sensor = st.selectbox("ID do Sensor", lista_ids)
                    sel_tipo = st.selectbox("Tipo Medição", ["umidade", "temperatura", "fosforo", "potassio", "pH"])
                    val_leitura = st.number_input("Valor Medido", format="%.2f")
                    
                    if st.button("Salvar Leitura"):
                        conn = get_db_connection()
                        cursor = conn.cursor()
                        cursor.execute('''
                            INSERT INTO T_LEITURA_SENSOR (DATA_HORA, VALOR, TIPO_MEDICAO, ID_SENSOR)
                            VALUES (?, ?, ?, ?)
                        ''', (datetime.now(), val_leitura, sel_tipo, sel_sensor))
                        conn.commit()
                        conn.close()
                        st.success("Leitura salva!")
                        time.sleep(0.5)
                        st.rerun()

            elif acao == "Atualizar Valor":
                id_upd = st.number_input("ID da Leitura para Atualizar", min_value=1, step=1)
                novo_valor = st.number_input("Novo Valor", format="%.2f")
                if st.button("Atualizar"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE T_LEITURA_SENSOR SET VALOR = ? WHERE ID_LEITURA = ?", (novo_valor, id_upd))
                    conn.commit()
                    conn.close()
                    st.success("Atualizado!")
                    time.sleep(0.5)
                    st.rerun()

            elif acao == "Deletar Leitura":
                id_del = st.number_input("ID da Leitura para Deletar", min_value=1, step=1)
                if st.button("Deletar", type="primary"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM T_LEITURA_SENSOR WHERE ID_LEITURA = ?", (id_del,))
                    conn.commit()
                    conn.close()
                    st.warning("Deletado!")
                    time.sleep(0.5)
                    st.rerun()

        # Coluna da Direita: Visualização da Tabela
        with col_crud2:
            st.write("### 📋 Registros Atuais")
            conn = get_db_connection()
            # Join para mostrar qual sensor é (opcional, mas fica bonito)
            query = """
                SELECT L.ID_LEITURA, L.DATA_HORA, L.VALOR, L.TIPO_MEDICAO, L.ID_SENSOR, S.TIPO as MODELO_SENSOR
                FROM T_LEITURA_SENSOR L
                LEFT JOIN T_SENSOR S ON L.ID_SENSOR = S.ID_SENSOR
                ORDER BY L.ID_LEITURA DESC
            """
            try:
                df_leituras = pd.read_sql(query, conn)
                st.dataframe(df_leituras, use_container_width=True, height=400)
            except:
                st.info("Nenhuma leitura registrada ainda.")
            conn.close()

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
