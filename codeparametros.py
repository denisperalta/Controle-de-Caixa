from PyQt5 import QtWidgets, QtCore
import sys
import frmparametros


class parametrosApp(QtWidgets.QMainWindow, frmparametros.Ui_frmparametros):
    caller = None
    buscar = "%%"

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        # self.setFixedWidth(742)
        # self.setFixedHeight(272)
        self.btnbanco.clicked.connect(self.llamarbanco)
        self.btnconta.clicked.connect(self.llamarconta)
        self.btnfornecedor.clicked.connect(self.llamarfornecedor)

    def iniciar(self, caller):
        self.caller = caller
        self.cerrar = 0

    def closeEvent(self, evnt):
        if not self.cerrar == 1:
            self.caller.setEnabled(True)
        # self.close()

    def llamarfornecedor(self):
        self.cerrar = 1
        from codefornecedor import fornecedorApp
        self.fornecedor = fornecedorApp(parent=self)
        self.close()
        self.fornecedor.show()
        self.fornecedor.iniciar(self.caller)

    def llamarbanco(self):
        self.cerrar = 1
        from codebanco import bancoApp
        self.banco = bancoApp(parent=self)
        self.close()
        self.banco.show()
        self.banco.iniciar(self.caller)

    def llamarconta(self):
        self.cerrar = 1
        from codeconta import contaApp
        self.conta = contaApp(parent=self)
        self.close()
        self.conta.show()
        self.conta.iniciar(self.caller)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = parametrosApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
