import cv2
from tkinter import *
from PIL import Image, ImageTk
import numpy as np

#___________________________________________________Gestion des fichiers média __________________________________________
# Image lunettes
sunglasses = cv2.imread('sunglasses.png')
alpha_sunglasses = cv2.imread('alpha_sunglasses.png')
# Image foulard
scarf = cv2.imread('scarf.png')
alpha_scarf = cv2.imread('alpha_scarf.png')
# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)
# Récupérer les propriétés de la vidéo capturée
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# Récupérer les fichiers de cascades de haar pour la detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
#_________________________________________________Gestion de l'interface graphique_______________________________________
# Interface graphique Tkinter
master = Tk()
master.geometry("640x480")
# Création de la barre des menus
menuBar = Menu(master)
# Création du menu principal 'Fichier'
menuFichier = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Choix des filtres", menu=menuFichier)

#__________________________________________________Gestion du filtre lunnette____________________________________________
# Gestion du filtre lunnette avec une variable globale booléen
bool_activate_filtre_lunette = False
def filtre_lunette():
    global bool_activate_filtre_lunette
    bool_activate_filtre_lunette = not bool_activate_filtre_lunette
#_________________________________________________Gestion du filtre saturation_______________________________________________
bool_activate_filtre_saturation = False
def filtre_saturation():
    global bool_activate_filtre_saturation
    bool_activate_filtre_saturation = not bool_activate_filtre_saturation
#__________________________________________________Gestion du filtre foulard____________________________________________
# Gestion du filtre foulard avec une variable globale booléen
bool_activate_filtre_foulard = False
def filtre_foulard():
    global bool_activate_filtre_foulard
    bool_activate_filtre_foulard = not bool_activate_filtre_foulard
#_________________________________________________Gestion des filtre en sous menu_______________________________________
# Création des sous-menus : 'Filtre lunette de soleil', 'Quitter'
menuFichier.add_command(label="Activer/Desactiver le filtre foulard", command=filtre_foulard)
menuFichier.add_command(label="Activer/Desactiver le filtre lunette de soleil", command=filtre_lunette)
menuFichier.add_command(label="Activer/Desactiver le filtre saturation", command=filtre_saturation)
menuFichier.add_command(label="Quitter", command=master.quit)
# Configuration de la barre des menus
master.config(menu=menuBar)
# Créer une étiquette pour afficher l'image
panel = Label(master)
panel.pack(side="bottom", fill="both", expand="yes")
#___________________________________________________Gestion de l'enregistrement vidéo____________________________________________
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Vous pouvez également utiliser d'autres codecs comme MJPG, DIVX, XVID, etc.
saved_video = cv2.VideoWriter('video_enregistré.avi', fourcc, 20.0, (frame_width, frame_height))
#___________________________________________________Gestion de la vidéo webcam____________________________________________
# Fonction pour mettre à jour l'image
def update_image():
    ret, frame = cap.read()
    if ret:
        p1 = frame.copy()
        p1_gray = cv2.cvtColor(p1, cv2.COLOR_BGR2GRAY)
        # Detect faces
        faces = face_cascade.detectMultiScale(p1_gray, 1.1, 4)
        for (x,y,w,h) in faces :
            #____________________________________________Gestion du filtre foulards_______________________________________
            if bool_activate_filtre_foulard:
                scale_factor_scarf = 1.9
                width_scarf = int(w)
                height_scarf = int(h * scale_factor_scarf)
                scarf_resize = cv2.resize(scarf, (width_scarf, height_scarf), 1, 1)
                alpha_scarf_resize = cv2.resize(alpha_scarf, (width_scarf, height_scarf), 1, 1)
                # Calcul des décalages vertical et horizontal
                offset_y_scarf = int(height_scarf * 0.14)
                #________Dans cette boucle, j'enlève le fond noir de l'image foulard grâce au masque alpha_________
                debut_x_scarf = x
                debut_y_scarf = y - offset_y_scarf
                for i in range(0, scarf_resize.shape[0]) :
                    for j in range(0, scarf_resize.shape[1]) :
                        if alpha_scarf_resize[i, j, 0] != 0 :
                            p1[(i + debut_y_scarf) % p1.shape[0], (j + debut_x_scarf) % p1.shape[1]] = scarf_resize[i, j]
            #____________________________________________Gestion du filtre lunettes_______________________________________            
            if bool_activate_filtre_lunette:
                # Réduire la zone de détection au visage
                faceROI_gray = p1_gray[y:y+h,x:x+w]
                eyes = eyes_cascade.detectMultiScale(faceROI_gray, 1.3, 5)
                # Si on detecte 2 yeux
                if len(eyes) == 2:
                    # Largeur et hauteur des lunettes
                    #width_sunglasses = abs( (eyes[1, 0] + eyes[1, 2]) - eyes[0, 0])
                    position_x_de_l_oeil_A = eyes[0,0] - int(eyes[0,2]/2)
                    position_x_de_l_oeil_B = eyes[1,0] - int(eyes[1,2]/2)
                    position_x_minimum = min(position_x_de_l_oeil_A,position_x_de_l_oeil_B)

                    position_y_de_l_oeil_A = eyes[0,1] - int(eyes[0,3]/2)
                    position_y_de_l_oeil_B = eyes[1,1] - int(eyes[1,3]/2)
                    position_y_minimum = min(position_x_de_l_oeil_A,position_x_de_l_oeil_B)

                    if(position_x_de_l_oeil_A == position_x_minimum) :
                        position_x_de_l_oeil_B = eyes[1,0] + int(eyes[1,2]/2)
                    else :
                        position_x_de_l_oeil_A = eyes[0,0] + int(eyes[0,2]/2)

                    if(position_y_de_l_oeil_A == position_y_minimum) :
                        position_y_de_l_oeil_B = eyes[1,1] + int(eyes[1,3]/2)
                    else :
                        position_y_de_l_oeil_A = eyes[0,1] + int(eyes[0,3]/2)
                    width_sunglasses = abs(position_x_de_l_oeil_B - position_x_de_l_oeil_A)
                    height_sunglasses = abs(position_y_de_l_oeil_B - position_y_de_l_oeil_A)
                    # Redimenssion des lunettes
                    scale_factor_sunglasses = 1.5
                    width_sunglasses = int(width_sunglasses * scale_factor_sunglasses)
                    height_sunglasses = int(height_sunglasses * scale_factor_sunglasses)
                    if height_sunglasses != 0 and width_sunglasses != 0 :
                        # On redimensionne les lunettes
                        sunglasses_resize = cv2.resize(sunglasses, (width_sunglasses, height_sunglasses),1,1)
                        # On redimensionne aussi le masque alpha des lunettes
                        alpha_sunglasses_resize = cv2.resize(alpha_sunglasses, (width_sunglasses, height_sunglasses),1,1)
                        # Calcul du centre des yeux
                        center_x_sunglasses = int((eyes[0, 0] + eyes[1, 0] + eyes[0, 2] + eyes[1, 2]) / 2)
                        center_y_sunglasses = int((eyes[0, 1] + eyes[1, 1] + eyes[0, 3] + eyes[1, 3]) / 2)
                        # Calcul des décalages vertical et horizontal
                        offset_x_sunglasses = int(width_sunglasses * 0.12)  
                        offset_y_sunglasses = int(height_sunglasses * 0.2)
                        # Positions de départ des lunettes
                        debut_x_sunglasses = center_x_sunglasses - int(width_sunglasses / 2) - offset_x_sunglasses
                        debut_y_sunglasses = center_y_sunglasses - int(height_sunglasses / 2) - offset_y_sunglasses
                        #________Dans cette boucle, j'enlève le fond noir de l'image lunettes grâce au masque alpha_________
                        for i in range(0,sunglasses_resize.shape[0]) :
                            for j in range(0, sunglasses_resize.shape[1]) :
                                if alpha_sunglasses_resize[i,j,0] != 0 :
                                    p1[i+debut_y_sunglasses+y,j+debut_x_sunglasses+x] = sunglasses_resize[i,j]
        #____________________________________________Gestion du filtre saturation______________________________________________
        if bool_activate_filtre_saturation:
            hsv_image = cv2.cvtColor(p1, cv2.COLOR_BGR2HSV)
            saturation_factor = 1.7
            hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * saturation_factor, 0, 255)
            # Reconvertir l'image de HSV à BGR
            p1 = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

        # Enregistrer la frame de la vidéo
        saved_video.write(p1)
        # Convertir l'image OpenCV en image Pillow
        img = Image.fromarray(cv2.cvtColor(p1, cv2.COLOR_BGR2RGB))
        img = ImageTk.PhotoImage(image=img)
        # Mettre à jour l'image dans l'étiquette
        panel.configure(image=img)
        panel.image = img
    # Planifier la prochaine mise à jour
    master.after(10, update_image)
# Démarrer la mise à jour de l'image
update_image()
# Démarrer la boucle principale Tkinter
master.mainloop()
#___________________________________________________Gestion de la fin du programme____________________________________________
# Libérez les ressources
saved_video.release()
cap.release()
cv2.destroyAllWindows()
