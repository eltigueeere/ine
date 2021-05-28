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
    totalDefExc = math.floor(sumaColExcel01['PAN']) + math.floor(sumaColExcel01['PRI']) + math.floor(sumaColExcel01['PRD']) + math.floor(sumaColExcel01['PT']) + math.floor(sumaColExcel01['VERDE']) + math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']) + math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA_PARTIDO']) +  math.floor(sumaColExcel01['PES']) + math.floor(sumaColExcel01['RSP']) + math.floor(sumaColExcel01['FUERZA_POR_MEXICO']) +  math.floor(sumaColExcel01['CI_01_COLIMA']) + math.floor(sumaColExcel01['PAN_PRI_PRD']) + math.floor(sumaColExcel01['PAN_PRI']) + math.floor(sumaColExcel01['PAN_PRD']) + math.floor(sumaColExcel01['PRI_PRD']) + math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaColExcel01['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaColExcel01['PAN']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN']))),
    ('PRI', math.floor(sumaColExcel01['PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI']))),
    ('PRD', math.floor(sumaColExcel01['PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRD']))),
    ('VERDE', math.floor(sumaColExcel01['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE']))),
    ('PT', math.floor(sumaColExcel01['PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']))),
    ('MORENA_NUEVA_ALIANZA_PARTIDO', math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA_PARTIDO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA_PARTIDO']))),
    ('PES', math.floor(sumaColExcel01['PES']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PES']))),
    ('RSP', math.floor(sumaColExcel01['RSP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaColExcel01['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['FUERZA_POR_MEXICO']))),
    ('CI', math.floor(sumaColExcel01['CI_01_COLIMA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CI_01_COLIMA']))),
    ('PAN_PRI_PRD', math.floor(sumaColExcel01['PAN_PRI_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI_PRD']))),
    ('PAN_PRI', math.floor(sumaColExcel01['PAN_PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI']))),
    ('PAN_PRD', math.floor(sumaColExcel01['PAN_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRD']))),
    ('PRI_PRD', math.floor(sumaColExcel01['PRI_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI_PRD']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaColExcel01['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #print(datos)
    #rb = open_workbook('Colima.xls',formatting_info=True)
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
    #wb.save('Colima.xls')
    return datos
#**********************************
def excel02():        
    totalDefExc = math.floor(sumaCol['PAN']) + math.floor(sumaCol['PRI']) + math.floor(sumaCol['PRD']) + math.floor(sumaCol['PT']) + math.floor(sumaCol['VERDE']) + math.floor(sumaCol['MOVIMIENTO_CIUDADANO']) + math.floor(sumaCol['MORENA_NUEVA_ALIANZA_PARTIDO']) +  math.floor(sumaCol['PES']) + math.floor(sumaCol['RSP']) + math.floor(sumaCol['FUERZA_POR_MEXICO']) +  math.floor(sumaCol['CI_01_COLIMA']) + math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaCol['VOTOS_NULOS'])
    datos=[
    ('PAN', math.floor(sumaCol['PAN']),numerosLetras.numero_a_letras(math.floor(sumaCol['PAN']))),
    ('PRI', math.floor(sumaCol['PRI']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRI']))),
    ('PRD', math.floor(sumaCol['PRD']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRD']))),
    ('PT', math.floor(sumaCol['PT']),numerosLetras.numero_a_letras(math.floor(sumaCol['PT']))),
    ('VERDE', math.floor(sumaCol['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaCol['VERDE']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaCol['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MOVIMIENTO_CIUDADANO']))),
    ('MORENA_NUEVA_ALIANZA_PARTIDO', math.floor(sumaCol['MORENA_NUEVA_ALIANZA_PARTIDO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MORENA_NUEVA_ALIANZA_PARTIDO']))),
    ('PES', math.floor(sumaCol['PES']),numerosLetras.numero_a_letras(math.floor(sumaCol['PES']))),
    ('RSP', math.floor(sumaCol['RSP']),numerosLetras.numero_a_letras(math.floor(sumaCol['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaCol['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaCol['FUERZA_POR_MEXICO']))),
    ('CI', math.floor(sumaCol['CI_01_COLIMA']),numerosLetras.numero_a_letras(math.floor(sumaCol['CI_01_COLIMA']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaCol['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    ]
    #rb = open_workbook('Colima.xls',formatting_info=True)
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
    #wb.save('Colima.xls')
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
        'VERDE', math.floor(sumaColExcel01Excel01['VERDE']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['VERDE'])
    ),
    (
        'PT', math.floor(sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['MORENA'] + sumaColExcel01Excel01['NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_MORENA'] + sumaColExcel01Excel01['PT_NUEVA_ALIANZA'] + sumaColExcel01Excel01['MORENA_NUEVA_ALIANZA'] ), 
        numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['MORENA'] + sumaColExcel01Excel01['NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_MORENA_NUEVA_ALIANZA'] + sumaColExcel01Excel01['PT_MORENA'] + sumaColExcel01Excel01['PT_NUEVA_ALIANZA'] + sumaColExcel01Excel01['MORENA_NUEVA_ALIANZA'] ))
    ),
    (
        'MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO'])
    ),
    (
        'MORENA_NUEVA_ALIANZA_PARTIDO', math.floor(sumaColExcel01Excel01['MORENA_NUEVA_ALIANZA_PARTIDO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MORENA_NUEVA_ALIANZA_PARTIDO'])
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
        'CI', math.floor(sumaColExcel01Excel01['CI_01_COLIMA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['CI_01_COLIMA'])
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
estado='Colima'
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
can.drawString(60, 453, str(hora))
can.drawString(190, 453, str(dia))
can.drawString(30, 440, "CENTRO DE ESCRUTINIO Y CÓMPUTO")
can.drawString(90, 309, tb1[0][2]) 
can.drawString(280, 309, str(tb1[0][1])) 
can.drawString(90, 298, tb1[1][2]) 
can.drawString(280, 298, str(tb1[1][1])) 
can.drawString(90, 285, tb1[2][2]) 
can.drawString(280, 285, str(tb1[2][1])) 
can.drawString(90, 270, tb1[3][2]) 
can.drawString(280, 270, str(tb1[3][1])) 
can.drawString(90, 256, tb1[4][2]) 
can.drawString(280, 256, str(tb1[4][1])) 
can.drawString(90, 243, tb1[5][2]) 
can.drawString(280, 243, str(tb1[5][1])) 
can.drawString(90, 227, tb1[6][2]) 
can.drawString(280, 227, str(tb1[6][1]))
can.drawString(90, 213, tb1[7][2]) 
can.drawString(280, 213, str(tb1[7][1]))  
can.drawString(90, 200, tb1[8][2]) 
can.drawString(280, 200, str(tb1[8][1]))  
can.drawString(90, 186, tb1[9][2]) 
can.drawString(280, 186, str(tb1[9][1]))  
can.drawString(90, 173, tb1[10][2]) 
can.drawString(280, 173, str(tb1[10][1]))  
can.drawString(90, 160, tb1[11][2]) 
can.drawString(280, 160, str(tb1[11][1]))  
can.drawString(90, 148, tb1[12][2]) 
can.drawString(280, 148, str(tb1[12][1]))  
can.drawString(90, 132, tb1[13][2]) 
can.drawString(280, 132, str(tb1[13][1]))  
can.drawString(90, 118, tb1[14][2]) 
can.drawString(280, 118, str(tb1[14][1]))  
can.drawString(90, 105, tb1[15][2]) 
can.drawString(280, 105, str(tb1[15][1]))  
can.drawString(90, 90, tb1[16][2]) 
can.drawString(280, 90, str(tb1[16][1]))  
can.drawString(90, 77, tb1[17][2]) 
can.drawString(280, 77, str(tb1[17][1]))   
##tb2  
can.drawString(400, 490, tb2[0][2]) 
can.drawString(590, 490, str(tb2[0][1]))  
can.drawString(400, 477, tb2[1][2]) 
can.drawString(590, 477, str(tb2[1][1]))  
can.drawString(400, 460, tb2[2][2]) 
can.drawString(590, 460, str(tb2[2][1]))  
can.drawString(400, 444, tb2[3][2]) 
can.drawString(590, 444, str(tb2[3][1]))  
can.drawString(400, 428, tb2[4][2]) 
can.drawString(590, 428, str(tb2[4][1]))  
can.drawString(400, 413, tb2[5][2]) 
can.drawString(590, 413, str(tb2[5][1]))  
can.drawString(400, 395, tb2[6][2]) 
can.drawString(590, 395, str(tb2[6][1]))  
can.drawString(400, 380, tb2[7][2]) 
can.drawString(590, 380, str(tb2[7][1]))  
can.drawString(400, 363, tb2[8][2]) 
can.drawString(590, 363, str(tb2[8][1]))  
can.drawString(400, 346, tb2[9][2]) 
can.drawString(590, 346, str(tb2[9][1]))  
can.drawString(400, 330, tb2[10][2]) 
can.drawString(590, 330, str(tb2[10][1]))  
can.drawString(400, 313, tb2[11][2]) 
can.drawString(590, 313, str(tb2[11][1]))  
can.drawString(400, 298, tb2[12][2]) 
can.drawString(590, 298, str(tb2[12][1]))  
can.drawString(400, 280, tb2[13][2]) 
can.drawString(590, 280, str(tb2[13][1]))  
#Tb3
can.drawString(400, 235, tb3[0][2]) 
can.drawString(590, 235, str(tb3[0][1]))  
can.drawString(400, 221, tb3[1][2]) 
can.drawString(590, 221, str(tb3[1][1]))  
can.drawString(400, 207, tb3[2][2]) 
can.drawString(590, 207, str(tb3[2][1]))  
can.drawString(400, 191, tb3[3][2]) 
can.drawString(590, 191, str(tb3[3][1]))  
can.drawString(400, 177, tb3[4][2]) 
can.drawString(590, 177, str(tb3[4][1]))  
can.drawString(400, 158, tb3[5][2]) 
can.drawString(590, 158, str(tb3[5][1]))  
can.drawString(400, 145, tb3[6][2]) 
can.drawString(590, 145, str(tb3[6][1]))  
can.drawString(400, 128, tb3[7][2]) 
can.drawString(590, 128, str(tb3[7][1]))  
can.drawString(400, 111, tb3[8][2]) 
can.drawString(590, 111, str(tb3[8][1]))  
can.drawString(400, 93, tb3[9][2]) 
can.drawString(590, 93, str(tb3[9][1]))  
can.drawString(400, 78, tb3[10][2]) 
can.drawString(590, 78, str(tb3[10][1]))  
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(path+"pdfOrg/colima.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open(path+"pdfNew/colima.pdf", "wb")
output.write(outputStream)
outputStream.close()
print("Termina " + estado)