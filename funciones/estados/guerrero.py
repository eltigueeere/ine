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
    totalDefExc = math.floor(sumaColExcel01['PAN']) + math.floor(sumaColExcel01['PRI']) + math.floor(sumaColExcel01['PRD']) + math.floor(sumaColExcel01['PT']) + math.floor(sumaColExcel01['VERDE']) + math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']) + math.floor(sumaColExcel01['MORENA']) +  math.floor(sumaColExcel01['PES']) + math.floor(sumaColExcel01['RSP']) + math.floor(sumaColExcel01['FUERZA_POR_MEXICO']) +  math.floor(sumaColExcel01['CI_01_GUERRERO']) + math.floor(sumaColExcel01['PRI_PRD']) + math.floor(sumaColExcel01['PT_VERDE']) + math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaColExcel01['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaColExcel01['PAN']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN']))),
    ('PRI', math.floor(sumaColExcel01['PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI']))),
    ('PRD', math.floor(sumaColExcel01['PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRD']))),
    ('PT', math.floor(sumaColExcel01['PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT']))),
    ('VERDE', math.floor(sumaColExcel01['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaColExcel01['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA']))),
    ('PES', math.floor(sumaColExcel01['PES']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PES']))),
    ('RSP', math.floor(sumaColExcel01['RSP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaColExcel01['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['FUERZA_POR_MEXICO']))),
    ('CI', math.floor(sumaColExcel01['CI_01_GUERRERO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CI_01_GUERRERO']))),
    ('PRI_PRD', math.floor(sumaColExcel01['PRI_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI_PRD']))),
    ('PT_VERDE', math.floor(sumaColExcel01['PT_VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_VERDE']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaColExcel01['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #print(datos)
    #rb = open_workbook('Guerrero.xls',formatting_info=True)
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
    #wb.save('Guerrero.xls')
    return datos
#**********************************
def excel02():        
    totalDefExc = math.floor(sumaCol['PAN']) + math.floor(sumaCol['PRI']) + math.floor(sumaCol['PRD']) + math.floor(sumaCol['PT']) + math.floor(sumaCol['VERDE']) + math.floor(sumaCol['MOVIMIENTO_CIUDADANO']) + math.floor(sumaCol['MORENA']) +  math.floor(sumaCol['PES']) + math.floor(sumaCol['RSP']) + math.floor(sumaCol['FUERZA_POR_MEXICO']) +  math.floor(sumaCol['CI_01_GUERRERO']) + math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']) +  math.floor(sumaCol['VOTOS_NULOS'])
    datos=[
    ('PAN', math.floor(sumaCol['PAN']),numerosLetras.numero_a_letras(math.floor(sumaCol['PAN']))),
    ('PRI', math.floor(sumaCol['PRI']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRI']))),
    ('PRD', math.floor(sumaCol['PRD']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRD']))),
    ('PT', math.floor(sumaCol['PT']),numerosLetras.numero_a_letras(math.floor(sumaCol['PT']))),
    ('VERDE', math.floor(sumaCol['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaCol['VERDE']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaCol['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaCol['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaCol['MORENA']))),
    ('PES', math.floor(sumaCol['PES']),numerosLetras.numero_a_letras(math.floor(sumaCol['PES']))),
    ('RSP', math.floor(sumaCol['RSP']),numerosLetras.numero_a_letras(math.floor(sumaCol['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaCol['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaCol['FUERZA_POR_MEXICO']))),
    ('CI', math.floor(sumaCol['CI_01_GUERRERO']),numerosLetras.numero_a_letras(math.floor(sumaCol['CI_01_GUERRERO']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaCol['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    ]
    #rb = open_workbook('Guerrero.xls',formatting_info=True)
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
    #wb.save('Guerrero.xls')
    return datos
#**********************************                
def excel03():    
    sumaColExcel01Excel01=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]    
    datos=[
    (
        'PAN', math.floor(sumaColExcel01Excel01['PAN']),
        numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['PAN']))
    ),
    (
        'PRI_PRD', math.floor(sumaColExcel01Excel01['PRI'] + sumaColExcel01Excel01['PRD'] + sumaColExcel01Excel01['PRI_PRD']), numerosLetras.numero_a_letras( math.floor(sumaColExcel01Excel01['PRI'] + sumaColExcel01Excel01['PRD'] + sumaColExcel01Excel01['PRI_PRD']))
    ),
    (
        'PT_VERDE', math.floor(sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['VERDE'] + sumaColExcel01Excel01['PT_VERDE']), 
        numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['VERDE'] + sumaColExcel01Excel01['PT_VERDE']))
    ),
    (
        'MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO'])
    ),
    (
        'MORENA', math.floor(sumaColExcel01Excel01['MORENA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MORENA'])
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
        'CI', math.floor(sumaColExcel01Excel01['CI_01_GUERRERO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['CI_01_GUERRERO'])
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
estado='Guerrero'
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
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PRI_PRD'], dividendo=2), partidos=["PRI","PRD"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PRI_PRD'], dividendo=2), partidos=["PRI","PRD"] )
#***********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE'], dividendo=2), partidos=["PT","VERDE"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE'], dividendo=2), partidos=["PT","VERDE"] )
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
can.drawString(100, 493, "Guerrero")
can.drawString(60, 465, str(hora))
can.drawString(195, 465, str(dia))
can.drawString(30, 453, "CENTRO DE ESCRUTINIO Y CÓMPUTO")
can.drawString(90, 295, tb1[0][2]) 
can.drawString(280, 295, str(tb1[0][1])) 
can.drawString(90, 280, tb1[1][2]) 
can.drawString(280, 280, str(tb1[1][1])) 
can.drawString(90, 257, tb1[2][2]) 
can.drawString(280, 257, str(tb1[2][1])) 
can.drawString(90, 243, tb1[3][2]) 
can.drawString(280, 243, str(tb1[3][1])) 
can.drawString(90, 227, tb1[4][2]) 
can.drawString(280, 227, str(tb1[4][1])) 
can.drawString(90, 211, tb1[5][2]) 
can.drawString(280, 211, str(tb1[5][1])) 
can.drawString(90, 193, tb1[6][2]) 
can.drawString(280, 193, str(tb1[6][1]))
can.drawString(90, 173, tb1[7][2]) 
can.drawString(280, 173, str(tb1[7][1]))  
can.drawString(90, 155, tb1[8][2]) 
can.drawString(280, 155, str(tb1[8][1]))  
can.drawString(90, 139, tb1[9][2]) 
can.drawString(280, 139, str(tb1[9][1]))  
can.drawString(90, 122, tb1[10][2]) 
can.drawString(280, 122, str(tb1[10][1]))  
can.drawString(90, 105, tb1[11][2]) 
can.drawString(280, 105, str(tb1[11][1]))  
can.drawString(90, 87, tb1[12][2]) 
can.drawString(280, 87, str(tb1[12][1]))  
can.drawString(90, 73, tb1[13][2]) 
can.drawString(280, 73, str(tb1[13][1]))  
can.drawString(90, 54, tb1[14][2]) 
can.drawString(280, 54, str(tb1[14][1]))  
can.drawString(90, 39, tb1[15][2]) 
can.drawString(280, 39, str(tb1[15][1]))  
##tb2  
can.drawString(400, 510, tb2[0][2]) 
can.drawString(590, 510, str(tb2[0][1]))  
can.drawString(400, 490, tb2[1][2]) 
can.drawString(590, 490, str(tb2[1][1]))  
can.drawString(400, 474, tb2[2][2]) 
can.drawString(590, 474, str(tb2[2][1]))  
can.drawString(400, 456, tb2[3][2]) 
can.drawString(590, 456, str(tb2[3][1]))  
can.drawString(400, 440, tb2[4][2])
can.drawString(590, 440, str(tb2[4][1]))  
can.drawString(400, 417, tb2[5][2]) 
can.drawString(590, 417, str(tb2[5][1]))  
can.drawString(400, 400, tb2[6][2]) 
can.drawString(590, 400, str(tb2[6][1]))  
can.drawString(400, 384, tb2[7][2]) 
can.drawString(590, 384, str(tb2[7][1]))  
can.drawString(400, 367, tb2[8][2]) 
can.drawString(590, 367, str(tb2[8][1]))  
can.drawString(400, 350, tb2[9][2]) 
can.drawString(590, 350, str(tb2[9][1]))  
can.drawString(400, 334, tb2[10][2]) 
can.drawString(590, 334, str(tb2[10][1]))  
can.drawString(400, 315, tb2[11][2]) 
can.drawString(590, 315, str(tb2[11][1]))  
can.drawString(400, 298, tb2[12][2]) 
can.drawString(590, 298, str(tb2[12][1]))  
can.drawString(400, 278, tb2[13][2]) 
can.drawString(590, 278, str(tb2[13][1]))  
#Tb3
can.drawString(400, 230, tb3[0][2]) 
can.drawString(590, 230, str(tb3[0][1]))  
can.drawString(400, 212, tb3[1][2]) 
can.drawString(590, 212, str(tb3[1][1]))  
can.drawString(400, 193, tb3[2][2]) 
can.drawString(590, 193, str(tb3[2][1]))  
can.drawString(400, 175, tb3[3][2]) 
can.drawString(590, 175, str(tb3[3][1]))  
can.drawString(400, 157, tb3[4][2]) 
can.drawString(590, 157, str(tb3[4][1]))  
can.drawString(400, 137, tb3[5][2]) 
can.drawString(590, 137, str(tb3[5][1]))  
can.drawString(400, 117, tb3[6][2]) 
can.drawString(590, 117, str(tb3[6][1]))  
can.drawString(400, 97, tb3[7][2]) 
can.drawString(590, 97, str(tb3[7][1]))  
can.drawString(400, 77, tb3[8][2]) 
can.drawString(590, 77, str(tb3[8][1]))  
can.drawString(400, 57, tb3[9][2]) 
can.drawString(590, 57, str(tb3[9][1]))  
can.drawString(400, 37, tb3[10][2]) 
can.drawString(590, 37, str(tb3[10][1]))  
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(path+"pdfOrg/guerrero.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open(path+"pdfNew/guerrero.pdf", "wb")
output.write(outputStream)
outputStream.close()
print("Termina " + estado)