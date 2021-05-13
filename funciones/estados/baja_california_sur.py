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
    totalDefExc = math.floor(sumaColExcel01['UNIDOS_CONTIGO']) + math.floor(sumaColExcel01['PT']) + math.floor(sumaColExcel01['VERDE']) + math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']) + math.floor(sumaColExcel01['MORENA']) +  math.floor(sumaColExcel01['COHERENTE']) + math.floor(sumaColExcel01['NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PES']) + math.floor(sumaColExcel01['RSP']) + math.floor(sumaColExcel01['FUERZA_POR_MEXICO']) +  math.floor(sumaColExcel01['RAMON_PARRA']) + math.floor(sumaColExcel01['MORENA_PT'])  + math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaColExcel01['VOTOS_NULOS'])
    datos=(
    ('UNIDOS_CONTIGO', math.floor(sumaColExcel01['UNIDOS_CONTIGO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['UNIDOS_CONTIGO']))),
    ('PT', math.floor(sumaColExcel01['PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT']))),
    ('VERDE', math.floor(sumaColExcel01['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaColExcel01['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA']))),
    ('COHERENTE', math.floor(sumaColExcel01['COHERENTE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['COHERENTE']))),
    ('NUEVA_ALIANZA', math.floor(sumaColExcel01['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['NUEVA_ALIANZA']))),
    ('PES', math.floor(sumaColExcel01['PES']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PES']))),
    ('RSP', math.floor(sumaColExcel01['RSP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaColExcel01['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['FUERZA_POR_MEXICO']))),
    ('RAMON_PARRA', math.floor(sumaColExcel01['RAMON_PARRA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['RAMON_PARRA']))),
    ('MORENA_PT', math.floor(sumaColExcel01['MORENA_PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA_PT']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaColExcel01['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    print(datos)
    #rb = open_workbook('Baja_California_Sur.xls',formatting_info=True)
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
    #wb.save('Baja_California_Sur.xls')
    return datos
#**********************************
def excel02():        
    totalDefExc = math.floor(sumaCol['UNIDOS_CONTIGO']) + math.floor(sumaCol['PT']) + math.floor(sumaCol['VERDE']) + math.floor(sumaCol['MOVIMIENTO_CIUDADANO']) + math.floor(sumaCol['MORENA']) +  math.floor(sumaCol['COHERENTE']) + math.floor(sumaCol['NUEVA_ALIANZA']) + math.floor(sumaCol['PES']) + math.floor(sumaCol['RSP']) + math.floor(sumaCol['FUERZA_POR_MEXICO']) +  math.floor(sumaCol['RAMON_PARRA']) + math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaCol['VOTOS_NULOS'])
    datos=(
    ('UNIDOS_CONTIGO', math.floor(sumaCol['UNIDOS_CONTIGO']),numerosLetras.numero_a_letras(math.floor(sumaCol['UNIDOS_CONTIGO']))),
    ('PT', math.floor(sumaCol['PT']),numerosLetras.numero_a_letras(math.floor(sumaCol['PT']))),
    ('VERDE', math.floor(sumaCol['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaCol['VERDE']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaCol['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaCol['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaCol['MORENA']))),
    ('COHERENTE', math.floor(sumaCol['COHERENTE']),numerosLetras.numero_a_letras(math.floor(sumaCol['COHERENTE']))),
    ('NUEVA_ALIANZA', math.floor(sumaCol['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaCol['NUEVA_ALIANZA']))),
    ('PES', math.floor(sumaCol['PES']),numerosLetras.numero_a_letras(math.floor(sumaCol['PES']))),
    ('RSP', math.floor(sumaCol['RSP']),numerosLetras.numero_a_letras(math.floor(sumaCol['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaCol['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaCol['FUERZA_POR_MEXICO']))),
    ('RAMON_PARRA', math.floor(sumaCol['RAMON_PARRA']),numerosLetras.numero_a_letras(math.floor(sumaCol['RAMON_PARRA']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaCol['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #rb = open_workbook('Baja_California_Sur.xls',formatting_info=True)
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
    #wb.save('Baja_California_Sur.xls')
    return datos
#**********************************                
def excel03():    
    sumaColExcel01Excel01=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]    
    datos=[
    (
        'UNIDOS_CONTIGO', math.floor(sumaColExcel01Excel01['UNIDOS_CONTIGO']),
        numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['UNIDOS_CONTIGO']))
    ),
    (
        'MORENA_PT', math.floor(sumaColExcel01Excel01['MORENA_PT'] + sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['MORENA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MORENA_PT'] + sumaColExcel01Excel01['PT'] + sumaColExcel01Excel01['MORENA'])
    ),
    (
        'VERDE', math.floor(sumaColExcel01Excel01['VERDE']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['VERDE'])
    ),
    (
        'MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['MOVIMIENTO_CIUDADANO'])
    ),
    (
        'COHERENTE', math.floor(sumaColExcel01Excel01['COHERENTE']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['COHERENTE'])
    ),
    (
        'NUEVA_ALIANZA', math.floor(sumaColExcel01Excel01['NUEVA_ALIANZA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['NUEVA_ALIANZA'])
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
        'RAMON_PARRA', math.floor(sumaColExcel01Excel01['RAMON_PARRA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['RAMON_PARRA'])
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
estado='Baja_California_Sur'
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
#vmre=pd.ExcelFile('C:/Users/eduardo.guerrero/OneDrive - Instituto Nacional Electoral/vmre/vmre.xlsx')
vmre=pd.ExcelFile('C:/vmre/Aqui_datos/vmre.xlsx')
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
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['MORENA_PT'], dividendo=2), partidos=["PT","MORENA"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['MORENA_PT'], dividendo=2), partidos=["PT","MORENA"] )
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
path="C:/vmre/funciones/estados/"
tb1=excel01()
tb2=excel02()
tb3=excel03()
packet = io.BytesIO()
# create a new PDF with Reportlab
can = canvas.Canvas(packet, pagesize=letter)
can.drawString(133, 680, "Baja California Sur")
can.drawString(100, 665, str(hora))
can.drawString(253, 665, str(dia))
can.drawString(100, 650, "CENTRO DE ESCRUTINIO Y CÓMPUTO")
can.drawString(170, 405, tb1[0][2]) 
can.drawString(350, 405, str(tb1[0][1])) 
can.drawString(170, 380, tb1[1][2]) 
can.drawString(350, 380, str(tb1[1][1])) 
can.drawString(170, 355, tb1[2][2]) 
can.drawString(350, 355, str(tb1[2][1])) 
can.drawString(170, 330, tb1[3][2]) 
can.drawString(350, 330, str(tb1[3][1])) 
can.drawString(170, 305, tb1[4][2]) 
can.drawString(350, 305, str(tb1[4][1])) 
can.drawString(170, 280, tb1[5][2]) 
can.drawString(350, 280, str(tb1[5][1])) 
can.drawString(170, 255, tb1[6][2]) 
can.drawString(350, 255, str(tb1[6][1]))
can.drawString(170, 230, tb1[7][2]) 
can.drawString(350, 230, str(tb1[7][1]))  
can.drawString(170, 205, tb1[8][2]) 
can.drawString(350, 205, str(tb1[8][1]))  
can.drawString(170, 180, tb1[9][2]) 
can.drawString(350, 180, str(tb1[9][1]))  
can.drawString(170, 155, tb1[10][2]) 
can.drawString(350, 155, str(tb1[10][1]))  
can.drawString(170, 130, tb1[11][2]) 
can.drawString(350, 130, str(tb1[11][1]))  
can.drawString(170, 105, tb1[12][2]) 
can.drawString(350, 105, str(tb1[12][1]))  
can.drawString(170, 80, tb1[13][2]) 
can.drawString(350, 80, str(tb1[13][1]))  
can.drawString(170, 55, tb1[14][2]) 
can.drawString(350, 55, str(tb1[14][1]))  
#tb2  
can.drawString(590, 659, tb2[0][2]) 
can.drawString(760, 659, str(tb2[0][1]))  
can.drawString(590, 635, tb2[1][2]) 
can.drawString(760, 635, str(tb2[1][1]))  
can.drawString(590, 611, tb2[2][2]) 
can.drawString(760, 611, str(tb2[2][1]))  
can.drawString(590, 587, tb2[3][2]) 
can.drawString(760, 587, str(tb2[3][1]))  
can.drawString(590, 566, tb2[4][2]) 
can.drawString(760, 566, str(tb2[4][1]))  
can.drawString(590, 542, tb2[5][2]) 
can.drawString(760, 542, str(tb2[5][1]))  
can.drawString(590, 518, tb2[6][2]) 
can.drawString(760, 518, str(tb2[6][1]))  
can.drawString(590, 497, tb2[7][2]) 
can.drawString(760, 497, str(tb2[7][1]))  
can.drawString(590, 474, tb2[8][2]) 
can.drawString(760, 474, str(tb2[8][1]))  
can.drawString(590, 451, tb2[9][2]) 
can.drawString(760, 451, str(tb2[9][1]))  
can.drawString(590, 428, tb2[10][2]) 
can.drawString(760, 428, str(tb2[10][1]))  
can.drawString(590, 405, tb2[11][2]) 
can.drawString(760, 405, str(tb2[11][1]))  
can.drawString(590, 382, tb2[12][2]) 
can.drawString(760, 382, str(tb2[12][1])) 
can.drawString(590, 359, tb2[13][2]) 
can.drawString(760, 359, str(tb2[13][1])) 
#Tb3
can.drawString(590, 284, tb3[0][2]) 
can.drawString(760, 284, str(tb3[0][1]))  
can.drawString(590, 261, tb3[1][2]) 
can.drawString(760, 261, str(tb3[1][1]))  
can.drawString(590, 240, tb3[2][2]) 
can.drawString(760, 240, str(tb3[2][1]))  
can.drawString(590, 220, tb3[3][2]) 
can.drawString(760, 220, str(tb3[3][1]))  
can.drawString(590, 200, tb3[4][2]) 
can.drawString(760, 200, str(tb3[4][1]))  
can.drawString(590, 180, tb3[5][2]) 
can.drawString(760, 180, str(tb3[5][1]))  
can.drawString(590, 158, tb3[6][2]) 
can.drawString(760, 158, str(tb3[6][1]))  
can.drawString(590, 138, tb3[7][2]) 
can.drawString(760, 138, str(tb3[7][1]))  
can.drawString(590, 115, tb3[8][2]) 
can.drawString(760, 115, str(tb3[8][1]))  
can.drawString(590, 93, tb3[9][2]) 
can.drawString(760, 93, str(tb3[9][1]))  
can.drawString(590, 73, tb3[10][2]) 
can.drawString(760, 73, str(tb3[10][1]))  
can.drawString(590, 53, tb3[11][2]) 
can.drawString(760, 53, str(tb3[11][1]))  
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(path+"pdfOrg/baja_california_sur.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open(path+"pdfNew/baja_california_sur.pdf", "wb")
output.write(outputStream)
outputStream.close()

