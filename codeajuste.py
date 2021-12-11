class ajuste:
    def ajustarstr(self, dato, lon):
        res = ""
        nom = ""
        if (len(dato)) > int(lon):
            for i in range(int(lon)):
                res = res + dato[i]
        else:
            var = int(lon) - len(dato)
            for i in range(var):
                nom = nom + ' '
            res = dato + nom
        return res
        # ------------------------

    def ajustarnum(self, dato, lon):
        res = ""
        nom = ""
        if (len(str(dato))) > int(lon):
            for i in range(int(lon)):
                res = res + dato[i]
        else:
            var = int(lon) - len(str(dato))
            for i in range(var):
                nom = nom + ' '
            res = nom + dato
        return res
