import cv2
import os
import numpy as np

# Charger l'animation
animation_folder_bird = 'Dossier_d_animation_oiseau'
animation_files_bird = sorted(os.listdir(animation_folder_bird))

alpha_animation_folder = 'Dossier_d_animation_oiseau_alpha'
alpha_animation_files = sorted(os.listdir(alpha_animation_folder))

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)
compteur_image_animation = 0

# Capture d'image du fond
ret, capture_d_image_de_fond = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Incruster l'animation
    if animation_files_bird and alpha_animation_files:
        animation_frame = cv2.imread(os.path.join(animation_folder_bird, animation_files_bird[compteur_image_animation]))
        alpha_animation_frame = cv2.imread(os.path.join(alpha_animation_folder, alpha_animation_files[compteur_image_animation]))

        # Vous pouvez ajuster la position, la taille, etc.
        animation_frame_resize = cv2.resize(animation_frame, (frame.shape[1], frame.shape[0]))
        alpha_animation_frame_resize = cv2.resize(alpha_animation_frame, (frame.shape[1], frame.shape[0]))

        # Convertir l'image alpha en niveaux de gris
        gray_alpha_animation_frame_resize = cv2.cvtColor(alpha_animation_frame_resize, cv2.COLOR_BGR2GRAY)

        # Comparaison des images en niveaux de gris
        mask = ((cv2.absdiff(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.cvtColor(capture_d_image_de_fond, cv2.COLOR_BGR2GRAY)) < 20) & (gray_alpha_animation_frame_resize != np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)))

        # Incrustation de l'animation basée sur le masque
        frame[mask] = animation_frame_resize[mask]

    # Afficher le résultat
    cv2.imshow('Webcam avec Animation', frame)

    # Mise à jour du compteur pour passer à la frame suivante de l'animation
    compteur_image_animation = (compteur_image_animation + 1) % len(animation_files_bird)

    if cv2.waitKey(1) == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
