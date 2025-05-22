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
