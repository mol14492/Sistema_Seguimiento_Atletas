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
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time 
import serial
# ******************************************************** #
# ******************************************************** #
#Se inicia la comunicacion serial con el arduino. 
try:
    try:
        ser =  ser = serial.Serial('/dev/cu.usbmodem14101',9600,timeout=0.1)
    except:
        ser =  ser = serial.Serial('/dev/cu.usbmodem14201',9600,timeout=0.1)
except:
    print "ERROR:No es posible conectar con el dispositivo!"
##################################################################
## CODIGO DE OPENCV ##
##################################################################
    """ 
    Funcion: seguidor
    Descripcion: 
    Esta funcion realiza el seguimienot de un objeto, en base al color
    seleccionado. 
    """  
def seguidor(colorBajo, colorAlto,nombreAtleta):
     try:
        # Si es camara externa 0, si es interna 1.
         cam =0
        # Se establece los fps, el ancho y alto del video. 
         altoVideo=480
         anchoVideo=720
         fps=24
         #Se crea el bufer y argumentos. 
         ap = argparse.ArgumentParser()
         ap.add_argument("-v", "--video",
             help="path to the (optional) video file")
         ap.add_argument("-b", "--buffer", type=int, default=32,
             help="max buffer size")
         args = vars(ap.parse_args())
         #Se inicializan las coordenadas y los puntos.
         pts = deque(maxlen=args["buffer"])
         counter = 0
         (dX, dY) = (0, 0)
         direction = ""
         #Entrada de Video (Camara)
         vs = VideoStream(src=cam).start()
         time.sleep(2.0)
         # Creamos un nuevo video. 
         cap = cv2.VideoCapture(cam)
         frame_width = int(cap.get(3))
         frame_height = int(cap.get(4))
         fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
         dia=time.strftime("%d")
         mes=time.strftime("%m")
         anio=time.strftime("%y")
         hora=time.strftime("%H")
         minutos=time.strftime("%M")
         nombreVideo='videos/'+nombreAtleta+'  '+dia+'_'+mes+'_'+anio+'  '+hora+'_'+minutos+'.mov'
         print "Video guardado como:"+nombreVideo
         out = cv2.VideoWriter(nombreVideo, fourcc, fps, (frame_width,frame_height))
         # Loop del Video
         while True:
            ################## Escritura de Video #############
            ###################################################
             ret, vid = cap.read()
             if ret == True:
                 out.write(vid)
            ###################################################
            ###################################################
             #Se lee el frame actual o se termina el video. 
             frame = vs.read()
             frame = frame[1] if args.get("video", False) else frame
             if frame is None:
                 break
             # Se le dan las dimensiones al video ancho y altura.
             frame = imutils.resize(frame, width=anchoVideo, height=altoVideo)
             # Se filtra el video, con un Gaussean blur
             blurred = cv2.GaussianBlur(frame, (11, 11), 0)
             hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
             # Se pasa el frame a HSV
             mask = cv2.inRange(hsv, colorBajo, colorAlto)
             mask = cv2.erode(mask, None, iterations=2)
             mask = cv2.dilate(mask, None, iterations=2)
             # Se busca el objeto
             cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                 cv2.CHAIN_APPROX_SIMPLE)
             cnts = imutils.grab_contours(cnts)
             center = None
             if len(cnts) > 0:
                 c = max(cnts, key=cv2.contourArea)
                 ((x, y), radius) = cv2.minEnclosingCircle(c)
                 M = cv2.moments(c)
                 center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                 #Se define el tamaño minimo del objeto. 
                 if radius > 10:
                     pts.appendleft(center)
             for i in np.arange(1, len(pts)):

                 if pts[i - 1] is None or pts[i] is None:
                     continue
                 if counter >= 10 and i == 1 and pts[-10] is not None:
                     dX = pts[-10][0] - pts[i][0]
                     dY = pts[-10][1] - pts[i][1]
                     (dirX, dirY) = ("", "")
             # show the movement deltas and the direction of movement on
             # the frame
             cv2.putText(frame, "TECLA Q PARA SALIR.", (anchoVideo-(anchoVideo/2) , altoVideo-100), cv2.FONT_HERSHEY_SIMPLEX,
                 0.65, (255, 255, 255), 2)
             # show the frame to our screen and increment the frame counter
             cv2.imshow("Frame", frame)
             key = cv2.waitKey(1) & 0xFF
             counter += 1
             controlador(dX)
             # if the 'q' key is pressed, stop the loop
             if key == ord("q"):
                 ser.write('q')
                 break

         # if we are not using a video file, stop the camera video stream
         if not args.get("video", False):
             vs.stop()

         # otherwise, release the camera
         else:
             vs.release()
             out.release()
             cap.release()
         # close all windows
         cv2.destroyAllWindows()
     except:
         print "ERROR: no se pudo detectar al atleta. Intentelo de nuevo."
def controlador(dX):
    try:
        if np.abs(dX) > 30:
            diX = "Iz" if np.sign(dX) == 1 else "Der"
            if (diX=="Der"):
                ser.write('a')
                print "Izquierda"
            if (diX=="Iz"):
                ser.write('b')
                print "Derecha"
        if np.abs(dX) < 30:
            ser.write('c')
            print "Quieto"
    except:
        print "ERROR: Ocurrió un error en el controlador."
   







