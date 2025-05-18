
# pegando a biblioteca flash e pegar a class flask 
from flask import Flask

# nome do aplicativo vai se chamar main também
app = Flask(__name__)

# passando uma rota 
@app.route('/') # raiz do aplicativo so com a barra 
def homepage():  #função de renderização da pagina 
    return "meu exercicio"


if __name__ == '__main__':  # para "rodar" no lugar certo, vamos utilizar o nome do app, ou seja, so vai rodar se quem chamar for o main
    app.run(debug=True) # sempre que estiver atualização ele restarta a aplicação 