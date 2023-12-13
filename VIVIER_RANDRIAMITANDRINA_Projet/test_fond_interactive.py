import cv2
import os

# Charger l'animation (par exemple, une séquence d'images)
animation_folder = 'Dossier_d_animation'
animation_files = sorted(os.listdir(animation_folder))

# Initialiser la capture vidéo
cap = cv2.VideoCapture(0)
compteur_image_animation = 0

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
    if animation_files:
        animation_frame = cv2.imread(os.path.join(animation_folder, animation_files[compteur_image_animation]))
        # Vous pouvez ajuster la position, la taille, etc.
        animation_frame_resize = cv2.resize(animation_frame, (frame.shape[1], frame.shape[0]),1,1)
        h, w, _ = animation_frame_resize.shape
        #roi = frame[:h, :w]
        # Incrustation de fond
        for i in range (0,frame.shape[0]):
            for j in range (0,frame.shape[1]):
                #print(capture_d_image_de_fond[i,j,0], frame[i,j,0])
                if (capture_d_image_de_fond[i,j,0] == frame[i,j,0]):
                    #cv2.addWeighted(roi, 1, animation_frame_resize, 0.9, 0, roi)
                    frame[i,j]=animation_frame_resize[i,j]
    # Afficher le résultat
    cv2.imshow('Webcam avec Animation', frame)
    compteur_image_animation = (compteur_image_animation + 1)% len(animation_files)
    if cv2.waitKey(1) == ord('q'):
        break

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()
