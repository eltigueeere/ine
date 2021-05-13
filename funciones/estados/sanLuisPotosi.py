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
    totalDefExc = math.floor(sumaColExcel01['PAN']) + math.floor(sumaColExcel01['PRI']) + math.floor(sumaColExcel01['PRD']) + math.floor(sumaColExcel01['PT']) + math.floor(sumaColExcel01['VERDE']) + math.floor(sumaColExcel01['CP']) + math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']) + math.floor(sumaColExcel01['MORENA']) + + math.floor(sumaColExcel01['NUEVA_ALIANZA']) +  math.floor(sumaColExcel01['PES']) + math.floor(sumaColExcel01['RSP']) + math.floor(sumaColExcel01['FUERZA_POR_MEXICO']) +  math.floor(sumaColExcel01['CI_01_SAN_LUIS_POTOSI']) + math.floor(sumaColExcel01['PAN_PRI_PRD_CP']) + math.floor(sumaColExcel01['PAN_PRI_PRD']) + math.floor(sumaColExcel01['PAN_PRI_CP']) + math.floor(sumaColExcel01['PAN_PRD_CP'])+ math.floor(sumaColExcel01['PRI_PRD_CP']) + math.floor(sumaColExcel01['PAN_PRI'])+ math.floor(sumaColExcel01['PAN_PRD']) + math.floor(sumaColExcel01['PAN_CP']) + math.floor(sumaColExcel01['PRI_PRD'])+ math.floor(sumaColExcel01['PRI_CP']) + math.floor(sumaColExcel01['PRD_CP'])+ math.floor(sumaColExcel01['PT_VERDE']) + math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaColExcel01['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaColExcel01['PAN']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN']))),
    ('PRI', math.floor(sumaColExcel01['PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI']))),
    ('PRD', math.floor(sumaColExcel01['PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRD']))),
    ('VERDE', math.floor(sumaColExcel01['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE']))),
    ('PT', math.floor(sumaColExcel01['PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT']))),
    ('CP', math.floor(sumaColExcel01['CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CP']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaColExcel01['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA']))),
    ('NUEVA ALIANZA', math.floor(sumaColExcel01['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['NUEVA_ALIANZA']))),
    ('PES', math.floor(sumaColExcel01['PES']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PES']))),
    ('RSP', math.floor(sumaColExcel01['RSP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaColExcel01['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['FUERZA_POR_MEXICO']))),
    ('CI', math.floor(sumaColExcel01['CI_01_SAN_LUIS_POTOSI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CI_01_SAN_LUIS_POTOSI']))),
    ('PAN_PRI_PRD_CP', math.floor(sumaColExcel01['PAN_PRI_PRD_CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI_PRD_CP']))),
    ('PAN_PRI_PRD', math.floor(sumaColExcel01['PAN_PRI_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI_PRD']))),
    ('PAN_PRI_CP', math.floor(sumaColExcel01['PAN_PRI_CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI_CP']))),
    ('PAN_PRD_CP', math.floor(sumaColExcel01['PAN_PRD_CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRD_CP']))),
    ('PRI_PRD_CP', math.floor(sumaColExcel01['PRI_PRD_CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI_PRD_CP']))),
    ('PAN_PRI', math.floor(sumaColExcel01['PAN_PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRI']))),
    ('PAN_PRD', math.floor(sumaColExcel01['PAN_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_PRD']))),
    ('PAN_CP', math.floor(sumaColExcel01['PAN_CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN_CP']))),
    ('PRI_PRD', math.floor(sumaColExcel01['PRI_PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI_PRD']))),
    ('PRI_CP', math.floor(sumaColExcel01['PRI_CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI_CP']))),
    ('PRD_CP', math.floor(sumaColExcel01['PRD_CP']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRD_CP']))),
    ('PT_VERDE', math.floor(sumaColExcel01['PT_VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT_VERDE']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaColExcel01['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    print(datos)
    #rb = open_workbook('San_Luis_Potosi.xls',formatting_info=True)
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
    #wb.save('San_Luis_Potosi.xls')
    return datos
#**********************************
def excel02():        
    totalDefExc = math.floor(sumaCol['PAN']) + math.floor(sumaCol['PRI']) + math.floor(sumaCol['PRD']) + math.floor(sumaCol['PT']) + math.floor(sumaCol['VERDE']) + math.floor(sumaCol['CP']) + math.floor(sumaCol['MOVIMIENTO_CIUDADANO']) + math.floor(sumaCol['MORENA']) + + math.floor(sumaCol['NUEVA_ALIANZA']) +  math.floor(sumaCol['PES']) + math.floor(sumaCol['RSP']) + math.floor(sumaCol['FUERZA_POR_MEXICO']) +  math.floor(sumaCol['CI_01_SAN_LUIS_POTOSI']) + math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaCol['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaCol['PAN']),numerosLetras.numero_a_letras(math.floor(sumaCol['PAN']))),
    ('PRI', math.floor(sumaCol['PRI']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRI']))),
    ('PRD', math.floor(sumaCol['PRD']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRD']))),
    ('VERDE', math.floor(sumaCol['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaCol['VERDE']))),
    ('PT', math.floor(sumaCol['PT']),numerosLetras.numero_a_letras(math.floor(sumaCol['PT']))),
    ('CP', math.floor(sumaCol['CP']),numerosLetras.numero_a_letras(math.floor(sumaCol['CP']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaCol['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaCol['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaCol['MORENA']))),
    ('NUEVA ALIANZA', math.floor(sumaCol['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaCol['NUEVA_ALIANZA']))),
    ('PES', math.floor(sumaCol['PES']),numerosLetras.numero_a_letras(math.floor(sumaCol['PES']))),
    ('RSP', math.floor(sumaCol['RSP']),numerosLetras.numero_a_letras(math.floor(sumaCol['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaCol['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaCol['FUERZA_POR_MEXICO']))),
    ('CI', math.floor(sumaCol['CI_01_SAN_LUIS_POTOSI']),numerosLetras.numero_a_letras(math.floor(sumaCol['CI_01_SAN_LUIS_POTOSI']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaCol['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #rb = open_workbook('San_Luis_Potosi.xls',formatting_info=True)
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
    #wb.save('San_Luis_Potosi.xls')
    return datos
#**********************************                
def excel03():    
    sumaColExcel01Excel01=df.groupby(by=['estados']).sum().groupby(level=[0]).cumsum().loc[estado]    
    datos=[
    (
        'PAN_PRI_PRD_CP', math.floor(sumaColExcel01Excel01['PAN'] + sumaColExcel01Excel01['PRI'] + sumaColExcel01Excel01['PRD'] + sumaColExcel01Excel01['CP'] + sumaColExcel01Excel01['PAN_PRI_PRD_CP'] + sumaColExcel01Excel01['PAN_PRI_PRD'] + sumaColExcel01Excel01['PAN_PRI_CP'] + sumaColExcel01Excel01['PAN_PRD_CP'] + sumaColExcel01Excel01['PRI_PRD_CP'] + sumaColExcel01Excel01['PAN_PRI'] + sumaColExcel01Excel01['PAN_PRD'] + sumaColExcel01Excel01['PAN_CP'] + sumaColExcel01Excel01['PRI_PRD'] + sumaColExcel01Excel01['PRI_CP'] + sumaColExcel01Excel01['PRD_CP']), 
        numerosLetras.numero_a_letras(math.floor(sumaColExcel01Excel01['PAN'] + sumaColExcel01Excel01['PRI'] + sumaColExcel01Excel01['PRD'] + sumaColExcel01Excel01['CP'] + sumaColExcel01Excel01['PAN_PRI_PRD_CP'] + sumaColExcel01Excel01['PAN_PRI_PRD'] + sumaColExcel01Excel01['PAN_PRI_CP'] + sumaColExcel01Excel01['PAN_PRD_CP'] + sumaColExcel01Excel01['PRI_PRD_CP'] + sumaColExcel01Excel01['PAN_PRI'] + sumaColExcel01Excel01['PAN_PRD'] + sumaColExcel01Excel01['PAN_CP'] + sumaColExcel01Excel01['PRI_PRD'] + sumaColExcel01Excel01['PRI_CP'] + sumaColExcel01Excel01['PRD_CP']))
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
        'CI', math.floor(sumaColExcel01Excel01['CI_01_SAN_LUIS_POTOSI']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['CI_01_SAN_LUIS_POTOSI'])
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
estado='San_Luis_Potosi'
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
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRI_PRD_CP'], dividendo=4), partidos=["PAN","PRI","PRD","CP"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRI_PRD_CP'], dividendo=4), partidos=["PAN","PRI","PRD","CP"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRI_PRD'], dividendo=3), partidos=["PAN","PRI","PRD"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRI_PRD'], dividendo=3), partidos=["PAN","PRI","PRD"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRI_CP'], dividendo=3), partidos=["PAN","PRI","CP"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRI_CP'], dividendo=3), partidos=["PAN","PRI","CP"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRD_CP'], dividendo=3), partidos=["PAN","PRD","CP"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRD_CP'], dividendo=3), partidos=["PAN","PRD","CP"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PRI_PRD_CP'], dividendo=3), partidos=["PRI","PRD","CP"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PRI_PRD_CP'], dividendo=3), partidos=["PRI","PRD","CP"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRI'], dividendo=2), partidos=["PAN","PRI"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRI'], dividendo=2), partidos=["PAN","PRI"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_PRD'], dividendo=2), partidos=["PAN","PRD"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_PRD'], dividendo=2), partidos=["PAN","PRD"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PAN_CP'], dividendo=2), partidos=["PAN","CP"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PAN_CP'], dividendo=2), partidos=["PAN","CP"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PRI_PRD'], dividendo=2), partidos=["PRI","PRD"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PRI_PRD'], dividendo=2), partidos=["PRI","PRD"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PRI_CP'], dividendo=2), partidos=["PRI","CP"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PRI_CP'], dividendo=2), partidos=["PRI","CP"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PRD_CP'], dividendo=2), partidos=["PRD","CP"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PRD_CP'], dividendo=2), partidos=["PRD","CP"] )
##**********************************
divicionDeVotos(fraccionVotos(votosTotalCoalicion=sumaCol['PT_VERDE'], dividendo=2), partidos=["PT","VERDE"])
divicionDeVotosSobranteTres(fraccionSobrante(votosTotalCoalicion=sumaCol['PT_VERDE'], dividendo=2), partidos=["PT","VERDE"] )
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
can.drawString(43, 516, str(hora))
#can.drawString(190, 513, str(dia))
#can.drawString(30, 503, "CENTRO DE ESCRUTINIO Y CÓMPUTO")
can.drawString(90, 371, tb1[0][2]) 
can.drawString(280, 371, str(tb1[0][1])) 
can.drawString(90, 360, tb1[1][2]) 
can.drawString(280, 360, str(tb1[1][1])) 
can.drawString(90, 348, tb1[2][2]) 
can.drawString(280, 348, str(tb1[2][1])) 
can.drawString(90, 336, tb1[3][2]) 
can.drawString(280, 336, str(tb1[3][1])) 
can.drawString(90, 324, tb1[4][2]) 
can.drawString(280, 324, str(tb1[4][1])) 
can.drawString(90, 311, tb1[5][2]) 
can.drawString(280, 311, str(tb1[5][1])) 
can.drawString(90, 299, tb1[6][2]) 
can.drawString(280, 299, str(tb1[6][1]))
can.drawString(90, 287, tb1[7][2]) 
can.drawString(280, 287, str(tb1[7][1]))  
can.drawString(90, 273, tb1[8][2]) 
can.drawString(280, 273, str(tb1[8][1]))  
can.drawString(90, 260, tb1[9][2]) 
can.drawString(280, 260, str(tb1[9][1]))  
can.drawString(90, 247, tb1[10][2]) 
can.drawString(280, 247, str(tb1[10][1]))  
can.drawString(90, 235, tb1[11][2]) 
can.drawString(280, 235, str(tb1[11][1]))  
can.drawString(90, 222, tb1[12][2]) 
can.drawString(280, 222, str(tb1[12][1]))  
can.drawString(90, 210, tb1[13][2]) 
can.drawString(280, 210, str(tb1[13][1]))  
can.drawString(90, 197, tb1[14][2]) 
can.drawString(280, 197, str(tb1[14][1]))  
can.drawString(90, 185, tb1[15][2]) 
can.drawString(280, 185, str(tb1[15][1]))  
can.drawString(90, 173, tb1[16][2]) 
can.drawString(280, 173, str(tb1[16][1]))  
can.drawString(90, 161, tb1[17][2]) 
can.drawString(280, 161, str(tb1[17][1]))  
can.drawString(90, 149, tb1[18][2]) 
can.drawString(280, 149, str(tb1[18][1]))  
can.drawString(90, 137, tb1[19][2]) 
can.drawString(280, 137, str(tb1[19][1]))  
can.drawString(90, 125, tb1[20][2]) 
can.drawString(280, 125, str(tb1[20][1]))  
can.drawString(90, 113, tb1[21][2]) 
can.drawString(280, 113, str(tb1[21][1]))  
can.drawString(90, 101, tb1[22][2]) 
can.drawString(280, 101, str(tb1[22][1]))  
can.drawString(90, 87, tb1[23][2]) 
can.drawString(280, 87, str(tb1[23][1]))  
can.drawString(90, 74, tb1[24][2]) 
can.drawString(280, 74, str(tb1[24][1]))  
can.drawString(90, 62, tb1[25][2]) 
can.drawString(280, 62, str(tb1[25][1]))  
can.drawString(90, 50, tb1[26][2]) 
can.drawString(280, 50, str(tb1[26][1]))  
can.drawString(90, 38, tb1[27][2]) 
can.drawString(280, 38, str(tb1[27][1]))   
##tb2
#   
can.drawString(400, 507, tb2[0][2]) 
can.drawString(590, 507, str(tb2[0][1]))  
can.drawString(400, 490, tb2[1][2]) 
can.drawString(590, 490, str(tb2[1][1]))  
can.drawString(400, 473, tb2[2][2]) 
can.drawString(590, 473, str(tb2[2][1]))  
can.drawString(400, 456, tb2[3][2]) 
can.drawString(590, 456, str(tb2[3][1]))  
can.drawString(400, 438, tb2[4][2]) 
can.drawString(590, 438, str(tb2[4][1]))  
can.drawString(400, 420, tb2[5][2]) 
can.drawString(590, 420, str(tb2[5][1]))  
can.drawString(400, 402, tb2[6][2]) 
can.drawString(590, 402, str(tb2[6][1]))  
can.drawString(400, 384, tb2[7][2]) 
can.drawString(590, 384, str(tb2[7][1]))  
can.drawString(400, 366, tb2[8][2]) 
can.drawString(590, 366, str(tb2[8][1]))  
can.drawString(400, 348, tb2[9][2]) 
can.drawString(590, 348, str(tb2[9][1]))  
can.drawString(400, 332, tb2[10][2]) 
can.drawString(590, 332, str(tb2[10][1]))  
can.drawString(400, 315, tb2[11][2]) 
can.drawString(590, 315, str(tb2[11][1]))  
can.drawString(400, 299, tb2[12][2]) 
can.drawString(590, 299, str(tb2[12][1]))  
can.drawString(400, 285, tb2[13][2]) 
can.drawString(590, 285, str(tb2[13][1]))  
can.drawString(400, 270, tb2[14][2]) 
can.drawString(590, 270, str(tb2[14][1]))  
can.drawString(400, 256, tb2[15][2]) 
can.drawString(590, 256, str(tb2[15][1]))
#Tb3
can.drawString(400, 198, tb3[0][2]) 
can.drawString(590, 198, str(tb3[0][1]))  
can.drawString(400, 180, tb3[1][2]) 
can.drawString(590, 180, str(tb3[1][1]))  
can.drawString(400, 164, tb3[2][2]) 
can.drawString(590, 164, str(tb3[2][1]))  
can.drawString(400, 147, tb3[3][2]) 
can.drawString(590, 147, str(tb3[3][1]))  
can.drawString(400, 130, tb3[4][2]) 
can.drawString(590, 130, str(tb3[4][1]))  
can.drawString(400, 115, tb3[5][2]) 
can.drawString(590, 115, str(tb3[5][1]))  
can.drawString(400, 98, tb3[6][2]) 
can.drawString(590, 98, str(tb3[6][1]))  
can.drawString(400, 81, tb3[7][2]) 
can.drawString(590, 81, str(tb3[7][1]))  
can.drawString(400, 64, tb3[8][2]) 
can.drawString(590, 64, str(tb3[8][1]))  
can.drawString(400, 50, tb3[9][2]) 
can.drawString(590, 50, str(tb3[9][1]))  
can.drawString(400, 36, tb3[10][2]) 
can.drawString(590, 36, str(tb3[10][1]))  
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(path+"pdfOrg/san_luis.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open(path+"pdfNew/san_luis.pdf", "wb")
output.write(outputStream)
outputStream.close()

