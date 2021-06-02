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
    totalDefExc = math.floor(sumaColExcel01['PAN']) + math.floor(sumaColExcel01['PRI']) + math.floor(sumaColExcel01['PRD']) + math.floor(sumaColExcel01['PT']) + math.floor(sumaColExcel01['VERDE']) + math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']) + math.floor(sumaColExcel01['MORENA']) + math.floor(sumaColExcel01['NUEVA_ALIANZA']) + math.floor(sumaColExcel01['VIVA']) + math.floor(sumaColExcel01['L_N_MANOS']) + math.floor(sumaColExcel01['PES']) + math.floor(sumaColExcel01['RSP']) + math.floor(sumaColExcel01['FUERZA_POR_MEXICO']) + math.floor(sumaColExcel01['PAN_PRI_PRD']) + math.floor(sumaColExcel01['PAN_PRI']) + math.floor(sumaColExcel01['PAN_PRD']) + math.floor(sumaColExcel01['PRI_PRD']) + math.floor(sumaColExcel01['PT_VERDE_MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PT_VERDE_MORENA']) + math.floor(sumaColExcel01['PT_VERDE_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PT_MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['VERDE_MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['PT_VERDE']) + math.floor(sumaColExcel01['PT_MORENA']) + math.floor(sumaColExcel01['PT_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['VERDE_MORENA']) + math.floor(sumaColExcel01['VERDE_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['MORENA_NUEVA_ALIANZA']) + math.floor(sumaColExcel01['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaColExcel01['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaColExcel01['PAN']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PAN']))),
    ('PRI', math.floor(sumaColExcel01['PRI']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRI']))),
    ('PRD', math.floor(sumaColExcel01['PRD']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PRD']))),
    ('PT', math.floor(sumaColExcel01['PT']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['PT']))),
    ('VERDE', math.floor(sumaColExcel01['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VERDE']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaColExcel01['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['MORENA']))),
    ('NUEVA ALIANZA', math.floor(sumaColExcel01['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['NUEVA_ALIANZA']))),
    ('VIVA', math.floor(sumaColExcel01['VIVA']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['VIVA']))),
    ('L_N_MANOS', math.floor(sumaColExcel01['L_N_MANOS']),numerosLetras.numero_a_letras(math.floor(sumaColExcel01['L_N_MANOS']))),
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
    #rb = open_workbook('Nayarit.xls',formatting_info=True)
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
    #wb.save('Nayarit.xls')
    return datos
#**********************************
def excel02():        
    totalDefExc = math.floor(sumaCol['PAN']) + math.floor(sumaCol['PRI']) + math.floor(sumaCol['PRD']) + math.floor(sumaCol['PT']) + math.floor(sumaCol['VERDE']) + math.floor(sumaCol['MOVIMIENTO_CIUDADANO']) + math.floor(sumaCol['MORENA']) + math.floor(sumaCol['NUEVA_ALIANZA']) + math.floor(sumaCol['VIVA']) + math.floor(sumaCol['L_N_MANOS']) + math.floor(sumaCol['PES']) + math.floor(sumaCol['RSP']) + math.floor(sumaCol['FUERZA_POR_MEXICO']) + math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']) + math.floor(sumaCol['VOTOS_NULOS'])
    datos=(
    ('PAN', math.floor(sumaCol['PAN']),numerosLetras.numero_a_letras(math.floor(sumaCol['PAN']))),
    ('PRI', math.floor(sumaCol['PRI']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRI']))),
    ('PRD', math.floor(sumaCol['PRD']),numerosLetras.numero_a_letras(math.floor(sumaCol['PRD']))),
    ('PT', math.floor(sumaCol['PT']),numerosLetras.numero_a_letras(math.floor(sumaCol['PT']))),
    ('VERDE', math.floor(sumaCol['VERDE']),numerosLetras.numero_a_letras(math.floor(sumaCol['VERDE']))),
    ('MOVIMIENTO CIUDADANO', math.floor(sumaCol['MOVIMIENTO_CIUDADANO']),numerosLetras.numero_a_letras(math.floor(sumaCol['MOVIMIENTO_CIUDADANO']))),
    ('MORENA', math.floor(sumaCol['MORENA']),numerosLetras.numero_a_letras(math.floor(sumaCol['MORENA']))),
    ('NUEVA ALIANZA', math.floor(sumaCol['NUEVA_ALIANZA']),numerosLetras.numero_a_letras(math.floor(sumaCol['NUEVA_ALIANZA']))),
    ('VIVA', math.floor(sumaCol['VIVA']),numerosLetras.numero_a_letras(math.floor(sumaCol['VIVA']))),
    ('L_N_MANOS', math.floor(sumaCol['L_N_MANOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['L_N_MANOS']))),
    ('PES', math.floor(sumaCol['PES']),numerosLetras.numero_a_letras(math.floor(sumaCol['PES']))),
    ('RSP', math.floor(sumaCol['RSP']),numerosLetras.numero_a_letras(math.floor(sumaCol['RSP']))),
    ('FUERZA POR MEXICO', math.floor(sumaCol['FUERZA_POR_MEXICO']),numerosLetras.numero_a_letras(math.floor(sumaCol['FUERZA_POR_MEXICO']))),
    ('CANDIDATOS_NO_REGISTRADOS', math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['CANDIDATOS_NO_REGISTRADOS']))),
    ('VOTOS_NULOS', math.floor(sumaCol['VOTOS_NULOS']),numerosLetras.numero_a_letras(math.floor(sumaCol['VOTOS_NULOS']))),
    ('TOTAL', totalDefExc, numerosLetras.numero_a_letras(totalDefExc))
    )
    #rb = open_workbook('Nayarit.xls',formatting_info=True)
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
    #wb.save('Nayarit.xls')
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
        'VIVA', math.floor(sumaColExcel01Excel01['VIVA']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['VIVA'])
    ),
    (
        'L_N_MANOS', math.floor(sumaColExcel01Excel01['L_N_MANOS']), numerosLetras.numero_a_letras(sumaColExcel01Excel01['L_N_MANOS'])
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
estado='Nayarit'
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
can.drawString(90, 529, "Nayarit")
can.drawString(60, 513, str(hora))
can.drawString(190, 513, str(dia))
can.drawString(30, 500, "CENTRO DE ESCRUTINIO Y CÓMPUTO")
can.drawString(90, 370, tb1[0][2]) 
can.drawString(280, 370, str(tb1[0][1])) 
can.drawString(90, 359, tb1[1][2]) 
can.drawString(280, 359, str(tb1[1][1])) 
can.drawString(90, 348, tb1[2][2]) 
can.drawString(280, 348, str(tb1[2][1])) 
can.drawString(90, 337, tb1[3][2]) 
can.drawString(280, 337, str(tb1[3][1])) 
can.drawString(90, 326, tb1[4][2]) 
can.drawString(280, 326, str(tb1[4][1])) 
can.drawString(90, 315, tb1[5][2]) 
can.drawString(280, 315, str(tb1[5][1])) 
can.drawString(90, 304, tb1[6][2]) 
can.drawString(280, 304, str(tb1[6][1]))
can.drawString(90, 293, tb1[7][2]) 
can.drawString(280, 293, str(tb1[7][1]))  
can.drawString(90, 282, tb1[8][2]) 
can.drawString(280, 282, str(tb1[8][1]))  
can.drawString(90, 271, tb1[9][2]) 
can.drawString(280, 271, str(tb1[9][1]))  
can.drawString(90, 260, tb1[10][2]) 
can.drawString(280, 260, str(tb1[10][1]))  
can.drawString(90, 249, tb1[11][2]) 
can.drawString(280, 249, str(tb1[11][1]))  
can.drawString(90, 238, tb1[12][2]) 
can.drawString(280, 238, str(tb1[12][1]))  
can.drawString(90, 227, tb1[13][2]) 
can.drawString(280, 227, str(tb1[13][1]))  
can.drawString(90, 216, tb1[14][2]) 
can.drawString(280, 216, str(tb1[14][1]))  
can.drawString(90, 205, tb1[15][2]) 
can.drawString(280, 205, str(tb1[15][1]))  
can.drawString(90, 194, tb1[16][2]) 
can.drawString(280,194, str(tb1[16][1]))  
can.drawString(90, 183, tb1[17][2]) 
can.drawString(280, 183, str(tb1[17][1]))  
can.drawString(90, 172, tb1[18][2]) 
can.drawString(280, 172, str(tb1[18][1]))  
can.drawString(90, 161, tb1[19][2]) 
can.drawString(280, 161, str(tb1[19][1]))  
can.drawString(90, 150, tb1[20][2]) 
can.drawString(280, 150, str(tb1[20][1]))  
can.drawString(90, 139, tb1[21][2]) 
can.drawString(280, 139, str(tb1[21][1]))  
can.drawString(90, 128, tb1[22][2]) 
can.drawString(280, 128, str(tb1[22][1]))  
can.drawString(90, 117, tb1[23][2]) 
can.drawString(280, 117, str(tb1[23][1]))  
can.drawString(90, 106, tb1[24][2]) 
can.drawString(280, 106, str(tb1[24][1]))  
can.drawString(90, 95, tb1[25][2]) 
can.drawString(280, 95, str(tb1[25][1]))  
can.drawString(90, 84, tb1[26][2]) 
can.drawString(280, 84, str(tb1[26][1]))  
can.drawString(90, 73, tb1[27][2]) 
can.drawString(280, 73, str(tb1[27][1]))   
can.drawString(90, 62, tb1[28][2]) 
can.drawString(280, 62, str(tb1[28][1]))   
can.drawString(90, 51, tb1[29][2]) 
can.drawString(280, 51, str(tb1[29][1]))   
can.drawString(90, 40, tb1[30][2]) 
can.drawString(280, 40, str(tb1[30][1]))   
##tb2
#   
can.drawString(400, 515, tb2[0][2]) 
can.drawString(590, 515, str(tb2[0][1]))  
can.drawString(400, 499, tb2[1][2]) 
can.drawString(590, 499, str(tb2[1][1]))  
can.drawString(400, 483, tb2[2][2]) 
can.drawString(590, 483, str(tb2[2][1]))  
can.drawString(400, 467, tb2[3][2]) 
can.drawString(590, 467, str(tb2[3][1]))  
can.drawString(400, 451, tb2[4][2]) 
can.drawString(590, 451, str(tb2[4][1]))  
can.drawString(400, 435, tb2[5][2]) 
can.drawString(590, 435, str(tb2[5][1]))  
can.drawString(400, 419, tb2[6][2]) 
can.drawString(590, 419, str(tb2[6][1]))  
can.drawString(400, 403, tb2[7][2]) 
can.drawString(590, 403, str(tb2[7][1]))  
can.drawString(400, 387, tb2[8][2]) 
can.drawString(590, 387, str(tb2[8][1]))  
can.drawString(400, 371, tb2[9][2]) 
can.drawString(590, 371, str(tb2[9][1]))  
can.drawString(400, 355, tb2[10][2]) 
can.drawString(590, 355, str(tb2[10][1]))  
can.drawString(400, 339, tb2[11][2]) 
can.drawString(590, 339, str(tb2[11][1]))  
can.drawString(400, 323, tb2[12][2]) 
can.drawString(590, 323, str(tb2[12][1]))  
can.drawString(400, 307, tb2[13][2]) 
can.drawString(590, 307, str(tb2[13][1]))  
can.drawString(400, 291, tb2[14][2]) 
can.drawString(590, 291, str(tb2[14][1]))  
can.drawString(400, 275, tb2[15][2]) 
can.drawString(590, 275, str(tb2[15][1]))  
#Tb3
can.drawString(400, 227, tb3[0][2]) 
can.drawString(590, 227, str(tb3[0][1]))  
can.drawString(400, 206, tb3[1][2]) 
can.drawString(590, 206, str(tb3[1][1]))  
can.drawString(400, 185, tb3[2][2]) 
can.drawString(590, 185, str(tb3[2][1]))  
can.drawString(400, 164, tb3[3][2]) 
can.drawString(590, 164, str(tb3[3][1]))  
can.drawString(400, 143, tb3[4][2]) 
can.drawString(590, 143, str(tb3[4][1]))  
can.drawString(400, 122, tb3[5][2]) 
can.drawString(590, 122, str(tb3[5][1]))  
can.drawString(400, 101, tb3[6][2]) 
can.drawString(590, 101, str(tb3[6][1]))  
can.drawString(400, 80, tb3[7][2]) 
can.drawString(590, 80, str(tb3[7][1]))  
can.drawString(400, 59, tb3[8][2]) 
can.drawString(590, 59, str(tb3[8][1]))  
can.drawString(400, 38, tb3[9][2]) 
can.drawString(590, 38, str(tb3[9][1]))  
can.save()

#move to the beginning of the StringIO buffer
packet.seek(0)
new_pdf = PdfFileReader(packet)
# read your existing PDF
existing_pdf = PdfFileReader(open(path+"pdfOrg/nayarit.pdf", "rb"))
output = PdfFileWriter()
# add the "watermark" (which is the new pdf) on the existing page
page = existing_pdf.getPage(0)
page.mergePage(new_pdf.getPage(0))
output.addPage(page)
# finally, write "output" to a real file
outputStream = open(path+"pdfNew/nayarit.pdf", "wb")
output.write(outputStream)
outputStream.close()
print("Termina " + estado)