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
    ('VERDE_MORENA', math.floor(sumaColExcel01['VERDE_MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE_MORENA']))),
    ('VERDE_NUEVA_ALIANZA', math.floor(sumaColExcel01['VERDE_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE_NUEVA_ALIANZA']))),
    ('MORENA_NUEVA_ALIANZA', math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaColExcel01['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #print(datos)
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
can.drawString(60, 513, str(hora))
can.drawString(190, 513, str(dia))
can.drawString(30, 503, "CENTRO DE ESCRUTINIO Y C??MPUTO")
can.drawString(90, 370, tb1[0][2]) 
can.drawString(280, 370, str(tb1[0][1])) 
can.drawString(90, 360, tb1[1][2]) 
can.drawString(280, 360, str(tb1[1][1])) 
can.drawString(90, 350, tb1[2][2]) 
can.drawString(280, 350, str(tb1[2][1])) 
can.drawString(90, 340, tb1[3][2]) 
can.drawString(280, 340, str(tb1[3][1])) 
can.drawString(90, 329, tb1[4][2]) 
can.drawString(280, 329, str(tb1[4][1])) 
can.drawString(90, 319, tb1[5][2]) 
can.drawString(280, 319, str(tb1[5][1])) 
can.drawString(90, 309, tb1[6][2]) 
can.drawString(280, 309, str(tb1[6][1]))
can.drawString(90, 297, tb1[7][2]) 
can.drawString(280, 297, str(tb1[7][1]))  
can.drawString(90, 288, tb1[8][2]) 
can.drawString(280, 288, str(tb1[8][1]))  
can.drawString(90, 277, tb1[9][2]) 
can.drawString(280, 277, str(tb1[9][1]))  
can.drawString(90, 266, tb1[10][2]) 
can.drawString(280, 266, str(tb1[10][1]))  
can.drawString(90, 256, tb1[11][2]) 
can.drawString(280, 256, str(tb1[11][1]))  
can.drawString(90, 246, tb1[12][2]) 
can.drawString(280, 246, str(tb1[12][1]))  
can.drawString(90, 236, tb1[13][2]) 
can.drawString(280, 236, str(tb1[13][1]))  
can.drawString(90, 226, tb1[14][2]) 
can.drawString(280, 226, str(tb1[14][1]))  
can.drawString(90, 216, tb1[15][2]) 
can.drawString(280, 216, str(tb1[15][1]))  
can.drawString(90, 205, tb1[16][2]) 
can.drawString(280, 205, str(tb1[16][1]))  
can.drawString(90, 194, tb1[17][2]) 
can.drawString(280, 194, str(tb1[17][1]))  
can.drawString(90, 184, tb1[18][2]) 
can.drawString(280, 184, str(tb1[18][1]))  
can.drawString(90, 174, tb1[19][2]) 
can.drawString(280, 174, str(tb1[19][1]))  
can.drawString(90, 164, tb1[20][2]) 
can.drawString(280, 164, str(tb1[20][1]))  
can.drawString(90, 154, tb1[21][2]) 
can.drawString(280, 152, str(tb1[21][1]))  
can.drawString(90, 142, tb1[22][2]) 
can.drawString(280, 142, str(tb1[22][1]))  
can.drawString(90, 132, tb1[23][2]) 
can.drawString(280, 132, str(tb1[23][1]))  
can.drawString(90, 122, tb1[24][2]) 
can.drawString(280, 122, str(tb1[24][1]))  
can.drawString(90, 112, tb1[25][2]) 
can.drawString(280, 112, str(tb1[25][1]))  
can.drawString(90, 102, tb1[26][2]) 
can.drawString(280, 102, str(tb1[26][1]))  
can.drawString(90, 90, tb1[27][2]) 
can.drawString(280, 90, str(tb1[27][1]))   
can.drawString(90, 80, tb1[28][2]) 
can.drawString(280, 80, str(tb1[28][1]))   
can.drawString(90, 70, tb1[29][2]) 
can.drawString(280, 70, str(tb1[29][1]))   
can.drawString(90, 60, tb1[30][2]) 
can.drawString(280, 60, str(tb1[30][1]))   
can.drawString(90, 50, tb1[31][2]) 
can.drawString(280, 50, str(tb1[31][1]))   
can.drawString(90, 40, tb1[32][2]) 
can.drawString(280, 40, str(tb1[32][1])) 
##tb2
#   
can.drawString(400, 520, tb2[0][2]) 
can.drawString(590, 520, str(tb2[0][1]))  
can.drawString(400, 505, tb2[1][2]) 
can.drawString(590, 505, str(tb2[1][1]))  
can.drawString(400, 487, tb2[2][2]) 
can.drawString(590, 487, str(tb2[2][1]))  
can.drawString(400, 475, tb2[3][2]) 
can.drawString(590, 475, str(tb2[3][1]))  
can.drawString(400, 460, tb2[4][2]) 
can.drawString(590, 460, str(tb2[4][1]))  
can.drawString(400, 445, tb2[5][2]) 
can.drawString(590, 445, str(tb2[5][1]))  
can.drawString(400, 430, tb2[6][2]) 
can.drawString(590, 430, str(tb2[6][1]))  
can.drawString(400, 415, tb2[7][2]) 
can.drawString(590, 415, str(tb2[7][1]))  
can.drawString(400, 399, tb2[8][2]) 
can.drawString(590, 399, str(tb2[8][1]))  
can.drawString(400, 385, tb2[9][2]) 
can.drawString(590, 385, str(tb2[9][1]))  
can.drawString(400, 370, tb2[10][2]) 
can.drawString(590, 370, str(tb2[10][1]))  
can.drawString(400, 358, tb2[11][2]) 
can.drawString(590, 358, str(tb2[11][1]))  
can.drawString(400, 345, tb2[12][2]) 
can.drawString(590, 345, str(tb2[12][1]))  
can.drawString(400, 330, tb2[13][2]) 
can.drawString(590, 330, str(tb2[13][1]))  
can.drawString(400, 315, tb2[14][2]) 
can.drawString(590, 315, str(tb2[14][1]))  
can.drawString(400, 303, tb2[15][2]) 
can.drawString(590, 303, str(tb2[15][1]))  
can.drawString(400, 290, tb2[16][2]) 
can.drawString(590, 290, str(tb2[16][1]))  
can.drawString(400, 275, tb2[17][2]) 
can.drawString(590, 275, str(tb2[17][1]))  
#Tb3
can.drawString(400, 227, tb3[0][2]) 
can.drawString(590, 227, str(tb3[0][1]))  
can.drawString(400, 213, tb3[1][2]) 
can.drawString(590, 213, str(tb3[1][1]))  
can.drawString(400, 200, tb3[2][2]) 
can.drawString(590, 200, str(tb3[2][1]))  
can.drawString(400, 182, tb3[3][2]) 
can.drawString(590, 182, str(tb3[3][1]))  
can.drawString(400, 162, tb3[4][2]) 
can.drawString(590, 162, str(tb3[4][1]))  
can.drawString(400, 142, tb3[5][2]) 
can.drawString(590, 142, str(tb3[5][1]))  
can.drawString(400, 130, tb3[6][2]) 
can.drawString(590, 130, str(tb3[6][1]))  
can.drawString(400, 110, tb3[7][2]) 
can.drawString(590, 110, str(tb3[7][1]))  
can.drawString(400, 97, tb3[8][2]) 
can.drawString(590, 97, str(tb3[8][1]))  
can.drawString(400, 78, tb3[9][2]) 
can.drawString(590, 78, str(tb3[9][1]))  
can.drawString(400, 58, tb3[10][2]) 
can.drawString(590, 58, str(tb3[10][1]))  
can.drawString(400, 38, tb3[11][2]) 
can.drawString(590, 38, str(tb3[11][1]))  
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
print("Termina " + estado)