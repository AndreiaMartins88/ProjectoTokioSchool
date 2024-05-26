from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt6.QtWidgets import QTableWidgetItem
import paginaPrincipal
from datetime import datetime, timedelta

#Variáveis globais
today = datetime.now()
# esta é usada no método def enviarParaManutencao(self):
listaTabela1 = []

#Funções globais que vão ser necessarias utilizar em mais do que uma slot(método)

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

#Acesso à base de dados DBmotas.db e extração dos seus dados.
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

#####################################################################################################################
# Esta página tem três propositos 1º servir de alerta caso existam veículos com necessidade de entrar em manutenção
# (se existir veiculos para entrar em manutenção será exibido de cor diferente na paginaPrincipal da aplicação o botão
# no cabeçalho Manutenção com as letras a azul em vez de branco). 2º são exibidos os veículos numa tabela dentro desta
# página manutenção (QDialog), e 3º poderá colocar qualquer veículo para manutenção assim que desejar, esse veiculo
# fica indisponivel na base de dados, o que o vai tornar indisponivel para arrendamento durante o periodo que este
# estiver em manutenção.
#####################################################################################################################

#####################################################################################################################
# Classe principal do widget/pagina QDialog nesta classe estão todos os widgets e elementos do styleSheet que dão à
# página o seu aspecto visua. Está dividida em duas partes principais o header(cabeçalho) e o body(corpo) da
# aplicação, este, por sua vez, está dividido em duas partes principais, o lado esquerdo exibe uma tabela com as
# viaturas que necessitam de ser intervencionadas, e o lado direito onde podemos submeter as viaturas para
# manutenção, e desta forma ficam sem poder ser alugadas pelos clientes no site.
#####################################################################################################################
class Ui_ManutecaoDialog(object):
    def setupUi(self, ManutecaoDialog):
        ManutecaoDialog.setObjectName("ManutecaoDialog")
        ManutecaoDialog.resize(1109, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ManutecaoDialog.sizePolicy().hasHeightForWidth())
        ManutecaoDialog.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        ManutecaoDialog.setFont(font)
        ManutecaoDialog.setStyleSheet("*{\n"
"    border:none;\n"
"    background: transparent;\n"
"    background-color: transparent;\n"
"    padding: 0;\n"
"    color: #FFF;\n"
"}\n"
"#Dialog, #mainBody, #idLineEdit, #marcaLineEdit,#modeloLineEdit, #matriculaLineEdit, #kmLineEdit, #manutencaoSubBtn{\n"
"    background-color: #1f2329;\n"
"}\n"
"#header, #body{\n"
"    background-color: #27263c;\n"
"}\n"
"#manutencaoLabel{\n"
"    padding-right: 7px;\n"
"}\n"
"#LuxuryLabel{\n"
"    padding-left:7px;\n"
"}\n"
"\n"
"#mainBody{\n"
"    border-radius:12px;\n"
"}\n"
"\n"
"#manutencaoSubBtn{\n"
"    border-radius: 12px;\n"
"    border: 2px solid #0080FF\n"
"}\n"
"#textBrowser{\n"
"    margin-top:70px\n"
"}")
        #############################################################################################################
        # Cabeçalho do Widget/pagina, o cabeçalho é composto pelo nome da empresa no lado esquerdo usando para o
        # efeito um QLabel e no lado direito utilizando também um QLabel, consta a identificação da pagina neste
        # caso Manutenção, são também utilizados outros widgets que não são visiveis no produto final mas
        # necessários para atingir a estetica pretendida como os QSize para defenir as dimensões do cabeçalho,
        # layouts(QVBoxLayout ou QHBoxLayout), os frames(QFrame), os QFont(para escolher o tipo de fonte e tamanho
        # das letras que pretendemos utilizar.
        #############################################################################################################
        self.header = QtWidgets.QWidget(parent=ManutecaoDialog)
        self.header.setGeometry(QtCore.QRect(0, 0, 1111, 61))
        self.header.setObjectName("header")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.LuxuryLabel = QtWidgets.QLabel(parent=self.header)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        self.LuxuryLabel.setFont(font)
        self.LuxuryLabel.setObjectName("LuxuryLabel")
        self.horizontalLayout.addWidget(self.LuxuryLabel)
        self.manutencaoLabel = QtWidgets.QLabel(parent=self.header)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.manutencaoLabel.setFont(font)
        self.manutencaoLabel.setObjectName("manutencaoLabel")
        self.horizontalLayout.addWidget(self.manutencaoLabel, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        ##############################################################################################################
        #Body inicia aqui com o uso de diferentes widgets com destaque particular para o QTableWidget, utilizado para
        # fazer a tabela que vai receber os dados dos veiculos para manutenção, assim como QLineEdit,
        # que ao contrário da QLabel, aqui serve para receber os inputs do cliente onde o utilizador pode selecionar o
        # veículo que pretende enviar para manutenção, colocando assim o veículo indisponível alugar. Temos também
        # ainda o QButton, este widget é utilizado para submeter o input dado pelo utilizador.
        # Existem ainda outros widgets já referidos anteriormente, e que são necessários para compôr o restante
        # ambiente gráfico
        ##############################################################################################################
        self.body = QtWidgets.QWidget(parent=ManutecaoDialog)
        self.body.setGeometry(QtCore.QRect(0, 70, 1109, 531))
        self.body.setMinimumSize(QtCore.QSize(1109, 0))
        self.body.setObjectName("body")
        self.mainBody = QtWidgets.QWidget(parent=self.body)
        self.mainBody.setGeometry(QtCore.QRect(19, 19, 781, 491))
        self.mainBody.setObjectName("mainBody")
        self.tituloLabel = QtWidgets.QLabel(parent=self.mainBody)
        self.tituloLabel.setGeometry(QtCore.QRect(280, 10, 241, 16))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.tituloLabel.setFont(font)
        self.tituloLabel.setObjectName("tituloLabel")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.mainBody)
        self.tableWidget.setGeometry(QtCore.QRect(10, 40, 761, 441))
        self.tableWidget.setStyleSheet("color: #0080FF")
        self.tableWidget.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
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
        self.tableWidget.horizontalHeader().setDefaultSectionSize(150)
        self.frame = QtWidgets.QFrame(parent=self.body)
        self.frame.setGeometry(QtCore.QRect(820, 20, 271, 481))
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(47)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(17)
        font.setBold(True)
        self.textBrowser.setFont(font)
        self.textBrowser.setLineWrapColumnOrWidth(0)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.matriculaLineEdit = QtWidgets.QLineEdit(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.matriculaLineEdit.setFont(font)
        self.matriculaLineEdit.setReadOnly(False)
        self.matriculaLineEdit.setObjectName("matriculaLineEdit")
        self.verticalLayout.addWidget(self.matriculaLineEdit)
        self.kmLineEdit = QtWidgets.QLineEdit(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.kmLineEdit.setFont(font)
        self.kmLineEdit.setObjectName("kmLineEdit")
        self.verticalLayout.addWidget(self.kmLineEdit)
        self.manutencaoSubBtn = QtWidgets.QPushButton(parent=self.frame)
        self.manutencaoSubBtn.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(11)
        font.setBold(True)
        self.manutencaoSubBtn.setFont(font)
        self.manutencaoSubBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.manutencaoSubBtn.setObjectName("manutencaoSubBtn")
        ##############################################################################################################
        # Signal que vai enviar os veículos que quero que sejam colocados em manuteção(na pagina principal menu
        # lateral esquerdo) e os km do campo ultimaRevisao serão actualizados na base de dados DBcarros ou DBmotas
        # mediante o veículo selecionado.
        ##############################################################################################################
        self.manutencaoSubBtn.clicked.connect(self.enviarParaManutencao)
        self.verticalLayout.addWidget(self.manutencaoSubBtn)

        self.retranslateUi(ManutecaoDialog)
        QtCore.QMetaObject.connectSlotsByName(ManutecaoDialog)

        ##############################################################################################################
        # Como eu pretendia que nesta secção de veículos para manutenção constassem na mesma tabela os veiculos carros e
        # motas criei uma variável que junta-se os dados de ambas as bases de dados em forma de lista. Da variável
        # 'listaVeiculos' vão ser extraídos os km actuais da viatura para a variável 'kmActuais' e a última revisão(
        # os km que tinha na última revisão feita a viatura) para a variável 'ultimaRevisao'. Após ter estes dados
        # nestas duas variáveis, é feita uma condição em que se os km actuais da viatura, forem maiores ou iguais aos
        # kilometros que a viatura tinha quando fez a última revisão mais 5000, então, está na altura de se fazer uma
        # nova revisão. (Aqui coloquei como espaçamento entre revisões cinco mil kilometros, daí os + 5000). se a
        # condição for cumprida é feito um append à variavel 'listaLinhas' dos elementos que quero que apareçam na
        # tabela à cerca daquela viatura, uma vez que não é necessária toda a informação que está dentro da base de
        # dados sobre a viatura. A variável 'listaTabela' vai receber todos os dados relativos às viaturas que estão
        # para manutenção e utilizando um ciclo for envia-se esses dados para dentro da tabela (tableWidget).
        ##############################################################################################################
        listaVeiculos = updateDBCarros() + updateDBMotas()
        listaTabela = []
        for x in range(len(listaVeiculos)):
            kmActuais = int(listaVeiculos[x][6])
            ultimaRevisao = int(listaVeiculos[x][7])

            if kmActuais >= (ultimaRevisao + 5000):
                listaLinhas = []
                listaLinhas.append(listaVeiculos[x][0])
                listaLinhas.append(listaVeiculos[x][2])
                listaLinhas.append(listaVeiculos[x][3])
                listaLinhas.append(listaVeiculos[x][5])
                listaLinhas.append(listaVeiculos[x][7])

                listaTabela.append(listaLinhas)

        self.tableWidget.setRowCount(0)

        for row_number, row_data in enumerate(listaTabela):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    ##################################################################################################################
    # Slot/ método que vai enviar os veículos para a página principal no separador manutenção, (quando os veículos são
    # enviados através dete método para a manutenção ficam de forma efectiva sem possibilidade de ser
    # arrendados), é o utilizador que decide quando o veículo entra em manutenção, sempre que recebe o alerta para a
    # cumprir com essa necessidade pode decidir a altura certa para submeter o veículo para manutenção. Desde que a
    # matrícula exista na base de dados, o veículo pode ser colocado emmanutenção, por exemplo, se houver um sinistro
    # com a viatura ela pode ser colocada em reparação por esta via. No entanto, a intenção primária é que seja
    # utilizado para as manutenções periódicas de cada viatura.
    ##################################################################################################################
    def enviarParaManutencao(self):
        #variáveis que vão receber os valores inseridos pelo utilizador
        matricula = self.matriculaLineEdit.text().upper()
        km = self.kmLineEdit.text()
        #variável que recebe a data do dia em que é inserido o veículo mais 30 dias para que este fique indisponível
        # até um maximo de 30 dias
        novadata = today.date() + timedelta(days=30)
        #variável que recebe os dados que são necessários fazer um update nas bases de dados dos carros ou das motas
        info = [0,km,1,novadata.strftime("%Y-%m-%d"),matricula]

        # condicionais em que se os campos, 'matricula' e/ou 'km' estiver vazio e tentarem submeter a viatura para
        # manutenção, aparecerá uma linha de cor a azul a indicar que falta preencher o campo para puder submeter o
        # veiculo.
        if self.matriculaLineEdit.text() == "":
            self.matriculaLineEdit.setStyleSheet("border-bottom: 2px solid #0080FF")
        else:
            self.matriculaLineEdit.setStyleSheet("border-bottom:None")

        if self.kmLineEdit.text() == "":
            self.kmLineEdit.setStyleSheet("border-bottom: 2px solid #0080FF")
        else:
            self.kmLineEdit.setStyleSheet("border-bottom:None")

        # Se ambos os campos estiverem preenchidos então é feito o update dos dados na base de dados a que
        # corresponde a viatura
        if  self.matriculaLineEdit.text() != "" and self.kmLineEdit.text() != "":
            db = ""
            query = ""
            #actualizar matricula na base de dados necessária
            for x in range(len(updateDBCarros())):
                if matricula in updateDBCarros()[x]:
                    db = "database/DBcarros.db"
                    query = "UPDATE carro SET Disponibilidade = ?,UltimaRevisao = ?,Manutencao = ?, ManutencaoAte = ? " \
                            "where Matricula = ?"

            for y in range(len(updateDBMotas())):
                if matricula in updateDBMotas()[y]:
                    db = "database/DBmotas.db"
                    query = "UPDATE mota SET Disponibilidade = ?, UltimaRevisao = ?,Manutencao = ?, ManutencaoAte = ? " \
                            "where Matricula = ?"
            try:
                con = sqlite3.connect(db)
                cursor = con.cursor()
                cursor.execute(query, info)
                con.commit()
                con.close()
                print("Veiculo actualizado com sucesso")
            except:
                print("Veiculo actualizado sem sucesso")

        ###############################################################################################################
        # Esta parte de código serve para reunir a informação das viaturas que foram enviadas para manutençao pelo
        # utilizador da aplicação. Para puder enviar esses dados para o separador Manutenção da paginaPrincipal.
            #variável que junta os valores extraídos de ambas as bases de dados
            valueVeiculos= updateDBCarros() + updateDBMotas()
            # extração da informação necessária para enviar para a tabela do separador Manutenção da páginaPrincipal
            for x in range(len(valueVeiculos)):
                if matricula in valueVeiculos[x]:
                    listaLinhas1 = []
                    listaLinhas1.append(valueVeiculos[x][0])
                    listaLinhas1.append(valueVeiculos[x][1])
                    listaLinhas1.append(valueVeiculos[x][2])
                    listaLinhas1.append(valueVeiculos[x][3])
                    listaLinhas1.append(valueVeiculos[x][5])
                    listaLinhas1.append(valueVeiculos[x][11])
                    break

            # listaTabela1 vai receber os dados que serão necessários para preencher a tabela que se encontra no
            # separador Manutenção da paginaPrincipal
            listaTabela1.append(listaLinhas1)
            # Variável de controlo, que será usada para confirmar se existem veiculos para colocar na tabela referida
            # anteriormente
            paginaPrincipal.enviarParaManutencao = True
            #os dados serão passados para uma variavel do tipo lista que será inicializada vazia na paginaPrincipal,
            # se houver veiculos para manutencão efectiva esta variável receberá os dados a que estão na listaTabela1
            paginaPrincipal.receberListaTabela = listaTabela1


    def retranslateUi(self, ManutecaoDialog):
        _translate = QtCore.QCoreApplication.translate
        ManutecaoDialog.setWindowTitle(_translate("ManutecaoDialog", "Manutenção"))
        self.LuxuryLabel.setText(_translate("ManutecaoDialog", "Luxury Wheels"))
        self.manutencaoLabel.setText(_translate("ManutecaoDialog", "Manutenção"))
        self.tituloLabel.setText(_translate("ManutecaoDialog", "Veiculos a necessitar de Manutenção"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ManutecaoDialog", "Id Veiculo"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ManutecaoDialog", "Marca"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ManutecaoDialog", "Modelo"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("ManutecaoDialog", "Matrícula"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("ManutecaoDialog", "Última Revisão"))
        self.textBrowser.setHtml(_translate("ManutecaoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:17pt; font-weight:700; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt;\">Ao submeter uma viatura para manutenção, esta ficará indisponivel pelo um  período mínimo de 30 dias.</span></p></body></html>"))
        self.matriculaLineEdit.setPlaceholderText(_translate("ManutecaoDialog", "Matrícula"))
        self.kmLineEdit.setPlaceholderText(_translate("ManutecaoDialog", "Km"))
        self.manutencaoSubBtn.setText(_translate("ManutecaoDialog", "Submeter"))

