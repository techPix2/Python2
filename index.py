
import platform
import os
import time
from database import buscarUsuario
from setup import get_system_components
from extract import monitorar_componentes_selecionados

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def selecionar_componentes(so):
    """Permite ao usuário selecionar quais componentes monitorar"""
    componentes = get_system_components(so)
    
    clear_screen()
    print("=== Seleção de Componentes ===")
    print("\nSelecione os componentes para monitorar:\n")
    
    for idx, comp in enumerate(componentes, 1):
        print(f"{idx}. {comp['type']} ({comp['name']})")
    
    print("\nDigite os números dos componentes separados por vírgula (ex: 1,2,3,4,5)")
    print("Ou pressione Enter para monitorar todos")
    
    selecao = input("\n>> ").strip()
    
    if selecao:
        indices = [int(i.strip()) - 1 for i in selecao.split(",") if i.strip().isdigit()]
        return [componentes[i] for i in indices if 0 <= i < len(componentes)]
    return componentes

def login():
    clear_screen()
    print("=== TechPix - Sistema de Monitoramento ===")
    print("\nPor favor, faça login")

    while True:
        email = input("\nEmail do Usuário: ")
        password = input("Senha: ")

        user_data = buscarUsuario(email, password)
        if user_data:
            return True
        else:
            print("\nCredenciais inválidas. Tente novamente.")

def main():
    if login():
        so = platform.system().lower()
        componentes = selecionar_componentes(so)
        monitorar_componentes_selecionados(componentes)

if __name__ == "__main__":
    main()
