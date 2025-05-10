
# import os
# import psutil
# from datetime import datetime
# import time
# from setup import getDiscos


# def cpuData():
#     cpuFreq = psutil.cpu_freq()
#     cpuPercent = psutil.cpu_percent()
#     return cpuFreq, cpuPercent

# def ramData():
#     ramUsed = psutil.virtual_memory().used
#     ramPercent = psutil.virtual_memory().percent
#     return ramUsed, ramPercent

# def diskData(path):
#     diskUsed = psutil.disk_usage(path).used
#     diskPercent = psutil.disk_usage(path).percent
#     return diskUsed, diskPercent

# def netData():
#     bytesSend = psutil.net_io_counters().bytes_sent
#     bytesRecv = psutil.net_io_counters().bytes_recv
#     return [bytesRecv, bytesSend]

# def processData():
#     processes = []
#     for proc in psutil.process_iter(['name', 'memory_percent', 'cpu_percent', 'memory_info']):
#         try:
#             process_info = {
#                 'name': proc.info['name'],
#                 'memory_percent': proc.info['memory_percent'],
#                 'cpu_percent': proc.info['cpu_percent'],
#                 'vms': proc.info['memory_info'].vms if proc.info['memory_info'] else None
#             }
#             processes.append(process_info)
#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue
#     return processes

# def colectALL(discos):
#     cpuFreq, cpuPercent = cpuData()
#     ramUsed, ramPercent = ramData()
#     netRecv, netSend = netData()

#     row = [
#         cpuFreq.current,
#         cpuPercent,
#         ramUsed,
#         ramPercent,
#         netRecv,
#         netSend
#     ]

#     for disco in discos:
#         try:
#             disk_used, disk_percent = diskData(disco['path'])
#             row.extend([disk_used, disk_percent])
#         except Exception as e:
#             print(f"Erro ao acessar disco {disco['path']}: {str(e)}")
#             row.extend([None, None])

#     return row

# def monitorar():
#     discos = getDiscos("linux")

#     while True:
#         try:
#             dados = colectALL(discos)
#             print("Dados coletados:", dados)

#             processos = processData()
#             print("Total de processos monitorados:", len(processos))
#             for proc in processos:
#                 print(proc)
#             print(dados)     
#             print(processos)     
#             time.sleep(2)

#         except KeyboardInterrupt:
#             print("\nMonitoramento encerrado pelo usuário")
#             break

#         except Exception as e:
#             print(f"Erro durante o monitoramento: {str(e)}")
#             time.sleep(2)

# monitorar()

import psutil
import time
from datetime import datetime

def obter_dados_cpu():
    freq = psutil.cpu_freq()
    return {
        'percent': psutil.cpu_percent(),
        'freq_current': freq.current,
        'freq_min': freq.min,
        'freq_max': freq.max
    }

def obter_dados_ram():
    mem = psutil.virtual_memory()
    return {
        'used': mem.used,
        'percent': mem.percent,
        'available': mem.available,
        'total': mem.total
    }

def obter_dados_disco(path):
    uso = psutil.disk_usage(path)
    return {
        'used': uso.used,
        'percent': uso.percent,
        'free': uso.free,
        'total': uso.total
    }

def obter_dados_rede():
    io = psutil.net_io_counters()
    return {
        'bytes_sent': io.bytes_sent,
        'bytes_recv': io.bytes_recv,
        'packets_sent': io.packets_sent,
        'packets_recv': io.packets_recv
    }

def obter_processos():
    processos = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            processos.append({
                'pid': proc.info['pid'],
                'name': proc.info['name'],
                'memory_percent': proc.info['memory_percent'],
                'cpu_percent': proc.info['cpu_percent']
            })
        except psutil.NoSuchProcess:
            continue
    return processos

def monitorar_componentes_selecionados(componentes):
    try:
        while True:
            dados = {}
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for comp in componentes:
                try:
                    if comp['type'] == 'cpu':
                        dados['cpu'] = obter_dados_cpu()
                    elif comp['type'] == 'ram':
                        dados['ram'] = obter_dados_ram()
                    elif comp['type'] == 'disk' and comp['path']:  # Verifica se há path
                        try:
                            dados['disk'] = {
                                'path': comp['path'],
                                **obter_dados_disco(comp['path'])
                            }
                        except Exception as e:
                            print(f"Erro ao monitorar disco {comp['path']}: {str(e)}")
                            dados['disk'] = None
                    elif comp['type'] == 'network':
                        dados['network'] = obter_dados_rede()
                except Exception as e:
                    print(f"Erro ao monitorar {comp['type']}: {str(e)}")
                    dados[comp['type']] = None
            
            # Exibir dados formatados
            print(f"\n=== Dados em {timestamp} ===")
            for tipo, valores in dados.items():
                if valores is None:
                    continue
                    
                print(f"\n{tipo.upper()}:")
                if tipo == 'disk':
                    print(f"  Disco: {valores['path']}")
                    for chave, valor in valores.items():
                        if chave != 'path':
                            print(f"  {chave}: {valor}")
                else:
                    for chave, valor in valores.items():
                        print(f"  {chave}: {valor}")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado pelo usuário")
    except Exception as e:
        print(f"\nErro no monitoramento: {str(e)}")


   