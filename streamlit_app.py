import streamlit as st
import pandas as pd
import numpy as np
import joblib
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
     "Fase 1: Calculo Area", 
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
    st.header("📡 Fase 3: Monitoramento IoT & Controle")
    st.markdown("Interface de Gêmeo Digital: Simula a lógica do firmware ESP32 em tempo real.")

    # Layout: Coluna da Esquerda (Simulador Físico) | Coluna da Direita (Painel de Monitoramento)
    col_simulacao, col_painel = st.columns([1, 2])

    with col_simulacao:
        st.subheader("🎛️ Simulador de Hardware")
        st.caption("Ajuste os valores como se fossem os sensores físicos:")
        
        # 1. Simula o DHT22 (Umidade)
        # No C++: float umidade = dht.readHumidity();
        input_umidade = st.slider("Umidade do Solo (%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        
        # 2. Simula o sensor de pH (LDR)
        # No C++: int ph = analogRead(SENSOR_PH); (0 a 4095 no ESP32)
        input_ph_raw = st.slider("Leitura pH (LDR / Analógico)", 0, 4095, 2000)
        
        # 3. Simula os Botões de Nutrientes
        # No C++: digitalRead(...) == LOW;
        st.markdown("**Sensores de Nutrientes**")
        tem_fosforo = st.checkbox("Fósforo Presente?", value=True)
        tem_potassio = st.checkbox("Potássio Presente?", value=True)

    with col_painel:
        st.subheader("📊 Painel de Controle (Dashboard)")
        
        # --- LÓGICA DO FIRMWARE TRADUZIDA PARA PYTHON ---
        # No C++: if (umidade < 40.0) { digitalWrite(LED_BOMBA, HIGH); }
        estado_bomba = "DESLIGADA"
        cor_bomba = "off" # cinza
        
        if input_umidade < 40.0:
            estado_bomba = "LIGADA 💧"
            cor_bomba = "normal" # verde no st.metric não tem cor direta, mas usamos delta
            delta_bomba = "Ativa"
            msg_bomba = "⚠️ Umidade Crítica! Bomba acionada automaticamente."
            tipo_msg = st.warning
        else:
            delta_bomba = "Inativa"
            msg_bomba = "✅ Umidade adequada. Bomba em stand-by."
            tipo_msg = st.success

        # Exibição dos Cards (Metrics)
        m1, m2, m3 = st.columns(3)
        m1.metric("Umidade Atual", f"{input_umidade:.1f}%", delta="- Seco" if input_umidade < 40 else "+ Úmido")
        
        # Conversão visual simples do LDR para escala 0-14 (apenas estimativa visual)
        # Supondo que 0=Ácido(0) e 4095=Alcalino(14)
        ph_estimado = (input_ph_raw / 4095) * 14
        m2.metric("Nível pH (Est.)", f"{ph_estimado:.1f}", delta=f"Raw: {input_ph_raw}")
        
        m3.metric("Status Bomba", estado_bomba, delta=delta_bomba, delta_color="inverse" if input_umidade < 40 else "normal")

        # Exibição do Alerta da Bomba
        tipo_msg(msg_bomba)

        st.divider()

        # --- MONITOR DE NUTRIENTES ---
        st.write("#### 🧪 Monitor de Nutrientes")
        
        c_fos, c_pot = st.columns(2)
        
        # Lógica C++: if (!fosforo) Serial.println("Alerta...");
        with c_fos:
            if tem_fosforo:
                st.success("Fósforo (P): **OK**")
            else:
                st.error("Fósforo (P): **AUSENTE!**")
                st.caption("Ação: Aplicar fertilizante rico em P.")

        with c_pot:
            if tem_potassio:
                st.success("Potássio (K): **OK**")
            else:
                st.error("Potássio (K): **AUSENTE!**")
                st.caption("Ação: Aplicar fertilizante rico em K.")

    # Gráfico em tempo real (Simulação Visual)
    st.divider()
    st.caption("Simulação do Serial Plotter (Histórico Recente)")
    
    # Criando dados aleatórios próximos do valor selecionado para dar efeito de "leitura real"
    dados_grafico = pd.DataFrame({
        'Umidade': [input_umidade + np.random.uniform(-1, 1) for _ in range(20)],
        'Linha de Corte': [40] * 20
    })
    st.line_chart(dados_grafico, color=["#3366cc", "#ff0000"])

# --- FASE 4: MACHINE LEARNING ---
elif fase_selecionada == "Fase 4: ML & Decisão":
    # 1. Título e Descrição (Adaptado do seu st.title)
    st.header("💧 Previsão de Irrigação - FarmTech Solutions")
    st.markdown("Este sistema decide se é necessário irrigar com base na umidade do solo.")

    # 2. Carregar modelo (Com proteção para não travar o app se faltar o arquivo)
    modelo = None
    try:
        import joblib # Importação local para garantir
        modelo = joblib.load("modelo_irrigacao.pkl")
    except FileNotFoundError:
        st.error("⚠️ O arquivo 'modelo_irrigacao.pkl' não foi encontrado na pasta.")
    except Exception as e:
        st.error(f"Erro ao carregar modelo: {e}")

    # 3. Entrada manual
    umidade = st.slider("Umidade do Solo (%)", min_value=0.0, max_value=100.0, step=0.1)

    # 4. Previsão
    if st.button("Verificar Necessidade de Irrigação"):
        if modelo is not None:
            # Seu código original de predição
            resultado = modelo.predict([[umidade]])[0]
            
            if resultado == 1:
                st.warning("🚨 Irrigação Necessária!")
            else:
                st.success("✅ Solo não precisa ser irrigado.")
        else:
            # Fallback caso o modelo não tenha carregado
            st.info("O modelo não está carregado, mas baseado na regra (Umidade < 40%):")
            if umidade < 40:
                st.warning("🚨 Irrigação Necessária! (Simulação)")
            else:
                st.success("✅ Solo não precisa ser irrigado. (Simulação)")

    # 5. Exibir CSV original para contexto
    st.divider()
    st.subheader("📊 Base de Dados Simulada")
    
    try:
        df = pd.read_csv("dataset_umidade.csv")
        st.dataframe(df.head(20), use_container_width=True)
    except FileNotFoundError:
        st.warning("O arquivo 'dataset_umidade.csv' não foi encontrado para visualização.")
            
# --- FASE 5: CLOUD COMPUTING ---
elif fase_selecionada == "Fase 5: Cloud AWS":
    st.header("☁️ Fase 5: Integração Cloud (AWS SNS)")
    st.markdown("Serviço de mensageria para disparar alertas de segurança via nuvem.")

    col_monitor, col_log = st.columns([1, 1])

    with col_monitor:
        st.subheader("Monitoramento de Umidade")
        st.info("O sistema verifica automaticamente se a umidade está abaixo de 40%.")

        # Slider para simular o sensor
        umidade_aws = st.slider("Simular Sensor de Umidade (%)", 0, 100, 35)

        # Botão para testar o envio
        if st.button("Verificar e Disparar Alerta", type="primary"):
            
            # Lógica de Monitoramento
            if umidade_aws < 40:
                st.warning(f"⚠️ Umidade Crítica detectada: {umidade_aws}%")
                st.toast("Conectando à AWS...", icon="☁️")
                
                # --- AQUI CHAMAMOS O SEU ARQUIVO EXTERNO ---
                try:
                    from sns_alerta import enviar_alerta_aws
                    
                    mensagem_envio = f"ALERTA FARMTECH: Umidade do solo crítica ({umidade_aws}%). Acionar irrigação imediatamente."
                    sucesso, retorno = enviar_alerta_aws(mensagem_envio)

                    if sucesso:
                        st.success(f"✅ Alerta enviado para AWS SNS! ID: {retorno}")
                        st.json({"Status": "Sent", "MessageId": retorno, "Topic": "FarmTech-Alerts"})
                    else:
                        st.error(f"❌ Falha na conexão AWS: {retorno}")
                        st.caption("Dica: Verifique se o arquivo 'aws_credentials.json' está na pasta com as chaves corretas.")
                
                except ImportError:
                    st.error("Erro: O arquivo 'sns_alerta.py' não foi encontrado na pasta do projeto.")
            
            else:
                st.success(f"✅ Níveis normais ({umidade_aws}%). Nenhum alerta necessário.")

    with col_log:
        st.subheader("Arquitetura da Solução")
        st.markdown("""
        **Como funciona essa integração:**
        1. O Script Python detecta a condição crítica (`< 40%`).
        2. O sistema lê as credenciais seguras do arquivo `json`.
        3. Utiliza a biblioteca **Boto3** para conectar ao serviço SNS.
        4. O SNS dispara o e-mail/SMS para o agrônomo responsável.
        """)
        
        # Mostra o código JSON de exemplo para fins didáticos (ocultando chaves reais se quiser)
        with st.expander("Ver Estrutura do JSON de Credenciais"):
            st.code("""
{
    "AWS_ACCESS_KEY": "AKIA...",
    "AWS_SECRET_KEY": "wJalr...",
    "SNS_ARN": "arn:aws:sns:us-east-1:..."
}
            """, language="json")
# --- FASE 6: VISÃO COMPUTACIONAL ---
elif fase_selecionada == "Fase 6: Visão Computacional":
    st.header("👁️ Fase 6: Detecção Visual de Doenças (YOLO)")
    st.markdown("""
    Módulo de análise de imagens utilizando Redes Neurais Convolucionais (YOLOv8) 
    para identificar doenças em folhas de batata.
    """)

    # Layout de duas colunas: Upload na esquerda, Resultado na direita
    col_upload, col_resultado = st.columns([1, 1.5], gap="large")

    with col_upload:
        st.subheader("📷 Coleta de Imagem")
        st.info("Faça o upload de uma imagem clara de uma folha de batata.")
        
        # Widget para subir a foto
        uploaded_file = st.file_uploader("Escolha uma imagem (.jpg, .png)", type=["jpg", "png", "jpeg"])

        if uploaded_file is not None:
            # Mostra a imagem carregada com borda arredondada
            st.image(uploaded_file, caption="Imagem Carregada", use_container_width=True)

    with col_resultado:
        st.subheader("🧠 Análise da Inteligência Artificial")

        if uploaded_file is None:
            st.warning("👈 Aguardando upload de imagem para iniciar a análise.")
        else:
            # Botão para disparar a "análise"
            if st.button("🔍 Iniciar Diagnóstico com YOLO", type="primary"):
                
                # 1. Simulação do tempo de processamento da GPU
                with st.spinner("Processando imagem na rede neural..."):
                    time.sleep(3) # Espera 3 segundos para parecer real
                
                # 2. Lógica de Simulação (Sorteio de Resultados Realistas para Batata)
                import random
                # Lista de possíveis diagnósticos
                diagnosticos_possiveis = [
                    {"label": "SAUDÁVEL (Healthy)", "conf": 0.96, "tipo": "ok", "msg": "Planta sem sinais de patógenos."},
                    {"label": "PINTA PRETA (Early Blight)", "conf": 0.89, "tipo": "doenca", "msg": "Fungo *Alternaria solani* detectado. Requer fungicida."},
                    {"label": "REQUEIMA (Late Blight)", "conf": 0.92, "tipo": "doenca", "msg": "Doença grave (*Phytophthora infestans*). Ação imediata necessária."}
                ]
                # Sorteia um para mostrar na tela
                resultado_final = random.choice(diagnosticos_possiveis)
                
                # 3. Exibição dos Resultados
                st.divider()
                st.write(f"### Diagnóstico: **{resultado_final['label']}**")
                
                # Barra de confiança
                st.progress(resultado_final["conf"], text=f"Confiança do Modelo: {resultado_final['conf']*100:.1f}%")
                
                if resultado_final["tipo"] == "ok":
                    st.success(f"✅ {resultado_final['msg']}")
                else:
                    # Se for doença, mostra alerta vermelho e OPÇÃO DE AWS
                    st.error(f"🚨 {resultado_final['msg']}")
                    
                    st.markdown("---")
                    st.subheader("⚠️ Ação Crítica Necessária")
                    st.write("A doença detectada requer notificação imediata ao agrônomo responsável.")
                

# --- RODAPÉ ---
st.sidebar.markdown("---")
st.sidebar.caption("FIAP - Projeto Fase 7 Consolidação")
