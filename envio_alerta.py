from sns_alerta import enviar_alerta

def monitorar_umidade(valor):
    print(f"Umidade atual: {valor}%")

    if valor < 40:
        enviar_alerta(f"Umidade muito baixa: {valor}%. Acionar irrigação!")
