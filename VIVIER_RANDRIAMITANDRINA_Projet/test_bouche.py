import cv2
import numpy as np

# Charger les images
scarf = cv2.imread('scarf.png')
alpha_scarf = cv2.imread('alpha_scarf.png')
mole = cv2.imread('mole.png')
alpha_mole = cv2.imread('alpha_mole.png')

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Convertir en niveaux de gris
    p1 = frame
    p1_gray = cv2.cvtColor(p1, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(p1_gray, 1.1, 4)
    # Détection des visages
    mouth_cascade = cv2.CascadeClassifier('haarcascade_mcs_mouth.xml')    
    for (x, y, w, h) in faces:
        # Pour la bouche, on va réduire la zone de recherche à la moitié du dessous du visage
        partie_inférieur_du_visage = int(y+(h*2/3))
        faceROI_gray = p1_gray[partie_inférieur_du_visage:y+h, x:x+w]
        faceROI_rgb = p1[partie_inférieur_du_visage:y+h, x:x+w]
        mouths = mouth_cascade.detectMultiScale(faceROI_gray, 1.7, 4)    
        for (x1,y1,w1,h1) in mouths:
            scale_factor_mole = 0.2
            width_mole = int(w* scale_factor_mole)
            height_mole = int(h * scale_factor_mole)
            mole_resize = cv2.resize(mole, (width_mole, height_mole), 1, 1)
            alpha_mole_resize = cv2.resize(alpha_mole, (width_mole, height_mole), 1, 1)
            faceROI_rgb = cv2.ellipse(faceROI_rgb, (x1 + int(w1*0.5), y1 + int(h1*0.5)), (int(w1*0.5),int(h1*0.5)), 0,0,360,(255, 0, 0), 4)
            #faceROI_rgb[0:mole.shape[],0:mole.shape[0]] = mole
            offset_y_mole = int(height_mole * 2.9)
            debut_x_mole = int(x1+w1*3/4)
            debut_y_mole = y1 + offset_y_mole
            for i in range (0,mole_resize.shape[0]) :
                for j in range (0,mole_resize.shape[1]) :
                    if alpha_mole_resize[i, j, 0] != 0 :
                        p1[(y+i + debut_y_mole) % p1.shape[0], (x+j + debut_x_mole) % p1.shape[1]] = mole_resize[i, j]
            break
        scale_factor_scarf = 1.9
        width_scarf = int(w)
        height_scarf = int(h * scale_factor_scarf)
        scarf_resize = cv2.resize(scarf, (width_scarf, height_scarf), 1, 1)
        alpha_scarf_resize = cv2.resize(alpha_scarf, (width_scarf, height_scarf), 1, 1)
        # Calcul des décalages vertical et horizontal
        offset_y_scarf = int(height_scarf * 0.14)  # Ajustez la valeur selon votre besoin
        #________Dans cette boucle, j'enlève le fond noir de l'image foulard grâce au masque alpha_________
        debut_x_scarf = x
        debut_y_scarf = y - offset_y_scarf
        for i in range(0, scarf_resize.shape[0]) :
            for j in range(0, scarf_resize.shape[1]) :
                if alpha_scarf_resize[i, j, 0] != 0 :
                    p1[(i + debut_y_scarf) % p1.shape[0], (j + debut_x_scarf) % p1.shape[1]] = scarf_resize[i, j]

    # Copier la partie traitée vers la trame
    frame = p1
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
