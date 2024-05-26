# Python version 3.10.10
# pip version 22.3.1
from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime,timedelta
import sqlite3
import time

# Na app encontra-se o nosso servidor web de Flask
app = Flask(__name__)
# A informação continda no session está no webserver pelo que o uso de uma secre_key é necessario
# para desencriptar e incriptar a informação contida na session
app.secret_key = "ProjectoTokioSchool"

# classe que irá servir para introduzir os dados de cada novo utilizador na base de dados BDutilizadores.db
# assim como proceder à actualização dos dados do utilizador através dos métodos inserir_user() e actualizar_user()
class NovoUser:
    ###################################################################################################################
    #inicia-se a classe com todos os paramentros que ela vai ter de receber
    # id = None é aqui necessário para ser usado pelo método actualizar_user, no metodo inserir_user ele não é necessário
    # e por essa razão é feito um .pop() para o exculir uma vez que ele é criado automáticamente na base de dados a cada
    # inserção de um novo utilizador
    ###################################################################################################################
    def __init__(self,nome,apelido,email,contacto,nascimento,sexo,morada,cidade,codigoPostal,cartaConducao,
                 emissaoCartaConducao,validadeCartaConducao,numeroCartaoCidadao,numeroContribuinte,
                 validadeCartaoCidadao,categoria,passwordUtilizador,id = None):

        #aqui são inseridos todos os atributos da classe, dentro de uma lista, para serem armazenados na base de dados
        self.dados = [nome,apelido,email,contacto,nascimento,sexo,morada,cidade,codigoPostal,cartaConducao,
                      emissaoCartaConducao,validadeCartaConducao,numeroCartaoCidadao,numeroContribuinte,
                      validadeCartaoCidadao,categoria,passwordUtilizador,id]

    # método que serve para inserir um novo utilizador e acrescentar a sua informação à base de dados
    def inserir_user(self):

        # É feita a conecção com a base de dados DButilizadores para se ter acesso à tabela utilizador
        con = sqlite3.connect("database/DButilizadores.db")
        # criação do cursor para puder proceder à consulta dentro da base de dados
        cursor = con.cursor()
        # este pop serve para retirar o ultimo elemento da lista que para este método em especifico não é necessário ser
        # chamado, uma vez que se trata do id e este é gerado automáticamente dentro da tabela da base de dados sempre
        # que é inserido um novo utilizador
        self.dados.pop()
        # Inserçao de dados dentro da tabela utilizador
        cursor.execute("INSERT INTO utilizador VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.dados)
        # As alteraçoes feitas na tabela utilizador são guardadas
        con.commit()
        # É encerrada a conecçao com a base de dados
        con.close()

    # metódo que tem por finalidade alterar os dados do utilizador caso este assim o deseje
    def actualizar_user(self):
        # É feita a conecção com a base de dados DButilizadores para se ter acesso à tabela utilizador
        con = sqlite3.connect("database/DButilizadores.db")
        # criação do cursor para puder proceder à consulta dentro da base de dados DButilizadores.db
        cursor = con.cursor()
        # Update dos valores contidos dentro da tabela excepto o id, este tem de premanecer igual
        cursor.execute("UPDATE utilizador SET Nome = ?, Apelido = ?, Email=?, Contacto = ?, Nascimento = ?, Sexo = ?, Morada = ?, Cidade = ?,"
                               "CodigoPostal = ?, CartaConducao = ?, EmissaoCConducao = ?, ValidadeCConducao = ?,"
                               "CartaoCidadao = ?, NIF = ?, ValidadeCCidadao = ?, CategoriaCliente = ?, Password = ?"
                               " WHERE IdCliente = ?", self.dados)
        # As alteraçoes feitas na tabela utilizador são guardadas
        con.commit()
        # É encerrada a conecçao com a base de dados
        con.close()

# função para aceder a toda a informação de um utilizador
def info_user_reserva(id):

    # É feita a conecção com a base de dados DBreservas para se ter acesso à tabela reserva
    con = sqlite3.connect("database/DBreservas.db")
    # criação do cursor para puder proceder à consulta (query) dentro da base de dados
    cursor = con.cursor()
    # com o comando SELECT * é selecionada a informação toda, referente à reserva acedendo à coluna específica da
    # tabela na linha que lhe corresponde
    cursor.execute("SELECT * FROM reserva WHERE IdCliente = ?", [id])
    # É feita a extração de toda a informação da reserva
    value = cursor.fetchall()
    # É encerrada a conecção com a base de dados
    con.close()
    return value

def update_valorTotal(id_Reserva):
    # É estabelecida a conecção com a base de dados DBreservas.db
    con = sqlite3.connect("database/DBreservas.db")
    # Criação do cursor para inserir a informação na tabela
    cursor = con.cursor()
    cursor.execute("UPDATE reserva SET valorTotal=0 WHERE IdReserva=?",[id_Reserva])
    # As alteraçoes feitas na tabela reserva são guardadas
    con.commit()
    # É encerrada a conecçao com a base de dados
    con.close()

# função para identificar se um determinado contribuinte já existe dentro da base dados, associado a algum utilizador
# para desta forma evitar duplicação de contas de utilizadores.
def verificacao_user(nif):

    # É feita a conecção com a base de dados DButilizadores para se ter acesso à tabela utilizador
    con = sqlite3.connect("database/DButilizadores.db")
    # criação do cursor para puder proceder à consulta (query) dentro da base de dados
    cursor = con.cursor()
    # executa-se um comando try and except por motivos de segurança
    try:
        # com o comando SELECT NIF o cursor acede à informação da coluna NIF dentro da tabela utilizadores para
        # verificar se o NIF já existem
        cursor.execute("SELECT NIF FROM utilizador WHERE NIF = ?", [nif])
        # como neste caso sabemos que ele apenas irá retornar uma linha da coluna NIF (se já existir) é utilizado o
        # comando fetchone()
        value = cursor.fetchone()
        # é utilizado um if caso o valor que nos seja devolvido pelo value seja um int começando desde o inicio da coluna,
        # e percorrendo a informação dessa coluna linha a linha inciando na posição zero
        if int(nif) == value[0]:
            # Encerra-se a connecção com a tabela
            con.close()
        # devolve o valor a true
        return True
    # caso o valor retornado nao seja um int
    except:
        # é encerrada a conecção
        con.close()
        # devolve o valor a false
        return False

# método de verificação do login necessário para cada utilizador que será utilizado para a pagina de login
def verificacao_login(email,password):

    # Faz-se a conecção à base de dados DButilizadores.
    con = sqlite3.connect("database/DButilizadores.db")
    # criação do cursor para puder proceder à consulta (query) dos dados dentro da tabela utilizador
    cursor = con.cursor()
    # executa-se um comando try and except por motivos de segurança
    try:
        # é feita uma consulta (query) à base de dados para ver se o email inserido no login existe atravé do cursor
        cursor.execute("SELECT * FROM utilizador WHERE Email = ?", [email])
        # se o valor que está a ser pesquisado existir ele é extraído da linha em que se encontra na tabela da base
        # de dados
        value = cursor.fetchone()
        # se a variável email for igual ao valor extraído da tabela na posição 3 (que correscponde ao Email
        # dentro da tabela)
        if email == value[3]:
            # e se a variável passaword tiver um valor igual ao que consta na posição 17(que corresponde
            # à password do utilizador dentro da tabela)
            if password == value[17]:
                # A conecção com a base de dados é encerrada
                con.close()
                # se todos os parâmetros forem cumpridos retorna o valor a true e o utlizador poderá iniciar a sessão
                return True
    except: # caso contrário
        # é fechada a conecção com a base de dados
        con.close()
        # e o valor retornado é falso e nao será possível aceder à sessão do utilizador
        return False

#Função para adquirir a informação do utilizador que é utilizada para inserir na sessions (pagina login)
def id_user(email):

    # É aberta a conecção com a base de dados DButilizadores
    con = sqlite3.connect("database/DButilizadores.db")
    # Cria-se um cursor para se proceder à consulta da informação que se encontra dentro da tabela utilizador
    cursor = con.cursor()
    # dentro de todos os dados que constam nessa tabela é solicitado que o cursor faça uma consulta na coluna que
    # corresponde ao Email
    cursor.execute("SELECT * FROM utilizador WHERE Email = ?", [email])
    # Os valores são extraidos para uma lista para que possam ser manipulados em caso de necessidade, uma vez que se não
    # for exigido que o valor retornado venha como lista este virá por defeito em formato de tupla
    value = list(cursor.fetchone())
    # conecção com a base de dados é encerrada
    con.close()
    return value

# função para aceder aos dados dos veiculos (carros e motas)
def info_veiculo(veiculoId):

    # se c ou C estiver dentro da variável veiculoId é defenido os parametros de conecção(db) e de pesquisa(query)
    if ("c" or "C") in veiculoId:
        # a variavel db é o caminho para a base de dados carros
        db="database/DBcarros.db"
        # a variável armazena o comando que vai ser necessário para fazer a pesquisa dentro da base de dados DBcarros
        query="SELECT * FROM carro WHERE IdCarro = ?"
    # se m ou M estiver dentro da variável veiculoId
    elif ("m" or "M") in veiculoId:
        # a variavel db é o caminho para a base de dados motas é defenido os parametros de conecção(db) e de
        # pesquisa(query)
        db = "database/DBmotas.db"
        # a variável aramzena o comando que vai ser necessário para fazer a pesquisa dentro da base de dados DBmotas
        query = "SELECT * FROM mota WHERE IdMota = ?"

    # De acordo com o parametro/valor passado para a variável db é aberta a conecção com a base de dados desejada quer
    #seja a dos carros ou das motas
    con = sqlite3.connect(db)
    #É criado um cursor para proceder à consulta da informação que se encontra dentro da tabela carro ou mota
    cursor = con.cursor()
    # é solicitada que essa consulta seja feita na coluna que corresponde ao id do veiculo
    cursor.execute(query,[veiculoId])
    # o cursor ira enviar para a variavel value uma tupla com todas as linhas dos veiculos que partilham o mesmo id
    # dentro da tabela
    value = cursor.fetchall()
    # encerra-se a conecção com a base de dados
    con.close()
    #retorna uma tupla com todos os resultados reunidos durante a consulta
    return value

# class Reservas que é chamada na construção da página pagamento, é só neste momento que a base de dados vai receber a
# informação da reserva e gerar um id de reserva, apos o pagamento
class Reservas:

    def __init__(self, idCliente, idVeiculo, matricula, categoriaVeiculo, marca, modelo,
                 dataLevantamento, dataEntrega,valorTotal):

        self.reservas = [idCliente, idVeiculo, matricula, categoriaVeiculo, marca, modelo,
                             dataLevantamento,dataEntrega,valorTotal]

    # método que irá receber os dados da reserva para guardar na base de dados e gerar o id da reserva
    def dadosReserva(self):

        # É estabelecida a conecção com a base de dados DBreservas.db
        con = sqlite3.connect("database/DBreservas.db")
        # Criação do cursor para inserir a informação na tabela
        cursor = con.cursor()
        # Comando para inserir os valores da reserva dentro da tabela
        cursor.execute("INSERT INTO reserva VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.reservas)
        # É feito um commit para guardar as novas informações dentro da tabela
        con.commit()
        # A connecção é encerrada com a base de dados
        con.close()

    # método que irá extrair os dados da reserva que já incluí o id da reserva
    def extrair_id_reserva(self):

        # É estabelecida a conecção com a base de dados DBreservas.db
        con = sqlite3.connect("database/DBreservas.db")
        # Criação do cursor para pesquisar a informação na tabela
        cursor = con.cursor()
        ###############################################################################################################
        # para que haja total segurança, em que os dados que estão a ser extraidos,correspondem de facto a reserva que é
        # pretendida ir buscar, o id do cliente tem corresponder ao id do veiculo e este corresponder à matricula e por sua
        #vez este corresponder à data de levantamento e à data de entrega, ( sendo estes o principais), no entanto para
        # manter a certeza coloquei todos os parametro que se encontram dentro da tabela reserva, pois nunca podem
        # existir duas reservas totalmente iguais
        ###############################################################################################################
        cursor.execute(
            "SELECT * FROM reserva WHERE IdCliente=? AND IdVeiculo=? AND Matricula=? AND CategoriaVeiculo=? AND Marca=? "
            "AND Modelo=? AND DataLevantamento=? AND DataEntrega=? AND ValorTotal=?",
            self.reservas)
        # como só pode existir uma linha em que todos esses parametros são cumpridos utilizei o fetchone para me devolver
        # apenas a informação relativa a uma linha
        value = cursor.fetchone()
        # Caso haja alguma alteração estas serão guardadas
        con.commit()
        # é encerrada a conecção com a base de dados
        con.close()
        # o value vai retornar o valor que está na posição 0 que corresponde ao id da reserva que vai ser necessário na
        # saber na pagina pagamento
        return value[0]



# Classe utilizada também na pagina pagamento, que será necessária para inserir os dados do pagamento na base de dados
# DBpagamentos
class Pagamentos:

    def __init__(self, idReserva, idCliente, cartaoCredito, mesAno, cvv, titularCartao):

        self.pagamentos = [idReserva, idCliente, cartaoCredito, mesAno, cvv, titularCartao]

    # Método que vai inserir a informação dos pagamentos na base de dados
    def dadosPagamento(self):

        con = sqlite3.connect("database/DBpagamentos.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO pagamento VALUES (NULL, ?, ?, ?, ?, ?, ?)",self.pagamentos)
        con.commit()
        con.close()

# fução necessária para saber se a viatura que o cliente solicitou está disponivel e qual é a que está disponivel,
# recorrendo à matricula como forma de distinção entre todos os veiculos, uma vez que este é o único valor que nunca
# se repete
def data_veiculo_disponivel(matriculas):

    # é feita a connecção com a base de dados DBreservas.db
    con = sqlite3.connect("database/DBreservas.db")
    # Criação do cursor para se proceder à consulta da informação contida na tabela da base de dados
    cursor = con.cursor()
    # variável do tipo dicionario vazia que irá receber como parametros "matricula" e "data"
    dic = {}

    # para cada vez que a variavel "x" precorrer a informação contida dentro da lista matriculas (que pode conter até
    # três matriculas diferentes referente a cada veiculo)
    for x in range(len(matriculas)):
        # será feita uma consulta por cada matricula que esteja dentro da lista e as datas que cada uma tenha já
        # de reservas
        cursor.execute("SELECT * FROM reserva WHERE Matricula =?", [matriculas[x]])
        # value irá receber toda a informação linha a linha respeitante a cada vez que a matricula pesquisada for
        # encontrada
        value = cursor.fetchall()
        # dataNova é uma variavel necessária para receber o valor das datas que vao ser extraidas a partir do ciclo for
        dataNova= 0
        # de acordo com o comprimento da lista value é solicitado que
        for y in range(len(value)):
            # a variável dataLista receba a informação em formato string de data que corresponde à coluna 8 da tabela
            # reserva
            dataLista =  int(value[y][8].replace("-", ""))
            # aqui é feita uma comparação entre todas as datas referente à matricula da viatura, para que seja recolhida
            # a informação da data maior(mais longe)
            if dataNova < dataLista:
                # dataNova recebe a data maior da dataLista
                dataNova = dataLista

        # O dicionario vai receber a matricula de matriculas como Key,e o value será dataNova convertida do formato
        # string para int
        dic[matriculas[x]] = dataNova

    # variável vazia que vai receber a data
    data = 0
    # variavel vazia que vai receber a matricula
    matricula = ""
    # utilizando o metodo items(), vai nos ser retornado do dicionario ambos os items como tuplas dentro de uma lista
    for key,value in dic.items():
        # se o value for maior que a data então a
        if value > data:
            # data vai receber o value mais alto
            data = value
            # e a matricula recebe o valor da key correspondente à variável data
            matricula = key

    # fechada a concecçao com a base de dados
    con.close()

    # criação de uma lista vazia info=[] para receber os valores da matrícula e da data, de forma a retornar essa
    # informação para a reserva
    info=[]
    info.append(matricula)
    info.append(data)

    return info

# Função que vai servir para calcular o número de dias da reserva que o cliente pertende retornado assim o preço total
# relativo aos dias da reserva do veiculo, esta função é chamada na pagina reserva para o cliente ver o valor final
def calcular_total(precoDia,dataLevantamento,dataEntrega):

#utilizei um try and execpt por questões de segurança
    try:
        # calcula o número de dias que é feito o arrendamento do veiculo utilizando o datetime() para obter o numero de
        # dias de forma correcta
        dias = datetime(int(dataEntrega[:4]), int(dataEntrega[5:7]), int(dataEntrega[8:])) - datetime(
            int(dataLevantamento[:4]), int(dataLevantamento[5:7]),
            int(dataLevantamento[8:]))
        #após obter o número de dias da reserva é feito o calculo que nos irá retornar o preço da reserva
        valorTotal = precoDia * dias.days
    # exepto se o valor total for igual a zero
    except:
        valorTotal=0
    # será retornada a variavel valorTotal que tem o preço total da reserva
    return valorTotal

#Função para actualizar os dados de uma sessão, para quando existe a necessidade de fazer alteração aos dados do cliente
def update_session():

    # se a sessão do utilizador estiver sido iniciada
    if "user_id" in session:
        # É aberta a conencção com a base de dados DButilizadores
        con = sqlite3.connect("database/DButilizadores.db")
        # Cria-se um cursor para proceder à consulta da informação que está na tabela utilizador
        cursor = con.cursor()
        # de entre todos os dados que constam dentro da tabela utilizador, pedimos para que seja acedida a informação
        # que consta dentro da coluna idCliente, correspondente à session do utilizador
        cursor.execute("SELECT * FROM utilizador WHERE IdCliente = ?", [session["user_id"][0]])
        # cursor devolve o resultado da consulta feita à base de dados do tipo lista para que estes possam ser alterados
        session["user_id"] = list(cursor.fetchone())
        # Conecção com a base de dados é encerrada
        con.close()
#######################################################################################################################
# criação da 1º página do site - tem sempre de ter o route e uma função
# defenido o link da pagina principal que é basicamente uma pagina de apresentação com dois botões no corpo da pagina e
# varios links no cabeçalho
#######################################################################################################################
@app.route("/")
def homepage():
    # caso exista uma session do user_id (o utilizador) sempre que ele retorne à pagina principal terá a opção de fazer
    #logout sem que tenha de retornar à sua pagina de utilizador, ou poderá ir directamente para a sua área pessoal
    if "user_id" in session:
        # retorna à sua pagina com os seus dados ou pode fazer logout
        return render_template("index.html", minha_pagina="Minha Página", logout = "Logout")
    else:
        # caso nao exista nenhuma sessão e por razões de segurança, retorna à página principal
        return render_template("index.html")


# criação página Login
 # o método POST é aqui utilizado como uma forma segura de enviar informação para o website, por se tratar de informação
# mais sensivel.
@app.route("/login", methods = ['POST', 'GET'])
def login():
    mensagem = ""
    if request.method == 'POST':# o método POST é aqui utilizado como uma forma segura de enviar informação para o
        # website, por se tratar de informação mais sensivel.
        # o session.pop serve para fechar a sessao do cliente quando este sair do site mesmo sem ter feito o logout
        session.pop('user_id', None)
        # se o email inserido pelo utilizador, ja existir na base de dados na coluna userEmail, e na mesma linha da
        # tabela na coluna userPasword estiver a pasword igual à inserida também pelo utilizador é feito o login
        # com sucesso
        if verificacao_login(request.form['userEmail'],request.form['userPassword']):
            ###########################################################################################################
            # inicia-se o session que irá conter temporariamente toda a informação do utilizador no webserver e que vai
            # permitir que toda essa informação seja passada de pagina em pagina enquanto o utilizador andar a navegar
            # no site com a sua sessao iniciada, é muito util no caso do  cliente querer efectuar uma reserva, pois toda
            # essa informação já la está. quando o utilizador sai do site essa session desaparece
            ###########################################################################################################
            session['user_id'] = id_user(request.form['userEmail'])
            # ao ser bem sucedido o login a pagina login é redirecionada para a pagina utilizador na sessão desse
            # utilizador
            return redirect(url_for("utilizadores"))
        # caso contrário retorna a mensagem de email ou Password invalidos para que o utilizador possa repetir o login
        else:
            mensagem = "Email ou Password invalidos"
            # caso o utilizador se engane a escrever o email ou  a pasword surge uma mensagem de alerta para confirmar
            # os dados inseridos
            return render_template("login.html", mensagem=mensagem)
    else:
        # Caso o request.method nao seja igual a 'POST' e sim um 'GET', retorna a entrar na pagina login
        return render_template("login.html")
#######################################################################################################################
# criação do Registo
# Criação de Novo Utilizador, mas ao mesmo tempo verificar se já existe esse utilizador na base dados, podemos usar
# vários parametros, tais como "NIF, Telemovel, etc"
# aqui além da rota(route)da web page, acrescentei os métodos que me permitem aceder à informação de forma segura 'POST'
# e de forma default que é com o 'GET'
#######################################################################################################################
@app.route("/registo",  methods = ['POST', 'GET'])
def registo():
    # variável vazia para receber receber uma mensagem consoante a condição e exibir na webpage essa mesma mensagem
    mensagem = ""
    session.pop("user_id", None)
    # Aqui determinamos que estamos a utilizar o metodo POST utilizando o request por se tratar de informação mais
    # sensivel e que queremos protegida
    if request.method == 'POST':
        # Se o utilizador tentar duplicar um registo, é utilizado aqui o pedido de verifiação do número de contribuinte
        # que está a ser inserido , com os que já existem na base de dados
        if verificacao_user(request.form['numeroContribuinte']):
            # caso ja exista irá retornar a seginte mensagem informativa
            mensagem = "Utilizador Já se encontra registado"
            # Se o utilizador já tiver um registo é redirecionado para a pagina login.html, e proceder à entrada dentro
            # da sua área privada de utilizador
            return render_template("login.html", mensagem=mensagem)
        else:
            # se os valore da password inserida pelo cliente for igual ao valor da verificação de password, então todos
            # os restantes valores serão guardados dentro das respectivas variáveis, em que cada uma corresponde a um
            # lugar na tabela da base de dados DButilidores.db
            if request.form['passwordUtilizador'] == request.form['confirmacaoPasswordUtilizador']:
                nome = request.form['nomeUtilizador']
                apelido = request.form['apelidoUtilizador']
                email = request.form['emailUtilizador']
                contacto = request.form['contactoUtilizador']
                nascimento = request.form['nascimentoUtilizador']
                sexo = request.form['sexoUtilizador']
                morada = request.form['moradaUtilizador']   #váriáveis que recebem a informação inserda pelo utilizador
                cidade = request.form['cidadeUtilizador']
                codigoPostal = request.form['codigoPostalUtilizador']
                cartaConducao = request.form['numeroCartaConducao']
                emissaoCartaConducao = request.form['emissaoCartaConducao']
                validadeCartaConducao = request.form['validadeCartaConducao']
                numeroCartaoCidadao = request.form['numeroCartaoCidadao']
                numeroContribuinte = request.form['numeroContribuinte']
                validadeCartaoCidadao = request.form['validadeCartaoCidadao']
                categoria = request.form['categoria']
                passwordUtilizador = request.form['passwordUtilizador']

                # A class NovoUser(), recebe os argumentos que vão receber os dados inseridos pelo utilizador na
                # pagina registo e retornar para dentro da tabela DButilizadores.db atraves do método inserir_user()
                novouser =NovoUser(nome, apelido, email, contacto, nascimento, sexo, morada, cidade, codigoPostal,
                            cartaConducao,emissaoCartaConducao, validadeCartaConducao, numeroCartaoCidadao,
                            numeroContribuinte,validadeCartaoCidadao, categoria, passwordUtilizador)

                # A instancia novouser da classe NovoUser, vai buscar o método inserir_user() para inserir os dados do
                # novo utilizador que efectuou o registo
                novouser.inserir_user()
                # é criada uma session com todos os dados do utilizador desta forma o utilizador poderá navegar pelas
                #diferentes paginas do site com a sua sessao iniciada e passar a informação necessária caso queira
                # efetuar uma reserva de um dos veiculos
                session['user_id'] = id_user(request.form['emailUtilizador'])
                # este primeiro return retorna-nos à pagina registo.html com a mensagem Utilizador Criado com Sucesso,
                # se os dados forem registados com sucesso.
                return redirect(url_for("utilizadores"))
            else:
                # caso o utilizador ao fazer o registo no momento de confirmação da password se tiver enganado, retorna
                # à pagina registo e é lhe ezibida a mensagem: As passwords não estão iguais
                mensagem = "As passwords não estão iguais"
                return render_template("registo.html", mensagem=mensagem)
    # Caso o request.method nao seja igual a 'POST' e sim um 'GET', retorna a entrar na pàgina registo para tentar
    # efetuar novo registo
    return render_template("registo.html")
#######################################################################################################################
# criação de uma 'pagina' que retorna à pagina pessoal do utilizador por meio de um link que se encontra no cabeçalho
# das paginas, caso o utilizador já tenha uma sessão iniciada na sua conta.
# Aqui não necessitamos colocar o method POST pois só é possivel aceder aos dados sensiveis caso o utilizador ja tenha
# iniciado uma sessão passando primeiramente por uma sessão com um POST e navegando pelo site com um session que é uma
# forma temporaria de guardar os dados
#######################################################################################################################
@app.route("/minhaPagina")
def minhaPagina():
    # Se o utilizador já tiver uma sessão iniciada e necessitar de voltar à pagina com os seus dados, basta clicar no
    # link no cabeçalho da página, A minha pagina
    if "user_id" in session:
        # e retorna à sua pagina com todos os seus dados
        return  redirect(url_for("utilizadores"))
    else:
        # se não tiver a sessão iniciada o utilizador é redirecionado para a página login para puder iniciar uma
        # nova sessão
        return redirect(url_for("login"))
#######################################################################################################################
#logout
# Aqui não necessitamos colocar o method POST pelas mesmas razões referidas para a def minhaPagina, tanto esta como a
# função minha pagina são chamadas na primeira pagina do site
#######################################################################################################################
@app.route("/logout")
def logout():
    # se existir uma sessão iniciada
    if "user_id" in session:
        # é feito um pop à sessão e esta é encerrada
        session.pop("user_id", None)
        # se não tiver a sessão iniciada o utilizador é redirecionado para a página login para puder iniciar uma
        # nova sessão
        return redirect(url_for("homepage"))

#######################################################################################################################
# criação da 4º página do site Actuallizar Clientes é necessária no caso do cliente querer actualizar ou alterar dados
# Por estar-mos a mexer novamente com dados sensíveis acrescentei os métodos que me permitem aceder à informação de
# forma segura 'POST' e de forma default que é como o 'GET'
#######################################################################################################################
@app.route("/actualizarclientes", methods=['POST', 'GET'])
def actualizarclientes():
    if request.method == 'POST':
        #se existir uma sessão inciada do utilizador
        if "user_id" in session:
            # o utilizador poderá proceder à alteração de todos os seus dados exepto o NIF
            # numeroContribuinte = session["user_id"][14] que é aqui utilizado como um identificador constante
            # juntamente com o id do utlizador
            if request.form['Actualizar'] == "act": # se o botao actualizar for precionado **
                nome = request.form['nomeUtilizador']
                apelido = request.form['apelidoUtilizador']
                email = request.form['emailUtilizador']
                contacto = request.form['contactoUtilizador']
                nascimento = request.form['nascimentoUtilizador']
                sexo = request.form['sexoUtilizador']
                morada = request.form['moradaUtilizador']
                cidade = request.form['cidadeUtilizador']
                codigoPostal = request.form['codigoPostalUtilizador']
                cartaConducao = request.form['numeroCartaConducao']
                emissaoCartaConducao = request.form['emissaoCartaConducao']
                validadeCartaConducao = request.form['validadeCartaConducao']
                numeroCartaoCidadao = request.form['numeroCartaoCidadao']
                numeroContribuinte = session["user_id"][14]
                validadeCartaoCidadao = request.form['validadeCartaoCidadao']
                categoria = request.form['categoria']
                passwordUtilizador = request.form['passwordUtilizador']

                # a instância da classe NovoUser é criada e recebe todos os valores que foram alterados e os que se
                # mantiveram iguais também para puder guardar a informação e fazer um update
                actualizaCliente=NovoUser(nome,apelido,email,contacto,nascimento,sexo,morada,cidade,codigoPostal,
                                cartaConducao,emissaoCartaConducao,validadeCartaConducao,numeroCartaoCidadao,
                                numeroContribuinte, validadeCartaoCidadao,categoria,passwordUtilizador,
                                session["user_id"][0])

                # Para que as novas informações sejam guardadas o objecto da classe NovoUser, chama o método
                # actualizar_user() da classe NovoUser
                actualizaCliente.actualizar_user()
                # Retornando para a página utilizadores após o botao actualizar for precionado ** com os novos dados
                return redirect(url_for("utilizadores"))
    else:
        # caso não haja alterações aos dados retorna a pagina do utilizador com os dados antigos
        return render_template("actualizarclientes.html", cliente_nome= session['user_id'][1],
                    cliente_apelido= session['user_id'][2],cliente_email=session['user_id'][3],
                    cliente_contacto=session['user_id'][4], cliente_nascimento=session['user_id'][5],
                    cliente_sexo=session['user_id'][6],cliente_morada=session['user_id'][7],
                    cliente_cidade=session['user_id'][8], cliente_codigoPostal=session['user_id'][9],
                    cliente_cartaConducao=session['user_id'][10],cliente_cartaConducaoEmissao=session['user_id'][11],
                    cliente_cartacConducaoValidade=session['user_id'][12],cliente_numeroCidadao=session['user_id'][13],
                    cliente_numeroContribuinte=session['user_id'][14],cliente_cartaoCidadaoValidade=session['user_id'][15],
                    cliente_categoria=session['user_id'][16],cliente_password=session['user_id'][17])

#######################################################################################################################
# criação da pagina utilizadores, onde o utilizador poderá ver os seus dados, proceder à actualização dos seus dados e
# ser direcionado para a pagina de veiculos de acordo com a sua categoria, no entanto e desde que ele nao encerre a sua
# sessão poderá navegar pelas diferentes paginas de veiculos e de diferentes categorias aquela que ele selecionou
#######################################################################################################################
@app.route("/utilizadores", methods= ['POST', 'GET'])
def utilizadores():
    # o update session serve para
    update_session()
    # Aqui determinamos que estamos a utilizar o metodo POST utilizando por se tratar de informação mais sensivel e que
    # queremos protegida
    if request.method == 'POST':
        # Se o utilizador estiver dentro da sua sessao ser-lhe à sugerido por meio de um botão que ele possa ver
        # veículos directamente de acordo com a categoria que tiver selecionado para si no acto do registo
        if "user_id" in session:
            if request.form['Sugestao'] == "Sugestao":
                # Se na sessao do utilizador na posição categoria corresponder a Gold
                if session['user_id'][16] == "Gold":
                    # O botao redereciona para a pagina veiculosGold
                    return redirect(url_for("veiculosGold"))
                # Se na sessao do utilizador na posição categoria corresponder a Silver
                elif session['user_id'][16] == "Silver":
                    # O botao redereciona para a pagina veiculosSilver
                    return redirect(url_for("veiculosSilver"))
                # Se na sessao do utilizador na posição categoria corresponder a Eco
                elif session['user_id'][16] == "Eco":
                    # O botao redereciona para a pagina veiculosEconomicos
                    return redirect(url_for("veiculosEconomicos"))
    else:
        # se o request.method == 'POST' então abre se a pagina do utilizador com as suas informações pessoais

        return render_template("utilizadores.html", cliente_nome= session['user_id'][1], cliente_apelido= session['user_id'][2],
                               cliente_email=session['user_id'][3], cliente_contacto=session['user_id'][4],
                               cliente_nascimento=session['user_id'][5],cliente_sexo=session['user_id'][6],
                               cliente_morada=session['user_id'][7], cliente_cidade=session['user_id'][8],
                               cliente_codigoPostal=session['user_id'][9],cliente_cartaConducao=session['user_id'][10],
                               cliente_cartaConducaoEmissao=session['user_id'][11],cliente_cartacConducaoValidade=session['user_id'][12],
                               cliente_numeroCidadao=session['user_id'][13],cliente_numeroContribuinte=session['user_id'][14],
                               cliente_cartaoCidadaoValidade=session['user_id'][15],cliente_categoria=session['user_id'][16])

#######################################################################################################################
# criação da página carros
# o método POST é aqui utilizado como uma forma segura de enviar informação para o website, por se tratar de informação
# mais sensivel.
#######################################################################################################################
@app.route("/carros", methods = ['POST', 'GET'])
def carros():

    # Aqui determinamos que estamos a utilizar o metodo POST utilizando o request por se tratar de informação mais
    # sensivel e que queremos protegida
    if request.method == 'POST':
        # Aqui o session é utilizado para que o cliente a partir da sua sessao possa aceder aos veiculos e caso assim o
        # deseje realizar a reserva de algum
        if "user_id" in session:
            # variável vazia que vai receber o valor do veiculo selecionado
            veiculo_id=""
            session.pop('veiculo_id', None) #
            if request.form['reservarCarro'] == "c1":
                veiculo_id = "c1"
            elif request.form['reservarCarro'] == "c2":
                veiculo_id = "c2"
            elif request.form['reservarCarro'] == "c3":
                veiculo_id = "c3"
            elif request.form['reservarCarro'] == "c4":
                veiculo_id = "c4"
            elif request.form['reservarCarro'] == "c5":
                veiculo_id = "c5"
            elif request.form['reservarCarro'] == "c6":
                veiculo_id = "c6"
            elif request.form['reservarCarro'] == "c7":
                veiculo_id = "c7"
            elif request.form['reservarCarro'] == "c8":
                veiculo_id = "c8"
            elif request.form['reservarCarro'] == "c9":
                veiculo_id = "c9"
            elif request.form['reservarCarro'] == "c10":
                veiculo_id = "c10"
            elif request.form['reservarCarro'] == "c11":
                veiculo_id = "c11"
            elif request.form['reservarCarro'] == "c12":
                veiculo_id = "c12"
            elif request.form['reservarCarro'] == "c13":
                veiculo_id = "c13"
            elif request.form['reservarCarro'] == "c14":
                veiculo_id = "c14"
            elif request.form['reservarCarro'] == "c15":
                veiculo_id = "c15"
            # vamos inserir o valor do veiculo id dentro da sessao 'veiculo_id'
            session['veiculo_id'] = veiculo_id
            # Será feito um redirect para a pagina reserva
            return redirect(url_for("reserva"))
        else:
            # Casso o utilizador não tenha ainda procedido ao login e queira fazer uma reserva será redirececionado para
            # a pagina login para entrar na sua conta
            return redirect(url_for("login"))
    else:
        # caso se aceda à pagina atraves do métod POST entramos na pagina carros
        return render_template("carros.html")

#######################################################################################################################
# criação da pagina motas
# o método POST é aqui utilizado como uma forma segura de enviar informação para o website, por se tratar de informação
# mais sensivel.
#######################################################################################################################
@app.route("/motas",  methods = ['POST', 'GET'])
def motas():

    # Aqui determinamos que estamos a utilizar o metodo POST utilizando por se tratar de informação mais sensivel e que
    # queremos protegida
    if request.method == 'POST':
        # Aqui o session é utilizado para que o cliente a partir da sua sessao possa aceder aos veiculos e caso assim o
        # deseje realizar a reserva de algum veiculo
        if "user_id" in session:
            # variável vazia que vai receber o valor do veiculo selecionado
            veiculo_id = ""
            # caso o cliente saia do site neste momento a sua sessao será encerrada
            session.pop('veiculo_id', None)
            if request.form['reservarMota'] == "m1":
                veiculo_id = "m1"
            elif request.form['reservarMota'] == "m2":
                veiculo_id = "m2"
            elif request.form['reservarMota'] == "m3":
                veiculo_id = "m3"
            elif request.form['reservarMota'] == "m4":
                veiculo_id = "m4"
            elif request.form['reservarMota'] == "m5":
                veiculo_id = "m5"
            elif request.form['reservarMota'] == "m6":
                veiculo_id = "m6"
            elif request.form['reservarMota'] == "m7":
                veiculo_id = "m7"
            elif request.form['reservarMota'] == "m8":
                veiculo_id = "m8"
            elif request.form['reservarMota'] == "m9":
                veiculo_id = "m9"
            elif request.form['reservarMota'] == "m10":
                veiculo_id = "m10"
            elif request.form['reservarMota'] == "m11":
                veiculo_id = "m11"
            elif request.form['reservarMota'] == "m12":
                veiculo_id = "m12"
            elif request.form['reservarMota'] == "m13":
                veiculo_id = "m13"
            elif request.form['reservarMota'] == "m14":
                veiculo_id = "m14"
            elif request.form['reservarMota'] == "m15":
                veiculo_id = "m15"
            # vamos inserir o valor do veiculo id dentro da sessao 'veiculo_id'
            session['veiculo_id'] = veiculo_id
            # Será feito um redirect para a pagina reserva
            return redirect(url_for("reserva"))
        else:
            # Casso o utilizador nao tenha ainda procedido ao login e queira fazer uma reserva será redirececionado para
            # a pagina login para entrar na sua conta
            return redirect(url_for("login"))
    else:
        # caso se aceda à pagina atraves do métod POST entramos na página motas
        return render_template("motas.html")

# criação da pagina veículos Gold 8ºpag
@app.route("/veiculosGold", methods= ['POST', 'GET'])
def veiculosGold():

    if request.method =='POST':
        # Aqui o session é utilizado para que o cliente a partir da sua sessao possa aceder aos veiculos e caso assim o
        # deseje realizar a reserva de algum veiculo
        if "user_id" in session:
            # variável vazia que vai receber o valor do veiculo selecionado
            veiculo_id = ""
            # caso o cliente saia do site neste momento a sua sessao será encerrada
            session.pop('veiculo_id', None)
            if request.form["reservarGold"] == "c1":
                veiculo_id = "c1"
            elif request.form["reservarGold"] == "c2":
                veiculo_id = "c2"
            elif request.form["reservarGold"] == "c3":
                veiculo_id = "c3"
            elif request.form["reservarGold"] == "c4":
                veiculo_id = "c4"
            elif request.form["reservarGold"] == "c5":
                veiculo_id = "c5"
            elif request.form["reservarGold"] == "m1":
                veiculo_id = "m1"
            elif request.form["reservarGold"] == "m2":
                veiculo_id = "m2"
            elif request.form["reservarGold"] == "m3":
                veiculo_id = "m3"
            elif request.form["reservarGold"] == "m4":
                veiculo_id = "m4"
            elif request.form["reservarGold"] == "m5":
                veiculo_id = "m5"
            # vamos inserir o valor do veiculo id dentro da sessao 'veiculo_id'
            session['veiculo_id'] = veiculo_id
            # Será feito um redirect para a pagina reserva
            return redirect(url_for("reserva"))
        else:
            # Caso o utilizador não tenha efetuado ainda procedido ao login e queira fazer uma reserva será
            # redirececionado para a página login para entrar na sua conta
            return redirect(url_for("login"))
    else:
        # caso se aceda à pagina atraves do métod POST entramos na página veiculosGold
        return render_template("veiculosGold.html")

# criação da pagina veiculosSilver
@app.route("/veiculosSilver", methods=['POST', 'GET'])
def veiculosSilver():

    if request.method =='POST':
        # Aqui o session é utilizado para que o cliente a partir da sua sessao possa aceder aos veiculos e caso assim o
        # deseje realizar a reserva de algum veiculo
        if "user_id" in session:
            # variável vazia que vai receber o valor do veiculo selecionado
            veiculo_id = ""
            session.pop('veiculo_id', None)
            if request.form["reservarSilver"] == "c6":
                veiculo_id = "c6"
            elif request.form["reservarSilver"] == "c7":
                veiculo_id = "c7"
            elif request.form["reservarSilver"] == "c8":
                veiculo_id = "c8"
            elif request.form["reservarSilver"] == "c9":
                veiculo_id = "c9"
            elif request.form["reservarSilver"] == "c10":
                veiculo_id = "c10"
            elif request.form["reservarSilver"] == "m6":
                veiculo_id = "m6"
            elif request.form["reservarSilver"] == "m7":
                veiculo_id = "m7"
            elif request.form["reservarSilver"] == "m8":
                veiculo_id = "m8"
            elif request.form["reservarSilver"] == "m9":
                veiculo_id = "m9"
            elif request.form["reservarSilver"] == "m10":
                veiculo_idd = "m10"
            # vamos inserir o valor do veiculo id dentro da sessao 'veiculo_id'
            session['veiculo_id'] = veiculo_id
            # Será feito um redirect para a pagina reserva
            return redirect(url_for("reserva"))
        else:
            # Caso o utilizador não tenha efetuado ainda procedido ao login e queira fazer uma reserva será
            # redirececionado para a página login para entrar na sua conta
            return redirect(url_for("login"))
    else:
        # caso se aceda à pagina atraves do métod POST entramos na página veiculosSilver
        return render_template("veiculosSilver.html")

# criação da pagina veiculosEconómicos
@app.route("/veiculosEconomicos", methods=['POST', 'GET'])
def veiculosEconomicos():

    if request.method == 'POST':
        # Aqui o session é utilizado para que o cliente a partir da sua sessão possa aceder aos veículos e caso assim o
        # deseje realizar a reserva de algum veiculo
        if "user_id" in session:
            # variável vazia que vai receber o valor do veiculo selecionado
            veiculo_id = ""
            session.pop('veiculo_id', None)
            if request.form["reservarEconomico"] == "c11":
                veiculo_id = "c11"
            elif request.form["reservarEconomico"] == "c12":
                veiculo_id = "c12"
            elif request.form["reservarEconomico"] == "c13":
                veiculo_id = "c13"
            elif request.form["reservarEconomico"] == "c14":
                veiculo_id = "c14"
            elif request.form["reservarEconomico"] == "c15":
                veiculo_id = "c15"
            elif request.form["reservarEconomico"] == "m11":
                veiculo_id = "m11"
            elif request.form["reservarEconomico"] == "m12":
                veiculo_id = "m12"
            elif request.form["reservarEconomico"] == "m13":
                veiculo_id = "m13"
            elif request.form["reservarEconomico"] == "m14":
                veiculo_id = "m14"
            elif request.form["reservarEconomico"] == "m15":
                veiculo_id = "m15"
            # vamos inserir o valor do veiculo id dentro da sessao 'veiculo_id'
            session['veiculo_id'] = veiculo_id
            # Será feito um redirect para a pagina reserva
            return redirect(url_for("reserva"))
        else:
            # Caso o utilizador não tenha efetuado ainda procedido ao login e queira fazer uma reserva será
            # redirececionado para a página login para entrar na sua conta
            return redirect(url_for("login"))
    else:
        # caso se aceda à pagina através do métod POST entramos na página veiculosEconomicos
        return render_template("veiculosEconomicos.html")

# criação da página reserva onde o utilizador escolhe a data de levantamento e de entrega do veículo
@app.route("/reserva", methods= ['POST', 'GET'])
def reserva():

    dataLevantamento = ""
    dataEntrega = ""
    valorTotal = 0

    # se tanto a session do utilizador como a session do veículo estiverem activas
    if "user_id" in session and "veiculo_id" in session:

        # vai ser extraída a informação dos veículos motas ou carros de acordo com a respectiva session do veículo id
        informacaoVeiculo = info_veiculo(session["veiculo_id"])
        # variável do tipo lista vazia que irá receber as matrículas das viaturas que existem de acordo com cada id do
        # veiculo que for selecionado
        matriculas = []

        # a variável x percorre a tupla informacaoVeiculo para extrair as matrículas respeitantes ao id do veículo
        # selecionado para reservar
        for x in range(len(informacaoVeiculo)):
            # é adicionado à lista vazia as matrículas que existirem mediante o id selecionado
            matriculas.append(informacaoVeiculo[x][5])
        # infoMatricula vai receber a matrícula com data mais distante de reserva de entre as matrículas que foram
        # dentro de "matrículas"
        infoMatricula = data_veiculo_disponivel(matriculas)

        # enviadas para a função data_veiculo_disponivel como parametro, para que desta forma se possa verificar qual a
        # viatura que se encontra disponivel para a data que o cliente estará a solicitar a reserva
        dataPossivelLevantamento = datetime.strptime(str(infoMatricula[1]), "%Y%m%d")
        dataPossivelLevantamento += timedelta(days=2)

        # verifica se houve algum metodo post do html
        if request.method == 'POST':

            # caso a checkbox não seja assinalada, os valores da reserva mantem-se gravados mas, o utilizador não será
            # enviado para o pagamento
            dataLevantamento = request.form['DataLevantamento']
            dataEntrega = request.form['DataEntrega']
            dataLevantamento = dataLevantamento
            valorTotal = calcular_total(informacaoVeiculo[0][12], dataLevantamento, dataEntrega)

            # se o botao calcular for presionado
            if request.form['botao'] == "Calcular €":

                if valorTotal < 0:
                    mensagem = "A data escolhida é inválida"
                    # aqui é retornado os valores respeitantes aos dados da reserva que incluem o do veículo e das datas
                    # da reserva, assim como o total
                    return render_template("reserva.html", categoria_veiculo=informacaoVeiculo[0][1],
                                           preco_diario=informacaoVeiculo[0][12], marca_veiculo=informacaoVeiculo[0][2],
                                           modelo_veiculo=informacaoVeiculo[0][3], valor_Total="Valor Inválido",
                                           data_levantamento=dataLevantamento, data_entrega=dataEntrega,
                                           data_reserva=dataPossivelLevantamento.date(), mensagem=mensagem)
                else:
                    # aqui é retornado os valores respeitantes aos dados da reserva que incluem o do veículo e das datas
                    # da reserva, assim como o total
                    return render_template("reserva.html", categoria_veiculo=informacaoVeiculo[0][1],
                                   preco_diario=informacaoVeiculo[0][12], marca_veiculo=informacaoVeiculo[0][2],
                                   modelo_veiculo=informacaoVeiculo[0][3], valor_Total=valorTotal,
                                   data_levantamento=dataLevantamento, data_entrega=dataEntrega,
                                   data_reserva=dataPossivelLevantamento.date())
            ############################################################################################################
            # se o botão 'ir para pagamento' for acionado mais a checkbox dos termos e condições e se a data de entrega não
            # estiver vazia e a data de levantamento escolhida pelo client for maior ou igual à data de levantamento a
            #partir do qual a viatura está disponivel e a datalevantamento em que a viatura estiver disponível for igual
            # ou inferior à datalevantamento que o cliente escolher
            ############################################################################################################
            elif request.form['botao'] == "Ir para pagamento" and request.form.get('checkbox') == "checkbox" and \
                    request.form['DataEntrega'] is not "" and int(request.form['DataLevantamento'].replace("-","")) >= \
                    int(dataPossivelLevantamento.strftime('%Y%m%d')) and \
                    int(request.form['DataLevantamento'].replace("-","")) < int(request.form['DataEntrega'].replace("-","")):

                ########################################################################################################
                # Criação de uma lista vazia que vai receber todos os valores necessários para retornar a informação
                # para a base de dados Reservas, e para a criação de uma session que contenha toda a informação da
                # reserva do cliente para seguir para o pagamento
                ########################################################################################################
                lista_reserva = []
                lista_reserva.append(session["user_id"][0])
                lista_reserva.append(informacaoVeiculo[0][0])
                lista_reserva.append(infoMatricula[0])
                lista_reserva.append(informacaoVeiculo[0][1])
                lista_reserva.append(informacaoVeiculo[0][2])
                lista_reserva.append(informacaoVeiculo[0][3])
                lista_reserva.append(request.form['DataLevantamento'])
                lista_reserva.append(request.form['DataEntrega'])
                lista_reserva.append(valorTotal)

                # Criação da session respeitante à Reserva (que guarda toda a informação necessária para armazenar)
                session['lista_reserva'] = lista_reserva

                # a reserva prosegue para o pagamento
                return redirect(url_for("pagamento"))

            else:
                # aqui é retornado os valores respeitantes aos dados da reserva que incluem o do veículo e das datas da
                # reserva, assim como o total
                return render_template("reserva.html", categoria_veiculo=informacaoVeiculo[0][1],
                                       preco_diario=informacaoVeiculo[0][12], marca_veiculo=informacaoVeiculo[0][2],
                                       modelo_veiculo=informacaoVeiculo[0][3], valor_Total=valorTotal,
                                       data_levantamento=dataPossivelLevantamento.date(), data_entrega=dataEntrega,
                                       data_reserva=dataPossivelLevantamento.date(), mensagem="Dados Inválidos")

        # é quando entra a primeira vez na pagina reserva
        return render_template("reserva.html", categoria_veiculo=informacaoVeiculo[0][1],
                               preco_diario=informacaoVeiculo[0][12], marca_veiculo=informacaoVeiculo[0][2],
                               modelo_veiculo=informacaoVeiculo[0][3], valor_Total=valorTotal,
                               data_levantamento=dataPossivelLevantamento.date(), data_entrega=dataEntrega,
                               data_reserva=dataPossivelLevantamento.date())
    else:
        # se tentarem fazer uma reserva sem ter uma sessao iniciada o utilizador será redirecionado para a página login
        return redirect(url_for("login"))

# criação da pagina reservaUtilizador
@app.route("/reservaUtilizador", methods= ['POST','GET'])
def reservaUtilizador():

    mensagem = ""
    today = datetime.now()

    # se a session do utilizador estiver ativa
    if "user_id" in session:

        # vão ser extraídas as informações da reserva de acordo com a respectiva session do user_id
        info_reserva_inicial = info_user_reserva(session["user_id"][0])

        print(info_reserva_inicial)
        #uma vez que pode existir mais do que uma reserva feita pelo cliente('exemplo de reservas feitas anteriormente')
        #é necessário encontrar qual a reserva que está válida ou foi feita mais recentemente, para que na eventualidade
        # do cliente querer cancelar dentro do prazo certo o puder fazer, é feito dada uma variável iniciada a zero(
        # data_inicial)de seguida é feito um ciclo for que vai percorrer os elementos contidos na variável
        # 'info_reserva_inicial', seguida de uma comparação com a variável 'data_inicial'. Como se pretende fazer uma
        # comparação entre as datas de levantamento de um x número de reservas feitas pelo o utilizador e estas vem
        # em formato string, tem de ser convertido para inteiro e retira-se os '-'(traços) para que seja devolvido um
        # número inteiro como forma de comparação, 'info_reserva' vai receber a lista relativa à reserva mais recente
        # e que esteja válida(com possibilidade de cancelamento)
        data_incial = 0
        for x in range(len(info_reserva_inicial)):
            if data_incial < int(info_reserva_inicial[x][7].replace("-","")):
                info_reserva = info_reserva_inicial[x]

        # Como é necessário mostrar ao cliente qual a data limite para proceder ao cancelamento da sua reserva,
        # é extraída a data da lista data_info_reserva do tipo datetime. Posteriormente e como limite de cancelamento
        # é até ao dia anterior à reserva, a variável 'data_limite', recebe a data contida em 'data_info_reserva'
        # menos 1 dia 'timedelta(days=1)
        data_info_reserva = datetime.strptime(str(info_reserva[7]), "%Y-%m-%d")
        data_limite = data_info_reserva - timedelta(days=1)

        # Verifica se houve algum método post do html
        if request.method == 'POST':
            # Se o botão 'Cancelar Reserva' for presionado, e a variável 'today.day' for maior que a variável
            # 'data_limite.day', será lançada uma mensagem a informar o utilizador de que data limite de cancelamento
            # expirou, caso seja ao contrário a reserva será cacelada e a mensagem de aviso aparece a indicar que a
            # reserva foi cancelada e o dinheiro será retornado ao cliente num prazo de 24H
            if request.form['botao'] == "Cancelar Reserva":
                if today.day > data_limite.day:
                    mensagem = "A data limite de cancelamento da reserva expirou"
                elif today.day <= data_limite.day:
                    update_valorTotal(info_reserva[0])
                    mensagem = "Reserva cancelada dentro de 24h devolveremos o seu dinheiro!"



        return render_template("reservaUtilizador.html", categoria_veiculo=info_reserva[4],
                               marca_veiculo=info_reserva[5], modelo_veiculo=info_reserva[6],
                               valor_Total=info_reserva[9], data_levantamento=info_reserva[7],
                               data_entrega=info_reserva[8],data_antesLevantamento=data_limite.date(),mensagem=mensagem)


#   else:
     #   mensagem = "De momento não tem nenhuma reserva efectuada"
       # return render_template("reservaUtilizador.html", mensagem=mensagem)


# criação da pagina pagamento
@app.route("/pagamento", methods= ['POST', 'GET'])
def pagamento():

    # Se a sessão o utilizador e a sessão da reserva estiverem iniciadas
    if "user_id" in session and "lista_reserva" in session:
        # Se o request.method for igual a POST e o botão finalizar for precionado assim como a checkbox for preenchida
        # os dados de pagamento serão armazenados nas 4 variáveis abaixo
        if request.method == 'POST' and request.form["botao"] == "Finalizar Reserva" and request.form.get('checkbox') == "checkbox":
            numCartaoCredito = request.form['clienteCartaoCredito']
            dataCartaoCredito = request.form['mesCartaoCredito']
            cvv = request.form['cvv']
            nomeCartaoCredito = request.form['titularCartaoCredito']
            # instância da classe Reserva que vai enviar as informações que estão dentro da session reserva para a base
            # de dados resevas.db utilizando para isso o método dadosReserva()
            info_reserva = Reservas(session["lista_reserva"][0],session["lista_reserva"][1],
            session["lista_reserva"][2],session["lista_reserva"][3],session["lista_reserva"][4],
            session["lista_reserva"][5],session["lista_reserva"][6],session["lista_reserva"][7],
            session["lista_reserva"][8])

            info_reserva.dadosReserva()
            #idReserva vai extrair a informação necessária através do método extrair_id_reserva() da classe Reservas
            idReserva = info_reserva.extrair_id_reserva()

            # instância da classe Pagamento que vai enviar as informações do cartão do cliente assim como o id da reserva
            # e do cliente
            info_pagamento = Pagamentos(idReserva, session["lista_reserva"][0],numCartaoCredito,
            dataCartaoCredito, cvv, nomeCartaoCredito)

            #info_pagamento irá guardar as informações da reserva na base de dados pagamentos
            info_pagamento.dadosPagamento()
            # é aqui utilizado um time.sleep de 7 segundos para que o utilizador possa visualizar a mensagem que lhe
            # será apresentada no modal que aparece como confirmação da sua reserva
            time.sleep(7)
            # e de seguida será redirecionado para a sua página de utilizador
            return redirect(url_for("utilizadores"))
        else:
            # caso contrario retorna à pagina de pagamento relativo à sua reserva
            return render_template("pagamento.html")
    else:
        # caso não exista uma session do utilizador ou da reserva ou ambas então será retornado para o login para
        # iniciar uma sessão de utilizador
        return redirect(url_for("login"))

if __name__ == '__main__':
    # O debug = True faz com que cada vez que reiniciar-mos o servidor ou modificar-mos o código, o servidor de Flask
    # reinicia-se sozinho de forma automatica
    app.run(debug=True)

