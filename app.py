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
from funciones.estados import zacatecas as zacatecas
from funciones.estados import cdmx as cdmx
from funciones.estados import michoacan as michoacan
from funciones.estados import nayarit as nayarit
from funciones.estados import baja_california_sur as baja_california_sur
from funciones.estados import queretaro as queretaro


app=Flask(__name__)
@app.route('/')
def index():
    return "VMRE 2021"
    

@app.route('/zacatecas')
def zacatecasF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/zacatecas.html", lalos=zacatecas.excel01(), lalos2=zacatecas.excel02(), lalos3=zacatecas.excel03(), dia=dia, hora=hora )  

@app.route('/downloadZacatecas')
def downloadZacatecasF():
	path="C:/vmre/funciones/estados/pdfNew/zacatecas.pdf"
	return send_file(path, as_attachment=True)
    

@app.route('/chihuahua')
def chihuahuaF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/chihuahua.html", lalos=chihuahua.excel01(), lalos2=chihuahua.excel02(), lalos3=chihuahua.excel03(), dia=dia, hora=hora )  


@app.route('/downloadChihuahua')
def downloadChihuahuaF():
	path="C:/vmre/funciones/estados/pdfNew/chihuahua.pdf"
	return send_file(path, as_attachment=True)



@app.route('/colima')
def colimaF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/colima.html", lalos=colima.excel01(), lalos2=colima.excel02(), lalos3=colima.excel03(), dia=dia, hora=hora )  

@app.route('/downloadColima')
def downloadColimaF():
	path="C:/vmre/funciones/estados/pdfNew/colima.pdf"
	return send_file(path, as_attachment=True)


@app.route('/guerrero')
def guerreroF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/guerrero.html", lalos=guerrero.excel01(), lalos2=guerrero.excel02(), lalos3=guerrero.excel03(), dia=dia, hora=hora )  


@app.route('/downloadGuerrero')
def downloadGuerreroF():
	path="C:/vmre/funciones/estados/pdfNew/guerrero.pdf"
	return send_file(path, as_attachment=True)




@app.route('/sanLuisPotosi')
def sanLuisPotosiF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/sanLuisPotosi.html", lalos=sanLuisPotosi.excel01(), lalos2=sanLuisPotosi.excel02(), lalos3=sanLuisPotosi.excel03(), dia=dia, hora=hora )  


@app.route('/downloadSanLuisPotosi')
def downloadSanLuisPotosiF():
	path="C:/vmre/funciones/estados/pdfNew/san_luis.pdf"
	return send_file(path, as_attachment=True)


@app.route('/jalisco')
def jaliscoF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/jalisco.html", lalos=jalisco.excel01(), dia=dia, hora=hora )  


@app.route('/downloadJalisco')
def downloadJaliscoF():
	path="C:/vmre/funciones/estados/pdfNew/jalisco.pdf"
	return send_file(path, as_attachment=True)



@app.route('/cdmx')
def cdmxF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/cdmx.html", lalos=cdmx.excel01(), dia=dia, hora=hora )  


@app.route('/downloadCdmx')
def downloadCdmxF():
	path="C:/vmre/funciones/estados/pdfNew/cdmx.pdf"
	return send_file(path, as_attachment=True)



@app.route('/michoacan')
def michoacanF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/michoacan.html", lalos=michoacan.excel01(), lalos2=michoacan.excel02(), lalos3=michoacan.excel03(), dia=dia, hora=hora )  


@app.route('/downloadMichoacan')
def downloadMichoacanF():
	path="C:/vmre/funciones/estados/pdfNew/michoacan.pdf"
	return send_file(path, as_attachment=True)



@app.route('/nayarit')
def nayaritF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/nayarit.html", lalos=nayarit.excel01(), lalos2=nayarit.excel02(), lalos3=nayarit.excel03(), dia=dia, hora=hora )  


@app.route('/downloadNayarit')
def downloadNayaritF():
	path="C:/vmre/funciones/estados/pdfNew/nayarit.pdf"
	return send_file(path, as_attachment=True)

@app.route('/baja_california_sur')
def baja_california_surF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/baja_california_sur.html", lalos=baja_california_sur.excel01(), lalos2=baja_california_sur.excel02(), lalos3=baja_california_sur.excel03(), dia=dia, hora=hora )  


@app.route('/downloadBaja_california_sur')
def downloadBaja_california_surF():
	path="C:/vmre/funciones/estados/pdfNew/baja_california_sur.pdf"
	return send_file(path, as_attachment=True)


@app.route('/queretaro')
def queretaroF():
    dia=time.strftime('%d', time.localtime())
    hora=time.strftime('%H:%M:%S', time.localtime())
    return render_template("pdf/queretaro.html", lalos=queretaro.excel01(), lalos2=queretaro.excel02(), lalos3=queretaro.excel03(), dia=dia, hora=hora )  


@app.route('/downloadQueretaro')
def downloadQueretaroF():
	path="C:/vmre/funciones/estados/pdfNew/queretaro.pdf"
	return send_file(path, as_attachment=True)


if __name__ == '__main__':
    #app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    app.run(debug=True)