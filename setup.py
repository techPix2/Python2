
# import os
# import platform
# import socket
# import subprocess
# import json
# import re

# # Configuração do sistema
# so = platform.system().lower()

# class MonitorConfig:
#     def __init__(self):
#         self.intervalo = 2  # segundos
#         self.limite_cpu = 80  # %
#         self.limite_ram = 80  # %
#         self.limite_disco = 80  # %

# def obter_id_placa_mae():
#     try:
#         if so == "windows":
#             cmd = "wmic baseboard get serialnumber"
#             resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             return resultado.stdout.strip().split('\n')[-1] or "DESCONHECIDO"
#         else:
#             cmd = "dmidecode -s system-serial-number"
#             resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             return resultado.stdout.strip() or "DESCONHECIDO"
#     except Exception as e:
#         print(f"Erro ao obter ID da placa-mãe: {str(e)}")
#         return "ERRO"

# def obter_hostname():
#     try:
#         return socket.gethostname()
#     except:
#         try:
#             return os.uname().nodename
#         except:
#             return "HOSTNAME-DESCONHECIDO"

# def obter_mac_address():
#     try:
#         if so == "windows":
#             cmd = "getmac /v /FO CSV"
#         else:
#             cmd = "ip link show | grep 'link/ether' | awk '{print $2}' | head -n1"
        
#         resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#         return resultado.stdout.strip().split(',')[0] if so == "windows" else resultado.stdout.strip()
#     except Exception as e:
#         print(f"Erro ao obter MAC: {str(e)}")
#         return "00:00:00:00:00:00"

# def obter_discos():
#     discos = []
#     try:
#         if so == "windows":
#             cmd = "wmic diskdrive get DeviceID,Size /format:csv"
#             resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             # Processar resultado...
#         else:
#             cmd = "lsblk -d -b -n -o NAME,SIZE"
#             resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             # Processar resultado...
        
#         # Adicionar lógica de processamento aqui
#         return discos
        
#     except Exception as e:
#         print(f"Erro ao obter discos: {str(e)}")
#         return discos

# def obter_info_sistema():
#     return {
#         'so': platform.system(),
#         'versao': platform.release(),
#         'arquitetura': platform.architecture()[0],
#         'hostname': obter_hostname(),
#         'mac': obter_mac_address(),
#         'placa_mae': obter_id_placa_mae(),
#         'discos': obter_discos()
#     }

# def get_system_components(so):
#     """Obtém todos os componentes do sistema de forma padronizada"""
#     componentes = []
    
#     # CPU
#     try:
#         if so == "windows":
#             cmd = "wmic cpu get name"
#         else:
#             cmd = "cat /proc/cpuinfo | grep 'model name' | uniq | cut -d ':' -f 2"
        
#         resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#         nome_cpu = resultado.stdout.strip().split('\n')[-1] if so == "windows" else resultado.stdout.strip()
        
#         componentes.append({
#             'type': 'cpu',  # Alterado para minúsculo
#             'name': nome_cpu or "CPU Desconhecida",
#             'description': None,
#             'path': None  # Adicionado campo path
#         })
#     except Exception as e:
#         print(f"Erro ao obter CPU: {str(e)}")
    
#     # RAM
#     try:
#         componentes.append({
#             'type': 'ram',  # Alterado para minúsculo
#             'name': 'Memória Principal',
#             'description': None,
#             'path': None  # Adicionado campo path
#         })
#     except Exception as e:
#         print(f"Erro ao obter RAM: {str(e)}")
    
#     # Discos (corrigido)
#     try:
#         if so == "windows":
#             cmd = "wmic logicaldisk get deviceid,size /format:csv"
#             resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             linhas = [linha.split(',') for linha in resultado.stdout.strip().split('\n')[1:] if linha]
#             for linha in linhas:
#                 if len(linha) >= 3:
#                     componentes.append({
#                         'type': 'disk',
#                         'name': f"Disco {linha[1]}",
#                         'description': f"{linha[2]} bytes" if linha[2].isdigit() else "Tamanho desconhecido",
#                         'path': linha[1] + '\\'  # Adiciona barra invertida para Windows
#                     })
#         else:  # Linux
#             cmd = "df -h --output=source,pcent,size | awk 'NR>1 {print $1,$2,$3}'"
#             resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#             for linha in resultado.stdout.strip().split('\n'):
#                 partes = linha.split()
#                 if len(partes) >= 3:
#                     componentes.append({
#                         'type': 'disk',
#                         'name': f"Disco {partes[0]}",
#                         'description': f"{partes[2]}B ({partes[1]} usado)",
#                         'path': partes[0]  # Caminho do dispositivo
#                     })
#     except Exception as e:
#         print(f"Erro ao obter discos: {str(e)}")
    
#     # Rede
#     componentes.append({
#         'type': 'network',
#         'name': 'Interface de Rede',
#         'description': None,
#         'path': None
#     })
    
#     return componentes

import platform
import psutil
import os

def get_system_components(so):
    """Detecta componentes com foco nos parâmetros solicitados"""
    # Disco principal (apenas um)
    disco_principal = {
        'type': 'disk',
        'name': 'Disco Principal',
        'path': 'C:\\' if os.name == 'nt' else '/',
        'description': 'Uso percentual'
    }
    
    # CPU
    cpu_info = {
        'type': 'cpu',
        'name': 'Processador',
        'description': 'Uso e frequência',
        'path': None
    }
    
    # Memória RAM
    ram_info = {
        'type': 'ram',
        'name': 'Memória RAM',
        'description': 'Uso, used, available',
        'path': None
    }
    
    # Rede
    network_info = {
        'type': 'network',
        'name': 'Interface de Rede',
        'description': 'Pacotes enviados/recebidos',
        'path': None
    }
    
    return [cpu_info, ram_info, disco_principal, network_info]
