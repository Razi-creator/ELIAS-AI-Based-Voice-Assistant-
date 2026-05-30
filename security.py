import cv2
import face_recognition
import os
import time

def login():
    current_folder = os.getcwd()
    image_path = os.path.join(current_folder, "owner.jpg")
    
    if not os.path.exists(image_path):
        print("❌ ERROR: 'owner.jpg' not found.")
        return False

    try:
        img_bgr = cv2.imread(image_path)
        if img_bgr is None: return False
        owner_image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        owner_encodings = face_recognition.face_encodings(owner_image)
        if not owner_encodings: return False
        owner_encoding = owner_encodings[0]
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print("📸 Initializing Biometric Scan...")
    video_capture = cv2.VideoCapture(0)
    
    access_granted = False
    start_time = time.time()
    scan_duration = 4  # Give the user 4 seconds to align their face

    while (time.time() - start_time) < scan_duration:
        ret, frame = video_capture.read()
        if not ret: break

        # --- THE FIX: SHOW THE CAMERA TO THE USER ---
        # Add a cool scanning text overlay
        cv2.putText(frame, "ELIAS BIOMETRIC SCAN IN PROGRESS...", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Display the video window
        cv2.imshow("ELIAS Security Check", frame)
        cv2.waitKey(1) # Required for the window to actually render

        # Analyze the frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces([owner_encoding], face_encoding, tolerance=0.45)
            if True in matches:
                access_granted = True
                break 
        
        if access_granted:
            # Show a green "Granted" box for a split second before closing
            cv2.putText(frame, "MATCH FOUND!", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow("ELIAS Security Check", frame)
            cv2.waitKey(500)
            break 

    # Clean up and close the camera window
    video_capture.release()
    cv2.destroyAllWindows()
    
    return access_granted

if __name__ == "__main__":
    login()