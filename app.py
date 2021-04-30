#**********************************IMPORT
from xlrd import open_workbook
from xlutils.copy import copy
from numpy.lib import index_tricks
import pandas as pd
import numpy as np
import os
import time
import math
from datetime import datetime
from openpyxl import Workbook
from pandas.core.reshape.pivot import pivot
#**********************************PDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
#**********************************IMPORT
from flask import Flask
from flask import render_template, send_file
from funciones import numero_letras as numerosLetras
from funciones.estados import chihuahua as chihuahua
from funciones.estados import colima as colima
from funciones.estados import guerrero as guerrero
from funciones.estados import sanLuisPotosi as sanLuisPotosi
from funciones.estados import jalisco as jalisco

app=Flask(__name__)
@app.route('/zacatecas')
def index():    
    # -*- coding: utf-8 -*-
    """
    Created on Mon Apr  5 18:41:52 2021
    @author: eduardo.guerrero
    """
    #**********************************FUNCIONES VOTOS
    def fraccionVotos(votosTotalCoalicion, dividendo):
        fracicion = votosTotalCoalicion/dividendo
        fracicion = math.floor(fracicion)
        #print("1-->" + str (fracicion))
        return fracicion
    #********************************************************************
    def fraccionSobrante(votosTotalCoalicion, dividendo):
        fracicion = votosTotalCoalicion/dividendo
        fracicion = math.floor(fracicion)
        fraccionSobranteR = votosTotalCoalicion-fracicion*dividendo
        #print("2-->" + str (fraccionSobranteR))
        return fraccionSobranteR
    #**********************************
    def divicionDeVotos(fraccionVotos, partidos):
        for part in partidos:
            sumaCol[part] = sumaCol[part] + fraccionVotos
    #**********************************
    def divicionDeVotosSobranteUno(fraccionSobrante, partidos):
        if(sumaCol[partidos[0]] == sumaCol[partidos[1]]):
            sumaCol[partidos[0]] = sumaCol[partidos[0]] + fraccionSobrante
        else:
            partidoMayor = elMayor(partidos)
            sumaCol[partidoMayor] = sumaCol[partidoMayor] + fraccionSobrante

    #**********************************
    def divicionDeVotosSobranteDos(fraccionSobrante, partidos):
        if( fraccionSobrante == 2  )    :
            fraccionSobrante = fraccionSobrante -1
            if(sumaCol[partidos[0]] == sumaCol[partidos[1]] and
            sumaCol[partidos[0]] == sumaCol[partidos[2]]):
                sumaCol[partidos[0]] = sumaCol[partidos[0]] + fraccionSobrante
                sumaCol[partidos[1]] = sumaCol[partidos[1]] + fraccionSobrante
            else:
                partidoMayor = elMayor(partidos)
                sumaCol[partidoMayor] = sumaCol[partidoMayor] + fraccionSobrante
                if(len(partidos) > 2 ):
                    partidos.remove(partidoMayor)
                divicionDeVotosSobranteUno(fraccionSobrante, partidos)
        else:
            divicionDeVotosSobranteUno(fraccionSobrante, partidos)
    #**********************************
    def divicionDeVotosSobranteTres(fraccionSobrante, partidos):
        if( fraccionSobrante == 3 ):
            fraccionSobrante = fraccionSobrante - 2
            if(sumaCol[partidos[0]] == sumaCol[partidos[1]] and
            sumaCol[partidos[0]] == sumaCol[partidos[2]] and
            sumaCol[partidos[0]] == sumaCol[partidos[3]]):
                sumaCol[partidos[0]] = sumaCol[partidos[0]] + fraccionSobrante
                sumaCol[partidos[1]] = sumaCol[partidos[1]] + fraccionSobrante
                sumaCol[partidos[2]] = sumaCol[partidos[3]] + fraccionSobrante
            else:
                partidoMayor = elMayor(partidos)
                sumaCol[partidoMayor] = sumaCol[partidoMayor] + fraccionSobrante
                if(len(partidos) > 3 ):
                    partidos.remove(partidoMayor)
                divicionDeVotosSobranteDos(fraccionSobrante+1, partidos)
        else:
            divicionDeVotosSobranteDos(fraccionSobrante, partidos)

    #**********************************
    def elMayor(partidos):
        elMayorNum=0
        elMayorStr=""
        for part in partidos:
            if(sumaCol[part] > elMayorNum):
                elMayorNum = sumaCol[part]
                elMayorStr = part
                #print(sumaCol[part])
            #else:
                #print("NADA")
        return elMayorStr
    #**********************************
    def excel01():
        sumaColExcel01=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]
        totalDefExc = math.floor(sumaColExcel01['PAN']) + math.floor(sumaColExcel01['PRI']) + math.floor(sumaColExcel01['PRD']) + math.floor(sumaColExcel01['PT']) + math.floor(sumaColExcel01['VERDE']) + math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']) + math.floor(sumaColExcel01['MORENA']) + math.floor(sumaColExcel01['NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PAZ']) + math.floor(sumaColExcel01['DIGNIDAD']) + math.floor(sumaColExcel01['PP']) + math.floor(sumaColExcel01['LA_FAMILIA']) + math.floor(sumaColExcel01['PES']) + math.floor(sumaColExcel01['RSP']) + math.floor(sumaColExcel01['FUERZA_POR_MEXICO']) + math.floor(sumaColExcel01['PAN_PRI_PRD']) + math.floor(sumaColExcel01['PAN_PRI']) + math.floor(sumaColExcel01['PAN_PRD']) + math.floor(sumaColExcel01['PRI_PRD']) + math.floor(sumaColExcel01['PT_VERDE_MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PT_VERDE_MORENA']) + math.floor(sumaColExcel01['PT_VERDE_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PT_MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['VERDE_MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PT_VERDE']) + math.floor(sumaColExcel01['PT_MORENA']) + math.floor(sumaColExcel01['PT_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['VERDE_MORENA']) + math.floor(sumaColExcel01['VERDE_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaColExcel01['VOTOS_NULOS'])
        datos=(
        ('PAN', math.floor(sumaColExcel01['PAN']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN']))),
        ('PRI', math.floor(sumaColExcel01['PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI']))),
        ('PRD', math.floor(sumaColExcel01['PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRD']))),
        ('PT', math.floor(sumaColExcel01['PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT']))),
        ('VERDE', math.floor(sumaColExcel01['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE']))),
        ('MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']))),
        ('MORENA', math.floor(sumaColExcel01['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA']))),
        ('NUEVA ALIANZA', math.floor(sumaColExcel01['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['NUEVA_ALIANZA']))),
        ('PAZ', math.floor(sumaColExcel01['PAZ']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAZ']))),
        ('DIGNIDAD', math.floor(sumaColExcel01['DIGNIDAD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['DIGNIDAD']))),
        ('PP', math.floor(sumaColExcel01['PP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PP']))),
        ('LA FAMILIA', math.floor(sumaColExcel01['LA_FAMILIA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['LA_FAMILIA']))),
        ('PES', math.floor(sumaColExcel01['PES']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PES']))),
        ('RSP', math.floor(sumaColExcel01['RSP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['RSP']))),
        ('FUERZA POR MEXICO', math.floor(sumaColExcel01['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['FUERZA_POR_MEXICO']))),
        ('PAN_PRI_PRD', math.floor(sumaColExcel01['PAN_PRI_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI_PRD']))),
        ('PAN_PRI', math.floor(sumaColExcel01['PAN_PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI']))),
        ('PAN_PRD', math.floor(sumaColExcel01['PAN_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRD']))),
        ('PRI_PRD', math.floor(sumaColExcel01['PRI_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI_PRD']))),
        ('PT_VERDE_MORENA_NUEVA_ALIANZA', math.floor(sumaColExcel01['PT_VERDE_MORENA_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_VERDE_MORENA_NUEVA_ALIANZA']))),
        ('PT_VERDE_MORENA', math.floor(sumaColExcel01['PT_VERDE_MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_VERDE_MORENA']))),
        ('PT_VERDE_NUEVA_ALIANZA', math.floor(sumaColExcel01['PT_VERDE_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_VERDE_NUEVA_ALIANZA']))),
        ('PT_MORENA_NUEVA_ALIANZA', math.floor(sumaColExcel01['PT_MORENA_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_MORENA_NUEVA_ALIANZA']))),
        ('VERDE_MORENA_NUEVA_ALIANZA', math.floor(sumaColExcel01['VERDE_MORENA_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE_MORENA_NUEVA_ALIANZA']))),
        ('PT_VERDE', math.floor(sumaColExcel01['PT_VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_VERDE']))),
        ('PT_MORENA', math.floor(sumaColExcel01['PT_MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_MORENA']))),
        ('PT_NUEVA_ALIANZA', math.floor(sumaColExcel01['PT_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_NUEVA_ALIANZA']))),
        ('VERDE_MORENA', math.floor(sumaColExcel01['VERDE_MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE_NUEVA_ALIANZA']))),
        ('VERDE_NUEVA_ALIANZA', math.floor(sumaColExcel01['VERDE_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE_NUEVA_ALIANZA']))),
        ('MORENA_NUEVA_ALIANZA', math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA']))),
        ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']))),
        ('VOTOS_NULOS', math.floor(sumaColExcel01['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VOTOS_NULOS']))),
        ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
        )
        print(datos)
        #rb = open_workbook('Zacatecas.xls',formatting_info=True)
        #wb = copy(rb)
        #sheet = wb.get_sheet('dato')
        #sheet.write(0,0,dia)
        #sheet.write(0,1,hora)
        #sheet.write(1,0,"VOTOS GENERAL")
        #row1=2
        #row2=2
        #for dato in zip(datos):
        #    sheet.write(row1, 1, str(dato[0][0]))
        #    sheet.write(row2, 0, dato[0][1])
        #    row1 = row1 + 1
        #    row2 = row2 + 1
        #wb.save('Zacatecas.xls')
        return datos
    #**********************************
    def excel02():        
        totalDefExc = math.floor(sumaCol['PAN']) + math.floor(sumaCol['PRI']) + math.floor(sumaCol['PRD']) + math.floor(sumaCol['PT']) + math.floor(sumaCol['VERDE']) + math.floor(sumaCol['MOVIMIENTO_CIUDADANO']) + math.floor(sumaCol['MORENA']) + math.floor(sumaCol['NUEVA_ALIANZA']) + math.floor(sumaCol['PAZ']) + math.floor(sumaCol['DIGNIDAD']) + math.floor(sumaCol['PP']) + math.floor(sumaCol['LA_FAMILIA']) + math.floor(sumaCol['PES']) + math.floor(sumaCol['RSP']) + math.floor(sumaCol['FUERZA_POR_MEXICO']) + math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaCol['VOTOS_NULOS'])
        datos=[
        ('PAN', math.floor(sumaCol['PAN']),numerosLetras.numero_a_letras(math.floor(sumaCol['PAN']))),
        ('PRI', math.floor(sumaCol['PRI']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRI']))),
        ('PRD', math.floor(sumaCol['PRD']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRD']))),
        ('PT', math.floor(sumaCol['PT']),numerosLetras.numero_a_letras(math.floor(sumaCol['PT']))),
        ('VERDE', math.floor(sumaCol['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaCol['VERDE']))),
        ('MOVIMIENTO CIUDADANO', math.floor(sumaCol['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MOVIMIENTO_CIUDADANO']))),
        ('MORENA', math.floor(sumaCol['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaCol['MORENA']))),
        ('NUEVA ALIANZA', math.floor(sumaCol['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaCol['NUEVA_ALIANZA']))),
        ('PAZ', math.floor(sumaCol['PAZ']),numerosLetras.numero_a_letras(math.floor(sumaCol['PAZ']))),
        ('DIGNIDAD', math.floor(sumaCol['DIGNIDAD']),numerosLetras.numero_a_letras(math.floor(sumaCol['DIGNIDAD']))),
        ('PP', math.floor(sumaCol['PP']),numerosLetras.numero_a_letras(math.floor(sumaCol['PP']))),
        ('LA FAMILIA', math.floor(sumaCol['LA_FAMILIA']),numerosLetras.numero_a_letras(math.floor(sumaCol['LA_FAMILIA']))),
        ('PES', math.floor(sumaCol['PES']),numerosLetras.numero_a_letras(math.floor(sumaCol['PES']))),
        ('RSP', math.floor(sumaCol['RSP']),numerosLetras.numero_a_letras(math.floor(sumaCol['RSP']))),
        ('FUERZA POR MEXICO', math.floor(sumaCol['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaCol['FUERZA_POR_MEXICO']))),
        ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']))),
        ('VOTOS_NULOS', math.floor(sumaCol['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['VOTOS_NULOS']))),
        ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
        ]
        #rb = open_workbook('Zacatecas.xls',formatting_info=True)
        #wb = copy(rb)
        #sheet = wb.get_sheet('dato')
        #sheet.write(1,3,"Votos Fracionados")
        #row1=2
        #row2=2
        #for dato in zip(datos):
        #    sheet.write(row1, 4, str(dato[0][0]))
        #    sheet.write(row2, 3, dato[0][1])
        #    row1 = row1 + 1
        #    row2 = row2 + 1
        #wb.save('Zacatecas.xls')
        return datos
    #**********************************                
    def excel03():    
        sumaColExcel01Excel01=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]    
        datos=[
        (
            'PAN_PRI_PRD', math.floor(sumaColExcel01Excel01['PAN'] + sumaColExcel01Excel01['PRI']  + sumaColExcel01Excel01['PRD'] + sumaColExcel01Excel01['PAN_PRI'] + sumaColExcel01Excel01['PAN_PRD'] + sumaColExcel01Excel01['PRI_PRD'] + sumaColExcel01Excel01['PAN_PRI_PRD']),
            numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['PAN'] + sumaColExcel01Excel01['PRI']  + sumaColExcel01Excel01['PRD'] + sumaColExcel01Excel01['PAN_PRI'] + sumaColExcel01Excel01['PAN_PRD'] + sumaColExcel01Excel01['PRI_PRD'] + sumaColExcel01Excel01['PAN_PRI_PRD']))
        ),
        (
            'PT_VERDE_MORENA_NUEVA_ALIANZA', math.floor(sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['VERDE'] +  sumaColExcel01Excel01['MORENA'] +  sumaColExcel01Excel01['NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_VERDE_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_VERDE_MORENA'] + sumaColExcel01Excel01['PT_VERDE_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['VERDE_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_VERDE'] + sumaColExcel01Excel01['PT_MORENA'] + sumaColExcel01Excel01['PT_NUEVA_ALIANZA'] + sumaColExcel01Excel01['VERDE_MORENA'] + sumaColExcel01Excel01['VERDE_NUEVA_ALIANZA'] + sumaColExcel01Excel01['MORENA_NUEVA_ALIANZA'] ),
            numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['VERDE'] +  sumaColExcel01Excel01['MORENA'] +  sumaColExcel01Excel01['NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_VERDE_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_VERDE_MORENA'] + sumaColExcel01Excel01['PT_VERDE_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['VERDE_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_VERDE'] + sumaColExcel01Excel01['PT_MORENA'] + sumaColExcel01Excel01['PT_NUEVA_ALIANZA'] + sumaColExcel01Excel01['VERDE_MORENA'] + sumaColExcel01Excel01['VERDE_NUEVA_ALIANZA'] + sumaColExcel01Excel01['MORENA_NUEVA_ALIANZA'] ))
        ),
        (
            'MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO'])
        ),
        (
            'PAZ', math.floor(sumaColExcel01Excel01['PAZ']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['PAZ'])
        ),
        (
            'DIGNIDAD', math.floor(sumaColExcel01Excel01['DIGNIDAD']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['DIGNIDAD'])
        ),
        (
            'PP', math.floor(sumaColExcel01Excel01['PP']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['PP'])
        ),
        (
            'LA FAMILIA', math.floor(sumaColExcel01Excel01['LA_FAMILIA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['LA_FAMILIA'])
        ),
        (
            'PES', math.floor(sumaColExcel01Excel01['PES']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['PES'])
        ),
        (
            'RSP', math.floor(sumaColExcel01Excel01['RSP']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['RSP'])
        ),
        (
            'FUERZA POR MEXICO', math.floor(sumaColExcel01Excel01['FUERZA_POR_MEXICO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['FUERZA_POR_MEXICO'])
        ),
        (
            'CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01Excel01['CANDIDATOS_NO_REGISTRADOS']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['CANDIDATOS_NO_REGISTRADOS'])
        ),
        (
            'VOTOS_NULOS', math.floor(sumaColExcel01Excel01['VOTOS_NULOS']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['VOTOS_NULOS'])
        )
        ]
        return datos
    #**********************************VAR
    partidos=[]
    estado='Zacatecas'
    coalicionDeCuatroPartidoUno=""
    coalicionDeCuatroPartidoDos=""
    coalicionDeCuatroPartidoTres=""
    coalicionDeCuatroPartidoCuatro=""
    coalicionDeCuatroPargtidos=""
    coalicionDeTresPartidoUno=""
    coalicionDeTresPartidoDos=""
    coalicionDeTresPartidoTres=""
    coalicionDeTresPartidos=""
    coalicionDeDosPartidoUno=""
    coalicionDeDosPartidoDos=""
    coalicionDeDosPartidos=""
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    #**********************************ARCHIVO
    vmre=pd.ExcelFile('C:/Users/eduardo.guerrero/OneDrive - Instituto Nacional Electoral/vmre/vmre.xlsx')
    df=vmre.parse('Hoja1')
    #**********************************AGRUPAR
    sumaCol=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]
    print("Suma voto " + estado + " PAN = " + str(sumaCol['PAN']))
    print("Suma voto " + estado + " PRI = " + str(sumaCol['PRI']))
    print("Suma voto " + estado + " PRD = " + str(sumaCol['PRD']))
    print("Suma voto " + estado + " VERDE = " + str(sumaCol['VERDE']))
    print("Suma voto " + estado + " PT = " + str(sumaCol['PT']))
    print("Suma voto " + estado + " MOVIMIENTO_CIUDADANO = " + str(sumaCol['MOVIMIENTO_CIUDADANO']))
    print("Suma voto " + estado + " MORENA = " + str(sumaCol['MORENA']))
    print("Suma voto " + estado + " PES = " + str(sumaCol['PES']))
    print("Suma voto " + estado + " RSP = " + str(sumaCol['RSP']))
    print("Suma voto " + estado + " FUERZA_POR_MEXICO = " + str(sumaCol['FUERZA_POR_MEXICO']))
    print("Suma voto " + estado + " NUEVA_ALIANZA = " + str(sumaCol['NUEVA_ALIANZA']))
    ##
    print("Suma voto " + estado + " PAZ = " + str(sumaCol['PAZ']))
    print("Suma voto " + estado + " DIGNIDAD = " + str(sumaCol['DIGNIDAD']))
    print("Suma voto " + estado + " PP = " + str(sumaCol['PP']))
    print("Suma voto " + estado + " LA_FAMILIA = " + str(sumaCol['LA_FAMILIA']))
    print("Suma voto " + estado + " PAN_PRI_PRD = " + str(sumaCol['PAN_PRI_PRD']))
    print("Suma voto " + estado + " PAN_PRI = " + str(sumaCol['PAN_PRI']))
    print("Suma voto " + estado + " PAN_PRD = " + str(sumaCol['PAN_PRD']))
    print("Suma voto " + estado + " PRI_PRD = " + str(sumaCol['PRI_PRD']))
    print("Suma voto " + estado + " PT_VERDE_MORENA_NUEVA_ALIANZA = " + str(sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA']))
    print("Suma voto " + estado + " PT_VERDE_MORENA = " + str(sumaCol['PT_VERDE_MORENA']))
    print("Suma voto " + estado + " PT_VERDE_NUEVA_ALIANZA = " + str(sumaCol['PT_VERDE_NUEVA_ALIANZA']))
    print("Suma voto " + estado + " PT_MORENA_NUEVA_ALIANZA = " + str(sumaCol['PT_MORENA_NUEVA_ALIANZA']))
    print("Suma voto " + estado + " VERDE_MORENA_NUEVA_ALIANZA = " + str(sumaCol['VERDE_MORENA_NUEVA_ALIANZA']))
    print("Suma voto " + estado + " PT_VERDE = " + str(sumaCol['PT_VERDE']))
    print("Suma voto " + estado + " PT_MORENA = " + str(sumaCol['PT_MORENA']))
    print("Suma voto " + estado + " PT_NUEVA_ALIANZA = " + str(sumaCol['PT_NUEVA_ALIANZA']))
    print("Suma voto " + estado + " VERDE_MORENA = " + str(sumaCol['VERDE_MORENA']))
    print("Suma voto " + estado + " VERDE_NUEVA_ALIANZA = " + str(sumaCol['VERDE_NUEVA_ALIANZA']))
    print("Suma voto " + estado + " MORENA_NUEVA_ALIANZA = " + str(sumaCol['MORENA_NUEVA_ALIANZA']))
    #**********************************Fraccion Votos
    #fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA'], dividendo=4)
    #fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA'], dividendo=4)
    #**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRI_PRD'], dividendo=3), partidos=["PAN","PRI","PRD"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRI_PRD'], dividendo=3), partidos=["PAN","PRI","PRD"] )
    #**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRI'], dividendo=2), partidos=["PAN","PRI"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRI'], dividendo=2), partidos=["PAN","PRI"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRD'], dividendo=2), partidos=["PAN","PRD"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRD'], dividendo=2), partidos=["PAN","PRD"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PRI_PRD'], dividendo=2), partidos=["PRI","PRD"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PRI_PRD'], dividendo=2), partidos=["PRI","PRD"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA'], dividendo=4), partidos=["PT","VERDE","MORENA","NUEVA_ALIANZA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA'], dividendo=4), partidos=["PT","VERDE","MORENA","NUEVA_ALIANZA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA'], dividendo=3), partidos=["PT","VERDE","MORENA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA'], dividendo=3), partidos=["PT","VERDE","MORENA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE_NUEVA_ALIANZA'], dividendo=3), partidos=["PT","VERDE","NUEVA_ALIANZA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE_NUEVA_ALIANZA'], dividendo=3), partidos=["PT","VERDE","NUEVA_ALIANZA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_MORENA_NUEVA_ALIANZA'], dividendo=3), partidos=["PT","MORENA","NUEVA_ALIANZA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_MORENA_NUEVA_ALIANZA'], dividendo=3), partidos=["PT","MORENA","NUEVA_ALIANZA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['VERDE_MORENA_NUEVA_ALIANZA'], dividendo=3), partidos=["VERDE","MORENA","NUEVA_ALIANZA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['VERDE_MORENA_NUEVA_ALIANZA'], dividendo=3), partidos=["VERDE","MORENA","NUEVA_ALIANZA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE'], dividendo=2), partidos=["PT","VERDE"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE'], dividendo=2), partidos=["PT","VERDE"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_MORENA'], dividendo=2), partidos=["PT","MORENA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_MORENA'], dividendo=2), partidos=["PT","MORENA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_NUEVA_ALIANZA'], dividendo=2), partidos=["PT","NUEVA_ALIANZA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_NUEVA_ALIANZA'], dividendo=2), partidos=["PT","NUEVA_ALIANZA"] )
    ##**********************************
    #divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_NUEVA_ALIANZA'], dividendo=2), partidos=["PT","NUEVA_ALIANZA"])
    #divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_NUEVA_ALIANZA'], dividendo=2), partidos=["PT","NUEVA_ALIANZA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['VERDE_MORENA'], dividendo=2), partidos=["VERDE","MORENA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['VERDE_MORENA'], dividendo=2), partidos=["VERDE","MORENA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['VERDE_NUEVA_ALIANZA'], dividendo=2), partidos=["VERDE","NUEVA_ALIANZA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['VERDE_NUEVA_ALIANZA'], dividendo=2), partidos=["VERDE","NUEVA_ALIANZA"] )
    ##**********************************
    divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['MORENA_NUEVA_ALIANZA'], dividendo=2), partidos=["MORENA", "NUEVA_ALIANZA"])
    divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['MORENA_NUEVA_ALIANZA'], dividendo=2), partidos=["MORENA", "NUEVA_ALIANZA"] )
    #**********************************
    #**********************************VER FINAL
    print("\n")
    print("####### RESULTADOS FINALES #######")
    print("Suma voto " + estado + " PAN = " + str(sumaCol['PAN']))
    print("Suma voto " + estado + " PRI = " + str(sumaCol['PRI']))
    print("Suma voto " + estado + " PRD = " + str(sumaCol['PRD']))
    print("Suma voto " + estado + " VERDE = " + str(sumaCol['VERDE']))
    print("Suma voto " + estado + " PT = " + str(sumaCol['PT']))
    print("Suma voto " + estado + " MOVIMIENTO_CIUDADANO = " + str(sumaCol['MOVIMIENTO_CIUDADANO']))
    print("Suma voto " + estado + " MORENA = " + str(sumaCol['MORENA']))
    print("Suma voto " + estado + " PES = " + str(sumaCol['PES']))
    print("Suma voto " + estado + " RSP = " + str(sumaCol['RSP']))
    print("Suma voto " + estado + " FUERZA_POR_MEXICO = " + str(sumaCol['FUERZA_POR_MEXICO']))
    print("Suma voto " + estado + " NUEVA_ALIANZA = " + str(sumaCol['NUEVA_ALIANZA']))
    ##
    print("Suma voto " + estado + " PAZ = " + str(sumaCol['PAZ']))
    print("Suma voto " + estado + " DIGNIDAD = " + str(sumaCol['DIGNIDAD']))
    print("Suma voto " + estado + " PP = " + str(sumaCol['PP']))
    print("Suma voto " + estado + " LA_FAMILIA = " + str(sumaCol['LA_FAMILIA']))
    #*********************PDF
    return render_template("pdf/zacatecas.html", lalos = excel01(), lalos2 = excel02(), lalos3 = excel03(), dia = dia, hora=hora )  
    #*********************PDF
    path="C:/Users/eduardo.guerrero/Documents/ine/flask/vmre/funciones/estados/"
    tb1=excel01()
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(100, 370, tb1[0][2]) #letr
    can.drawString(280, 370, str(tb1[0][1])) #numero  350 3renglon
    can.drawString(100, 360, tb1[1][2]) #letr
    can.drawString(280, 360, str(tb1[1][1])) #numero  350 3renglon
    can.drawString(100, 350, tb1[2][2]) #letr
    can.drawString(280, 350, str(tb1[2][1])) #numero  350 3renglon
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(path+"pdfOrg/zacatecas.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(path+"pdfNew/zacatecas.pdf", "wb")
    output.write(outputStream)
    outputStream.close()

@app.route('/downloadZacatecas')
def downloadZacatecasF():
	path="C:/Users/eduardo.guerrero/Documents/ine/flask/vmre/funciones/estados/pdfNew/zacatecas.pdf"
	return send_file(path, as_attachment=True)


    
@app.route('/')
def laloInicio():
    return "VMRE 2021"

@app.route('/chihuahua')
def chihuahuaF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/chihuahua.html", lalos=chihuahua.excel01(), lalos2=chihuahua.excel02(), lalos3=chihuahua.excel03(), dia=dia, hora=hora )  



@app.route('/colima')
def colimaF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/colima.html", lalos=colima.excel01(), lalos2=colima.excel02(), lalos3=colima.excel03(), dia=dia, hora=hora )  

@app.route('/downloadColima')
def downloadColimaF():
	path="C:/Users/eduardo.guerrero/Documents/ine/flask/vmre/funciones/estados/pdfNew/colima.pdf"
	return send_file(path, as_attachment=True)



@app.route('/guerrero')
def guerreroF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/guerrero.html", lalos=guerrero.excel01(), lalos2=guerrero.excel02(), lalos3=guerrero.excel03(), dia=dia, hora=hora )  



@app.route('/sanLuisPotosi')
def sanLuisPotosiF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/sanLuisPotosi.html", lalos=sanLuisPotosi.excel01(), lalos2=sanLuisPotosi.excel02(), lalos3=sanLuisPotosi.excel03(), dia=dia, hora=hora )  



@app.route('/jalisco')
def jaliscoF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/jalisco.html", lalos=jalisco.excel01(), dia=dia, hora=hora )  



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)


