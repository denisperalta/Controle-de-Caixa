from PyQt5 import QtWidgets, QtCore
import sys
import os
import frmmenu
import time
import subprocess
from codeconexion import conexion


class menuApp(QtWidgets.QMainWindow, frmmenu.Ui_frmmenu):
    conexion = conexion()
    estado = 0

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.btnabrircaixas.pressed.connect(self.abrircaixas)
        self.btnabrirmovimento.pressed.connect(self.abrirmovimento)
        # self.btnlista.pressed.connect(self.abrirlista)
        # self.tabla.cellDoubleClicked.connect(self.modifcheque)
        # self.btnimprimir.clicked.connect(self.imprimir)
        self.setFixedWidth(332)
        self.setFixedHeight(281)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        # self.lblindice.setVisible(False)
        # self.proximos()
        # -----
        # self.tabla.setSortingEnabled(True)
        # self.tabla.resizeRowsToContents()
        # self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        # header = self.tabla.horizontalHeader()
        # header.setStretchLastSection(True)
        # -----

    def closeEvent(self, evnt):
        self.conexion.conectar()
        os.system(r'if not exist "C:\BackupSisCaixa" mkdir C:\BackupSisCaixa')
        direccion = r'-f C:\BackupSisCaixa\BackupSisCaixa.dump siscaixa'

        file = r'"C:\Program Files\PostgreSQL\14\bin\pg_dump.exe"' #PC DENIS
        subprocess.call(file + ' -U postgres -C ' + direccion)
        # os.system("\"C:\\Program Files\\PostgreSQL\\13\\bin\\pg_dump.exe" -U postgres -C + direccion) # PC DENIS
        # os.system(r'"C:\Program Files\PostgreSQL\11\bin\pg_dump.exe" -U postgres -C ' + direccion)

        # try:
        #
        #     con = self.conexion.conectar()
        #     cur = con.cursor()
        #     cur.execute('select b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor, a.datacheque, '
        #                 'e.nom_loja, a.pagado from cheque a, banco b, agencia c, conta d, loja e where '
        #                 'a.cod_conta=d.cod_conta and d.cod_agencia=c.cod_agencia and c.cod_banco=b.cod_banco and '
        #                 'a.cod_loja=e.cod_loja order by d.cod_conta, a.datacheque asc')
        #     f = open(r'C:\BackupCheque\backupcheque.sql', 'w')
        #     for row in cur:
        #         f.write("insert into backup values (" + str(row) + ");")
        # # except psycopg2.error as e:
        # #     print(('Error %s' % e))
        # #     sys.exit(1)
        # finally:
        #     if con:
        # con.close()

    # def imprimir(self):
    #     from codepdf import pdf
    #     pdf().generar(self.fechamin, self.fechamax, self.rows[0], self.cheque, 4, 0, 0, self.suma)

    # def modifcheque(self):
    #     item = self.cheque[int(self.lblindice.text())]
    #     cod = item[0]
    #     from coderegistro import registroApp
    #     self.registro = registroApp(parent=self)
    #     self.registro.show()
    #     self.registro.iniciar(cod, self, 1)
    #
    #     # self.caller.txtcodprod.setText(unicode(item[0]))
    #     # self.caller.txtnomprod.setText(item[1])
    #     # self.caller.txtprecio.setText(unicode(item[3]))
    #     # self.caller.txtcantidad.setFocus()
    #     # self.caller.actualizar()
    #     # self.close()

    def abrirmovimento(self):
        from codesaldo import saldoApp
        self.setEnabled(False)
        saldo = saldoApp(parent=self)
        saldo.abrir(self)
        saldo.show()

    def abrircaixas(self):
        from codecaixa import caixaApp
        self.setEnabled(False)
        self.caixa = caixaApp(parent=self)
        self.caixa.show()
        self.caixa.iniciar(self)

    # def abrirlista(self):
    #     from codelista import listaApp
    #     self.setEnabled(False)
    #     self.lista = listaApp(parent=self)
    #     self.lista.show()
    #     self.lista.iniciar(self)

    # def limit(self, mes, anho):
    #     if mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
    #         limite = 31
    #         return limite
    #     elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
    #         limite = 30
    #         return limite
    #     elif mes == 2:
    #         if anho % 4 == 0:
    #             limite = 29
    #         else:
    #             limite = 28
    #         return limite

    # def calcularfecha(self):
    #     dia = (time.strftime("%d"))
    #     mes = (time.strftime("%m"))
    #     year = (time.strftime("%Y"))
    #     dia = int(dia)
    #     diamax = dia + 7
    #     mesmax = int(mes)
    #     yearmax = int(year)
    #     limite = self.limit(mesmax, yearmax)
    #     while (diamax > limite) or (mesmax > 12):
    #         while mesmax > 12:
    #             mesmax = mesmax - 12
    #             yearmax = yearmax + 1
    #             limite = self.limit(mesmax, yearmax)
    #
    #         if diamax > limite:
    #             diamax = diamax - limite
    #             mesmax = mesmax + 1
    #             limite = self.limit(mesmax, yearmax)
    #     if len(str(mesmax)) == 1:
    #         mesmax = '0' + str(mesmax)
    #     if len(str(diamax)) == 1:
    #         diamax = '0' + str(diamax)
    #     return diamax, mesmax, yearmax

    # def config(self):
    #     self.tabla.setColumnCount(9)
    #     self.tabla.setRowCount(int(self.rows[0]))
    #     lista = 'Codigo', 'Banco', 'Agencia', 'Conta', 'Numero', 'Valor', 'Data', 'Loja', 'Pagado'
    #     self.tabla.setHorizontalHeaderLabels(lista)
    #     self.tabla.setColumnWidth(0, 50)
    #     self.tabla.setColumnWidth(1, 139)
    #     self.tabla.setColumnWidth(2, 80)
    #     self.tabla.setColumnWidth(3, 80)
    #     self.tabla.setColumnWidth(4, 100)
    #     self.tabla.setColumnWidth(5, 80)
    #     self.tabla.setColumnWidth(6, 80)
    #     self.tabla.setColumnWidth(7, 95)
    #     self.tabla.setColumnWidth(8, 50)
    #
    #     # self.tabla.setSortingEnabled(True)
    #     self.tabla.resizeRowsToContents()
    #     self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)
    #
    #     header = self.tabla.horizontalHeader()
    #     header.setStretchLastSection(True)

    # def proximos(self):
    #     # cargar dia actual y comparar
    #     fechamin = (time.strftime("%d/%m/%Y"))
    #     fechamax = self.calcularfecha()
    #     fechamax = str(fechamax[0]) + '/' + str(fechamax[1]) + '/' + str(fechamax[2])
    #     self.lblfechamin.setText('Proximos cheques desde: ' + fechamin)
    #     self.lblfechamax.setText(fechamax)
    #     self.fechamin = fechamin
    #     self.fechamax = fechamax
    #     # ---------------------------
    #     con = self.conexion.conectar()
    #     cur = con.cursor()
    #     cur.execute('''select count(*) from cheque where datacheque between %s and %s and pagado='Nao' ''',
    #                 [fechamin, fechamax])
    #     rows = cur.fetchone()
    #     self.rows = rows
    #     suma = 0
    #     if int(rows[0]) > 0:
    #         self.lblsinreg.setVisible(False)
    #         self.config()
    #         cur.execute(
    #             '''select a.cod_cheque, b.nom_banco, c.num_agencia, d.num_conta, a.num_cheque, a.valor,
    #             to_char(a.datacheque,'DD/MM/YYYY'), e.nom_loja, a.pagado, d.cod_conta, e.cod_loja from cheque a,
    #             banco b, agencia c, conta d, loja e where a.cod_conta=d.cod_conta and d.cod_agencia=c.cod_agencia and
    #             c.cod_banco=b.cod_banco and a.cod_loja=e.cod_loja and a.pagado='Nao' and datacheque between %s and %s
    #             order by d.cod_conta, a.datacheque asc''',
    #             [fechamin, fechamax])
    #         self.cheque = cur.fetchall()
    #
    #         for i in range(int(rows[0])):
    #             item = self.cheque[i]
    #             suma = suma + item[5]
    #             self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
    #             self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(item[1]))
    #             self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(item[2]))
    #             self.tabla.setItem(i, 3, QtWidgets.QTableWidgetItem(item[3]))
    #             self.tabla.setItem(i, 4, QtWidgets.QTableWidgetItem(item[4]))
    #             self.tabla.setItem(i, 5, QtWidgets.QTableWidgetItem(str(item[5])))
    #             self.tabla.setItem(i, 6, QtWidgets.QTableWidgetItem(item[6]))
    #             self.tabla.setItem(i, 7, QtWidgets.QTableWidgetItem(item[7]))
    #             self.tabla.setItem(i, 8, QtWidgets.QTableWidgetItem(item[8]))
    #             self.suma = suma
    #
    #     else:
    #         self.lblsinreg.setVisible(True)
    #         self.tabla.setRowCount(0)
    #         self.tabla.setColumnCount(0)
    #         self.suma = 0
    #     self.lblsuma.setText(str(self.suma))


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = menuApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
