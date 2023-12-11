#A face detection

import cv2
import numpy as np
from matplotlib import pyplot as plt

from tkinter import *
import os

#____________________ Exercice 3____________

sunglasses = cv2.imread('sunglasses.png')
alpha_sunglasses = cv2.imread('alpha.png')
# Pour faire une capture vidéo de webcam

cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    #pass from RGB to graylevel
    p1 = frame;
    p1_gray = cv2.cvtColor(p1, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    eyes_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    # Detect faces
    faces = face_cascade.detectMultiScale(p1_gray, 1.1, 4)    
    #____________________ Exercice 3 ____________
    #for i in range (len(faces)):
    for (x,y,w,h) in faces :
        faceROI_gray = p1_gray[y:y+h,x:x+w]
        #p1 = cv2.ellipse(p1, (x + int(w*0.5), y + int(h*0.5)), (int(w*0.5),int(h*0.5)), 0,0,360,(255, 0, 255), 4)
        eyes = eyes_cascade.detectMultiScale(faceROI_gray, 1.3, 5)
        # Si on detecte 2 yeux
        if len(eyes) == 2 :
            # Largeur des lunettes
            width_sunglasses = abs(eyes[0,0] - (eyes[1,0] + eyes[1,2]))
            # Hauteur des lunettes
            height_sunglasses = abs (eyes[0,1] - (eyes[1,1] + eyes[1,3]))
            # Si les 2 yeux détectés ne sont pas les mêmes
            if height_sunglasses != 0 and width_sunglasses != 0 :
                # On redimensionne les lunnettes
                sunglasses_resize = cv2.resize(sunglasses, (width_sunglasses, height_sunglasses),1,1)
                # On redimensionne aussi le masque alpha des lunnettes
                alpha_sunglasses_resize = cv2.resize(alpha_sunglasses, (width_sunglasses, height_sunglasses),1,1)

                # Calcul du centre des yeux
                center_x = int((eyes[0, 0] + eyes[1, 0] + eyes[0, 2] + eyes[1, 2]) / 2)
                center_y = int((eyes[0, 1] + eyes[1, 1] + eyes[0, 3] + eyes[1, 3]) / 2)
                # Calcul des décalages vertical et horizontal
                offset_x = int(width_sunglasses * 0.2)  # Ajustez la valeur selon votre besoin
                offset_y = int(height_sunglasses * 0.2)  # Ajustez la valeur selon votre besoin
                # Positions de départ des lunettes
                debut_x = center_x - int(width_sunglasses / 2) - offset_x
                debut_y = center_y - int(height_sunglasses / 2) - offset_y
                def filtre_lunnette():
                        #________Dans cette boucle, j'enlève le fond noir de l'image lunettes grâce au masque alpha_________
                        for i in range(0,sunglasses_resize.shape[0]) :
                            for j in range(0, sunglasses_resize.shape[1]) :
                                if alpha_sunglasses_resize[i,j,0] != 0 :
                                    p1[i+debut_y+y,j+debut_x+x] = sunglasses_resize[i,j]
    p = p1        
    #copy processed part to frame
    frame = p
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

def new():
    # on exécute le même fichier menu_fichier.py
    os.popen("Code_Projet_VIVIER_RANDRIAMITANDRINA.py")
    
master = Tk()
master.geometry("300x150")
# Création de la barre des menu
menuBar = Menu(master) 
 
# Création du menu principal 'Fichier'
menuFichier  = Menu(menuBar, tearoff = 0) 
menuBar.add_cascade(label="Choix des filtres",menu = menuFichier) 
 
# Création des sous menus : 'Nouveau', 'Ouvrir', 'Quitter'
#menuFichier.add_command(label = "Nouveau" , command = new) 
menuFichier.add_command(label = "Filtre lunnette de soleil", command = filtre_lunnette) 
menuFichier.add_command(label = "Quitter", command = quit) 
 
# Configuration de la barre des menus
master.config(menu = menuBar)
master.mainloop()
cv2.destroyAllWindows()

