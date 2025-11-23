import boto3
import json

def enviar_alerta(mensagem):
    # Lê chaves de um arquivo (NÃO subir no GitHub!)
    with open("aws_credentials.json") as f:
        cred = json.load(f)

    sns = boto3.client(
        "sns",
        aws_access_key_id=cred["AWS_ACCESS_KEY"],
        aws_secret_access_key=cred["AWS_SECRET_KEY"],
        region_name="us-east-1"
    )

    sns.publish(
        TopicArn=cred["SNS_ARN"],
        Message=mensagem,
        Subject="Alerta Automático – FarmTech"
    )

    print("[AWS SNS] Alerta enviado:", mensagem)
