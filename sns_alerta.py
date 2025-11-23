import boto3
import streamlit as st 

def enviar_alerta_aws(mensagem):
    try:
        # Acessa as chaves de forma segura através do st.secrets
        # O Streamlit lê automaticamente o arquivo .streamlit/secrets.toml
        
        sns = boto3.client(
            "sns",
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY"],
            aws_secret_access_key=st.secrets["AWS_SECRET_KEY"],
            region_name="us-east-1"
        )

        response = sns.publish(
            TopicArn=st.secrets["SNS_ARN"],
            Message=mensagem,
            Subject="🚨 Alerta Crítico – FarmTech"
        )
        
        return True, response['MessageId']

    except KeyError as e:
        return False, f"Chave não encontrada nos Secrets: {e}"
    except Exception as e:
        return False, str(e)
