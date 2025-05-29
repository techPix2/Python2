import psutil
import os
import time
from datetime import datetime
import requests 




def inserirAlerta(enviados):
    try:
        fetch_inserirAlerta = "http://localhost:3333/"
        resposta = requests.post(fetch_inserirAlerta, json={"dadosEnviados": enviados})
        if resposta.status_code == 200:
            print("Alerta inserido com sucesso")
            print(resposta.json())
        else:
            print(f"Erro ao inserir alerta: {resposta.status_code}")
            print(resposta.text)
    except Exception as e:
        print(f"Erro ao conectar ROTA INSERIR: {e}")

def coletar_todas_metricas():
    return {
        'cpu': obter_metricas_cpu(),
        'ram': obter_metricas_ram(),
        'disk': obter_metricas_disco(),
        'network': obter_metricas_rede(),
        'top_processos': obter_top_processos_cpu()
    }


def obter_top_processos_cpu():
    processos = []

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            proc.cpu_percent(interval=None)
            processos.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    time.sleep(1)

    resultados = []

    for proc in processos:
        try:
            cpu = proc.cpu_percent(interval=None)
            if cpu > 0:
                if proc.info['name'] != "System Idle Process":
                    resultados.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'cpu_percent': cpu
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top_processos = sorted(resultados, key=lambda x: x['cpu_percent'], reverse=True)[:10]
    return top_processos

def obter_metricas_cpu():
    freq = psutil.cpu_freq()
    return {
        'Uso (%)': psutil.cpu_percent(interval=1),
        'Frequência (MHz)': freq.current
    }

def obter_metricas_ram():
    mem = psutil.virtual_memory()
    return {
        'Uso (%)': mem.percent,
        'Usado (GB)': round(mem.used / (1024**3), 2),
        'Disponível (GB)': round(mem.available / (1024**3), 2)
    }

def obter_metricas_disco():
    disco_principal = 'C:\\' if os.name == 'nt' else '/'
    uso = psutil.disk_usage(disco_principal)
    return {
        'Partição': disco_principal,
        'Uso (%)': uso.percent
    }

def obter_metricas_rede():
    io = psutil.net_io_counters()
    return {
        'Pacotes Enviados': io.packets_sent,
        'Pacotes Recebidos': io.packets_recv
    }

def monitorar_componentes_selecionados(componentes):
    try:
        print("=== TechPix Monitor ===")
        print("Pressione Ctrl+C para encerrar\n")
        
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n--- Atualização {timestamp} ---")
            
            for comp in componentes:
                try:
                    if comp['type'] == 'cpu':
                        metricas = obter_metricas_cpu()
                        print("\nCPU:")
                        for k, v in metricas.items():
                            print(f"  {k}: {v}")
                            
                    elif comp['type'] == 'ram':
                        metricas = obter_metricas_ram()
                        print("\nRAM:")
                        for k, v in metricas.items():
                            print(f"  {k}: {v}")
                            
                    elif comp['type'] == 'disk':
                        metricas = obter_metricas_disco()
                        print("\nDISCO:")
                        for k, v in metricas.items():
                            print(f"  {k}: {v}")
                            
                    elif comp['type'] == 'network':
                        metricas = obter_metricas_rede()
                        print("\nREDE:")
                        for k, v in metricas.items():
                            print(f"  {k}: {v}")

                    elif comp['type'] == 'process':
                        top_processos = obter_top_processos_cpu()
                        print("\nTOP 10 Processos por Uso de CPU:")
                        for proc in top_processos:
                           print("PID:", proc['pid'], "Nome:", proc['name'], "CPU:", proc['cpu_percent'], "%")

                except Exception as e:
                    print(f"\nErro ao monitorar {comp['type']}: {str(e)}")
            
            print("\n" + "="*40)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado pelo usuário")



enviados = coletar_todas_metricas()

