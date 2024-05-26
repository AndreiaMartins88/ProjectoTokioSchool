import sqlite3
from PyQt6 import QtCore, QtGui, QtWidgets
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pagGestaoStock
import pagLegalizacao
import pagManutencao
from PyQt6.QtWidgets import QTableWidgetItem, QDialog
#imports necessários para o grafico
from PyQt6.QtCharts import QBarSet, QBarSeries, QValueAxis, QChart, QChartView, QBarCategoryAxis
from PyQt6.QtCore import Qt
#versões das bibliotecas:
#PyQt6 - 6.6.1
#PyQT6-Charts - 6.6.1
#dateutil -2.8.2


# Variáveis globais
today = datetime.now()

#variável que vem da 'pagManutencao',e é iniciada a false na paginaPrincipal e utilizada no método def mostrarManuntencao(self):
enviarParaManutencao = False

# variável do tipo lista, que está vazia quando iniciada nesta página, e que será também utilizada no mesmo método da
# variável anterior
receberListaTabela = []

#######################################################################################################################
#Funções globais que vão ser necessarias utilizar em mais do que uma slot(método) e em outras funções, como é preciso
# aceder a diferentes bases de dados para extrair e manipular a informação. Fiz estas funções globais de forma a
# evitar a repetição de código
#######################################################################################################################
#Acesso à base de dados DBcarros.db e extração dos seus dados.
def updateDBCarros():
    try:
        con = sqlite3.connect("database/DBcarros.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM carro")
        valueCarros = cursor.fetchall()
        cursor.close()
        return valueCarros
    except:
        print("Nao foi possivel aceder a base de dados")

#Acesso à base de dados DBMotas.db e extração dos seus dados.
def updateDBMotas():
    try:
        con = sqlite3.connect("database/DBMotas.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM mota")
        valueMotas = cursor.fetchall()
        cursor.close()
        return valueMotas
    except:
        print("Nao foi possivel aceder a base de dados")

#Acesso à base de dados DButilizadores.db e extração dos seus dados.
def updateDBUtilizadores():
    try:
        con = sqlite3.connect("database/DButilizadores.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM utilizador")
        valueUtilizadores = cursor.fetchall()
        cursor.close()
        return valueUtilizadores
    except:
        print("Nao foi possivel aceder a base de dados")

#Acesso à base de dados DBreservas.db e extração dos seus dados.
def updateDBreservas():
    try:
        con = sqlite3.connect("database/DBreservas.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM reserva")
        valueReservas = cursor.fetchall()
        cursor.close()
        return valueReservas
    except:
        print("Nao foi possivel aceder a base de dados")

#####################################################################################################################
# Método necessário para que se possa visualizar um gráfico anual sempre que se inicia a aplicação. Este gráfico vai
# ter todos os meses do ano e irá registar as entradas e saídas de dinheiro mensais, mostrando desta forma a
# flutuação do valor em caixa. Para aceder aos valores das entradas de dinheiro tive de aceder à base de dados
# DBreservas.db, em que são contabilizadas todas as reservas pagas e respectivas datas em que foram pagas, uma vez que a
# reserva da viatura é feita no site e esta só fica gravada na base de dados após ter sido efectuado o pagamento
# optei por utilizar esta base de dados. Já para as saídas de dinheiro utilizei as bases de dados de ambos os
# veiculos retirado as informações das colunas legalização e datalegalização para contabilizar as saídas de dinheiro
#####################################################################################################################
def updateGraficoResumo():
        # Variaveis para o gráfico
        categorias = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro",
                      "Outubro",
                      "Novembro", "Dezembro"]

        # Variaveis para processamento de dados todas elas listas com 12 elementos (correspondente aos 12 meses do ano)
        listaMesesNumerico = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        valorSaidaDinheiro = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        valorEntradaDinheiro = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        totalVeiculos = updateDBCarros() + updateDBMotas()

        ################################################################################################################
        # Este ciclo "for" é necessário para extrair as saídas de dinheiro de acordo com cada mês do ano,
        # para isso este ciclo percorrer a lista 'totalVeiculos', e em cada um dos veiculos na coluna [8] que corresponde
        # à data da última legalização, a variável valor1 recebe essa informação. O segundo "for" percorre a
        # 'listaMesesNumerico' e se data do ano presente for igual ao mês e dia de alguma das datas presentes de
        # valor1, então a 'valorSaidaDinheiro' vai receber a soma de todas vezes em que num mesmo mês houveram saídas de
        # dinheiro para pagar legalizações acedendo à coluna [9] que corresponde ao preço da legalização.
        ################################################################################################################
        for x in range(len(totalVeiculos)):
                valor1 = totalVeiculos[x][8]
                for y in range(len(listaMesesNumerico)):
                        if today.year == int(valor1[:4]) and listaMesesNumerico[y] == int(valor1[5:7]):
                                valorSaidaDinheiro[y] += totalVeiculos[x][9]
        ################################################################################################################
        # Neste for a ideia é em muito semelhante à acima descrita, sendo que aqui é para extrair os valores de
        # entradas de dinheiro, e aqui acede-se directamente à base de dados das reservas, isto porque de acordo com
        # o que foi feito no site(que foi a primeira parte deste projecto), a base de dados reserva apenas ficava com
        # um registo gravado se o pagamento tivesse sido efectuado por parte do cliente. De resto o processo é
        # exatamente o mesmo, acedendo às colunas específicas que contém as datas de levantamento[7], e o valor total[9]
        # de cada renting efectuado. 'valorEntradaDinheiro' recebe o falor faturado de cada mês.
        ################################################################################################################
        for x in range(len(updateDBreservas())):
                valor2 = updateDBreservas()[x][7]
                for y in range(len(listaMesesNumerico)):
                        if today.year == int(valor2[:4]) and listaMesesNumerico[y] == int(valor2[5:7]):
                                valorEntradaDinheiro[y] += updateDBreservas()[x][9]

        # Aqui defeni o nome que irá aparecer em cada barra do gráfico, em cada mês serão mostradas 2 barras
        barra1 = QBarSet("Entrada de Dinheiro")
        barra2 = QBarSet("Saída de Dinheiro")
        # Cada barra recebe o valor correspondente à entrada e saída de dinheiro
        barra1.append(valorEntradaDinheiro)
        barra2.append(valorSaidaDinheiro)
        # As barras são adicionadas ao gráfico já com a informação
        barras = QBarSeries()
        barras.append(barra1)
        barras.append(barra2)

        grafico = QChart()
        grafico.addSeries(barras)
        grafico.setTitle("Entradas e Saídas de Dinheiro em Caixa")
        # aspecto visual do gráfico para se enquadrar melhor no design ChartThemeDark
        grafico.setTheme(QChart.ChartTheme.ChartThemeDark)

        axis_x = QBarCategoryAxis()
        axis_x.append(categorias)
        axis_x.setTitleText("Mês")
        grafico.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

        #Explicar o que está a acontecer na condição seguinte
        if max(valorSaidaDinheiro) > max(valorEntradaDinheiro):
                maximo = max(valorSaidaDinheiro)
        else:
                maximo = max(valorEntradaDinheiro)

        axis_y = QValueAxis()
        axis_y.setRange(0, maximo+100)
        axis_y.setTitleText("Valor Máximo")
        grafico.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

        barras.attachAxis(axis_x)
        barras.attachAxis(axis_y)

        visualizarGrafico = QChartView(grafico)

        return visualizarGrafico

######################################################################################################################
# Classe principal, aqui dentro encontra-se tudo o que é relacionado com o designe da aplicação, sendo esta a pagina
# principal, ela está dividida em header e body, por sua vez o body está dividio em um menu lateral esquerdo e um
# stackWidget com 5 camadas, para aceder ao conteúdo de cada camada será feito através dos botões que constam no menu
# lateral esquerdo que é onde estão os botões correspondentes. Ainda na zona do header(cabeça-lho) temos 3 botões que
# caso sejam precionados faz com que se abra uma pagina correspondente a esse botão. Estes botões do cabeça-lho
# servem também de alerta caso exista veiculos para manutenção o botão que é primariamente com o texto em branco
# torna-se azul, o mesmo acontece para os outros dois botões localizados no header (botão legalização, e Gestão Stock).
######################################################################################################################
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        # defenição das dimensões da janela principal
        MainWindow.resize(1102, 595)
        # defenição da estilização dos widgets
        MainWindow.setStyleSheet("*{\n"
"    border:none;\n"
"    background-color:transparent;\n"
"    background: transparent;\n"
"    padding:0;\n"
"    margin:0;\n"
"    color:#fff;\n"
"}\n"
"#centralwidget, #bodyContent, #kmLineEdit,#matriculaLineEdit, #submeterBtn,#kmLineEdit_2,#matriculaLineEdit_2, #submeterBtn_2,#kmLineEdit_3,#matriculaLineEdit_3,#submeterBtn_3{\n"
"    background-color: #1f2329;\n"
"}\n"
"#header,#mainBody,#frotaCarrosBtn,#frotaMotasBtn, #entregaVeiculo, #manutencaoVeiculo,#legalizacaoVeiculo{\n"
"    background-color:#27263c;\n"
"}\n"
"QPushButton{\n"
"    text-align:left;\n"
"    padding:3px 5px;\n"
"}\n"
"#frotaCarrosBtn,#frotaMotasBtn, #submeterBtn,#submeterBtn_2,#submeterBtn_3{\n"
"    border-radius: 12px;\n"
"    border: 2px solid #0080FF;\n"
"}\n"
"#tableWidget_2{\n"
"    margin-left: 55px;\n"
"}\n"
"\n"
"")
        MainWindow.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        #widget central sobre o qual foi desenhada toda aplicação relativa à página principal
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        # header widget que corresponde ao cabeçalho da aplicação, aqui consta o nome da empresa e 3 botões que além
        # de abrirem outras paginas secundárias servem também de alerta
        self.header = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.header.sizePolicy().hasHeightForWidth())
        self.header.setSizePolicy(sizePolicy)
        self.header.setObjectName("header")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_2 = QtWidgets.QFrame(parent=self.header)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.marcaLabel = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(20)
        font.setBold(True)
        self.marcaLabel.setFont(font)
        self.marcaLabel.setObjectName("marcaLabel")
        self.horizontalLayout_4.addWidget(self.marcaLabel)
        self.horizontalLayout.addWidget(self.frame_2, 0, QtCore.Qt.AlignmentFlag.AlignLeft)
        self.frame = QtWidgets.QFrame(parent=self.header)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # botão manutenção
        self.manutencaoHeaderBtn = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.manutencaoHeaderBtn.setFont(font)
        self.manutencaoHeaderBtn.setIconSize(QtCore.QSize(27, 27))
        self.manutencaoHeaderBtn.setObjectName("manutencaoHeaderBtn")
        self.horizontalLayout_3.addWidget(self.manutencaoHeaderBtn)
        # botão legalização
        self.legalizacaoHeaderBtn = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.legalizacaoHeaderBtn.setFont(font)
        self.legalizacaoHeaderBtn.setIconSize(QtCore.QSize(27, 27))
        self.legalizacaoHeaderBtn.setObjectName("legalizacaoHeaderBtn")
        self.horizontalLayout_3.addWidget(self.legalizacaoHeaderBtn)
        self.stockHeaderBtn = QtWidgets.QPushButton(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        # botão Gestão de Stock
        self.stockHeaderBtn.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icons/original_svg/book-open.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.stockHeaderBtn.setIcon(icon)
        self.stockHeaderBtn.setIconSize(QtCore.QSize(27, 27))
        self.stockHeaderBtn.setObjectName("stockHeaderBtn")
        self.horizontalLayout_3.addWidget(self.stockHeaderBtn)
        self.horizontalLayout.addWidget(self.frame, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.verticalLayout.addWidget(self.header, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.mainBody = QtWidgets.QWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainBody.sizePolicy().hasHeightForWidth())
        # mainBody aqui inicia a zona do corpo principal da aplicação onde consta o menu lateral esquerdo e body que
        # tem os stackedWidgets
        self.mainBody.setSizePolicy(sizePolicy)
        self.mainBody.setObjectName("mainBody")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.mainBody)
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        #Menu lateral esquerdo
        self.leftMenu = QtWidgets.QWidget(parent=self.mainBody)
        self.leftMenu.setMinimumSize(QtCore.QSize(200, 0))
        self.leftMenu.setObjectName("leftMenu")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.leftMenu)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.widget = QtWidgets.QWidget(parent=self.leftMenu)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_3 = QtWidgets.QFrame(parent=self.widget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        #botão lateral esquerdo resumo
        self.resumoBtn = QtWidgets.QPushButton(parent=self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.resumoBtn.setFont(font)
        self.resumoBtn.setIconSize(QtCore.QSize(21, 21))
        self.resumoBtn.setObjectName("resumoBtn")
        self.verticalLayout_5.addWidget(self.resumoBtn)
        #botão lateral esquerdo frota
        self.frotaBtn = QtWidgets.QPushButton(parent=self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.frotaBtn.setFont(font)
        self.frotaBtn.setIconSize(QtCore.QSize(21, 21))
        self.frotaBtn.setObjectName("frotaBtn")
        self.verticalLayout_5.addWidget(self.frotaBtn)
        self.verticalLayout_4.addWidget(self.frame_3)
        ##############################################################################################################
        # Espaçador para fazer uma separação entre os botões. Botão Resumo e Botão Fronta estão mais afastados dos
        # restantes botões; Botão Renting, Botão Manutenção e Botão Legalização, este separador foi colocado de forma
        # intencional pois os dois primeiros botões são apenas para visualizar informação ao contrário dos outros 3
        # que são para visualizar informação dentro dos stackedwidgets mas o utilizador pode também fazer ações como
        # disponibilizar veiculos novamente.
        ##############################################################################################################
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.frame_4 = QtWidgets.QFrame(parent=self.widget)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        #botão lateral esquerdo renting
        self.rentingBtn = QtWidgets.QPushButton(parent=self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.rentingBtn.setFont(font)
        self.rentingBtn.setIconSize(QtCore.QSize(21, 21))
        self.rentingBtn.setObjectName("rentingBtn")
        self.verticalLayout_6.addWidget(self.rentingBtn)
        #botão lateral esquerdo manutenção
        self.manutencaoBtn = QtWidgets.QPushButton(parent=self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.manutencaoBtn.setFont(font)
        self.manutencaoBtn.setIconSize(QtCore.QSize(21, 21))
        self.manutencaoBtn.setObjectName("manutencaoBtn")
        self.verticalLayout_6.addWidget(self.manutencaoBtn)
        #botao lateral esquerdo legalização
        self.legalizacaoBtn = QtWidgets.QPushButton(parent=self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.legalizacaoBtn.setFont(font)
        self.legalizacaoBtn.setIconSize(QtCore.QSize(21, 21))
        self.legalizacaoBtn.setObjectName("legalizacaoBtn")
        self.verticalLayout_6.addWidget(self.legalizacaoBtn)
        self.verticalLayout_4.addWidget(self.frame_4)
        self.verticalLayout_3.addWidget(self.widget)
        self.horizontalLayout_2.addWidget(self.leftMenu)
        self.bodyContent = QtWidgets.QWidget(parent=self.mainBody)
        self.bodyContent.setObjectName("bodyContent")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.bodyContent)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        ###############################################################################################################
        # StackedWidget composto por 5 folhas ou camadas, cada uma corresponde a um dos botões laterais acima referidos,
        # podendo ser acedidas clicando no botão, a camada que aparece no início e intecionalmente é a do resumo em
        # que mostra o grafico
        ###############################################################################################################
        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.bodyContent)
        self.stackedWidget.setObjectName("stackedWidget")
        # stackdeWidget Resumo
        self.pagResumo = QtWidgets.QWidget()
        self.pagResumo.setObjectName("pagResumo")
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.pagResumo)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(-1, -1, 881, 481))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget.addWidget(self.pagResumo)
        ###############################################################################################################
        # stackdeWidget Frota e seu conteúdo, é composto por uma tabela (QTable) e dois botões (QPushButton) para
        # aceder às diferentes tabelas qualquer um dos dois botões tem de ser precionado antes de visualizar qualquer
        # uma delas
        ###############################################################################################################
        self.pagFrota = QtWidgets.QWidget()
        self.pagFrota.setObjectName("pagFrota")
        self.frame_5 = QtWidgets.QFrame(parent=self.pagFrota)
        self.frame_5.setGeometry(QtCore.QRect(0, 10, 881, 421))
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setContentsMargins(0, 10, 0, 10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tabelaFrota = QtWidgets.QTableWidget(parent=self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabelaFrota.sizePolicy().hasHeightForWidth())
        self.tabelaFrota.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(8)
        self.tabelaFrota.setFont(font)
        self.tabelaFrota.setStyleSheet("color:#55aaff\n""")
        self.tabelaFrota.setObjectName("tabelaFrota")
        self.tabelaFrota.setColumnCount(10)
        self.tabelaFrota.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabelaFrota.setHorizontalHeaderItem(9, item)
        self.tabelaFrota.horizontalHeader().setDefaultSectionSize(88)
        self.tabelaFrota.verticalHeader().setDefaultSectionSize(30)
        self.horizontalLayout_6.addWidget(self.tabelaFrota)
        self.frame_6 = QtWidgets.QFrame(parent=self.pagFrota)
        self.frame_6.setGeometry(QtCore.QRect(673, 430, 191, 41))
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.frotaCarrosBtn = QtWidgets.QPushButton(parent=self.frame_6)
        self.frotaCarrosBtn.setMinimumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.frotaCarrosBtn.setFont(font)
        self.frotaCarrosBtn.setStyleSheet("text-align: center;\n""")
        self.frotaCarrosBtn.setObjectName("frotaCarrosBtn")
        self.horizontalLayout_5.addWidget(self.frotaCarrosBtn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.frotaMotasBtn = QtWidgets.QPushButton(parent=self.frame_6)
        self.frotaMotasBtn.setMinimumSize(QtCore.QSize(70, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.frotaMotasBtn.setFont(font)
        self.frotaMotasBtn.setStyleSheet("text-align:center;")
        self.frotaMotasBtn.setObjectName("frotaMotasBtn")
        self.horizontalLayout_5.addWidget(self.frotaMotasBtn, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.stackedWidget.addWidget(self.pagFrota)
        ##############################################################################################################
        # stackdeWidget Renting este é composto por uma tabela (QTable) que mostra os veiculos que estão em arrendamento
        # naquele momento. Tem também um campo que após devolução do veiculo, ele pode ficar imediatamente disponível,
        # basta para isso inserir a matricula e os km e carregar no botão submeter e ele fica disponivel, caso não se
        # proceda actualização manual do veículo na base de dados, essa actualização será feita pelo lado do site
        ###############################################################################################################
        self.pagRenting = QtWidgets.QWidget()
        self.pagRenting.setObjectName("pagRenting")
        self.frame_7 = QtWidgets.QFrame(parent=self.pagRenting)
        self.frame_7.setGeometry(QtCore.QRect(10, 20, 851, 371))
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.frame_7)
        self.tableWidget.setGeometry(QtCore.QRect(60, 0, 871, 371))
        self.tableWidget.setStyleSheet("color:#0080FF;\n""")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(124)
        self.entregaVeiculo = QtWidgets.QWidget(parent=self.pagRenting)
        self.entregaVeiculo.setGeometry(QtCore.QRect(-5, 440, 891, 48))
        self.entregaVeiculo.setObjectName("entregaVeiculo")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.entregaVeiculo)
        self.horizontalLayout_7.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_7.setSpacing(21)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.tituloLabel = QtWidgets.QLabel(parent=self.entregaVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.tituloLabel.setFont(font)
        self.tituloLabel.setScaledContents(False)
        self.tituloLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tituloLabel.setIndent(-1)
        self.tituloLabel.setObjectName("tituloLabel")
        self.horizontalLayout_7.addWidget(self.tituloLabel)
        self.matriculaLineEdit = QtWidgets.QLineEdit(parent=self.entregaVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.matriculaLineEdit.setFont(font)
        self.matriculaLineEdit.setObjectName("matriculaLineEdit")
        self.horizontalLayout_7.addWidget(self.matriculaLineEdit)
        self.kmLineEdit = QtWidgets.QLineEdit(parent=self.entregaVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.kmLineEdit.setFont(font)
        self.kmLineEdit.setObjectName("kmLineEdit")
        self.horizontalLayout_7.addWidget(self.kmLineEdit)
        self.submeterBtn = QtWidgets.QPushButton(parent=self.entregaVeiculo)
        self.submeterBtn.setMinimumSize(QtCore.QSize(85, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.submeterBtn.setFont(font)
        self.submeterBtn.setStyleSheet("text-align:center")
        self.submeterBtn.setObjectName("submeterBtn")
        self.horizontalLayout_7.addWidget(self.submeterBtn)
        self.stackedWidget.addWidget(self.pagRenting)
        ###############################################################################################################
        # stackdeWidget Manutenção, aqui temos uma tabela (QTable) que mostra quais os veiculos que foram enviados para
        # manutenção, na tabela surge uma data de fim de manutenção de 30 dias após a entrada do veículo em
        # manutenção, no entanto e caso esta termine a manutenção antes dos 30 dias poderá ser disponibilizada a
        # viatura antes desse tempo, bastando para isso inserir a matricula da viatura e os km da mesma e clicar no
        # botão submeter (QPushButton)
        ###############################################################################################################
        self.pagManutencao = QtWidgets.QWidget()
        self.pagManutencao.setObjectName("pagManutencao")
        self.manutencaoVeiculo = QtWidgets.QWidget(parent=self.pagManutencao)
        self.manutencaoVeiculo.setGeometry(QtCore.QRect(0, 440, 891, 48))
        self.manutencaoVeiculo.setObjectName("manutencaoVeiculo")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.manutencaoVeiculo)
        self.horizontalLayout_8.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_8.setSpacing(21)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.tituloLabel_2 = QtWidgets.QLabel(parent=self.manutencaoVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.tituloLabel_2.setFont(font)
        self.tituloLabel_2.setScaledContents(False)
        self.tituloLabel_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tituloLabel_2.setIndent(-1)
        self.tituloLabel_2.setObjectName("tituloLabel_2")
        self.horizontalLayout_8.addWidget(self.tituloLabel_2)
        self.matriculaLineEdit_2 = QtWidgets.QLineEdit(parent=self.manutencaoVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.matriculaLineEdit_2.setFont(font)
        self.matriculaLineEdit_2.setObjectName("matriculaLineEdit_2")
        self.horizontalLayout_8.addWidget(self.matriculaLineEdit_2)
        self.kmLineEdit_2 = QtWidgets.QLineEdit(parent=self.manutencaoVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.kmLineEdit_2.setFont(font)
        self.kmLineEdit_2.setStyleSheet("")
        self.kmLineEdit_2.setObjectName("kmLineEdit_2")
        self.horizontalLayout_8.addWidget(self.kmLineEdit_2)
        self.submeterBtn_2 = QtWidgets.QPushButton(parent=self.manutencaoVeiculo)
        self.submeterBtn_2.setMinimumSize(QtCore.QSize(85, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.submeterBtn_2.setFont(font)
        self.submeterBtn_2.setStyleSheet("text-align:center")
        self.submeterBtn_2.setObjectName("submeterBtn_2")
        self.horizontalLayout_8.addWidget(self.submeterBtn_2)
        self.frame_8 = QtWidgets.QFrame(parent=self.pagManutencao)
        self.frame_8.setGeometry(QtCore.QRect(0, 10, 881, 381))
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.tableWidget_2 = QtWidgets.QTableWidget(parent=self.frame_8)
        self.tableWidget_2.setStyleSheet("color:#0080FF;")
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(6)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(123)
        self.verticalLayout_7.addWidget(self.tableWidget_2)
        self.stackedWidget.addWidget(self.pagManutencao)
        ###############################################################################################################
        # stackdeWidget Legalização aqui surgem de forma directa todas as viaturas que estão com aproximação de 30
        # dias da data limite para renovação da legalização da viatura, podendo ser disponibilizada mais cedo
        # bastando para isso inserir a matricula os km e a data da nova legalização
        ###############################################################################################################
        self.pagLegalizacao = QtWidgets.QWidget()
        self.pagLegalizacao.setObjectName("pagLegalizacao")
        self.legalizacaoVeiculo = QtWidgets.QWidget(parent=self.pagLegalizacao)
        self.legalizacaoVeiculo.setGeometry(QtCore.QRect(0, 440, 881, 48))
        self.legalizacaoVeiculo.setObjectName("legalizacaoVeiculo")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.legalizacaoVeiculo)
        self.horizontalLayout_9.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_9.setSpacing(21)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.tituloLabel_3 = QtWidgets.QLabel(parent=self.legalizacaoVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.tituloLabel_3.setFont(font)
        self.tituloLabel_3.setScaledContents(False)
        self.tituloLabel_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.tituloLabel_3.setIndent(-1)
        self.tituloLabel_3.setObjectName("tituloLabel_3")
        self.horizontalLayout_9.addWidget(self.tituloLabel_3)
        self.matriculaLineEdit_3 = QtWidgets.QLineEdit(parent=self.legalizacaoVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.matriculaLineEdit_3.setFont(font)
        self.matriculaLineEdit_3.setObjectName("matriculaLineEdit_3")
        self.horizontalLayout_9.addWidget(self.matriculaLineEdit_3)
        self.kmLineEdit_3 = QtWidgets.QLineEdit(parent=self.legalizacaoVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.kmLineEdit_3.setFont(font)
        self.kmLineEdit_3.setStyleSheet("")
        self.kmLineEdit_3.setObjectName("kmLineEdit_3")
        self.horizontalLayout_9.addWidget(self.kmLineEdit_3)
        self.dataLegalizacao = QtWidgets.QDateEdit(parent=self.legalizacaoVeiculo)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.dataLegalizacao.setFont(font)
        self.dataLegalizacao.setDateTime(QtCore.QDateTime(QtCore.QDate(2024, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dataLegalizacao.setObjectName("dataLegalizacao")
        self.horizontalLayout_9.addWidget(self.dataLegalizacao)
        self.submeterBtn_3 = QtWidgets.QPushButton(parent=self.legalizacaoVeiculo)
        self.submeterBtn_3.setMinimumSize(QtCore.QSize(85, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.submeterBtn_3.setFont(font)
        self.submeterBtn_3.setStyleSheet("text-align:center")
        self.submeterBtn_3.setObjectName("submeterBtn_3")
        self.horizontalLayout_9.addWidget(self.submeterBtn_3)
        self.frame_9 = QtWidgets.QFrame(parent=self.pagLegalizacao)
        self.frame_9.setGeometry(QtCore.QRect(0, 10, 881, 401))
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tableWidget_3 = QtWidgets.QTableWidget(parent=self.frame_9)
        self.tableWidget_3.setStyleSheet("color:#0080FF;")
        self.tableWidget_3.setObjectName("tableWidget_3")
        self.tableWidget_3.setColumnCount(8)
        self.tableWidget_3.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(7, item)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(107)
        self.verticalLayout_8.addWidget(self.tableWidget_3)
        self.stackedWidget.addWidget(self.pagLegalizacao)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addWidget(self.bodyContent)
        self.verticalLayout.addWidget(self.mainBody)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        # widget principal do stackwidget que aparece inicalmente na abertura da aplicação e onde consta o gráfico
        self.stackedWidget.setCurrentWidget(self.pagResumo)

        # Signal's das slots de connecção dos botões às páginas do QDialog
        self.manutencaoHeaderBtn.clicked.connect(self.ligarManutencao)
        self.legalizacaoHeaderBtn.clicked.connect(self.ligarLegalizacao)
        self.stockHeaderBtn.clicked.connect(self.ligarStock)

        # Signal's das slots de connecção dos botões às páginas dos stackedWidgets
        self.resumoBtn.clicked.connect(self.mostrarResumo)
        self.frotaBtn.clicked.connect(self.mostrarFrota)
        self.rentingBtn.clicked.connect(self.mostrarRenting)
        self.manutencaoBtn.clicked.connect(self.mostrarManuntencao)
        self.legalizacaoBtn.clicked.connect(self.mostrarLegalizacao)




        # Signal visualizar frota carros que está dentro do stackedWidget Frota
        self.frotaCarrosBtn.clicked.connect(self.visualizarCarros)
        # Signal visualizar frota motas que está dentro do stackedWidget Frota
        self.frotaMotasBtn.clicked.connect(self.visualizarMotas)
        # Signal para visualizar quais os veiculos com aproximação de data de legalização anual
        self.legalizacaoBtn.clicked.connect(self.legalizacaoBotao)
        # Signal para actualizar os veículos que foram legalizados e disponibiliza-los na base de dados para renting
        # stackedWidget Legalizacao
        self.submeterBtn_3.clicked.connect(self.upDateVeiculosLegais)
        # Signal para visualizar que carros é que estão arrendados na data de hoje (botão renting menu lateral esquerdo)
        self.rentingBtn.clicked.connect(self.rentingVeiculos)
        # Signal para que os veiculos fiquem disponiveis e os km actualizados após a entrega da viatura nas instalações
        #stackedWidget Renting
        self.submeterBtn.clicked.connect(self.updateDevolucao)
        # Signal para que os veiculos fiquem disponíveis após finalizarem a manutenção stackedWidget Manutencao
        self.submeterBtn_2.clicked.connect(self.finalizarManutencao)


        ###############################################################################################################
        # Caso seja recomendado aumentar o stock de veiculos o botão de Gestão Stock que está no cabeçalho da
        # paginaPrincipal passa as letras de branco para azul como forma de sinalizar um alerta. É feita uma comparação
        # entre o número de veiculos existente em cada base de dados carros e motas, o número total de veiculos é
        # somado e posteriormente comparado ao número total de utilizadores. Esta verificação é feita sempre que
        # aplicação é iniciada. Como é pedido no enunciado, se o número de utilizadores + 5 for maior que o total de
        # veículos existentes nas bases de dados é recomendado que sejam adquiridos mais 5 veiculos.
        ###############################################################################################################
        totalCarros = len(updateDBCarros())
        totalMotas = len(updateDBMotas())
        totalVeiculos = totalCarros + totalMotas
        totalUtilizadores = len(updateDBUtilizadores())

        ##############################################################################################################
        # condicional que verifica a necessidade de aquisição de novas viaturas, mediante o resultado desta verificação
        # a variável 'verificacaoVeiculosNovos' (que remete para a 'pagGestaoStock') será exibido o número necessário
        # de novos veiculos
        ##############################################################################################################
        if (totalUtilizadores + 5) >= totalVeiculos:
                pagGestaoStock.verificacaoVeiculosNovos = True
                self.stockHeaderBtn.setStyleSheet("color: #0080FF;")

        ##############################################################################################################
        #Caso existam veículos com necessidade de actualizar a sua documentação legal, será emitido um sinal de
        # alerta, em que as letras do botão Legalização do cabeçalho da página principal passam a azul, para isso é
        # necessário confirmar qual o número total de veículos que estão para legalização, porém é gerado um sinal para
        # a paginaLegalizacao através da condição if
        ###############################################################################################################
        for x in range(len(updateDBMotas())):
            dataExtraidaMotas = datetime.strptime(str(updateDBMotas()[x][8]), "%Y-%m-%d")
            dataMaisAnoMotas = dataExtraidaMotas + relativedelta(years=1)
            dataNovaMotas = dataMaisAnoMotas - relativedelta(days=30)

            if today >= dataNovaMotas and today <= dataMaisAnoMotas :
                    pagLegalizacao.verificarLegalizacoesNovas = True
                    self.legalizacaoHeaderBtn.setStyleSheet("color: #0080FF;")
                    break

        for x in range(len(updateDBCarros())):
            dataExtraidaCarros = datetime.strptime(str(updateDBCarros()[x][8]), "%Y-%m-%d")
            dataMaisAnoCarros = dataExtraidaCarros + relativedelta(years=1)
            dataNovaCarros = dataMaisAnoCarros - relativedelta(days=30)

            if today >= dataNovaCarros and today <= dataMaisAnoCarros :
                    pagLegalizacao.verificarLegalizacoesNovas = True
                    self.legalizacaoHeaderBtn.setStyleSheet("color: #0080FF;")
                    break

        # Caso existam veículos com necessidade de entrar em manutenção um alerta será lançado passando o texto do
        # botão Manutenção do cabeçalho a azul(#0080FF) em vez de ter a cor branca.

        # variável que combina a informação das duas bases de dados
        listaVeiculos = updateDBCarros() + updateDBMotas()


        #São extraídos os elementos correspondentes aos km actuais e da última revisão da listaVeiculos de cada veículo
        for x in range(len(listaVeiculos)):
            kmActuais = int(listaVeiculos[x][6])
            ultimaRevisao = int(listaVeiculos[x][7])
            # se o valor dos kmActuais for maior ou igual aos km da ultimaRevisão mais 5000, então o botão de alerta
            # Manutencção que se encontra no cabeça-lho passa a cor azul
            if kmActuais >= (ultimaRevisao + 5000):
                  self.manutencaoHeaderBtn.setStyleSheet("color:#0080FF")
                  break

    ###############################################################################################################
    #Inicialização do gráfico, para quando a aplicação corre a primeira vez é automaticamente actualizado e apareça
    ################################################################################################################
        self.gridLayout.addWidget(updateGraficoResumo(), 1, 1)

    #################################################################################################################
    # Slot de ligação do botão do menu lateral 'Resumo' à sua respetiva páginas/camadas stackwidget
    def mostrarResumo(self):

        self.stackedWidget.setCurrentWidget(self.pagResumo)
        self.gridLayout.addWidget(updateGraficoResumo(),1,1)


    # Slot de ligação do botão do menu lateral 'Frota' à sua respetiva páginas/camadas stackwidget
    def mostrarFrota(self):
            self.stackedWidget.setCurrentWidget(self.pagFrota)

    # Slot de ligação do botão do menu lateral 'Renting' à sua respetiva páginas/camadas stackwidget
    def mostrarRenting(self):
            self.stackedWidget.setCurrentWidget(self.pagRenting)

    # Slot de ligação do botão 'Manutenção' à respetiva página stackedwidget que no momento de abertura recebe os
    # dados enviados da pagManutencao (Qdialog)
    def mostrarManuntencao(self):
            self.stackedWidget.setCurrentWidget(self.pagManutencao)
            # Ao entrar no separador Manutenção da 'paginaPrincipal', se houver veiculos que tenham sido submetidos
            # para manutenção através da 'pagManutencao' eles serão adicionados ao QTableWidget deste separador
            if enviarParaManutencao == True:
                self.tableWidget_2.setRowCount(0)
                # No primeiro 'for' é precorrida a variável receberListaTabela de maneira a enumerar as linhas da
                # tabela (row_number) e extrair a informação para cada linha (row_data), de seguida é precorrida a
                # variável row_data de maneira a enumerar as colunas (column_number) e enviar a informação para o
                # QTableWidgetItem
                for row_number, row_data in enumerate(receberListaTabela):
                   self.tableWidget_2.insertRow(row_number)
                   for column_number, data in enumerate(row_data):
                       self.tableWidget_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    #################################################################################################################
    # Slot/ método que vai servir para retirar os veículos do estado Manutenção e disponibilizar novamente a viatura
    # para aluguer.
    def finalizarManutencao(self):
            matricula = self.matriculaLineEdit_2.text().upper()
            km = self.kmLineEdit_2.text()
            # Ao ser disponibilizada a viatura, esta passa a disponível na base de dados, recebe os kms actualizados e
            # passa ao estado fora de manutenção, utilizando o valor da matricula para fazer esse update
            info = [1,km,0,matricula]
            db = ""
            query = ""

            # se os campos matricula e km não forem preenchidos irá aparecer uma linha azul nos campos que faltam
            # preencher no momento em que se pressionar o botão submeter, caso os campos estejam preenchidos a linha azul
            # desaparece
            if self.matriculaLineEdit_2.text() == "":
                self.matriculaLineEdit_2.setStyleSheet("border-bottom: 2px solid #0080FF")
            else:
                self.matriculaLineEdit_2.setStyleSheet("border-bottom:None")

            if self.kmLineEdit_2.text() == "":
                self.kmLineEdit_2.setStyleSheet("border-bottom: 2px solid #0080FF")
            else:
                self.kmLineEdit_2.setStyleSheet("border-bottom:None")

            if self.matriculaLineEdit_2.text() != "" and self.kmLineEdit_2.text() != "":
                #é feita a actualização da disponibilidade, dos km, e o estado de manutenção de acordo com a
                # matrícula da viatura neste caso se for um carro e a matrícula existir na base dados
                for x in range(len(updateDBCarros())):
                        if matricula in updateDBCarros()[x]:
                                db = "database/DBcarros.db"
                                query = "UPDATE carro SET Disponibilidade = ?, Km = ?, Manutencao = ? where Matricula = ?"

                # o mesmo código repete-se para a DBmotas e DBreservas
                for y in range(len(updateDBMotas())):
                        if matricula in updateDBMotas()[y]:
                                db = "database/DBmotas.db"
                                query = "UPDATE mota SET Disponibilidade = ?, Km = ?, Manutencao = ? where Matricula = ?"

                try:
                        con = sqlite3.connect(db)
                        cursor = con.cursor()
                        cursor.execute(query, info)
                        con.commit()
                        con.close()
                        print("Viatura novamente disponivel")
                except:
                        print("Nao foi possivel disponibilizar novamente a viatura")

    # Slot de ligação do botão do menu lateral 'Legalização' à sua respetiva páginas/camadas stackwidget
    def mostrarLegalizacao(self):
            self.stackedWidget.setCurrentWidget(self.pagLegalizacao)

    #################################################################################################################
    # Slots que fazem a ligação dos botões que se encontram no cabeçalho da 'paginaPrincipal' às suas respectivas
    # paginas (QDialog)

    def ligarStock(self):
            dialog = QDialog()
            ui = pagGestaoStock.Ui_StockDialog()
            ui.setupUi(dialog)
            dialog.exec()

    def ligarLegalizacao(self):
            dialog = QDialog()
            ui = pagLegalizacao.Ui_LegalizacaoDialog()
            ui.setupUi(dialog)
            dialog.exec()

    def ligarManutencao(self):
            dialog = QDialog()
            ui = pagManutencao.Ui_ManutecaoDialog()
            ui.setupUi(dialog)
            dialog.exec()
    ##################################################################################################################

    #Slot para visualizar todos os veículos nas bases de dados DBcarros e DBmotas(fiz duas slots separadas pois tenho
    # dois botões que mostram a informação de cada base de dados de acordo com o tipo da viatura) camada Frota
    def visualizarCarros(self):

            self.tabelaFrota.setRowCount(0)

            for row_number, row_data in enumerate(updateDBCarros()):
                    self.tabelaFrota.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                            self.tabelaFrota.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def visualizarMotas(self):

            self.tabelaFrota.setRowCount(0)

            for row_number, row_data in enumerate(updateDBMotas()):
                    self.tabelaFrota.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                            self.tabelaFrota.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    # Slot que serve para mostrar todos os veículos que estão alugados no dia em que acedemos à aplicação.
    # Camada Renting
    def rentingVeiculos(self):
            #variáveis que vão receber os inputs do utilizador
            mostrarReservas = []
            tabelaFinal = []
            # acesso à base de dados DBreservas.db
            con = sqlite3.connect("database/DBreservas.db")
            cursor = con.cursor()
            cursor.execute("SELECT * FROM reserva")
            valueReservas = cursor.fetchall()
            cursor.close()

            # são extraidas as datas de levantamento e de entrega prevista da viatura no formato string
            for x in range(len(valueReservas)):
                    dataLevantamento = datetime.strptime(str(valueReservas[x][7]), "%Y-%m-%d")
                    dataEntrega = datetime.strptime(str(valueReservas[x][8]), "%Y-%m-%d")
                    # se a data em que estamos aceder à aplicação for maior ou igual a dataLevantamento e igual ou
                    # menor à dataEntrega, então as viaturas que cumprirem com essa condição, são enviadas para a
                    # variável mostrarReservas
                    if today >= dataLevantamento and today <= dataEntrega:
                            mostrarReservas.append(valueReservas[x])
            # Como não é necessário que apareçam todos os elementos que correspondem a cada viatura, são extraídos
            # apenas os que são necessários exibir na tabela informativa
            for x in range(len(mostrarReservas)):
                    listaTemporaria = []
                    listaTemporaria.append(mostrarReservas[x][2])
                    listaTemporaria.append(mostrarReservas[x][4])
                    listaTemporaria.append(mostrarReservas[x][5])
                    listaTemporaria.append(mostrarReservas[x][6])
                    listaTemporaria.append(mostrarReservas[x][3])
                    listaTemporaria.append(mostrarReservas[x][8])

                    tabelaFinal.append(listaTemporaria)
                    # os elementos necessários exibir são enviados para a tabela
                    self.tableWidget.setRowCount(0)

                    for row_number, row_data in enumerate(tabelaFinal):
                            self.tableWidget.insertRow(row_number)
                            for column_number, data in enumerate(row_data):
                                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # Slot que disponibiliza os veículos após a entrega ser feita a partir da camada Renting e que actualiza os km da
    # viatura devolvida
    def updateDevolucao(self):
            # variáveis que vão receber a informação dada pelo utilizador
            matricula = self.matriculaLineEdit.text()
            km = self.kmLineEdit.text()
            # Listas com as variáveis necessarias para localizar os campos que são precisos actualizar dentro da base de
            # dados
            infoDBVeiculos = [1, km, matricula]
            infoDBReservas = [str(today.date()), matricula]
            # variáveis para aceder à base de dados necessária entre a DBcarros e DBmotas
            db = ""
            db2 = ""
            query = ""
            query2 = ""


            # se os campos matricula e km não forem preenchidos irá aparecer uma linha azul nos campos que faltam
            # preencher no momento em que se pressionar o botão submeter, caso os campos estejam preenchidos a linha azul
            # desaparece
            if self.matriculaLineEdit.text() == "":
                    self.matriculaLineEdit.setStyleSheet("border-bottom: 2px solid #0080FF")
            else:
                    self.matriculaLineEdit.setStyleSheet("border-bottom:None")

            if self.kmLineEdit.text() == "":
                    self.kmLineEdit.setStyleSheet("border-bottom: 2px solid #0080FF")
            else:
                    self.kmLineEdit.setStyleSheet("border-bottom:None")

            if self.matriculaLineEdit.text() != "" and self.kmLineEdit.text() != "":
            ##########################################################################################################
            # neste ciclo for x vai precorrer a base de dados carros, e se a matricula que tiver sido inserida pelo
            # utilizador corresponder a alguma matricula dentro desta base de dados, é feito um update à disponibilidade,
            # ficando o carro disponível na base de dados e os km são actualizados. A data de entrega na base de dados
            # DBreservas é também actualizada, desta forma a partir do momento em que a entrega é feita o carro sai da
            # tabela renting
            #########################################################################################################
                for x in range(len(updateDBCarros())):
                    if matricula in updateDBCarros()[x]:
                            db = "database/DBcarros.db"
                            query = "UPDATE carro SET Disponibilidade = ?,Km = ? where Matricula = ?"
                            db2 = "database/DBreservas.db"
                            query2 = "UPDATE reserva SET DataEntrega = ? where Matricula = ?"
            # o mesmo código repete-se para a DBmotas e DBreservas
                for y in range(len(updateDBMotas())):
                    if matricula in updateDBMotas()[y]:
                            db = "database/DBmotas.db"
                            query = "UPDATE mota SET Disponibilidade = ?, Km = ? where Matricula = ?"
                            db2 = "database/DBreservas.db"
                            query2 = "UPDATE reserva SET DataEntrega = ? where Matricula = ?"

            # caso algum dos ciclos for acima seja executado são estabelecidas as conecções com as bases de dados e os
            # updates são efetuados
                try:
                    con = sqlite3.connect(db)
                    cursor = con.cursor()
                    cursor.execute(query, infoDBVeiculos)
                    con.commit()
                    con = sqlite3.connect(db2)
                    cursor = con.cursor()
                    cursor.execute(query2, infoDBReservas)
                    con.commit()
                    con.close()
                    print("Update feito com sucesso")
                except:
                    print("Nao foi possivel fazer update")



    #Slot que mostra todos os veículos que tem de renovar a sua legalização dentro de um prazo de 30 dias pagLegalizacao

    def legalizacaoBotao(self):

            listaCarrosMotas = []
            listaTemporaria = []
            listaTabela = []

            # extracção dos dados contidos nas bases dados DBcarros e DBmotas, unindo todos esses dados numa unica
            # variável listaCarrosMotas
            for x in range(len(updateDBCarros())):
                    listaCarrosMotas.append(updateDBCarros()[x])
            for y in range(len(updateDBMotas())):
                    listaCarrosMotas.append(updateDBMotas()[y])

            # extracção dos dados de todos os veículos que terão de ser legalizados dentro de 30 dias, para uma variável
            # listaTemporaria
            for x in range(len(listaCarrosMotas)):
                    dataAntiga = datetime.strptime(str(listaCarrosMotas[x][8]), "%Y-%m-%d")
                    dataMaisAntiga = dataAntiga + relativedelta(years=1)
                    datafinal = dataMaisAntiga - relativedelta(days=30)

                    if today >= datafinal and today <= dataMaisAntiga:
                            listaTemporaria.append(listaCarrosMotas[x])

            # é feita a extração apenas dos elementos necessários para preencher todos os campos da tabela que está na
            # pagLegalizacao, para dentro de uma variável listaTabela
            for x in range(len(listaTemporaria)):
                    listaLinhas = []
                    listaLinhas.append(listaTemporaria[x][0])
                    listaLinhas.append(listaTemporaria[x][1])
                    listaLinhas.append(listaTemporaria[x][2])
                    listaLinhas.append(listaTemporaria[x][3])
                    listaLinhas.append(listaTemporaria[x][5])
                    listaLinhas.append(listaTemporaria[x][6])
                    listaLinhas.append(listaTemporaria[x][8])
                    listaLinhas.append(listaTemporaria[x][9])

                    listaTabela.append(listaLinhas)

            # Aqui é enviada toda a informação da listaTabela para a tableWidget_3 (tabela da pagLegalização)
            self.tableWidget_3.setRowCount(0)

            for row_number, row_data in enumerate(listaTabela):
                    self.tableWidget_3.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                            self.tableWidget_3.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    # Slot que disponibiliza o veiculo legalizado e data dessa legalização actualiza na base de dados do veículo
    # camadaLegalização

    def upDateVeiculosLegais(self):

            matricula = self.matriculaLineEdit_3.text()
            km = self.kmLineEdit_3.text()
            data = self.dataLegalizacao.date().toString("yyyy-MM-dd")

            info = [km, data, matricula]
            db = ""
            query = ""

            # se os campos matricula e km não forem preenchidos irá aparecer uma linha azul nos campos que faltam
            # preencher no momento em que se pressionar o botão submeter, caso os campos estejam preenchidos a linha azul
            # desaparece
            if self.matriculaLineEdit_3.text() == "":
                    self.matriculaLineEdit_3.setStyleSheet("border-bottom: 2px solid #0080FF")
            else:
                    self.matriculaLineEdit_3.setStyleSheet("border-bottom:None")

            if self.kmLineEdit_3.text() == "":
                    self.kmLineEdit_3.setStyleSheet("border-bottom: 2px solid #0080FF")
            else:
                    self.kmLineEdit_3.setStyleSheet("border-bottom:None")

            # se os campos matricula e km forem preenchidos pelo utilizador então é feita uma consulta à base de
            # dados das viaturas e se ela existir dentro da base de dados correspondente, estes serão actualizados,
            # ficando assim a viatura disponivel novamente
            if self.matriculaLineEdit_3.text() != "" and self.kmLineEdit_3.text() != "":

                for x in range(len(updateDBCarros())):
                    if matricula in updateDBCarros()[x]:
                            db = "database/DBcarros.db"
                            query = "UPDATE carro SET Km = ?, UltimaLegalizacao = ? where Matricula = ?"

                for y in range(len(updateDBMotas())):
                    if matricula in updateDBMotas()[y]:
                            db = "database/DBmotas.db"
                            query = "UPDATE mota SET Km = ?, UltimaLegalizacao = ? where Matricula = ?"

                try:
                    con = sqlite3.connect(db)
                    cursor = con.cursor()
                    cursor.execute(query, info)
                    con.commit()
                    con.close()
                    print("Update feito com sucesso")
                except:
                    print("Nao foi possivel fazer update")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.marcaLabel.setText(_translate("MainWindow", "Luxury Wheels"))
        self.manutencaoHeaderBtn.setText(_translate("MainWindow", "Manutenção"))
        self.legalizacaoHeaderBtn.setText(_translate("MainWindow", "Legalização"))
        self.stockHeaderBtn.setText(_translate("MainWindow", "Gestão Stock"))
        self.resumoBtn.setText(_translate("MainWindow", "Resumo Mensal"))
        self.frotaBtn.setText(_translate("MainWindow", "A Minha Frota"))
        self.rentingBtn.setText(_translate("MainWindow", "Renting"))
        self.manutencaoBtn.setText(_translate("MainWindow", "Manutenção"))
        self.legalizacaoBtn.setText(_translate("MainWindow", "Legalização"))
        item = self.tabelaFrota.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id Veiculo"))
        item = self.tabelaFrota.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Categoria"))
        item = self.tabelaFrota.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Marca"))
        item = self.tabelaFrota.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Modelo"))
        item = self.tabelaFrota.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Disponivel"))
        item = self.tabelaFrota.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Matrícula"))
        item = self.tabelaFrota.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Km"))
        item = self.tabelaFrota.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Última Revisão"))
        item = self.tabelaFrota.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Legalização €"))
        item = self.tabelaFrota.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Preço Dia"))
        self.frotaCarrosBtn.setText(_translate("MainWindow", "Carros"))
        self.frotaMotasBtn.setText(_translate("MainWindow", "Motas"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id Veiculo"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Categoria"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Marca"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Modelo"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Matricula"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Data Devolução"))
        self.tituloLabel.setText(_translate("MainWindow", "Devolução da viatura"))
        self.matriculaLineEdit.setPlaceholderText(_translate("MainWindow", "Matricula"))
        self.kmLineEdit.setPlaceholderText(_translate("MainWindow", "Km"))
        self.submeterBtn.setText(_translate("MainWindow", "Submeter"))
        self.tituloLabel_2.setText(_translate("MainWindow", "Fim de Manutenção"))
        self.matriculaLineEdit_2.setPlaceholderText(_translate("MainWindow", "Matricula"))
        self.kmLineEdit_2.setPlaceholderText(_translate("MainWindow", "Km"))
        self.submeterBtn_2.setText(_translate("MainWindow", "Submeter"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id Veiculo"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Categoria"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Marca"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Modelo"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Matricula"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Fim Manutenção"))
        self.tituloLabel_3.setText(_translate("MainWindow", "Legalização da Viatura"))
        self.matriculaLineEdit_3.setPlaceholderText(_translate("MainWindow", "Matricula"))
        self.kmLineEdit_3.setPlaceholderText(_translate("MainWindow", "Km"))
        self.submeterBtn_3.setText(_translate("MainWindow", "Submeter"))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Id Veiculo"))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Categoria"))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Marca"))
        item = self.tableWidget_3.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Modelo"))
        item = self.tableWidget_3.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Matricula"))
        item = self.tableWidget_3.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Km"))
        item = self.tableWidget_3.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Última Legalização"))
        item = self.tableWidget_3.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Preço Legalização"))

