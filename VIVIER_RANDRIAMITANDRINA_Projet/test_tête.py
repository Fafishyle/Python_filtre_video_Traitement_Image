import cv2
import numpy as np

# Charger les images
scarf = cv2.imread('scarf.png')
alpha_scarf = cv2.imread('alpha_scarf.png')

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
    
    # Détection des visages
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
    faces = face_cascade.detectMultiScale(p1_gray, 1.1, 4)    
    
    for (x, y, w, h) in faces:
        #p1 = cv2.ellipse(p1, (x + int(w*0.5), y + int(h*0.5)), (int(w*0.5),int(h*0.5)), 0,0,360,(255, 0, 255), 4)
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
