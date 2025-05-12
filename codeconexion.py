#!/usr/bin/python
# -*- coding: latin-1 -*-

import psycopg2
import sys
import easygui
#import MySQLdb
class conexion():

    def conectar(self):
        try:
            # con = psycopg2.connect("host='localhost' dbname='siscaixa' user='postgres' password='82647913'") # Local    
            con = psycopg2.connect("host='192.168.100.47' dbname='siscaixa' user='postgres' password='motor'") # Teste Server
            # con = psycopg2.connect("host='192.168.100.180' dbname='siscaixa' user='postgres' password='motor' connect_timeout=3") # Servidor SisCaixa
            con.set_client_encoding('LATIN1')  # or 'WIN1252', depending on your data

            return con
        except psycopg2.OperationalError:
            if easygui.ccbox('N�o foi poss�vel conectar ao servidor, restabele�a a conex�o e clique em continuar', 'Erro de conex�o'):
                self.conectar()
            else:
                sys.exit(0)

    def desconectar(self, con):
        if con:
            con.close()
