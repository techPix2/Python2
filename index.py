
# import platform
# import os
# import time
# from database import buscarUsuario
# from setup import get_system_components
# from extract import monitorar_componentes_selecionados

# def clear_screen():
#     os.system('cls' if os.name == 'nt' else 'clear')

# def selecionar_componentes(so):
#     """Permite ao usuário selecionar quais componentes monitorar"""
#     componentes = get_system_components(so)
    
#     clear_screen()
#     print("=== Seleção de Componentes ===")
#     print("\nSelecione os componentes para monitorar:\n")
    
#     for idx, comp in enumerate(componentes, 1):
#         print(f"{idx}. {comp['type']} ({comp['name']})")
    
#     print("\nDigite os números dos componentes separados por vírgula (ex: 1,2,3,4,5)")
#     print("Ou pressione Enter para monitorar todos")
    
#     selecao = input("\n>> ").strip()
    
#     if selecao:
#         indices = [int(i.strip()) - 1 for i in selecao.split(",") if i.strip().isdigit()]
#         return [componentes[i] for i in indices if 0 <= i < len(componentes)]
#     return componentes

# def login():
#     clear_screen()
#     print("=== TechPix - Sistema de Monitoramento ===")
#     print("\nPor favor, faça login")

#     while True:
#         email = input("\nEmail do Usuário: ")
#         password = input("Senha: ")

#         user_data = buscarUsuario(email, password)
#         if user_data:
#             return True
#         else:
#             print("\nCredenciais inválidas. Tente novamente.")

# def main():
#     if login():
#         so = platform.system().lower()
#         componentes = selecionar_componentes(so)
#         monitorar_componentes_selecionados(componentes)

# if __name__ == "__main__":
#     main()

import platform
import os
import time
from setup import get_system_components
from extract import monitorar_componentes_selecionados, processData
from database import buscarUsuario

def clear_screen():
    """Limpa o terminal de forma multiplataforma"""
    os.system('cls' if os.name == 'nt' else 'clear')

def selecionar_componentes(so):
    """Interface para seleção dos componentes com informações específicas"""
    componentes = get_system_components(so)
    
    clear_screen()
    print("=== TechPix - Seleção de Componentes ===")
    print("\nSelecione os componentes para monitorar:\n")
    
    for idx, comp in enumerate(componentes, 1):
        if comp['type'] == 'disk':
            print(f"{idx}. DISCO (Partição {comp['path']} - Uso %)")
        elif comp['type'] == 'ram':
            print(f"{idx}. MEMÓRIA RAM (Uso %, Used, Available)")
        elif comp['type'] == 'cpu':
            print(f"{idx}. CPU (Uso %, Frequência)")
        elif comp['type'] == 'network':
            print(f"{idx}. REDE (Pacotes Enviados/Recebidos)")
    
    print("\nDigite os números dos componentes separados por vírgula (ex: 1,2,3)")
    print("Pressione Enter para monitorar todos")
    
    selecao = input("\n>> ").strip()
    
    if selecao:
        indices = [int(i.strip()) - 1 for i in selecao.split(",") if i.strip().isdigit()]
        return [componentes[i] for i in indices if 0 <= i < len(componentes)]
    return componentes

def login():
    """Sistema de autenticação mantido"""
    clear_screen()
    print("=== TechPix - Autenticação ===")
    
    while True:
        email = input("\nEmail: ")
        senha = input("Senha: ")
        
        if buscarUsuario(email, senha):
            return True
        print("\nCredenciais inválidas. Tente novamente.")

def main():
    if login():
        so = platform.system().lower()
        componentes = selecionar_componentes(so)
        
        processData()
        if componentes:
            print("\nIniciando monitoramento...")
            print("Pressione Ctrl+C para encerrar\n")
            time.sleep(1)
            monitorar_componentes_selecionados(componentes)


if __name__ == "__main__":
    main()
