import cv2
import os

# Charger l'animation (par exemple, une séquence d'images)
animation_folder = 'Dossier_d_animation'
animation_files = sorted(os.listdir(animation_folder))

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)
compteur_animation_files = 0
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Incruster l'animation
    if animation_files:
        animation_frame = cv2.imread(os.path.join(animation_folder, animation_files[compteur_animation_files]))
        # Vous pouvez ajuster la position, la taille, etc.
        animation_frame_resize = cv2.resize(animation_frame, (frame.shape[1], frame.shape[0]),1,1)
        h, w, _ = animation_frame_resize.shape
        roi = frame[:h, :w]
        cv2.addWeighted(roi, 1, animation_frame_resize, 0.9, 0, roi)

    # Afficher le résultat
    cv2.imshow('Webcam avec Animation', frame)
    compteur_animation_files = (compteur_animation_files + 1 ) % (len(animation_files))
    if cv2.waitKey(1) == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
