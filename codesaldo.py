#!/usr/bin/python
# -*- coding: latin-1 -*-

from PyQt5 import QtWidgets
import sys
import frmsaldo
import os
from codeconexion import conexion
from datetime import date


class saldoApp(QtWidgets.QMainWindow, frmsaldo.Ui_frmsaldo):
    conexion = conexion()
    nomcaixa = ''
    modif = 0

    # caller = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.consultar()
        self.cancelar()
        self.configtipo()
        self.configmes()
        self.configano()
        self.setFixedWidth(938)
        self.setFixedHeight(443)
        self.cbotipo.currentIndexChanged.connect(self.cargartipo)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.cbocaixa.currentIndexChanged.connect(self.cargarcaixa)
        # self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnguardar.clicked.connect(self.guardar)
        self.btneliminar.clicked.connect(self.eliminar)
        self.tabla.cellDoubleClicked.connect(self.listamovimento)
        self.btnimprimir.clicked.connect(self.resumo)
        self.lblindice.setVisible(False)
        self.lblano.setVisible(False)
        self.lblmes.setVisible(False)
        self.cargarcaixa()
        self.dateEdit.setDate(date.today())
        # -----
        # self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)
        # -----
        # self.radiocredito.setChecked(True)

    def configano(self):
        self.cboano.insertItem(0, '2021')


    def configmes(self):
        self.cbomes.setMaxVisibleItems(12)
        self.cbomes.insertItem(0, 'Janeiro')
        self.cbomes.insertItem(1, 'Fevereiro')
        self.cbomes.insertItem(2, 'Março')
        self.cbomes.insertItem(3, 'Abril')
        self.cbomes.insertItem(4, 'Maio')
        self.cbomes.insertItem(5, 'Junho')
        self.cbomes.insertItem(6, 'Julho')
        self.cbomes.insertItem(7, 'Agosto')
        self.cbomes.insertItem(8, 'Setembro')
        self.cbomes.insertItem(9, 'Outubro')
        self.cbomes.insertItem(10, 'Novembro')
        self.cbomes.insertItem(11, 'Dezembro')

    def resumo(self):
        cod = self.tabla.item(int(self.lblindice.text()), 0).text()
        if cod is None:
            QtWidgets.QMessageBox.information(self, "Erro", "Não foi seleccionado um caixa para imprimir resumo!",
                                              QtWidgets.QMessageBox.Ok)
        else:

            self.cod = self.tabla.item(int(self.lblindice.text()), 0).text()
            con = self.conexion.conectar()
            cur = con.cursor()
            cur.execute('select nomcaixa from caixa where codcaixa = %s', [self.cod])
            self.nomcaixa = cur.fetchone()


            ano = int(self.lblano.text())
            mes = int(self.lblmes.text())

            # CONSULTA SQL
            con = self.conexion.conectar()
            cur = con.cursor()
            cur.execute('select codcaixa, sum(valor), tipo from '
                        'movimento where extract(month from data) = %s and extract(year from data) = %s and codcaixa = %s '
                        'group by codcaixa, tipo order by codcaixa', [mes + 1, ano, cod])
            lista = cur.fetchall()


            date = '01/' + str(mes + 1) + '/' + str(ano)

            cur.execute("select COALESCE(sum(valor), 0) from movimento where data < '" + date + "' and codcaixa = %s", [cod])
            anterior = cur.fetchone()

            #################################

            from coderesumo import resumo
            resumo().generar(cod, mes, ano, self.nomcaixa, lista, anterior)

    def listamovimento(self):
        item = self.caixa[int(self.lblindice.text())]
        cod = item[0]
        from codelistaseparada import listaseparadaApp
        self.setEnabled(False)
        self.listaseparada = listaseparadaApp(parent=self)
        self.listaseparada.show()
        self.listaseparada.iniciar(self, cod)

    def iniciarmodif(self, caller, cod):
        self.caller = caller
        self.modif = 1
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select a.codmovimento, a.codcaixa, b.nomcaixa, a.valor, a.descricao, a.data, a.tipo from movimento a, caixa b where a.codmovimento = %s and a.codcaixa = b.codcaixa',[cod])
        modif = cur.fetchone()
        self.txtcod.setText(str(modif[0]))
        self.txtvalor.setValue(modif[3])
        self.txtdescricao.setText(modif[4])
        self.dateEdit.setDate(modif[5])
        self.txtcodcaixa.setText(str(modif[1]))
        self.txtcodtipo.setText(str(modif[6]))
        cantcaixa = self.cbocaixa.count()
        for i in range(cantcaixa):
            if self.cbocaixa.itemText(i) == modif[2]:
                self.cbocaixa.setCurrentIndex(i)
                break

        if modif[6] == 0:
            self.cbotipo.setCurrentIndex(0)
        if modif[6] == 1:
            self.cbotipo.setCurrentIndex(1)
        if modif[6] == 2:
            self.cbotipo.setCurrentIndex(2)
        if modif[6] == 3:
            self.cbotipo.setCurrentIndex(3)
        if modif[6] == 4:
            self.cbotipo.setCurrentIndex(4)

        self.editar()

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)
        if self.modif == 1:
            self.caller.consultar()
        else:
            return
        self.modif = 0

        self.conexion.conectar()
        os.system(r'if not exist "C:\SisCaixa\" mkdir C:\SisCaixa')
        direccion = r'-f C:\SisCaixa\SisCaixa.dump siscaixa'

        os.system(r'"C:\Program Files\PostgreSQL\13\bin\pg_dump.exe" -U postgres -C ' + direccion)

    def abrir(self, menu):
        self.caller = menu

    def nuevo(self):
        self.cancelar()
        self.bnd = 0
        self.txtvalor.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)
        self.cbocaixa.setEnabled(True)

    def editar(self):
        self.bnd = 1
        self.txtvalor.setEnabled(True)
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(True)
        self.btncancelar.setEnabled(True)
        self.cbocaixa.setEnabled(True)
        self.cbotipo.setEnabled(True)

    def cancelar(self):
        self.txtvalor.setEnabled(False)

        self.txtvalor.clear()
        self.txtcod.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)
        self.cbocaixa.setEnabled(False)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        codcaixa = int(self.txtcodcaixa.text())
        data = self.dateEdit.date()
        data = str(data.toString('dd/MM/yyyy'))
        valor = str(self.txtvalor.text())

        # ----
        i = 0
        res = ''
        while i != len(valor):
            if valor[i] == ",":
                res = res + "."
            else:
                res = res + valor[i]
            i = i + 1
        # ----
        descricao = str(self.txtdescricao.toPlainText())

        # Controle de tipo de registro
        tipo = str(self.txtcodtipo.text())

        if len(valor) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into movimento (codcaixa, data, valor, descricao, tipo) values(%s,%s,%s,%s,%s)',
                            [codcaixa, data, res, descricao, tipo])
            else:
                cur.execute('update movimento set codcaixa=%s, data=%s, valor=%s, descricao=%s, tipo=%s where codmovimento=%s',
                            [codcaixa, data, res, descricao, tipo, cod])

            con.commit()
            self.cancelar()
            self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes",
                                              "Um campo nao cumpre os requisitos", QtWidgets.QMessageBox.Ok)

    def config(self, rows):
        self.tabla.setColumnCount(3)
        self.tabla.setRowCount(int(rows[0]))
        lista = 'Codigo', 'Caixa', 'Saldo'
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 230)

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

    def consultar(self):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from caixa')
        rows = cur.fetchone()
        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select a.codcaixa, a.nomcaixa, sum(b.valor) from caixa a, movimento b where a.codcaixa=b.codcaixa  '
                        'group by a.codcaixa order by a.codcaixa asc')
            self.caixa = cur.fetchall()
            for i in range(int(rows[0])):
                item = self.caixa[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(item[1]))
                self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item[2])))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)
        self.consultarcaixa(0)

    # def cargar(self):
    #     self.cancelar()
    #     index = int(self.lblindice.text())
    #     item = self.caixa[index]
    #     self.txtcod.setText(str(item[0]))
    #     self.txtnomcaixa.setText(str(item[1]))
    #     self.txtcodbanco.setText(str(item[3]))
    #     self.btnguardar.setVisible(False)
    #     self.btneditar.setVisible(True)
    #     self.btneditar.setEnabled(True)
    #     self.btneliminar.setEnabled(True)
    #     # ----
    #     cantbanco = self.cbobanco.count()
    #     banco = item[2]
    #
    #     for i in range(cantbanco):
    #         if self.cbobanco.itemText(i) == banco:
    #             self.cbobanco.setCurrentIndex(i)
    #             break
    #             # ----

    def consultarcaixa(self, sel):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from caixa')
        rowcaixa = cur.fetchone()
        self.rowcaixa = int(rowcaixa[0])
        cur.execute('select codcaixa, nomcaixa '
                    'from caixa order by codcaixa')
        self.vercaixa = cur.fetchall()
        self.cargarcaixa()
        if self.rowcaixa > 0:
            self.cbocaixa.setMaxVisibleItems(10)
            self.cbocaixa.clear()
            cont = int(rowcaixa[0] - 1)
            for row in range(self.rowcaixa):
                var = self.vercaixa[cont]
                self.cbocaixa.insertItem(0, var[1])
                cont = cont - 1
            self.cbocaixa.setCurrentIndex(0)
        if sel != 0:
            for cont in range(self.banco):
                carg = self.vercaixa[cont]
                if sel == int(carg[0]):
                    self.cbocaixa.setCurrentIndex(cont)
                    break

    def cargarcaixa(self):
        if self.rowcaixa > 0:
            valor = self.cbocaixa.currentIndex()
            item = self.vercaixa[int(valor)]
            self.txtcodcaixa.setText(str(item[0]))

    def eliminar(self):
        #TODO: Arreglar los delete del proyecto entero

        cod = int(self.txtcod.text())
        # con = self.conexion.conectar()
        # cur = con.cursor()

        if (QtWidgets.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                           QtWidgets.QMessageBox.Yes,
                                           QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
            con = self.conexion.conectar()
            cur = con.cursor()
            cur.execute('delete from movimento where codmovimento = %s', [cod])
            con.commit()
            self.cancelar()
            self.consultar()
            QtWidgets.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                    QtWidgets.QMessageBox.Ok)

def main():
    app = QtWidgets.QApplication(sys.argv)
    form = saldoApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
