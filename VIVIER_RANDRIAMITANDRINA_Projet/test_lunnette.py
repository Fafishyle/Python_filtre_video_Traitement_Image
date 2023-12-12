import cv2
import numpy as np

# Charger les images
sunglasses = cv2.imread('sunglasses.png')
alpha_sunglasses = cv2.imread('alpha_sunglasses.png')

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
    eyes_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
    faces = face_cascade.detectMultiScale(p1_gray, 1.04, 10)    
    
    for (x, y, w, h) in faces:
        partie_supérieur_du_visage = int(y+h*3/5)
        faceROI_gray = p1_gray[y:partie_supérieur_du_visage, x:x+w]
        faceROI_rgb = p1[y:y+h, x:x+w]
        
        # Détection des yeux
        eyes = eyes_cascade.detectMultiScale(faceROI_gray, 1.02, 10)
        for (x1,y1,w1,h1) in eyes:
            faceROI_rgb = cv2.ellipse(faceROI_rgb, (x1 + int(w1*0.5), y1 + int(h1*0.5)), (int(w1*0.5),int(h1*0.5)), 0,0,360,(255, 0, 0), 4)
        p1[y:y+h,x:x+w] = faceROI_rgb
        
        # Si on détecte 2 yeux
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
            scale_factor = 1.5
            width_sunglasses = int(width_sunglasses * scale_factor)
            height_sunglasses = int(height_sunglasses * scale_factor)
            if height_sunglasses != 0 and width_sunglasses != 0 :
                # On redimensionne les lunettes
                sunglasses_resize = cv2.resize(sunglasses, (width_sunglasses, height_sunglasses),1,1)
                # On redimensionne aussi le masque alpha des lunettes
                alpha_sunglasses_resize = cv2.resize(alpha_sunglasses, (width_sunglasses, height_sunglasses),1,1)
                # Calcul du centre des yeux
                center_x = int((eyes[0, 0] + eyes[1, 0] + eyes[0, 2] + eyes[1, 2]) / 2)
                center_y = int((eyes[0, 1] + eyes[1, 1] + eyes[0, 3] + eyes[1, 3]) / 2)
                # Calcul des décalages vertical et horizontal
                offset_x = int(width_sunglasses * 0.12)  # Ajustez la valeur selon votre besoin
                offset_y = int(height_sunglasses * 0.2)  # Ajustez la valeur selon votre besoin
                # Positions de départ des lunettes
                debut_x = center_x - int(width_sunglasses / 2) - offset_x
                debut_y = center_y - int(height_sunglasses / 2) - offset_y
                #________Dans cette boucle, j'enlève le fond noir de l'image lunettes grâce au masque alpha_________
                for i in range(0,sunglasses_resize.shape[0]) :
                    for j in range(0, sunglasses_resize.shape[1]) :
                        if alpha_sunglasses_resize[i,j,0] != 0 :
                            p1[i+debut_y+y,j+debut_x+x] = sunglasses_resize[i,j]
    # Copier la partie traitée vers la trame
    frame = p1
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
