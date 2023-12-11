import cv2
from tkinter import *
from PIL import Image, ImageTk

# Charger les images
sunglasses = cv2.imread('sunglasses.png')
alpha_sunglasses = cv2.imread('alpha.png')

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)

# Interface graphique Tkinter
master = Tk()
master.geometry("640x480")  # Ajustez la taille selon vos besoins

# Création de la barre des menus
menuBar = Menu(master)

# Création du menu principal 'Fichier'
menuFichier = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Choix des filtres", menu=menuFichier)

# Déclarer la variable globale
bool_activate_filtre_lunnette = False

def filtre_lunnette():
    global bool_activate_filtre_lunnette
    bool_activate_filtre_lunnette = not bool_activate_filtre_lunnette

# Création des sous-menus : 'Filtre lunette de soleil', 'Quitter'
menuFichier.add_command(label="Activer/Desactiver le filtre lunnette de soleil", command=filtre_lunnette)
menuFichier.add_command(label="Quitter", command=master.quit)

# Configuration de la barre des menus
master.config(menu=menuBar)

# Créer une étiquette pour afficher l'image
panel = Label(master)
panel.pack(side="bottom", fill="both", expand="yes")

# Fonction pour mettre à jour l'image
def update_image():
    ret, frame = cap.read()
    if ret:
        p1 = frame.copy()
        #______________ FILTRE LUNNETTE____________________
        if bool_activate_filtre_lunnette:
            p1_gray = cv2.cvtColor(p1, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
            eyes_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
            # Detect faces
            faces = face_cascade.detectMultiScale(p1_gray, 1.1, 4)
            for (x,y,w,h) in faces :
                faceROI_gray = p1_gray[y:y+h,x:x+w]
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

# Arrêter la capture vidéo lorsque la fenêtre est fermée
cap.release()
cv2.destroyAllWindows()
