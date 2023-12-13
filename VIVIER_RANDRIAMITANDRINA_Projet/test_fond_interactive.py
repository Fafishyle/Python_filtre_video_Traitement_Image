import cv2
import os

# Charger l'animation
animation_folder = 'Dossier_d_animation'
animation_files = sorted(os.listdir(animation_folder))

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
    if animation_files:
        animation_frame = cv2.imread(os.path.join(animation_folder, animation_files[compteur_image_animation]))
        
        # Vous pouvez ajuster la position, la taille, etc.
        animation_frame_resize = cv2.resize(animation_frame, (frame.shape[1], frame.shape[0]))

        #Mettre en gris la frame et l'image de fond
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_capture_d_image_de_fond = cv2.cvtColor(capture_d_image_de_fond, cv2.COLOR_BGR2GRAY)
        mask = ((gray_frame -30 <= gray_capture_d_image_de_fond) & (gray_capture_d_image_de_fond <= gray_frame + 30))

        # Incrustation de l'animation
        #mask = ((frame[:, :, 2] - 20 <= capture_d_image_de_fond[:, :, 2]) & (capture_d_image_de_fond[:, :, 2] <= frame[:, :, 2] + 20))
        frame[mask] = animation_frame_resize[mask]

    # Afficher le résultat
    cv2.imshow('Webcam avec Animation', frame)

    # Mise à jour du compteur pour passer à la frame suivante de l'animation
    compteur_image_animation = (compteur_image_animation + 1) % len(animation_files)

    if cv2.waitKey(1) == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
