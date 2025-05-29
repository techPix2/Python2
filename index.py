import os
import time
from extract import monitorar_componentes_selecionados
from database import buscarUsuario

def clear_screen():
    """Limpa o terminal de forma multiplataforma"""
    os.system('cls' if os.name == 'nt' else 'clear')

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
        componentes = [
            {'type': 'cpu'},
            {'type': 'ram'},
            {'type': 'disk'},
            {'type': 'network'},
            {'type': 'process'}
        ]
        
        print("\nIniciando monitoramento...")
        print("Pressione Ctrl+C para encerrar\n")
        time.sleep(1)

        monitorar_componentes_selecionados(componentes)


if __name__ == "__main__":
        main()


