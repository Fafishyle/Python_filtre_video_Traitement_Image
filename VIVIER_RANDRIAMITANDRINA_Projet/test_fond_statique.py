import cv2
import os

# Charger l'image de la cabane
fondimg = cv2.imread('cabane.png')

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)

# Capture de la première image (qui est le fond)
if cap.isOpened():
    ret, frame = cap.read()
    capture_d_image_de_fond = frame.copy()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Incruster l'image de la cabane
    # Vous pouvez ajuster la position, la taille, etc.
    fond_frame_resize = cv2.resize(fondimg, (frame.shape[1], frame.shape[0]))

    # Créer un masque basé sur la différence des valeurs des canaux de couleur
    mask = ((frame[:, :, 1] - 20 <= capture_d_image_de_fond[:, :, 1]) & (capture_d_image_de_fond[:, :, 1] <= frame[:, :, 1] + 20))

    # Appliquer le masque pour l'incrustation de l'image de la cabane sur le fond
    frame[mask] = fond_frame_resize[mask]

    # Afficher le résultat
    cv2.imshow('Webcam avec Animation', frame)
    
    if cv2.waitKey(1) == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
