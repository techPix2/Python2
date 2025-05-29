import psutil
import os
import time
from datetime import datetime
import requests
import json

# Função para enviar os dados via POST
def enviarDados(enviados):
    try:
        urlNode = "http://localhost:80/dashMatheus/dadosMaquina"
        resposta = requests.post(urlNode, json={"dadosEnviados": enviados})
        if resposta.status_code == 200:
            print("Dados enviados com sucesso")
            print(json.dumps(resposta.json(), indent=4))
        else:
            print(f"Erro ao enviar dados: {resposta.status_code}")
            print(resposta.text)
    except Exception as e:
        print(f"Erro ao enviar dados: {e}")

# Função principal que coleta todas as métricas
def coletar_todas_metricas():
    return {
        'cpu': obter_metricas_cpu(),
        'ram': obter_metricas_ram(),
        'disk': obter_metricas_disco(),
        'network': obter_metricas_rede(),
        'top_processos': obter_top_processos_cpu()
    }

# Função para obter o top 10 processos que mais consomem CPU
def obter_top_processos_cpu():
    processos = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc.cpu_percent(interval=None)
            processos.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(1)  # Espera para capturar o uso real de CPU

    resultados = []

    for proc in processos:
        try:
            cpu = proc.cpu_percent(interval=None)
            if cpu > 0 and proc.info['name'] != "System Idle Process":
                resultados.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': cpu
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_processos = sorted(resultados, key=lambda x: x['cpu_percent'], reverse=True)[:10]
    return top_processos

# Coleta métricas da CPU
def obter_metricas_cpu():
    freq = psutil.cpu_freq()
    return {
        'Uso (%)': psutil.cpu_percent(interval=1),
        'Frequência (MHz)': freq.current
    }

# Coleta métricas da RAM
def obter_metricas_ram():
    mem = psutil.virtual_memory()
    return {
        'Uso (%)': mem.percent,
        'Usado (GB)': round(mem.used / (1024**3), 2),
        'Disponível (GB)': round(mem.available / (1024**3), 2)
    }

# Coleta métricas do disco
def obter_metricas_disco():
    disco_principal = 'C:\\' if os.name == 'nt' else '/'
    uso = psutil.disk_usage(disco_principal)
    return {
        'Partição': disco_principal,
        'Uso (%)': uso.percent
    }

# Coleta métricas de rede
def obter_metricas_rede():
    io = psutil.net_io_counters()
    return {
        'Pacotes Enviados': io.packets_sent,
        'Pacotes Recebidos': io.packets_recv
    }

def loop_envio(intervalo=0.1):
    print("Iniciando envio contínuo de métricas...")
    while True:
        try:
            # 1. Coleta os dados
            metricas = coletar_todas_metricas()
            print("\n--- Dados Coletados ---")
            print(json.dumps(metricas, indent=2))  # Log para depuração

            # 2. Envia os dados para o servidor
            enviarDados(metricas)

            # 3. Aguarda o intervalo definido
            time.sleep(intervalo)

        except KeyboardInterrupt:
            print("\nMonitoramento encerrado pelo usuário.")
            break  # Sai do loop se o usuário pressionar Ctrl+C

        except Exception as e:
            print(f"\n[ERRO] Falha no ciclo de envio: {e}")
            print("Tentando novamente em 5 segundos...")
            time.sleep(2)  # Espera um pouco antes de tentar novamente
            continue  # Continua o loop
