from PyQt5 import QtWidgets
import sys

import frmfornecedor
from codeconexion import conexion


class fornecedorApp(QtWidgets.QMainWindow, frmfornecedor.Ui_frmfornecedor):
    conexion = conexion()

    # caller = None

    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        self.bnd = 0
        self.consultar()
        self.cancelar()
        self.setFixedWidth(830)
        self.setFixedHeight(260)
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
        # self.cargarfornecedor()

    def iniciar(self, caller):
        self.caller = caller

    def closeEvent(self, evnt):
        self.caller.setEnabled(True)

    def nuevo(self):
        self.cancelar()
        self.bnd = 0
        self.txtnomfornecedor.setEnabled(True)
        self.txtnomfornecedor.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btneditar.setEnabled(False)
        self.btnguardar.setVisible(True)
        self.btnguardar.setEnabled(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def editar(self):
        self.bnd = 1
        self.txtnomfornecedor.setEnabled(True)
        self.txtnomfornecedor.setFocus()
        self.btnnovo.setEnabled(False)
        self.btneditar.setVisible(False)
        self.btnguardar.setEnabled(True)
        self.btnguardar.setVisible(True)
        self.btneliminar.setEnabled(False)
        self.btncancelar.setEnabled(True)

    def cancelar(self):
        self.txtnomfornecedor.setEnabled(False)
        self.txtnomfornecedor.clear()
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
        nom = str(self.txtnomfornecedor.text())
        if len(nom) > 3:
            con = self.conexion.conectar()
            cur = con.cursor()
            if self.bnd == 0:
                cur.execute('insert into fornecedor (nomfornecedor) values(%s)', [nom])
            else:
                cur.execute('update fornecedor set nomfornecedor=%s where codfornecedor=%s', [nom, cod])
            con.commit()
            self.cancelar()
            self.consultar()
        else:
            QtWidgets.QMessageBox.information(self, "Caracteres insuficientes",
                                                    "Um campo nao cumpre os requisitos", QtWidgets.QMessageBox.Ok)

    def config(self, rows):
        lista = 'Codigo', 'Fornecedor'
        self.tabla.setColumnCount(2)
        self.tabla.setRowCount(int(rows[0]))
        self.tabla.setHorizontalHeaderLabels(lista)
        self.tabla.setColumnWidth(0, 50)
        self.tabla.setColumnWidth(1, 319)

    def consultar(self):
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from fornecedor')
        rows = cur.fetchone()

        if int(rows[0]) > 0:
            self.lblsinreg.setVisible(False)
            self.config(rows)
            cur.execute('select codfornecedor, nomfornecedor from fornecedor order by codfornecedor asc')
            self.fornecedor = cur.fetchall()

            for i in range(int(rows[0])):
                item = self.fornecedor[i]
                self.tabla.setItem(i, 0, QtWidgets.QTableWidgetItem(str(item[0])))
                self.tabla.setItem(i, 1, QtWidgets.QTableWidgetItem(str(item[1])))
        else:
            self.lblsinreg.setVisible(True)
            self.tabla.setRowCount(0)
            self.tabla.setColumnCount(0)

    def cargar(self):
        self.cancelar()
        index = int(self.lblindice.text())
        item = self.fornecedor[index]
        self.txtcod.setText(str(item[0]))
        self.txtnomfornecedor.setText(str(item[1]))
        self.btnguardar.setVisible(False)
        self.btneditar.setVisible(True)
        self.btneditar.setEnabled(True)
        self.btneliminar.setEnabled(True)

    def eliminar(self):
        cod = int(self.txtcod.text())
        con = self.conexion.conectar()
        cur = con.cursor()
        cur.execute('select count(*) from nota where codfornecedor=%s', [cod])
        #TODO: Arrumar aqui depois de criar notas delete
        rows = cur.fetchone()
        if int(rows[0]) == 0:
            if QtWidgets.QMessageBox.question(self, "Eliminando Registro",
                                              "Deseja Eliminar este Registro?", QtWidgets.QMessageBox.Yes,
                                              QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
                con = self.conexion.conectar()
                cur = con.cursor()
                cur.execute('delete from fornecedor where codfornecedor = %s', [cod])
                con.commit()
                self.cancelar()
                self.consultar()
                QtWidgets.QMessageBox.information(self, "Eliminando Registro",
                                                  "Registro Eliminado", QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.question(self, "Error ao eliminar registro",
                                           "Esse registro tem uma agencia registrada", QtWidgets.QMessageBox.Ok)


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = fornecedorApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
