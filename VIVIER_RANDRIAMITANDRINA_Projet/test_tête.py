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
    faces = face_cascade.detectMultiScale(p1_gray, 1.1, 4)    
    
    for (x, y, w, h) in faces:
        p1 = cv2.ellipse(p1, (x + int(w*0.5), y + int(h*0.5)), (int(w*0.5),int(h*0.5)), 0,0,360,(255, 0, 255), 4)
        
    # Copier la partie traitée vers la trame
    frame = p1
    cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
