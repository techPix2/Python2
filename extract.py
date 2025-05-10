import psutil
import os
import time
from datetime import datetime

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
        # Cabeçalho inicial
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
                            
                except Exception as e:
                    print(f"\nErro ao monitorar {comp['type']}: {str(e)}")
            
            print("\n" + "="*40)  # Linha separadora
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado pelo usuário")