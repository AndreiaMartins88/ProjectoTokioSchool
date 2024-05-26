from PyQt6 import QtCore, QtGui, QtWidgets
import sqlite3

#####################################################################################################################
# Esta página tem 2 propósitos, um emitir um alerta de que existe falta de veículos de acordo com o número de
# clientes, e é também a página onde o utilizador pode adicionar novas viaturas às bases de dados, para aumentar
# desta forma o stock e ter mais oferta de produto ao cliente final.
#####################################################################################################################

# variável global para verificar a necessidade de adquirir novos veiculos iniciada a False
verificacaoVeiculosNovos = False

#####################################################################################################################
# Classe principal do widget/pagina, 'pagGestão' (QDialog) nesta classe estão todos os widgets e elementos do styleSheet
# que dão à página o seu aspecto visua. Está dividida em duas partes principais o header(cabeçalho) e o body(corpo) da
# # aplicação, este, por sua vez, está dividido em duas partes principais, uma que é a do lado esquerdo consta a
# informação do número de veículos que deverão ser adquiridos, de acordo com o número de clientes da empresa. Do lado
# Direito está a área para adicionar veículos novos e adquiridos para o aumento da oferta aos clientes.
######################################################################################################################
class Ui_StockDialog(object):

    def setupUi(self, StockDialog):
        StockDialog.setObjectName("StockDialog")
        StockDialog.resize(1109, 600)
        StockDialog.setStyleSheet("*{\n"
"    border: none;\n"
"    background: transparent;\n"
"    background-color: transparent;\n"
"    padding: 0;\n"
"    color: #FFF;\n"
"}\n"
"#StockDialog, #alertaStock, #novaViatura{\n"
"    background-color: #1f2329;\n"
"}\n"
"#header,#body{\n"
"    background-color: #27263c;\n"
"}\n"
"#alertaStock, #novaViatura{\n"
"    border-radius:12px;\n"
"    margin-top: 7px;\n"
"    margin-bottom:7px;\n"
"}\n"
"#alertaStock{\n"
"    border: 2px solid #0080FF;\n"
"}\n"
"#subViaturaBtn{\n"
"    background-color: #27263c;\n"
"    border-radius:12px;\n"
"    border: 2px solid #0080FF;\n"
"}\n"
"#numeroViaturasLabel{\n"
"color:#0080FF;\n"
"}")
        # Header(cabeçalho) da página composto por dois QLabel onde consta o nome da empresa e outro onde consta o
        # título da página 'Gestão Stock'. É composto por outros widgets que definem a estetica do cabeçalho
        self.header = QtWidgets.QWidget(parent=StockDialog)
        self.header.setGeometry(QtCore.QRect(-1, -4, 1111, 59))
        self.header.setObjectName("header")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.header)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(parent=self.header)
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelLuxuryWheels = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        self.labelLuxuryWheels.setFont(font)
        self.labelLuxuryWheels.setObjectName("labelLuxuryWheels")
        self.verticalLayout_2.addWidget(self.labelLuxuryWheels, 0, QtCore.Qt.AlignmentFlag.AlignBottom)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(parent=self.header)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelGestaoStock = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.labelGestaoStock.setFont(font)
        self.labelGestaoStock.setObjectName("labelGestaoStock")
        self.verticalLayout.addWidget(self.labelGestaoStock, 0, QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignBottom)
        self.horizontalLayout.addWidget(self.frame_2)
        # Body da página, composta essencialmente por QTextBrowser, QLabel, QLineEdit e QPushButton, tem ainda outros
        # widgets que servem para posicionar estes principais e harmonizar os elementos estéticos
        self.body = QtWidgets.QWidget(parent=StockDialog)
        self.body.setGeometry(QtCore.QRect(-1, 70, 1111, 531))
        self.body.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.body.setObjectName("body")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.body)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.alertaStock = QtWidgets.QWidget(parent=self.body)
        self.alertaStock.setMinimumSize(QtCore.QSize(200, 0))
        self.alertaStock.setMaximumSize(QtCore.QSize(300, 16777215))
        self.alertaStock.setSizeIncrement(QtCore.QSize(0, 0))
        self.alertaStock.setObjectName("alertaStock")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.alertaStock)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_3 = QtWidgets.QFrame(parent=self.alertaStock)
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 200))
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.frame_3)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_5.addWidget(self.textBrowser)
        self.verticalLayout_3.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(parent=self.alertaStock)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.numeroViaturasLabel = QtWidgets.QLabel(parent=self.frame_4)
        self.numeroViaturasLabel.setGeometry(QtCore.QRect(90, 50, 101, 131))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(120)
        font.setBold(True)
        self.numeroViaturasLabel.setFont(font)
        self.numeroViaturasLabel.setText("")
        self.numeroViaturasLabel.setObjectName("numeroViaturasLabel")
        self.verticalLayout_3.addWidget(self.frame_4)
        self.horizontalLayout_2.addWidget(self.alertaStock)
        self.novaViatura = QtWidgets.QWidget(parent=self.body)
        self.novaViatura.setMaximumSize(QtCore.QSize(750, 16777215))
        self.novaViatura.setObjectName("novaViatura")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.novaViatura)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_5 = QtWidgets.QFrame(parent=self.novaViatura)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 30))
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.label_3 = QtWidgets.QLabel(parent=self.frame_5)
        self.label_3.setGeometry(QtCore.QRect(270, 10, 161, 21))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(False)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_6.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(parent=self.novaViatura)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.layoutWidget = QtWidgets.QWidget(parent=self.frame_6)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 0, 303, 452))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_7.setContentsMargins(0, 0, 115, 7)
        self.verticalLayout_7.setSpacing(12)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.labelTipoViatura = QtWidgets.QLabel(parent=self.layoutWidget)
        self.labelTipoViatura.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.labelTipoViatura.setFont(font)
        self.labelTipoViatura.setObjectName("labelTipoViatura")
        self.verticalLayout_7.addWidget(self.labelTipoViatura)
        self.comboBoxVeiculo = QtWidgets.QComboBox(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.comboBoxVeiculo.setFont(font)
        self.comboBoxVeiculo.setObjectName("comboBoxVeiculo")
        self.comboBoxVeiculo.addItem("")
        self.comboBoxVeiculo.addItem("")
        self.verticalLayout_7.addWidget(self.comboBoxVeiculo)
        self.lineEditID = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.lineEditID.setFont(font)
        self.lineEditID.setObjectName("lineEditID")
        self.verticalLayout_7.addWidget(self.lineEditID)
        self.labelTipoCategoria = QtWidgets.QLabel(parent=self.layoutWidget)
        self.labelTipoCategoria.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.labelTipoCategoria.setFont(font)
        self.labelTipoCategoria.setObjectName("labelTipoCategoria")
        self.verticalLayout_7.addWidget(self.labelTipoCategoria)
        self.comboBoxCategoria = QtWidgets.QComboBox(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.comboBoxCategoria.setFont(font)
        self.comboBoxCategoria.setObjectName("comboBoxCategoria")
        self.comboBoxCategoria.addItem("")
        self.comboBoxCategoria.addItem("")
        self.comboBoxCategoria.addItem("")
        self.verticalLayout_7.addWidget(self.comboBoxCategoria)
        self.lineEditMarca = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.lineEditMarca.setFont(font)
        self.lineEditMarca.setObjectName("lineEditMarca")
        self.verticalLayout_7.addWidget(self.lineEditMarca)
        self.lineEditModelo = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.lineEditModelo.setFont(font)
        self.lineEditModelo.setObjectName("lineEditModelo")
        self.verticalLayout_7.addWidget(self.lineEditModelo)
        self.lineEditMatricula = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.lineEditMatricula.setFont(font)
        self.lineEditMatricula.setObjectName("lineEditMatricula")
        self.verticalLayout_7.addWidget(self.lineEditMatricula)
        self.lineEditKm = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.lineEditKm.setFont(font)
        self.lineEditKm.setObjectName("lineEditKm")
        self.verticalLayout_7.addWidget(self.lineEditKm)
        self.labelDataLegalizacao = QtWidgets.QLabel(parent=self.layoutWidget)
        self.labelDataLegalizacao.setMaximumSize(QtCore.QSize(150, 20))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.labelDataLegalizacao.setFont(font)
        self.labelDataLegalizacao.setObjectName("labelDataLegalizacao")
        self.verticalLayout_7.addWidget(self.labelDataLegalizacao)
        self.dateEditLegalizao = QtWidgets.QDateEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.dateEditLegalizao.setFont(font)
        self.dateEditLegalizao.setObjectName("dateEditLegalizao")
        self.verticalLayout_7.addWidget(self.dateEditLegalizao)
        self.lineEditPrecoLegalizacao = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.lineEditPrecoLegalizacao.setFont(font)
        self.lineEditPrecoLegalizacao.setObjectName("lineEditPrecoLegalizacao")
        self.verticalLayout_7.addWidget(self.lineEditPrecoLegalizacao)
        self.lineEditPrecoDia = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setBold(True)
        self.lineEditPrecoDia.setFont(font)
        self.lineEditPrecoDia.setText("")
        self.lineEditPrecoDia.setObjectName("lineEditPrecoDia")
        self.verticalLayout_7.addWidget(self.lineEditPrecoDia)
        self.subViaturaBtn = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.subViaturaBtn.setMinimumSize(QtCore.QSize(150, 30))
        self.subViaturaBtn.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(10)
        font.setBold(True)
        self.subViaturaBtn.setFont(font)
        self.subViaturaBtn.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.subViaturaBtn.setObjectName("subViaturaBtn")

        # Signal que o botão recebe da Slot receberInfoVeiculos
        self.subViaturaBtn.clicked.connect(self.receberInfoVeiculos)

        self.verticalLayout_7.addWidget(self.subViaturaBtn)
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_6)
        self.frame_7.setGeometry(QtCore.QRect(360, 10, 351, 431))
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.textBrowserInformativo = QtWidgets.QTextBrowser(parent=self.frame_7)
        self.textBrowserInformativo.setGeometry(QtCore.QRect(30, 120, 256, 192))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.textBrowserInformativo.setFont(font)
        self.textBrowserInformativo.setStyleSheet("color:#ffaa00")
        self.textBrowserInformativo.setObjectName("textBrowserInformativo")
        self.verticalLayout_6.addWidget(self.frame_6)
        self.horizontalLayout_2.addWidget(self.novaViatura)

        self.retranslateUi(StockDialog)
        QtCore.QMetaObject.connectSlotsByName(StockDialog)

        # Se o número de veículos for insuficiente, aparece o número 5 como recomendação de nova aquisição de
        # veículos caso contrario aparece o número 0.
        if verificacaoVeiculosNovos == True:
                self.numeroViaturasLabel.setText("5")
        else:
                self.numeroViaturasLabel.setText("0")

    # Slot para inserir novos veiculos nas bases de dados DBcarros e DBmotas
    def receberInfoVeiculos(self):
            #########################################################################################################
            #Por uma questão de segurança extra e porque por vezes as pessoas se esquecem de preencher alguns campos
            # no momento de inserir dados num formulário, coloquei uma variável do tipo lista que tem uma mensagem de
            # acordo com cada um dos campos que tem de ser preenchidos, caso seja esquecido algum campo ou a pessoa
            # que estiver a inserir a viatura não quiser fornecer toda a informação essencial para o registo da nova
            # viatura na base de dados, esta não será acrescentada à base de dados assim como surgirá um alerta para
            # identificar qual o campo que ficou por preencher.
            ########################################################################################################
            prioridades = [[False, "Campo de ID Veiculo Vazio"],
                           [False, "Campo de marca vazio"],
                           [False, "Campo modelo vazio"],
                           [False, "Campo de matricula vazio"],
                           [False, "Campo Km Vazio"],
                           [False, "Campo Preço Legalização Vazio"],
                           [False, "Campo Preço Dia Vazio"]]

            #########################################################################################################
            # variável que vai ser usada para fazer o insert da informação nas bases de dados dos carros e das motas,
            # cada uma destas base de dados é composta por 13 colunas, e como no momento em que uma viatura é nova é
            # adicionada, algumas dessas colunas os valores que deveriam receber será sempre igual por isso é
            # colocado de forma "forçada". Desta forma não ocorrerá um erro e os dados ficarão todos preenchidos nas
            # colunas certas com a informação certa.
            #########################################################################################################
            dados = [0] * 13

            # Variável para fazer a verificação se o texto passado pelo o utilizador é numerico, ela é iniciada a True
            verificacao = True

            # QTextBrowser, é o widget que irá mostrar no outuput uma frase de aviso caso os campos abaixo sejam mal
            # preenchidos ou esquecidos de preencher
            self.textBrowserInformativo.setText("")

            # QComboBox, para escolher qual o tipo de veiculo que vai ser introduzido na base de dados, este campo é
            # importante para definir qual a base de dados que vai ser necessária aceder
            veiculo = self.comboBoxVeiculo.currentText()

            # QLineEdit serve para receber os inputs dados pelo utilizador, neste caso, refere-se ao ID do novo
            # veículo que vai ser inserido na base de dados. É utilizado um if para verificar se o campo não está vazio,
            # se este não se encontrar vazio, então a variável dados[0] vai receber os dados que são inseridos pelo
            # utilizador no terminal. Caso o campo não seja preenchido então surgiram um aviso no ecrã para o
            # utilizador através do textBrowserInformativo a dizer que o campo não está preenchido ("Campo de ID
            # Veiculo Vazio"). Utilizei o mesmo processo para os restantes lineEdits, com a excessão daqueles em que
            # necessitava de garantir que iriam receber valores numéricos.
            if self.lineEditID.text() == "":
                    prioridades[0][0] = True
            else:
                    dados[0] = self.lineEditID.text()

            # QComboBox, para escolher qual o tipo de categoria a que o veículo pertence.
            dados[1] = self.comboBoxCategoria.currentText()

            if self.lineEditMarca.text() == "":
                    prioridades[1][0] = True
            else:
                    dados[2] = self.lineEditMarca.text()

            if self.lineEditModelo.text() == "":
                    prioridades[2][0] = True
            else:
                    dados[3] = self.lineEditModelo.text()

            # Aqui está uma das colunas que necessita receber a informação, mas que não é pedida ao utilizador,
            # mas é-lhe fornecida por mim
            dados[4] = 1

            if self.lineEditMatricula.text() == "":
                    prioridades[3][0] = True
            else:
                    dados[5] = self.lineEditMatricula.text()

            ###########################################################################################################
            # No caso dos parametros que necessitava que recebessem valores numericos, tem de ser feitas duas verificações,
            # primeira se o campo foi preenchido, segunda se o valor que foi inserido é númerico.Se os dados não forem
            # numericos o output será uma mensagem de aviso que tem de ser inseridos números, caso o campo esteja vazio a
            # mensagem é a de que o campo está vazio, o mesmo processo foi utilizado nos restantes inputs desta função.
            ###########################################################################################################
            if self.lineEditKm.text() == "":
                    prioridades[4][0] = True
            elif self.lineEditKm.text() != "":
                    try:
                            dados[6] = float(self.lineEditKm.text())
                    except:
                            self.textBrowserInformativo.setText("Campo dos Km tem de ser numerico")
                            verificacao = False

            dados[7] = 0

            dados[8] = self.dateEditLegalizao.date().toString("yyyy-MM-dd")

            if self.lineEditPrecoLegalizacao.text() == "":
                    prioridades[5][0] = True
            elif self.lineEditPrecoLegalizacao.text() != "":
                    try:
                            dados[9] = float(self.lineEditPrecoLegalizacao.text())
                    except:
                            self.textBrowserInformativo.setText(
                                    "Os Dados inseridos no campo preço legalização estão incorretos, utilize apenas números")
                            verificacao = False

            dados[10] = 0
            dados[11] = 0

            if self.lineEditPrecoDia.text() == "":
                    prioridades[6][0] = True
            elif self.lineEditPrecoDia.text() != "":
                    try:
                            dados[12] = float(self.lineEditPrecoDia.text())
                    except:
                            self.textBrowserInformativo.setText(
                                    "Os Dados inseridos no campo Preço Dia estão incorretos, utilize apenas números")
                            verificacao = False

            if verificacao == True:
                    for x in range(len(prioridades)):
                            if prioridades[x][0] == True:
                                    self.textBrowserInformativo.setText(prioridades[x][1])
                                    break
            # De acordo com o veiculo selecionado na comboBoxVeiculo os dados recolhidos serão inceridos na base de
            # dados correspondente.

            if veiculo == "Carro":
                    db = "database/DBcarros.db"
                    query = "INSERT INTO carro VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"

            else:
                    db = "database/DBmotas.db"
                    query = "INSERT INTO carro VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)"

            # É feito um try and except como forma de ter uma segurança extra no comportamento do código
            try:
                    con = sqlite3.connect(db)
                    cursor = con.cursor()
                    cursor.execute(query, dados)
                    con.commit()
                    con.close()
                    self.textBrowserInformativo.setText("Veiculo Inserido com sucesso")
            except:
                    self.textBrowserInformativo.setText("Sem conecção à base de dados")



    def retranslateUi(self, StockDialog):
        _translate = QtCore.QCoreApplication.translate
        StockDialog.setWindowTitle(_translate("StockDialog", "Gestão de Stock"))
        self.labelLuxuryWheels.setText(_translate("StockDialog", "Luxury Wheels"))
        self.labelGestaoStock.setText(_translate("StockDialog", "Gestão de Stock"))
        self.textBrowser.setHtml(_translate("StockDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Segoe UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:700;\">Por forma a servir melhor os seus clientes é aconselhavel que o seu stock de veiculos seja actualizado com novas viaturas, aumentando assim o sua oferta.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt; font-weight:700;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:700;\">De momento é recomendado que adquira o seguinte número de viaturas:</span></p></body></html>"))
        self.label_3.setText(_translate("StockDialog", "Insira Novo Veículo"))
        self.labelTipoViatura.setText(_translate("StockDialog", "Escolha o tipo de viatura:"))
        self.comboBoxVeiculo.setItemText(0, _translate("StockDialog", "Carro"))
        self.comboBoxVeiculo.setItemText(1, _translate("StockDialog", "Mota"))
        self.lineEditID.setPlaceholderText(_translate("StockDialog", "Id da Viatura"))
        self.labelTipoCategoria.setText(_translate("StockDialog", "Escolha a categoria da viatura:"))
        self.comboBoxCategoria.setItemText(0, _translate("StockDialog", "Gold"))
        self.comboBoxCategoria.setItemText(1, _translate("StockDialog", "Silver"))
        self.comboBoxCategoria.setItemText(2, _translate("StockDialog", "Económico"))
        self.lineEditMarca.setPlaceholderText(_translate("StockDialog", "Marca"))
        self.lineEditModelo.setPlaceholderText(_translate("StockDialog", "Modelo"))
        self.lineEditMatricula.setPlaceholderText(_translate("StockDialog", "Matricula"))
        self.lineEditKm.setPlaceholderText(_translate("StockDialog", "Km"))
        self.labelDataLegalizacao.setText(_translate("StockDialog", "Data de Legalização"))
        self.lineEditPrecoLegalizacao.setPlaceholderText(_translate("StockDialog", "Preço da Legalização"))
        self.lineEditPrecoDia.setPlaceholderText(_translate("StockDialog", "Preço Dia"))
        self.subViaturaBtn.setText(_translate("StockDialog", "Submeter Viatura"))
        self.textBrowserInformativo.setHtml(_translate("StockDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:12pt; font-weight:700; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

