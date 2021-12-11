from PyQt5 import QtWidgets, QtCore
import sys
import frmlista
from codeconexion import conexion


class listaApp(QtWidgets.QMainWindow, frmlista.Ui_frmlista):
    conexion = conexion()
    caller = None
    buscar = "'%%'"
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        # self.pagado()
        # self.conta()


        # self.enableconta()
        # self.setFixedWidth(980)
        # self.setFixedHeight(539)
        self.datemin.setEnabled(False)
        self.datemax.setEnabled(False)
        self.checkdata.stateChanged.connect(self.enabledata)
        # self.checkconta.stateChanged.connect(self.enableconta)
        # self.txtbuscar.textChanged.connect(self.fbuscar)
        self.datemin.dateChanged.connect(self.consultar)
        self.datemax.dateChanged.connect(self.consultar)
        # self.cbopagado.currentIndexChanged.connect(self.consultar)
        # self.consultar()
        # -----
        # self.cboconta.currentIndexChanged.connect(self.cargarconta)
        self.tabla.cellDoubleClicked.connect(self.modifmovimento)
        # self.btnimprimir.clicked.connect(self.imprimir)
        # self.lblindice.setVisible(False)
        # self.lblconta.setVisible(False)
        # self.cargarconta()
        self.txtbuscar.setFocus()
        # self.enabledata()
        # self.iniciar(self, 1)

    def modifmovimento(self):
        item = self.movimento[int(self.lblindice.text())]
        cod = item[0]
        from codesaldo import saldoApp
        self.saldo = saldoApp(parent=self)
        self.saldo.show()
        self.saldo.iniciarmodif(self, cod)

    def iniciar(self, caller, cod):
        self.caller = caller
        self.codcaixa = cod
        self.consultar()

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)

    def enabledata(self):
        if self.checkdata.isChecked():
            self.datemin.setEnabled(True)
            self.datemax.setEnabled(True)
        else:
            self.datemin.setEnabled(False)
            self.datemax.setEnabled(False)
        self.consultar()

    def config(self):
        self.tabla.setColumnCount(5)
        self.tabla.setRowCount(int(self.rows[0]))
        lista = 'Codigo', 'Caixa', 'Valor', 'Data', 'Descrição'
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 160)
        self.tabla.setColumnWidth(2, 100)
        self.tabla.setColumnWidth(3, 100)
        self.tabla.setColumnWidth(4, 132)


        self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)

    def consultar(self):
        self.tabla.setSortingEnabled(False)
        con = self.conexion.conectar()
        cur = con.cursor()
        # --------------------
        self.fechamax = self.datemax.date()
        self.fechamax = str(self.fechamax.toString('dd/MM/yyyy'))
        self.fechamin = self.datemin.date()
        self.fechamin = str(self.fechamin.toString('dd/MM/yyyy'))
        fecha = ''
        if self.checkdata.isChecked():
            fecha = "a.data between '" + self.fechamin + "' and '" + self.fechamax + "'"
        #------------------------------
        if self.checkdata.isChecked():
            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(self.codcaixa) + ' and ' + fecha)
            bandera = 1
            print('ok')

        elif not self.checkdata.isChecked():
            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(self.codcaixa))
            bandera = 0
        # ------------------------------
        self.bandera = bandera
        rows = cur.fetchone()
        self.rows = rows
        # -----
        suma = 0
        # -----
        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config()
            datachar = "to_char(a.data,'DD/MM/YYYY')"
            if bandera == 0:
                cur.execute('select a.codmovimento, b.nomcaixa, a.valor, ' + datachar + ', a.descricao from movimento a, caixa b '
                            'where a.codcaixa = b.codcaixa and a.codcaixa = ' + str(self.codcaixa) + 'order by a.codmovimento')

            elif bandera == 1:
                cur.execute('select a.codmovimento, b.nomcaixa, a.valor, ' + datachar + ', a.descricao from movimento a, caixa b '
                            'where a.codcaixa = b.codcaixa and a.codcaixa = ' + str(self.codcaixa) + ' and ' + fecha + 'order by a.codmovimento')


            self.movimento = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.movimento[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(item[1]))
                self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                self.tabla.setItem(i, 3, QtWidgets.QTableWidgetItem(item[3]))
                self.tabla.setItem(i, 4, QtWidgets.QTableWidgetItem(item[4]))
                suma = suma + item[2]
                self.suma = suma
                self.lbltotal.setText(str(suma))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
            self.suma = 0

    def imprimir(self):
        from codepdf import pdf
        pdf().generar(self.fechamin, self.fechamax, self.rows[0], self.movimento, self.bandera, self.bndpago, self.conta, self.suma)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = listaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
