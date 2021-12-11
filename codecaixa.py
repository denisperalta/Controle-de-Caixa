from PyQt5 import QtWidgets
from datetime import date
import sys
import frmcaixa
from codeconexion import conexion


class caixaApp(QtWidgets.QMainWindow, frmcaixa.Ui_frmcaixa):
    conexion = conexion()

    # caller = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.consultar()
        self.cancelar()
        self.setFixedWidth(888)
        self.setFixedHeight(259)
        self.btnnovo.clicked.connect(self.nuevo)
        self.btncancelar.clicked.connect(self.cancelar)
        self.tabla.cellClicked.connect(self.cargar)
        self.btneditar.clicked.connect(self.editar)
        self.btnguardar.clicked.connect(self.guardar)
        self.btneliminar.clicked.connect(self.eliminar)
        self.lblindice.setVisible(False)
        # -----
        # self.tabla.setSortingEnabled(True)
        self.tabla.resizeRowsToContents()
        self.tabla.horizontalHeader().sortIndicatorChanged.connect(self.tabla.resizeRowsToContents)

        header = self.tabla.horizontalHeader()
        header.setStretchLastSection(True)
        # -----

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)


    def nuevo(self):
        self.cancelar()
        self.bnd = 0
        self.txtnomcaixa.setEnabled(True)
        self.txtsaldo.setEnabled(True)
        self.txtnomcaixa.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def editar(self):
        self.bnd = 1
        self.txtnomcaixa.setEnabled(True)
        self.txtsaldo.setEnabled(True)
        self.txtnomcaixa.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def cancelar(self):
        self.txtnomcaixa.setEnabled(False)
        self.txtsaldo.setEnabled(False)
        self.txtnomcaixa.clear()
        self.txtsaldo.clear()
        self.txtcod.clear()
        self.btnnovo.setEnabled(True)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(False)

    def guardar(self):
        if len(self.txtcod.text()) > 0:
            cod = str(self.txtcod.text())
        nom = str(self.txtnomcaixa.text())
        saldo = str(self.txtsaldo.text())
        if len(nom) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into caixa (nomcaixa) values(%s)', [nom])
                cur.execute('select max(codcaixa) from caixa')
                max = cur.fetchone()
                today = date.today().strftime("%d/%m/%Y")
                # today = date.today().strftime("%d/%m/%Y")
                cur.execute('insert into movimento (codcaixa, data, valor, tipo) values(%s,%s,%s,%s)',
                            [max, today, saldo, 5])
            else:
                cur.execute('update caixa set nomcaixa = %s where codcaixa=%s', [nom, cod])
                cur.execute('update movimento set valor = %s where codcaixa = %s and tipo = 5', [saldo, cod])

            con.commit()
            self.cancelar()
            self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtWidgets.QMessageBox.Ok)

    def config(self, rows):
        self.tabla.setColumnCount(3)
        self.tabla.setRowCount(int(rows[0]))
        lista = 'Codigo', 'Caixa', 'Saldo Inicial'
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 70)

    def consultar(self):
        # cod = str(self.txtcod.text())
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from caixa')
        rows = cur.fetchone()
        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select a.codcaixa, a.nomcaixa, b.valor from caixa a, movimento b where b.tipo = 5 and a.codcaixa = b.codcaixa '
                        'order by codcaixa asc')
            self.caixa = cur.fetchall()

            # cur.execute('select a.valor from movimento a, caixa b where a.tipo = 5 and a.codcaixa = b.codcaixa and a.codcaixa = %s', [cod])
            for i in range(int(rows[0])):
                item = self.caixa[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(item[1]))
                self.tabla.setItem(i, 2, QtWidgets.QTableWidgetItem(str(item[2])))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.caixa[index]
        self.txtcod.setText(str(item[0]))
        self.txtnomcaixa.setText(str(item[1]))
        self.txtsaldo.setValue(item[2])
        self.btnguardar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)
        # ----
       
    def eliminar(self):
        #TODO: Arreglar los delete del proyecto entero

        cod = int(self.txtcod.text())
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from movimento where codcaixa=%s', [cod])
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            if (QtWidgets.QMessageBox.question(self, "Eliminando Registro", "Deseja Eliminar este Registro?",
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes):
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from caixa where codcaixa = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                QtWidgets.QMessageBox.information(self, "Eliminando Registro", "Registro Eliminado",
                                                        QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.question(self, "Error ao eliminar registro",
                                                 "Esse registro tem um movimento registrado", QtWidgets.QMessageBox.Ok)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = caixaApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
