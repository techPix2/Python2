import psutil
import os
import time
from datetime import datetime
import requests
import json
import base64

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


def criar_issue_jira(titulo, descricao):
    JIRA_DOMAIN = 'techpix.atlassian.net'  
    PROJECT_KEY = 'TECH'                    
    JIRA_EMAIL = 'techpix.sptech@gmail.com'       
    JIRA_API_TOKEN = 'ATATT3xFfGF0633uV3Ia8PHiXys7NGu0Q1GEekwjkJRncW4NHaXNpiH4ZrzW5dChG0_XDMvABd-JWlM-eCTy3hIGNXX6ttVeZT8SDc_6_mjAxKTw5ba_n14vbGT5v-tbgwul4zp5duLoyDVQjoAPKf8SMNuV9xS_W_W8-YOtGLxa06v3Iq_vOLU=03A2E16C'     
        

    url = f'https://{JIRA_DOMAIN}/rest/api/2/issue'

    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "summary": titulo,
            "description": descricao,
            "issuetype": {"name": "Task"},
            "priority": { "name": "High" },
             
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()).decode()
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            print("[JIRA] Issue criada com sucesso:", response.json()['key'])
        else:
            print("[JIRA] Erro ao criar issue:", response.status_code)
            print(response.text)
    except Exception as e:
        print(f"[JIRA] Exceção ao criar issue: {e}")

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
            print(json.dumps(metricas, indent=2))

            # 2. Envia os dados para o servidor
            enviarDados(metricas)


            # 3. Verificação de alertas
            cpu = metricas['cpu']['Uso (%)']
            ram = metricas['ram']['Uso (%)']
            disco = metricas['disk']['Uso (%)']

            if cpu > 75:
                criar_issue_jira(
                    titulo="⚠️ Alerta: CPU acima de 75%",
                    descricao=f"O uso da CPU atingiu {cpu}%."
                )

            if ram > 75:
                criar_issue_jira(
                    titulo="⚠️ Alerta: RAM acima de 75%",
                    descricao=f"O uso de RAM atingiu {ram}%."
                )

            if disco > 90:
                criar_issue_jira(
                    titulo="⚠️ Alerta: Disco acima de 75%",
                    descricao=f"O uso de disco atingiu {disco}%."
                )

            # 4. Aguarda o intervalo
            time.sleep(intervalo)

        except KeyboardInterrupt:
            print("\nMonitoramento encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"\n[ERRO] Falha no ciclo de envio: {e}")
            print("Tentando novamente em 5 segundos...")
            time.sleep(5)



# função  loopenvio padrão para testes sem enviar  para o jira 

# def loop_envio(intervalo=0.1):
#     print("Iniciando envio contínuo de métricas...")
#     while True:
#         try:
#             # 1. Coleta os dados
#             metricas = coletar_todas_metricas()
#             print("\n--- Dados Coletados ---")
#             print(json.dumps(metricas, indent=2))

#             # 2. Envia os dados para o servidor
#             enviarDados(metricas)
#                 # 4. Aguarda o intervalo
#             time.sleep(intervalo)

#         except KeyboardInterrupt:
#             print("\nMonitoramento encerrado pelo usuário.")
#             break
#         except Exception as e:
#             print(f"\n[ERRO] Falha no ciclo de envio: {e}")
#             print("Tentando novamente em 5 segundos...")
#             time.sleep(5)