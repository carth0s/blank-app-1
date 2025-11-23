import boto3
import json

def enviar_alerta_aws(mensagem):
    try:
        # Tenta carregar as credenciais
        with open("aws_credentials.json") as f:
            cred = json.load(f)

        # Conecta na AWS
        sns = boto3.client(
            "sns",
            aws_access_key_id=cred["AWS_ACCESS_KEY"],
            aws_secret_access_key=cred["AWS_SECRET_KEY"],
            region_name="us-east-1"
        )

        # Envia a mensagem
        response = sns.publish(
            TopicArn=cred["SNS_ARN"],
            Message=mensagem,
            Subject="🚨 Alerta Crítico – FarmTech"
        )
        
        # Retorna Sucesso e o ID da mensagem para mostrar no log
        return True, response['MessageId']

    except FileNotFoundError:
        return False, "Arquivo 'aws_credentials.json' não encontrado."
    except Exception as e:
        return False, str(e)
