# -*- coding: utf-8 -*-

# Formulario que Genera PDF

import os
import time
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from codeajuste import ajuste


class pdf:
    ajustador = ajuste()

    def generar(self, fechamin, fechamax, rows, movimento, bandera, positivo, negativo, suma, txttipo):

        fecha = time.strftime("%d/%m/%y")
        hora = time.strftime("%H:%M")
        # ----------------------

        # ----------------------
        titulo = ''
        if bandera == 0:

            titulo = ' de forma ' + txttipo

        elif bandera == 1:
            titulo = ' de forma ' + txttipo + ' entre ' + fechamin + ' e ' + fechamax
        # ----------------------

        c = canvas.Canvas("ListaCaixa.pdf", pagesize=landscape(A4))
        c.setFont("Courier", 9)
        co = 0
        rowsnegativo = 0
        rowspositivo = 0
        print(rows)

        for i in range(rows):
            item = movimento[i]
            if(float(item[2])<0):
                rowsnegativo = rowsnegativo + 1
            else:
                rowspositivo = rowspositivo + 1

        print(rowspositivo)
        print(rowsnegativo)

        if rowspositivo > 0:
            for i in range(rows):
                item = movimento[i]
                if (float(item[2]) > 0):
                    renglon = 450 - co

                    if renglon < 50:
                        renglon = 450
                        co = 0
                        c.showPage()

                    if renglon == 450:
                        c.setFont("Courier", 12)
                        c.drawString(300, 540, '     Sistema "SisCaixa"')
                        c.drawString(50, 560, ("Data: " + fecha))
                        c.drawString(700, 560, ("Hora: " + hora))

                        if bandera == 0:
                            c.drawString(0, 520, '                                   Registros positivos' + titulo)
                        else:
                            c.drawString(0, 520, '                   Registros positivos' + titulo)

                        c.drawString(0, 500, (
                            "____________________________________________________________________________________________________________________________"))
                        c.drawString(10, 480, (
                            "       Data            Valor      Descrição"))
                        c.drawString(0, 470, (
                            "____________________________________________________________________________________________________________________________"))

                    valorcero = self.ajustador.ajustarnum(str('%.2f' % (float(item[2]))), 10)
                    datacero = self.ajustador.ajustarstr(str(item[3]), 10)
                    descricaocero = self.ajustador.ajustarstr(str(item[4]), 75)
                    co = co + 20

                    c.drawString(0, renglon, (
                            '      ' + datacero + "     " + valorcero + "    " + descricaocero))

            sumacero = self.ajustador.ajustarnum(str('%.2f' % float(positivo)), 10)
            c.drawString(0, renglon - 20, (
                "____________________________________________________________________________________________________________________________"))
            c.drawString(11, renglon - 35, ("   Total:       " + sumacero))
            c.drawString(0, renglon - 40, (
                "____________________________________________________________________________________________________________________________"))
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

        if rowsnegativo > 0 and rowspositivo > 0:

            renglon = 450
            c.showPage()
            co = 0

        if rowsnegativo > 0:

            for i in range(rows):
                item = movimento[i]
                if(float(item[2]) < 0):
                    renglon = 450 - co

                    if renglon < 50:
                        renglon = 450
                        co = 0
                        c.showPage()

                    print(renglon)

                    if renglon == 450:
                        c.setFont("Courier", 12)
                        c.drawString(300, 540, '     Sistema "SisCaixa"')
                        c.drawString(50, 560, ("Data: " + fecha))
                        c.drawString(700, 560, ("Hora: " + hora))

                        if bandera == 0:
                            c.drawString(0, 520, '                                   Registros negativos' + titulo)
                        else:
                            c.drawString(0, 520, '                   Registros negativos' + titulo)

                        c.drawString(0, 500, (
                            "____________________________________________________________________________________________________________________________"))
                        c.drawString(10, 480, (
                            "       Data            Valor      Descrição"))
                        c.drawString(0, 470, (
                            "____________________________________________________________________________________________________________________________"))

                    valorcero = self.ajustador.ajustarnum(str('%.2f' % (float(item[2]))), 10)
                    datacero = self.ajustador.ajustarstr(str(item[3]), 10)
                    descricaocero = self.ajustador.ajustarstr(str(item[4]), 75)
                    co = co + 20

                    c.drawString(0, renglon, (
                            '      ' + datacero + "     " + valorcero + "    " + descricaocero))

            sumacero = self.ajustador.ajustarnum(str('%.2f' % float(negativo)), 10)
            c.drawString(0, renglon - 20, (
                "____________________________________________________________________________________________________________________________"))
            c.drawString(11, renglon - 35, ("   Total:       " + sumacero))
            c.drawString(0, renglon - 40, (
                "____________________________________________________________________________________________________________________________"))

            renglon = 450 - co

            # if renglon < 40:
            #     renglon = 450
            #     c.showPage()

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




        c.save()
        os.system("start ListaCaixa.pdf &")


if __name__ == "__main__":
    pdf().generar('19/01/2021', '26/01/2021', 3,
                  [(39, 'asdasdasd', '-613.90', '16/07/2021', 'Normal', 'asdasdasdasdasdadasdasd'),
                  (39, 'asdasdasd', '-613.90', '16/07/2021', 'Normal', 'asdasdasdasdasdadasdasd'),
                  (39, 'asdasdasd', '-613.90', '16/07/2021', 'Normal', 'asdasdasdasdasdadasdasd')],
                  1, 1000, 5000, 7000, 1)
