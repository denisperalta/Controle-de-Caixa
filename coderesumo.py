# -*- coding: utf-8 -*-

# Formulario que Genera PDF

import os
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from codeajuste import ajuste


class resumo:
    ajustador = ajuste()

    def generar(self, cod, mes, ano, nomcaixa, lista, anterior):


        fecha = time.strftime("%d/%m/%y")
        hora = time.strftime("%H:%M")

        # ----------------------
        titulo = 'Resumo dos lançamentos do caixa ' + nomcaixa[0] + ' no mês ' + str(mes + 1) + ' de ' + str(ano)

        # Pagamento 0
        # Venda com nota 1
        # Cheque emitido 2
        # Cheque devolvido 3
        # Deposito 4

        pagamento = '0'
        venda = '0'
        emitido = '0'
        devolvido = '0'
        deposito = '0'

        # print(lista)
        for i in lista:
            if(i[2] == 0):
                pagamento = i[1]
            if (i[2] == 1):
                venda = i[1]
            if (i[2] == 2):
                emitido = i[1]
            if (i[2] == 3):
                devolvido = i[1]
            if (i[2] == 4):
                deposito = i[1]

        total = float(anterior[0]) + float(pagamento) + float(venda) + float(emitido) + float(devolvido) + float(deposito)


        # print(pagamento + ' ' + venda + ' ' + emitido + ' ' + devolvido + ' ' + deposito)

        # ----------------------

        c = canvas.Canvas("Resumo.pdf", pagesize=landscape(A4))
        c.setFont("Courier", 9)
        co = 0

        renglon = 450 - co

        if renglon < 50:
            renglon = 450
            co = 0
            c.showPage()

        if renglon == 450:
            c.setFont("Courier", 12)
            # c.drawCentredString('Sistema "SisCaixa"')
            c.drawCentredString(400, 540, "Sistema SisCaixa")
            c.drawString(50, 560, ("Data: " + fecha))
            c.drawString(700, 560, ("Hora: " + hora))

            c.drawCentredString(400, 520, titulo)
            # c.drawCentredString()
            print('ok')

            c.drawString(0, 500, (
                "____________________________________________________________________________________________________________________________"))
            c.drawString(10, 480, (
                self.ajustador.ajustarstr("Saldo Anterior: ", 20) + self.ajustador.ajustarnum(str('%.2f' % (float(anterior[0]))), 12)))
            c.drawString(10, 460, (
                self.ajustador.ajustarstr("Venda a vista: ", 20) + self.ajustador.ajustarnum(str('%.2f' % (float(venda))), 12)))
            c.drawString(10, 440, (
                self.ajustador.ajustarstr("Cheques emitidos: ", 20) + self.ajustador.ajustarnum(str('%.2f' % (float(emitido))), 12)))
            c.drawString(10, 420, (
                self.ajustador.ajustarstr("Cheques devolvidos: ", 20) + self.ajustador.ajustarnum(str('%.2f' % (float(devolvido))), 12)))
            c.drawString(10, 400, (
                self.ajustador.ajustarstr("Depositos: ", 20) + self.ajustador.ajustarnum(str('%.2f' % (float(deposito))), 12)))
            c.drawString(10, 380, (
                    self.ajustador.ajustarstr("Pagamentos: ", 20) + self.ajustador.ajustarnum(str('%.2f' % (float(pagamento))), 12)))
            c.drawString(0, 370, (
                "____________________________________________________________________________________________________________________________"))
            c.drawString(10, 350, (
                self.ajustador.ajustarstr("TOTAL: ", 20) + self.ajustador.ajustarnum(str('%.2f' % (float(total))), 12)))

        # valorcero = self.ajustador.ajustarnum(str('%.2f' % (float(item[2]))), 10)
        # datacero = self.ajustador.ajustarstr(str(item[3]), 10)
        # descricaocero = self.ajustador.ajustarstr(str(item[4]), 75)
        # co = co + 20
        #
        # c.drawString(0, renglon, (
        #         '      ' + datacero + "     " + valorcero + "    " + descricaocero))
        #
        # sumacero = self.ajustador.ajustarnum(str('%.2f' % float(positivo)), 10)
        # c.drawString(0, renglon - 20, (
        #     "____________________________________________________________________________________________________________________________"))
        # c.drawString(11, renglon - 35, ("   Total:       " + sumacero))
        # c.drawString(0, renglon - 40, (
        #     "____________________________________________________________________________________________________________________________"))
        renglon = 450 - co

        # if renglon < 40:
        #     renglon = 450
        #     c.showPage()
        #
        # if renglon == 450:
        #     c.setFont("Courier", 9)
        #     c.drawString(230, 780, '     Sistema "SisCaixa"')
        #     c.drawString(50, 800, ("Data: " + fecha))
        #     c.drawString(480, 800, ("Hora: " + hora))
        #     c.drawString(0, 760, titulo)
        #     c.drawString(0, 740, (
        #         "____________________________________________________________________________________________________________________________"))
        #     c.drawString(10, 720, (
        #         "        Caixa             Valor             Data               Tipo                          Descrição"))
        #
        #     c.drawString(0, 710, (
        #         "____________________________________________________________________________________________________________________________"))

    # ---------------------------- PARA OS SALDOS NEGATIVOS -----------------------------------






        c.save()
        os.system("start Resumo.pdf &")


if __name__ == "__main__":
    resumo().generar('19/01/2021', '26/01/2021', 3,
                  [(39, 'asdasdasd', '-613.90', '16/07/2021', 'Normal', 'asdasdasdasdasdadasdasd'),
                  (39, 'asdasdasd', '-613.90', '16/07/2021', 'Normal', 'asdasdasdasdasdadasdasd'),
                  (39, 'asdasdasd', '-613.90', '16/07/2021', 'Normal', 'asdasdasdasdasdadasdasd')],
                  1, 1000, 5000, 7000, 1)
