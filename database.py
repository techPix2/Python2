import mysql.connector
from mysql.connector import Error

select = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="Nocelli@1",
    database="TechPix"
)

cursorSelect = select.cursor()

def buscarUsuario(email, password):
    """Retorna (success, company_id) se válido, False caso contrário"""
    query = "SELECT idEmployer, fkCompany FROM Employer WHERE email = %s AND password = %s"
    try:
        cursorSelect.execute(query, (email, password))
        result = cursorSelect.fetchone()
        if result:
            print("Login realizado com sucesso!")
            return (True)  
        else:
            print("Usuário ou senha incorretos!")
            return False
    except Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return False



