import cv2
import os

fond = cv2.imread('cabane.png')
# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)
# Capture d'image de la première image (qui est le fond)
if cap.isOpened():
    ret, frame = cap.read()
    capture_d_image_de_fond = frame

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # Incruster l'animation
    # Vous pouvez ajuster la position, la taille, etc.
    fond_frame_resize = cv2.resize(fond, (frame.shape[1], frame.shape[0]),1,1)
        # Incrustation de fond
    for i in range (0,frame.shape[0]):
        for j in range (0,frame.shape[1]):
            if (capture_d_image_de_fond[i,j,0] == frame[i,j,0]):
                    #cv2.addWeighted(roi, 1, animation_frame_resize, 0.9, 0, roi)
                    frame[i,j]=fond_frame_resize[i,j]
    # Afficher le résultat
    cv2.imshow('Webcam avec Animation', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
