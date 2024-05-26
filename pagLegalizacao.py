from PyQt6 import QtCore, QtGui, QtWidgets

#####################################################################################################################
# Esta página tem apenas um proposito servir de alerta para o utilizador de que existem veiculos por legalizar,
# este alerta é feito com pelo menos 30 dias de antecedencia da data limite para a renovação da legalização. Esta
# página terá para além do cabeçalho que é comum a todas as páginas, no body tera apenas duas caixas de texto em que
# a primeira mensagem é aunica que se altera em função de existir ou nao veiculos para legalizar. A segunda a
# mensagem é sempre a mesma.
######################################################################################################################

# Variável de verificação iniciada a False
verificarLegalizacoesNovas = False

# classe principal da página de alerta/aviso de que existem veiculos por legalizar, nesta classe estão todos os
# widgets e elementos do styleSheet que dão à pagina o seu aspecto visual
class Ui_LegalizacaoDialog(object):
    def setupUi(self, LegalizacaoDialog):
        LegalizacaoDialog.setObjectName("LegalizacaoDialog")
        LegalizacaoDialog.resize(1109, 600)
        LegalizacaoDialog.setStyleSheet("*{\n"
"    border:none;\n"
"    background:transparent;\n"
"    background-color: transparent;\n"
"    padding: 0;\n"
"    color:#FFF;\n"
"}\n"
"#LegalizacaoDialog, #textBrowser,#textBrowser_2{\n"
"    background-color: #1f2329;\n"
"}\n"
"#header, #body{\n"
"    background-color: #27263c;\n"
"    padding:-1\n"
"}\n"
"#textBrowser,#textBrowser_2{\n"
"    border-radius:12px;\n"
"    border-bottom: 2px solid #0080FF;\n"
"    border-right:2px solid #0080FF;\n"
"    margin-left: 70px\n"
"}")
        #############################################################################################################
        # Body é o corpo principal do widget/pagina, este é de todos os QDialogs, o mais simples desta aplicação, apenas
        # tem dois textBrowsers(QTextBrowser, um que vai receber um texto que difere a mensagem caso existam carros para
        # legalizar ou não. Caso haja carros para legalizar a mensagem será de que existem carros por legalizar e o
        # utilizador para as visualizar tera de ir à página pricinpal no menu legalização para visualizar quais as
        # viaturas que se encontram com necessidade de renovar a legalização, caso nao exista nenhuma viatura é
        # exibida uma mensagem a dizer que de momento não existe nenhuma viatura para legalizar. Existe ainda, um outro
        # textBrowser que tem sempre uma mensagem fixa para relembrar a importância de ter sempre os veículos
        # legalizados. Para alem dos QTextBrowser Wigdets são utilizados os seguintes widgets;QSize para definir as
        # dimensoes do body e dos QTextBrowser, QVBoxLayout para defenir o layout, QFont, para definir o tipo de letra
        # e tamanho.
        #############################################################################################################
        self.body = QtWidgets.QWidget(parent=LegalizacaoDialog)
        self.body.setGeometry(QtCore.QRect(0, 70, 1110, 533))
        self.body.setMinimumSize(QtCore.QSize(1110, 533))
        self.body.setMaximumSize(QtCore.QSize(16777215, 515))
        self.body.setObjectName("body")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.body)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.body)
        self.textBrowser.setMaximumSize(QtCore.QSize(1000, 75))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.textBrowser_2 = QtWidgets.QTextBrowser(parent=self.body)
        self.textBrowser_2.setMaximumSize(QtCore.QSize(1000, 75))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        self.textBrowser_2.setFont(font)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout.addWidget(self.textBrowser_2)
        #############################################################################################################
        # Cabeçalho do Widget/pagina, o cabeçalho é composto pelo nome da empresa no lado esquerdo usando para o
        # efeito um QLabel e no lado direito utilizando também um QLabel consta a identificação da pagina neste
        # caso legalização, são também utilizados outros widgets que não são visiveis no produto final mas
        # necessários para atingir a estetica pretendida como os QSize para defenir as dimensões do cabeçalho,
        # layouts(QVBoxLayout ou QHBoxLayout), os frames(QFrame), os QFont(para escolher o tipo de fonte e tamanho
        # que pretendemos utilizar das letras.
        #############################################################################################################
        self.header = QtWidgets.QWidget(parent=LegalizacaoDialog)
        self.header.setGeometry(QtCore.QRect(0, 0, 1109, 60))
        self.header.setMinimumSize(QtCore.QSize(1109, 60))
        self.header.setMaximumSize(QtCore.QSize(16777215, 50))
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
        self.LuxuyLabel = QtWidgets.QLabel(parent=self.frame)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(14)
        font.setBold(True)
        self.LuxuyLabel.setFont(font)
        self.LuxuyLabel.setObjectName("LuxuyLabel")
        self.verticalLayout_2.addWidget(self.LuxuyLabel)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(parent=self.header)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(parent=self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(12)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.horizontalLayout.addWidget(self.frame_2)

        self.retranslateUi(LegalizacaoDialog)
        QtCore.QMetaObject.connectSlotsByName(LegalizacaoDialog)

        # Mensagem que altera consoante se existe ou não viaturas por legalizar. É feito uma verificação para ver se
        # a variável 'verificarLegalizacoesNova' está igual a True. Esta verificação é feita na 'paginaPrincipal.py'

        if verificarLegalizacoesNovas == True:
                self.textBrowser.setText("Tem veículos por legalizar, dirija-se ao menu lateral para visualizar os "
                                         "veículos que necessitam de ser legalizados!")
        else:
                self.textBrowser.setText("De momento tem Zero Veículos por legalizar!")


    def retranslateUi(self, LegalizacaoDialog):
        _translate = QtCore.QCoreApplication.translate
        LegalizacaoDialog.setWindowTitle(_translate("LegalizacaoDialog", "Dialog"))
        self.textBrowser.setHtml(_translate("LegalizacaoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:14pt; font-weight:700; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.textBrowser_2.setHtml(_translate("LegalizacaoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Tahoma\'; font-size:14pt; font-weight:700; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Segoe UI\'; font-weight:400;\">Tenha sempre os seus veículos</span><span style=\" font-family:\'Segoe UI\';\"> legalizados</span><span style=\" font-family:\'Segoe UI\'; font-weight:400;\">, desta forma continuará a rentabiliza-los sem interrupções!</span></p></body></html>"))
        self.LuxuyLabel.setText(_translate("LegalizacaoDialog", "Luxury Wheels"))
        self.label_2.setText(_translate("LegalizacaoDialog", "Legalização"))

