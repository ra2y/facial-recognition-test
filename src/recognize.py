import cv2
import face_recognition
import pickle
import os

ENCODINGS_FILE = "data/known_faces/encodings.pkl"
TOLERANCE = 0.6  # lower = stricter match. 0.6 is face_recognition's default.
GRANT_COOLDOWN_FRAMES = 30 # avoid flickering text every single frame

def load_known_encodings():
    if not os.path.exists(ENCODINGS_FILE):
        print("No enrolled faces found. Run enroll.py first.")
        return {}, []

    with open(ENCODINGS_FILE, "rb") as f:
        known_encodings = pickle.load(f)

    names = list(known_encodings.keys())
    encodings = list(known_encodings.values())
    return dict(zip(names, encodings)), encodings

def main():
    known_dict, known_encodings_list = load_known_encodings()
    known_names_list = list(known_dict.keys())

    if not known_encodings_list:
        return

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        access_granted = False

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(
                known_encodings_list, face_encoding, tolerance=TOLERANCE
            )
            distances = face_recognition.face_distance(known_encodings_list, face_encoding)

            name = "Unknown"
            if True in matches:
                best_match_index = distances.argmin()
                if matches[best_match_index]:
                    name = known_names_list[best_match_index]
                    access_granted = True

            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Access banner
        banner_text = "ACCESS GRANTED" if access_granted else "ACCESS DENIED"
        banner_color = (0, 200, 0) if access_granted else (0, 0, 200)
        cv2.rectangle(frame, (0, 0), (frame.shape[1], 50), banner_color, -1)
        cv2.putText(frame, banner_text, (20, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()