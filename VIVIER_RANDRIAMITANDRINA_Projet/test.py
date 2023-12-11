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

# Création de la barre des menu
menuBar = Menu(master)

# Création du menu principal 'Fichier'
menuFichier = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Choix des filtres", menu=menuFichier)
bool_activate_filtre_lunnette = False
def filtre_lunnette():
   print("hello")
   bool_activate_filtre_lunnette = True
# Création des sous menus : 'Filtre lunette de soleil', 'Quitter'
menuFichier.add_command(label="Filtre lunette de soleil", command= filtre_lunnette)
menuFichier.add_command(label="Quitter", command=master.quit)

# Configuration de la barre des menus
master.config(menu=menuBar)

# Créer un label pour afficher l'image
panel = Label(master)
panel.pack(side="bottom", fill="both", expand="yes")

# Fonction pour mettre à jour l'image
def update_image():
    ret, frame = cap.read()

    if ret:
        p1 = frame.copy()

        # Votre code de détection de visage et d'yeux ici...
        print(bool_activate_filtre_lunnette)
        if(bool_activate_filtre_lunnette):
            p1 = 255 - p1
        # ... (votre code existant pour détecter les yeux et appliquer les lunettes)

        # Convertir l'image OpenCV en image Pillow
        img = Image.fromarray(cv2.cvtColor(p1, cv2.COLOR_BGR2RGB))
        img = ImageTk.PhotoImage(image=img)

        # Mettre à jour l'image dans le label
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
