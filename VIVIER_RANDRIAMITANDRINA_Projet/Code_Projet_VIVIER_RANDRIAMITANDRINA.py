import cv2
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import os

#___________________________________________________Gestion des fichiers média __________________________________________
# Image lunettes
sunglasses = cv2.imread('sunglasses.png')
alpha_sunglasses = cv2.imread('alpha_sunglasses.png')
# Image foulard
scarf = cv2.imread('scarf.png')
alpha_scarf = cv2.imread('alpha_scarf.png')
# Image grain de beauté
mole = cv2.imread('mole.png')
alpha_mole = cv2.imread('alpha_mole.png')
# Image fond ocean
ocean = cv2.imread('ocean.png')
# Image fond cabane
cabane = cv2.imread('cabane.png')
# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)
# Récupérer les propriétés de la vidéo capturée
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
# Récupérer les fichiers de cascades de haar pour la detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')
# Charger le dossier d'animation pour le fond animé
animation_folder = 'Dossier_d_animation'
animation_files = sorted(os.listdir(animation_folder))   
#_________________________________________________Gestion de l'interface graphique_______________________________________
# Interface graphique Tkinter
master = Tk()
master.geometry("640x480")
# Création de la barre des menus
menuBar = Menu(master)
# Création du menu principal 'Fichier'
menuFichier = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Choix des filtres", menu=menuFichier)
label = Label(master, text="", font=("Helvetica", 12))
# Placer le label en bas de la fenêtre
label.pack(side="bottom")
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
#__________________________________________________Gestion du filtre grain de beauté____________________________________________
# Gestion du filtre foulard avec une variable globale booléen
bool_activate_filtre_grain = False
def filtre_grain():
    global bool_activate_filtre_grain
    bool_activate_filtre_grain = not bool_activate_filtre_grain
#__________________________________________________Gestion du fond image animé plage____________________________________________
# Gestion du filtre fond animée plage avec une variable globale booléen
bool_activate_filtre_plage_animee = False
def filtre_plage_animee():
    global bool_activate_filtre_plage_animee
    global bool_activate_filtre_cabane
    global bool_activate_filtre_ocean
    bool_activate_filtre_cabane = False
    bool_activate_filtre_ocean = False
    bool_activate_filtre_plage_animee = not bool_activate_filtre_plage_animee
#__________________________________________________Gestion du fond image ocean____________________________________________
# Gestion du filtre fond ocean avec une variable globale booléen
bool_activate_filtre_ocean = False
def filtre_ocean():
    global bool_activate_filtre_ocean
    global bool_activate_filtre_cabane
    global bool_activate_filtre_plage_animee
    bool_activate_filtre_plage_animee = False   
    bool_activate_filtre_cabane = False
    bool_activate_filtre_ocean = not bool_activate_filtre_ocean
#__________________________________________________Gestion du fond image cabane____________________________________________
# Gestion du filtre fond cabane avec une variable globale booléen
bool_activate_filtre_cabane = False
def filtre_cabane():
    global bool_activate_filtre_cabane
    global bool_activate_filtre_ocean
    global bool_activate_filtre_plage_animee
    bool_activate_filtre_plage_animee = False 
    bool_activate_filtre_ocean = False
    bool_activate_filtre_cabane = not bool_activate_filtre_cabane
#_________________________________________________Gestion du sous menu de fond_______________________________________
def filtre_fond_menu ():
    menuFond = Menu(menuFichier)
    menuFond.add_command(label="Activer/Desactiver fond ocean", command=filtre_ocean)
    menuFond.add_command(label="Activer/Desactiver fond cabane", command=filtre_cabane)
    menuFond.add_command(label="Activer/Desactiver fond animée plage", command=filtre_plage_animee)
    return menuFond

#_________________________________________________Gestion des filtre en sous menu_______________________________________
# Création des sous-menus : 'Filtre lunette de soleil', 'Quitter'
menuFichier.add_command(label="Activer/Desactiver le filtre foulard", command=filtre_foulard)
menuFichier.add_command(label="Activer/Desactiver le filtre lunette de soleil", command=filtre_lunette)
menuFichier.add_command(label="Activer/Desactiver le filtre grain de beauté", command=filtre_grain)
menuFichier.add_command(label="Activer/Desactiver le filtre saturation", command=filtre_saturation)
menuFond = filtre_fond_menu()
menuFichier.add_cascade(label = "Filtre fond", menu = menuFond)
menuFichier.add_command(label="Quitter", command=master.quit)
# Configuration de la barre des menus
master.config(menu=menuBar)
# Créer une étiquette pour afficher l'image
panel = Label(master)
panel.pack(side="bottom", fill="both", expand="yes")
def is_in_range(value, lower_limit, upper_limit):
    return lower_limit <= value <= upper_limit
#_________________________________________________Gestion du texte sur la fenêtre_______________________________________
# Fonction pour mettre à jour le texte
def update_text():
    # Mettre à jour le texte avec vos informations
    text = "Votre texte ici"
    # Mettre à jour le texte du label
    label.config(text=text)
    # Planifier la prochaine mise à jour après un certain délai (en millisecondes)
    master.after(1000, update_text)
#___________________________________________________Gestion de l'enregistrement vidéo____________________________________________
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
saved_video = cv2.VideoWriter('video_enregistré.avi', fourcc, 20.0, (frame_width, frame_height))
#___________________________________________________Fonction pour modifier l'arrière plan statique de la webcam____________________________________________
def miseAJourFond(image, frame):
    fond_frame_resize = cv2.resize(image, (frame.shape[1], frame.shape[0]),1,1)
        # Incrustation de fond
    mask = (capture_d_image_de_fond == frame)
    frame[mask] = fond_frame_resize[mask]
    return frame
#___________________________________________________Gestion de l'arrière plan____________________________________________
compteur_image_animation = 0
# Capture d'image de la première image (qui sera l'arrière plan)
if cap.isOpened():
    ret, frame = cap.read()
    capture_d_image_de_fond = frame
#___________________________________________________Gestion de la vidéo webcam____________________________________________
# Fonction pour mettre à jour l'image
def update_image():
    global compteur_image_animation
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
                # Calcul des décalages vertical
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
                partie_supérieur_du_visage = int(y+h*3/5)
                # Réduire la zone de détection au visage
                faceROI_gray = p1_gray[y:partie_supérieur_du_visage, x:x+w]
                eyes = eyes_cascade.detectMultiScale(faceROI_gray, 1.02, 10)
                # Si on detecte 2 yeux
                if len(eyes) == 2:
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
            #____________________________________________Gestion du filtre grain de beauté_______________________________________            
            if bool_activate_filtre_grain:     
                partie_inférieur_du_visage = int(y+(h*2/3))
                faceROI_gray_mouth = p1_gray[partie_inférieur_du_visage:y+h, x:x+w]
                mouths = mouth_cascade.detectMultiScale(faceROI_gray_mouth, 1.7, 4)
                for (x2,y2,w2,h2) in mouths:
                    scale_factor_mole = 0.2
                    width_mole = int(w* scale_factor_mole)
                    height_mole = int(h * scale_factor_mole)
                    mole_resize = cv2.resize(mole, (width_mole, height_mole), 1, 1)
                    alpha_mole_resize = cv2.resize(alpha_mole, (width_mole, height_mole), 1, 1)
                    offset_y_mole = int(height_mole * 2.9)
                    debut_x_mole = int(x2+w2*3/4)
                    debut_y_mole = y2 + offset_y_mole
                    for i in range (0,mole_resize.shape[0]) :
                        for j in range (0,mole_resize.shape[1]) :
                            if alpha_mole_resize[i, j, 0] != 0 :
                                p1[(y+i + debut_y_mole) % p1.shape[0], (x+j + debut_x_mole) % p1.shape[1]] = mole_resize[i, j]
                    break
            #____________________________________________Gestion du filtre arrière plan plage animée_______________________________________                    
            if bool_activate_filtre_plage_animee:
                if animation_files:
                    animation_frame = cv2.imread(os.path.join(animation_folder, animation_files[compteur_image_animation]))
                    animation_frame_resize = cv2.resize(animation_frame, (p1.shape[1], p1.shape[0]),1,1)
                    # Incrustation de fond
                    mask = (capture_d_image_de_fond == p1)
                    p1[mask] = animation_frame_resize[mask]
                compteur_image_animation = (compteur_image_animation + 1)% len(animation_files)
            #____________________________________________Gestion du filtre arrière plan océan_______________________________________                    
            if bool_activate_filtre_ocean:
                p1 = miseAJourFond(ocean, p1)
            #____________________________________________Gestion du filtre arrière plan cabane_______________________________________                    
            if bool_activate_filtre_cabane:
                p1 = miseAJourFond(cabane, p1)
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
update_text()
# Démarrer la boucle principale Tkinter
master.mainloop()
#___________________________________________________Gestion de la fin du programme____________________________________________
# Libérez les ressources
saved_video.release()
cap.release()
cv2.destroyAllWindows()
