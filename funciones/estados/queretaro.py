#!/usr/bin/python
# -*- coding: utf-8 -*-

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
from funciones import numero_letras as numerosLetras
#**********************************PDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter



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
    totalDefExc = math.floor(sumaColExcel01['PAN']) + math.floor(sumaColExcel01['PRI']) + math.floor(sumaColExcel01['PRD']) + math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']) + math.floor(sumaColExcel01['VERDE']) + math.floor(sumaColExcel01['MORENA']) +  math.floor(sumaColExcel01['PT']) + math.floor(sumaColExcel01['QUERETARO_INDEPENDIENTE']) + math.floor(sumaColExcel01['PES']) + math.floor(sumaColExcel01['RSP']) + math.floor(sumaColExcel01['FUERZA_POR_MEXICO']) +  math.floor(sumaColExcel01['PAN_QUERETARO_INDEPENDIENTE']) + math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaColExcel01['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaColExcel01['PAN']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN']))),
    ('PRI', math.floor(sumaColExcel01['PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI']))),
    ('PRD', math.floor(sumaColExcel01['PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRD']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']))),
    ('VERDE', math.floor(sumaColExcel01['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE']))),
    ('MORENA', math.floor(sumaColExcel01['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA']))),
    ('PT', math.floor(sumaColExcel01['PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT']))),
    ('QUERETARO_INDEPENDIENTE', math.floor(sumaColExcel01['QUERETARO_INDEPENDIENTE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['QUERETARO_INDEPENDIENTE']))),
    ('PES', math.floor(sumaColExcel01['PES']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PES']))),
    ('RSP', math.floor(sumaColExcel01['RSP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaColExcel01['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['FUERZA_POR_MEXICO']))),
    ('PAN_QUERETARO_INDEPENDIENTE', math.floor(sumaColExcel01['PAN_QUERETARO_INDEPENDIENTE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_QUERETARO_INDEPENDIENTE']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaColExcel01['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #print(datos)
    #rb = open_workbook('Queretaro.xls',formatting_info=True)
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
    #wb.save('Queretaro.xls')
    return datos
#**********************************
def excel02():        
    totalDefExc = math.floor(sumaCol['PAN']) + math.floor(sumaCol['PRI']) + math.floor(sumaCol['PRD']) + math.floor(sumaCol['MOVIMIENTO_CIUDADANO']) + math.floor(sumaCol['VERDE']) + math.floor(sumaCol['MORENA']) +  math.floor(sumaCol['PT']) + math.floor(sumaCol['QUERETARO_INDEPENDIENTE']) + math.floor(sumaCol['PES']) + math.floor(sumaCol['RSP']) + math.floor(sumaCol['FUERZA_POR_MEXICO']) + math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaCol['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaCol['PAN']),numerosLetras.numero_a_letras(math.floor(sumaCol['PAN']))),
    ('PRI', math.floor(sumaCol['PRI']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRI']))),
    ('PRD', math.floor(sumaCol['PRD']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRD']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaCol['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MOVIMIENTO_CIUDADANO']))),
    ('VERDE', math.floor(sumaCol['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaCol['VERDE']))),
    ('MORENA', math.floor(sumaCol['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaCol['MORENA']))),
    ('PT', math.floor(sumaCol['PT']),numerosLetras.numero_a_letras(math.floor(sumaCol['PT']))),
    ('QUERETARO_INDEPENDIENTE', math.floor(sumaCol['QUERETARO_INDEPENDIENTE']),numerosLetras.numero_a_letras(math.floor(sumaCol['QUERETARO_INDEPENDIENTE']))),
    ('PES', math.floor(sumaCol['PES']),numerosLetras.numero_a_letras(math.floor(sumaCol['PES']))),
    ('RSP', math.floor(sumaCol['RSP']),numerosLetras.numero_a_letras(math.floor(sumaCol['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaCol['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaCol['FUERZA_POR_MEXICO']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaCol['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #rb = open_workbook('Queretaro.xls',formatting_info=True)
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
    #wb.save('Queretaro.xls')
    return datos
#**********************************                
def excel03():    
    sumaColExcel01Excel01=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]    
    datos=[
    (
        'PAN_QUERETARO_INDEPENDIENTE', math.floor(sumaColExcel01Excel01['PAN_QUERETARO_INDEPENDIENTE'] + sumaColExcel01Excel01['QUERETARO_INDEPENDIENTE'] + sumaColExcel01Excel01['PAN']),
        numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['PAN_QUERETARO_INDEPENDIENTE'] + sumaColExcel01Excel01['QUERETARO_INDEPENDIENTE'] + sumaColExcel01Excel01['PAN']))
    ),
    (
        'PRI', math.floor(sumaColExcel01Excel01['PRI']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['PRI'])
    ),
    (
        'PRD', math.floor(sumaColExcel01Excel01['PRD']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['PRD'])
    ),
    (
        'MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO'])
    ),
    (
        'VERDE', math.floor(sumaColExcel01Excel01['VERDE']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['VERDE'])
    ),
    (
        'MORENA', math.floor(sumaColExcel01Excel01['MORENA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MORENA'])
    ),
    (
        'PT', math.floor(sumaColExcel01Excel01['PT']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['PT'])
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
estado='Queretaro'
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
url=""
try:
    archivo = open('C:/vmre/vmre.cfg', 'r')
    ruta = archivo.read()
    url = ruta + "vmre.xlsx"
    print("Inicia " + estado)
except:
    print("Verificar la ruta --> " + url)
vmre = pd.ExcelFile(url)
df=vmre.parse('Hoja1')
#**********************************AGRUPAR
sumaCol=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]
#print("Suma voto " + estado + " PAN = " + str(sumaCol['PAN']))
#print("Suma voto " + estado + " PRI = " + str(sumaCol['PRI']))
#print("Suma voto " + estado + " PRD = " + str(sumaCol['PRD']))
#print("Suma voto " + estado + " VERDE = " + str(sumaCol['VERDE']))
#print("Suma voto " + estado + " PT = " + str(sumaCol['PT']))
#print("Suma voto " + estado + " MOVIMIENTO_CIUDADANO = " + str(sumaCol['MOVIMIENTO_CIUDADANO']))
#print("Suma voto " + estado + " MORENA = " + str(sumaCol['MORENA']))
#print("Suma voto " + estado + " PES = " + str(sumaCol['PES']))
#print("Suma voto " + estado + " RSP = " + str(sumaCol['RSP']))
#print("Suma voto " + estado + " FUERZA_POR_MEXICO = " + str(sumaCol['FUERZA_POR_MEXICO']))
#print("Suma voto " + estado + " NUEVA_ALIANZA = " + str(sumaCol['NUEVA_ALIANZA']))
###
#print("Suma voto " + estado + " PAZ = " + str(sumaCol['PAZ']))
#print("Suma voto " + estado + " DIGNIDAD = " + str(sumaCol['DIGNIDAD']))
#print("Suma voto " + estado + " PP = " + str(sumaCol['PP']))
#print("Suma voto " + estado + " LA_FAMILIA = " + str(sumaCol['LA_FAMILIA']))
#print("Suma voto " + estado + " PAN_PRI_PRD = " + str(sumaCol['PAN_PRI_PRD']))
#print("Suma voto " + estado + " PAN_PRI = " + str(sumaCol['PAN_PRI']))
#print("Suma voto " + estado + " PAN_PRD = " + str(sumaCol['PAN_PRD']))
#print("Suma voto " + estado + " PRI_PRD = " + str(sumaCol['PRI_PRD']))
#print("Suma voto " + estado + " PT_VERDE_MORENA_NUEVA_ALIANZA = " + str(sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA']))
#print("Suma voto " + estado + " PT_VERDE_MORENA = " + str(sumaCol['PT_VERDE_MORENA']))
#print("Suma voto " + estado + " PT_VERDE_NUEVA_ALIANZA = " + str(sumaCol['PT_VERDE_NUEVA_ALIANZA']))
#print("Suma voto " + estado + " PT_MORENA_NUEVA_ALIANZA = " + str(sumaCol['PT_MORENA_NUEVA_ALIANZA']))
#print("Suma voto " + estado + " VERDE_MORENA_NUEVA_ALIANZA = " + str(sumaCol['VERDE_MORENA_NUEVA_ALIANZA']))
#print("Suma voto " + estado + " PT_VERDE = " + str(sumaCol['PT_VERDE']))
#print("Suma voto " + estado + " PT_MORENA = " + str(sumaCol['PT_MORENA']))
#print("Suma voto " + estado + " PT_NUEVA_ALIANZA = " + str(sumaCol['PT_NUEVA_ALIANZA']))
#print("Suma voto " + estado + " VERDE_MORENA = " + str(sumaCol['VERDE_MORENA']))
#print("Suma voto " + estado + " VERDE_NUEVA_ALIANZA = " + str(sumaCol['VERDE_NUEVA_ALIANZA']))
#print("Suma voto " + estado + " MORENA_NUEVA_ALIANZA = " + str(sumaCol['MORENA_NUEVA_ALIANZA']))
#**********************************Fraccion Votos
#fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA'], dividendo=4)
#fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE_MORENA_NUEVA_ALIANZA'], dividendo=4)
#**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_QUERETARO_INDEPENDIENTE'], dividendo=2), partidos=["PAN","QUERETARO_INDEPENDIENTE"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_QUERETARO_INDEPENDIENTE'], dividendo=2), partidos=["PAN","QUERETARO_INDEPENDIENTE"] )
#**********************************
#**********************************VER FINAL
#print("\n")
#print("####### RESULTADOS FINALES #######")
#print("Suma voto " + estado + " PAN = " + str(sumaCol['PAN']))
#print("Suma voto " + estado + " PRI = " + str(sumaCol['PRI']))
#print("Suma voto " + estado + " PRD = " + str(sumaCol['PRD']))
#print("Suma voto " + estado + " VERDE = " + str(sumaCol['VERDE']))
#print("Suma voto " + estado + " PT = " + str(sumaCol['PT']))
#print("Suma voto " + estado + " MOVIMIENTO_CIUDADANO = " + str(sumaCol['MOVIMIENTO_CIUDADANO']))
#print("Suma voto " + estado + " MORENA = " + str(sumaCol['MORENA']))
#print("Suma voto " + estado + " PES = " + str(sumaCol['PES']))
#print("Suma voto " + estado + " RSP = " + str(sumaCol['RSP']))
#print("Suma voto " + estado + " FUERZA_POR_MEXICO = " + str(sumaCol['FUERZA_POR_MEXICO']))
#print("Suma voto " + estado + " NUEVA_ALIANZA = " + str(sumaCol['NUEVA_ALIANZA']))
###
#print("Suma voto " + estado + " PAZ = " + str(sumaCol['PAZ']))
#print("Suma voto " + estado + " DIGNIDAD = " + str(sumaCol['DIGNIDAD']))
#print("Suma voto " + estado + " PP = " + str(sumaCol['PP']))
#print("Suma voto " + estado + " LA_FAMILIA = " + str(sumaCol['LA_FAMILIA']))
#*********************PDF
path="C:/vmre/funciones/estados/"
tb1=excel01()
tb2=excel02()
tb3=excel03()
packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(70, 515, str(hora))
can.drawString(200, 515, str(dia))
can.drawString(50, 507, "CENTRO DE ESCRUTINIO Y CÓMPUTO")
can.drawString(150, 365, tb1[0][2]) 
can.drawString(280, 365, str(tb1[0][1])) 
can.drawString(150, 340, tb1[1][2]) 
can.drawString(280, 340, str(tb1[1][1])) 
can.drawString(150, 315, tb1[2][2]) 
can.drawString(280, 315, str(tb1[2][1])) 
can.drawString(150, 292, tb1[3][2]) 
can.drawString(280, 292, str(tb1[3][1])) 
can.drawString(150, 271, tb1[4][2]) 
can.drawString(280, 271, str(tb1[4][1])) 
can.drawString(150, 251, tb1[5][2]) 
can.drawString(280, 251, str(tb1[5][1])) 
can.drawString(150, 229, tb1[6][2]) 
can.drawString(280, 229, str(tb1[6][1]))
can.drawString(150, 205, tb1[7][2]) 
can.drawString(280, 205, str(tb1[7][1]))  
can.drawString(150, 181, tb1[8][2]) 
can.drawString(280, 181, str(tb1[8][1]))  
can.drawString(150, 161, tb1[9][2]) 
can.drawString(280, 161, str(tb1[9][1]))  
can.drawString(150, 136, tb1[10][2]) 
can.drawString(280, 136, str(tb1[10][1]))  
can.drawString(150, 115, tb1[11][2]) 
can.drawString(280, 115, str(tb1[11][1]))  
can.drawString(150, 91, tb1[12][2]) 
can.drawString(280, 91, str(tb1[12][1]))  
can.drawString(150, 69, tb1[13][2]) 
can.drawString(280, 69, str(tb1[13][1]))  
can.drawString(150, 47, tb1[14][2]) 
can.drawString(280, 47, str(tb1[14][1]))  
#tb2  
can.drawString(460, 517, tb2[0][2]) 
can.drawString(600, 517, str(tb2[0][1]))  
can.drawString(460, 497, tb2[1][2]) 
can.drawString(600, 497, str(tb2[1][1]))  
can.drawString(460, 477, tb2[2][2]) 
can.drawString(600, 477, str(tb2[2][1]))  
can.drawString(460, 457, tb2[3][2]) 
can.drawString(600, 457, str(tb2[3][1]))  
can.drawString(460, 439, tb2[4][2]) 
can.drawString(600, 439, str(tb2[4][1]))  
can.drawString(460, 422, tb2[5][2]) 
can.drawString(600, 422, str(tb2[5][1]))  
can.drawString(460, 405, tb2[6][2]) 
can.drawString(600, 405, str(tb2[6][1]))  
can.drawString(460, 387, tb2[7][2]) 
can.drawString(600, 387, str(tb2[7][1]))  
can.drawString(460, 370, tb2[8][2]) 
can.drawString(600, 370, str(tb2[8][1]))  
can.drawString(460, 352, tb2[9][2]) 
can.drawString(600, 352, str(tb2[9][1]))  
can.drawString(460, 334, tb2[10][2]) 
can.drawString(600, 334, str(tb2[10][1]))  
can.drawString(460, 317, tb2[11][2]) 
can.drawString(600, 317, str(tb2[11][1]))  
can.drawString(460, 298, tb2[12][2]) 
can.drawString(600, 298, str(tb2[12][1])) 
can.drawString(460, 279, tb2[13][2]) 
can.drawString(600, 279, str(tb2[13][1])) 
#Tb3
can.drawString(460, 235, tb3[0][2]) 
can.drawString(600, 235, str(tb3[0][1]))  
can.drawString(460, 219, tb3[1][2]) 
can.drawString(600, 219, str(tb3[1][1]))  
can.drawString(460, 200, tb3[2][2]) 
can.drawString(600, 200, str(tb3[2][1]))  
can.drawString(460, 183, tb3[3][2]) 
can.drawString(600, 183, str(tb3[3][1]))  
can.drawString(460, 166, tb3[4][2]) 
can.drawString(600, 166, str(tb3[4][1]))  
can.drawString(460, 149, tb3[5][2]) 
can.drawString(600, 149, str(tb3[5][1]))  
can.drawString(460, 132, tb3[6][2]) 
can.drawString(600, 132, str(tb3[6][1]))  
can.drawString(460, 115, tb3[7][2]) 
can.drawString(600, 115, str(tb3[7][1]))  
can.drawString(460, 98, tb3[8][2]) 
can.drawString(600, 98, str(tb3[8][1]))  
can.drawString(460, 79, tb3[9][2]) 
can.drawString(600, 79, str(tb3[9][1]))  
can.drawString(460, 61, tb3[10][2]) 
can.drawString(600, 61, str(tb3[10][1]))  
can.drawString(460, 42, tb3[11][2]) 
can.drawString(600, 42, str(tb3[11][1]))  
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(path+"pdfOrg/queretaro.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open(path+"pdfNew/queretaro.pdf", "wb")
output.write(outputStream)
outputStream.close()
print("Termina " + estado)