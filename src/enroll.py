import cv2
import face_recognition
import os
import pickle

KNOWN_FACES_DIR = "data/known_faces"
ENCODINGS_FILE = "data/known_faces/encodings.pkl"

def capture_reference_photo(name):
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture your photo, 'q' to cancel.")

    photo_path = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Enrollment - Press SPACE to capture", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):
            photo_path = os.path.join(KNOWN_FACES_DIR, f"{name}.jpg")
            cv2.imwrite(photo_path, frame)
            print(f"Saved photo to {photo_path}")
            break
        elif key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return photo_path

def generate_encoding(name, photo_path):
    image = face_recognition.load_image_file(photo_path)
    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        print("No face found in the photo! Try again with better lighting/framing.")
        return None

    if len(encodings) > 1:
        print("Multiple faces found — using the first one detected.")

    return encodings[0]

def save_encoding(name, encoding):
    # Load existing encodings dict, or start a new one
    if os.path.exists(ENCODINGS_FILE):
        with open(ENCODINGS_FILE, "rb") as f:
            known_encodings = pickle.load(f)
    else:
        known_encodings = {}

    known_encodings[name] = encoding

    with open(ENCODINGS_FILE, "wb") as f:
        pickle.dump(known_encodings, f)

    print(f"Enrolled '{name}' successfully.")

def main():
    name = input("Enter your name for enrollment: ").strip()
    photo_path = capture_reference_photo(name)

    if photo_path:
        encoding = generate_encoding(name, photo_path)
        if encoding is not None:
            save_encoding(name, encoding)

if __name__ == "__main__":
    main()