#************************************ #
# -*- coding: utf-8 -*-
# Autor: Gerardo Molina
# Ultima Modificacion: 13/09/19
# Nombre: Interfaz.py
# Descripcion: interfaz grafica y acciones de la interfaz.
#
#************************************ #
# ******************************************************** #
# ******************************************************** #
# Importamos las librerias necesarias. 
import subprocess
import signal
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time 
from Motor import *
# Se definen las variables del programa
# Variables Globales
global texto
global nombreAtleta
# Variables locales
texto="verde"
nombreAtleta="Atleta"
anchoVideo=1080
altoVideo=720
# ******************************************************** #
# Clase de la Interfaz Grafica
# ******************************************************** #
class Ui_VentanaBotones(object):
    """ 
    Funcion: setupUI
    Descripcion: 
    Esta funcion contiene todos los elementos de la interfaz grafica.
    """  
    def setupUi(self, VentanaBotones):
      VentanaBotones.setObjectName("VentanaBotones")
      VentanaBotones.resize(480, 600)
      VentanaBotones.setMinimumSize(QtCore.QSize(480, 600))
      VentanaBotones.setMaximumSize(QtCore.QSize(480, 600))
      VentanaBotones.setStyleSheet("")
      self.centralwidget = QtWidgets.QWidget(VentanaBotones)
      self.centralwidget.setObjectName("centralwidget")
      self.pushButton = QtWidgets.QPushButton(self.centralwidget)
      self.pushButton.setGeometry(QtCore.QRect(40, 200, 181, 121))
      self.pushButton.setStyleSheet("")
      self.pushButton.setObjectName("pushButton")
      self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
      self.pushButton_2.setGeometry(QtCore.QRect(260, 340, 181, 121))
      self.pushButton_2.setStyleSheet("")
      self.pushButton_2.setObjectName("pushButton_2")
      self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
      self.pushButton_3.setGeometry(QtCore.QRect(40, 340, 181, 121))
      self.pushButton_3.setStyleSheet("")
      self.pushButton_3.setObjectName("pushButton_3")
      self.label = QtWidgets.QLabel(self.centralwidget)
      self.label.setGeometry(QtCore.QRect(-10, -20, 501, 211))
      self.label.setObjectName("label")
      self.label_2 = QtWidgets.QLabel(self.centralwidget)
      self.label_2.setGeometry(QtCore.QRect(50, 480, 171, 16))
      self.label_2.setObjectName("label_2")
      self.line = QtWidgets.QFrame(self.centralwidget)
      self.line.setGeometry(QtCore.QRect(7, 460, 471, 20))
      self.line.setFrameShape(QtWidgets.QFrame.HLine)
      self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
      self.line.setObjectName("line")
      self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
      self.lineEdit.setGeometry(QtCore.QRect(50, 510, 381, 31))
      self.lineEdit.setObjectName("lineEdit")
      self.comboBox = QtWidgets.QComboBox(self.centralwidget)
      self.comboBox.setGeometry(QtCore.QRect(260, 250, 191, 41))
      self.comboBox.setObjectName("comboBox")
      self.label_3 = QtWidgets.QLabel(self.centralwidget)
      self.label_3.setGeometry(QtCore.QRect(260, 230, 191, 16))
      self.label_3.setObjectName("label_3")
      self.label.raise_()
      self.pushButton.raise_()
      self.pushButton_2.raise_()
      self.pushButton_3.raise_()
      self.label_2.raise_()
      self.line.raise_()
      self.lineEdit.raise_()
      self.comboBox.raise_()
      self.label_3.raise_()
      VentanaBotones.setCentralWidget(self.centralwidget)
      self.menubar = QtWidgets.QMenuBar(VentanaBotones)
      self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
      self.menubar.setObjectName("menubar")
      VentanaBotones.setMenuBar(self.menubar)
      self.statusbar = QtWidgets.QStatusBar(VentanaBotones)
      self.statusbar.setObjectName("statusbar")
      VentanaBotones.setStatusBar(self.statusbar)
      self.retranslateUi(VentanaBotones)
      QtCore.QMetaObject.connectSlotsByName(VentanaBotones)
      # Acciones de los elementos de la interfaz grafica
      self.pushButton.clicked.connect(self.colorGorro)
      self.pushButton_2.clicked.connect(openFile)
      self.pushButton_3.clicked.connect(openManual)
      self.comboBox.currentTextChanged.connect(self.comboCambio)
    """ 
    Funcion: retranslateUI
    Descripcion: 
    Esta funcion generada por Qt Designer y su traduccion a python, en esta se 
    redefinen algunos valores como el texto de las etiquetas, botones, y combos. 
    """   
    def retranslateUi(self, VentanaBotones):
      # Valores del combobox
       list1=[
         (""),
         ("Verde"),
         ("Rojo"),
         ("Azul"),
      ]
       _translate = QtCore.QCoreApplication.translate
       VentanaBotones.setWindowTitle(_translate("VentanaBotones", "MainWindow"))
       self.pushButton.setText(_translate("VentanaBotones", "Iniciar Rutina"))
       self.pushButton_2.setText(_translate("VentanaBotones", "Abrir Video"))
       self.pushButton_3.setText(_translate("VentanaBotones", "Ayuda"))
       self.label.setPixmap(QPixmap("encabezado.jpg"))
       self.label_2.setText(_translate("VentanaBotones", "Ingresar Nombre de Atleta:"))
       self.label_2.setText(_translate("VentanaBotones", "Ingresar Nombre de Atleta:"))
       self.label_3.setText(_translate("VentanaBotones", "Seleccionar Color del Gorro"))
       self.comboBox.clear()
       self.comboBox.addItems(list1)
       VentanaBotones.setWindowTitle("TRABAJO DE GRADUACION")

    """ 
    Funcion: comboCambio
    Descripcion: 
    Esta funcion toma el valor del combo box para seleccionar el color de gorro 
    deseado por el usuario. 
    """
    def comboCambio(self,text):
      try:
         global texto
         texto=text
         print "Se selecciono el color de gorro:" + texto
      except:
         print "ERROR: seleccionar nuevamente el color de gorro."
    """ 
    Funcion: colorGorro
    Descripcion: 
    Esta funcion establece el color del gorro seleccionado en comboCambio y llama
    a la funcion seguidor() enviando como argumento el colo seleccionado. 
    """
    def colorGorro(self):
         print "Iniciando rutina...esperar un momento."
         global nombreAtleta
         nombreAtleta=self.lineEdit.text()
         #Azul
         if texto=="Azul":
            colorLow=(8, 56, 168)
            colorHigh=(130, 250, 255)
         #Rojo
         if texto=="Rojo":
            colorLow=(0,50,50)
            colorHigh=(10,255,255)
         #verde
         else:
            colorLow=(29, 86, 6)
            colorHigh=(64, 255, 255)
         seguidor(colorLow,colorHigh,nombreAtleta)

# ******************************************************** #
# ******************************************************** #
""" 
Funcion: openManual
Descripcion: 
Esta funcion abre un archivo PDF que contiene el manual de usuario del dispositivo.
Si se desea abrrir el manual en la version web se debe decomentar las dos lineas comentadas
y comentar las que no estan comentadas. 
"""

def openManual(self):
    #url = QtCore.QUrl('https://sites.google.com/view/manualdeusuarioatletas/p%C3%A1gina-principal')
    #if not QtGui.QDesktopServices.openUrl(url):
        #QtGui.QMessageBox.warning(self, 'Open Url', 'Could not open url')
    filename='test.pdf'
    if sys.platform == "win32":
      os.startfile(filename)
    else:
      opener ="open" if sys.platform == "darwin" else "xdg-open"
      subprocess.call([opener, filename])
""" 
Funcion: openFIle
Descripcion: 
Esta funcion abre un cuadro de dialogo para que el usuario seleccione un video
luego abre el video utilizando imshow(). Para salir el usuario debe presionar la
tecla Q en su eclado. 

"""
def openFile(self):
    try:
       name=QtWidgets.QFileDialog.getOpenFileName(None,  "Abrir Video")
       print "Abriendo el video en: " +  name[0]
       cap = cv2.VideoCapture(name[0])
       while True:
        # Capture frame-by-frame
         ret, frame = cap.read()
         frame = imutils.resize(frame, width=anchoVideo, height=altoVideo)
         if ret == True:
            cv2.putText(frame, "TECLA Q PARA SALIR.", (anchoVideo-(anchoVideo/2) , altoVideo-120), cv2.FONT_HERSHEY_SIMPLEX,
                  0.65, (255, 255, 255), 2)
            cv2.imshow('Frame',frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
               break
         else:
            break
       cap.release()
       cv2.destroyAllWindows()
    except:
      print "ERROR: No es posible abrir el archivo selecionado, verificar que sea un archivo de video valido."
""" 
Inicializacion: 
Se inicia la interfaz grafica en 
"""

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    VentanaBotones = QtWidgets.QMainWindow()
    ui = Ui_VentanaBotones()
    ui.setupUi(VentanaBotones)
    VentanaBotones.show()
    sys.exit(app.exec_())


