from PyQt5 import QtWidgets, QtCore
import sys
import frmlistaseparada
import os
from codeconexion import conexion
from datetime import date


class listaseparadaApp(QtWidgets.QMainWindow, frmlistaseparada.Ui_frmlistaseparada):
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
        self.configtipo()
        self.datemax.setDate(date.today())
        self.datemin.setDate(date.today())
        self.cbotipo.currentIndexChanged.connect(self.cargartipo)
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
        self.tabladebito.cellDoubleClicked.connect(self.modifmovimentodebito)
        self.tablacredito.cellDoubleClicked.connect(self.modifmovimentocredito)
        self.btnimprimir.clicked.connect(self.imprimir)
        self.lblindice.setVisible(False)
        self.lblconta.setVisible(False)
        # self.cargarconta()
        self.txtbuscar.setFocus()
        # self.enabledata()
        self.iniciar(self, 1)

    def configtipo(self):
        self.cbotipo.setMaxVisibleItems(5)
        self.cbotipo.insertItem(0, 'Pagamento')
        self.cbotipo.insertItem(1, 'Venda com nota')
        self.cbotipo.insertItem(2, 'Cheque emitido')
        self.cbotipo.insertItem(3, 'Cheque devolvido')
        self.cbotipo.insertItem(4, 'Deposito')
        self.txtcodtipo.setText('0')

    def cargartipo(self):
        self.txtcodtipo.setText(str(self.cbotipo.currentIndex()))
        self.consultar()

    def modifmovimentocredito(self):
        cod = self.tablacredito.item(int(self.lblindice.text()), 0).text()
        from codesaldo import saldoApp
        self.setEnabled(False)
        self.saldo = saldoApp(parent=self)
        self.saldo.show()
        self.saldo.iniciarmodif(self, cod)

    def modifmovimentodebito(self):
        cod = self.tabladebito.item(int(self.lblindice.text()), 0).text()
        from codesaldo import saldoApp
        self.setEnabled(False)
        self.saldo = saldoApp(parent=self)
        self.saldo.show()
        self.saldo.iniciarmodif(self, cod)

    def iniciar(self, caller, cod):
        self.caller = caller
        self.codcaixa = cod
        self.consultar()

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)
        self.caller.consultar()
        self.caller.modif = 0
        #
        # self.conexion.conectar()
        # os.system(r'if not exist "C:\SisCaixa\" mkdir C:\SisCaixa')
        # direccion = r'-f C:\SisCaixa\SisCaixa.dump siscaixa'
        #
        # os.system(r'"C:\Program Files\PostgreSQL\13\bin\pg_dump.exe" -U postgres -C ' + direccion)

    def enabledata(self):
        if self.checkdata.isChecked():
            self.datemin.setEnabled(True)
            self.datemax.setEnabled(True)
        else:
            self.datemin.setEnabled(False)
            self.datemax.setEnabled(False)
        self.consultar()

    def config(self):
        self.tabladebito.setColumnCount(6)
        self.tabladebito.setRowCount(int(self.rowsnegativo[0]))

        listaseparada = 'Codigo', 'Caixa', 'Valor', 'Data', 'Tipo', 'Descrição'
        self.tabladebito.setHorizontalHeaderLabels(listaseparada)
        self.tabladebito.setColumnWidth(0, 50)
        self.tabladebito.setColumnWidth(1, 80)
        self.tabladebito.setColumnWidth(2, 100)
        self.tabladebito.setColumnWidth(3, 70)
        self.tabladebito.setColumnWidth(4, 100)
        self.tabladebito.setColumnWidth(5, 132)

        # self.tabla.setSortingEnabled(False)
        self.tabladebito.resizeRowsToContents()
        # self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)
        header = self.tabladebito.horizontalHeader()
        header.setStretchLastSection(True)

        self.tablacredito.setColumnCount(6)
        self.tablacredito.setRowCount(int(self.rowspositivo[0]))
        self.tablacredito.setHorizontalHeaderLabels(listaseparada)
        self.tablacredito.setColumnWidth(0, 50)
        self.tablacredito.setColumnWidth(1, 80)
        self.tablacredito.setColumnWidth(2, 100)
        self.tablacredito.setColumnWidth(3, 70)
        self.tablacredito.setColumnWidth(4, 100)
        self.tablacredito.setColumnWidth(5, 132)

        #self.tabla.setSortingEnabled(False)
        self.tablacredito.resizeRowsToContents()
        # self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tablacredito.horizontalHeader()
        header.setStretchLastSection(True)

    def consultar(self):
        # self.tabla.setSortingEnabled(False)
        con = self.conexion.conectar()
        cur = con.cursor()
        # --------------------
        self.fechamax = self.datemax.date()
        self.fechamax = str(self.fechamax.toString('dd/MM/yyyy'))
        self.fechamin = self.datemin.date()
        self.fechamin = str(self.fechamin.toString('dd/MM/yyyy'))
        self.fecha = ''

        if self.checkdata.isChecked():
            self.fecha = "a.data between '" + self.fechamin + "' and '" + self.fechamax + "'"

        #------------------------------    FILTRO PARA TIPO DE REGISTRO
        self.tipo = "tipo = '" + str(self.txtcodtipo.text()) + "'"

        #------------------------------

        #------------------------------
        if self.checkdata.isChecked():
            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(self.codcaixa) + ' and ' + self.fecha + ' and ' + self.tipo)
            self.rows = cur.fetchone()

            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(
                self.codcaixa) + ' and ' + self.fecha + ' and a.valor >= 0' + ' and ' + self.tipo)
            self.rowspositivo = cur.fetchone()

            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(
                self.codcaixa) + ' and ' + self.fecha + ' and a.valor < 0' + ' and ' + self.tipo)
            self.rowsnegativo = cur.fetchone()



            bandera = 1

        elif not self.checkdata.isChecked():
            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(self.codcaixa) + ' and ' + self.tipo)
            self.rows = cur.fetchone()

            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(self.codcaixa) + ' and a.valor >= 0' + ' and ' + self.tipo)
            self.rowspositivo = cur.fetchone()

            cur.execute('select count (*) from movimento a where a.codcaixa =' + str(self.codcaixa) + ' and a.valor < 0' + ' and ' + self.tipo)
            self.rowsnegativo = cur.fetchone()

            bandera = 0
        # ------------------------------
        self.bandera = bandera
        # self.rows = rows
        # -----
        suma = 0
        self.sumadebito = 0
        self.sumacredito = 0
        # -----
        if int(self.rows[0]) > 0:
            # self.lblsinregcredito.setVisible(False)
            # self.lblsinregdebito.setVisible(False)

            self.config()

            datachar = "to_char(a.data,'DD/MM/YYYY')"
            if bandera == 0:
                cur.execute('select a.codmovimento, b.nomcaixa, a.valor, ' + datachar + ', a.descricao, a.tipo from movimento a, caixa b '
                            'where a.codcaixa = b.codcaixa and a.codcaixa = ' + str(self.codcaixa) + ' and ' + self.tipo + 'order by a.data, a.valor')

            elif bandera == 1:
                cur.execute('select a.codmovimento, b.nomcaixa, a.valor, ' + datachar + ', a.descricao, a.tipo from movimento a, caixa b '
                            'where a.codcaixa = b.codcaixa and a.codcaixa = ' + str(self.codcaixa) + ' and ' + self.fecha + ' and ' + self.tipo + 'order by a.data, a.valor')

            self.movimento = cur.fetchall()
            self.negativo = 0
            self.positivo = 0
            self.txttipo = ''
            self.lbltotaldebito.setText('TOTAL DEBITO: 0')
            self.lbltotalcredito.setText('TOTAL CREDITO: 0')
            self.lblsinregcredito.setVisible(True)
            self.lblsinregdebito.setVisible(True)

            for i in range(int(self.rows[0])):
                item = self.movimento[i]
                if(item[5]==0):
                    self.txttipo = 'Pagamento'
                elif(item[5]==1):
                    self.txttipo = 'Venda com nota'
                elif(item[5]==2):
                    self.txttipo = 'Cheque emitido'
                elif(item[5]==3):
                    self.txttipo = 'Cheque devolvido'
                elif(item[5]==4):
                    self.txttipo = 'Deposito'
                if (item[2]<0):
                    self.tabladebito.setItem(self.negativo, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                    self.tabladebito.setItem(self.negativo, 1, QtWidgets.QTableWidgetItem(item[1]))
                    self.tabladebito.setItem(self.negativo, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                    self.tabladebito.setItem(self.negativo, 3, QtWidgets.QTableWidgetItem(item[3]))
                    self.tabladebito.setItem(self.negativo, 4, QtWidgets.QTableWidgetItem(self.txttipo))
                    self.tabladebito.setItem(self.negativo, 5, QtWidgets.QTableWidgetItem(item[4]))

                    self.sumadebito = self.sumadebito + item[2]
                    self.negativo = self.negativo + 1
                    self.lblsinregdebito.setVisible(False)
                    self.lbltotaldebito.setText('TOTAL DEBITO: ' + str(self.sumadebito))

                else:
                    self.tablacredito.setItem(self.positivo, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                    self.tablacredito.setItem(self.positivo, 1, QtWidgets.QTableWidgetItem(item[1]))
                    self.tablacredito.setItem(self.positivo, 2, QtWidgets.QTableWidgetItem(str(item[2])))
                    self.tablacredito.setItem(self.positivo, 3, QtWidgets.QTableWidgetItem(item[3]))
                    self.tablacredito.setItem(self.positivo, 4, QtWidgets.QTableWidgetItem(self.txttipo))
                    self.tablacredito.setItem(self.positivo, 5, QtWidgets.QTableWidgetItem(item[4]))
                    self.sumacredito = self.sumacredito + item[2]
                    self.positivo = self.positivo + 1
                    self.lblsinregcredito.setVisible(False)
                    self.lbltotalcredito.setText('TOTAL CREDITO: ' + str(self.sumacredito))

                suma = suma + item[2]
                self.suma = suma
                self.lbltotal.setText('TOTAL: ' + str(suma))
        else:
            self.lblsinregcredito.setVisible(True)
            self.lblsinregdebito.setVisible(True)
            self.tablacredito.setRowCount(0)
            self.tablacredito.setColumnCount(0)
            self.tabladebito.setRowCount(0)
            self.tabladebito.setColumnCount(0)
            self.suma = 0
            self.lbltotalcredito.setText('TOTAL: 0')
            self.lbltotaldebito.setText('TOTAL: 0')
            self.lbltotal.setText('TOTAL: 0')

    def imprimir(self):
        from codepdf import pdf
        pdf().generar(self.fechamin, self.fechamax, self.rows[0], self.movimento, self.bandera, self.sumacredito, self.sumadebito, self.suma, self.txttipo)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = listaseparadaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
