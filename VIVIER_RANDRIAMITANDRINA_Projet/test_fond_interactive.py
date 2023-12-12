import cv2
import os

# Charger l'animation (par exemple, une séquence d'images)
animation_folder = 'Dossier_d_animation'
animation_files = sorted(os.listdir(animation_folder))

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Incruster l'animation
    if animation_files:
        animation_frame = cv2.imread(os.path.join(animation_folder, animation_files[0]))
        # Vous pouvez ajuster la position, la taille, etc.
        h, w, _ = animation_frame.shape
        roi = frame[:h, :w]
        cv2.addWeighted(roi, 1, animation_frame, 0.7, 0, roi)

    # Afficher le résultat
    cv2.imshow('Webcam avec Animation', frame)

    if cv2.waitKey(1) == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
