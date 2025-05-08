import mysql.connector
from mysql.connector import Error

select = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="techpix_select",
    password="techpix#2024",
    database="TechPix"
)

cursorSelect = select.cursor()

def buscarUsuario(name, password):
    """Retorna (success, company_id) se válido, False caso contrário"""
    query = "SELECT idEmployer, fkCompany FROM Employer WHERE name = %s AND password = %s"
    try:
        cursorSelect.execute(query, (name, password))
        result = cursorSelect.fetchone()
        if result:
            print("Login realizado com sucesso!")
            return (True, result[1])  # (success, company_id)
        else:
            print("Usuário ou senha incorretos!")
            return False
    except Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return False



