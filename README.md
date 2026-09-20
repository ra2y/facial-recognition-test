# Facial Recognition Attendance App

A desktop app that uses your webcam to recognize your face, show an "Access Granted / Denied" overlay, and log each recognition event which includes a name and a timestamp to a local database.

---

## Design

### OpenCV / face_recognition / dlib
The libraries opencv-python, face_recognition are well documented. Recognition is a distance comparison between two 128-number vectors.

### SQLite for attendance logging
The attendance logs are structured and relational (a person, a timestamp).

---

## Project Structure & What Each File Does

```
face-recognition-app/
├── venv/
├── data/
│   ├── known_faces/         # Reference photos + stored face encodings (auto generated)
│   └── attendance.db        # SQLite database of recognition events (auto generated)
├── src/
│   ├── capture.py           # opens the webcam and displays the raw feed
│   ├── detect.py            # detects faces in the live feed and draws bounding boxes
│   ├── enroll.py            # captures reference photo and saves face encoding
│   ├── recognize.py         # live recognition, name labeling, and access granted/denied banner
│   ├── database.py          # SQLite schema creation and attendance logging functions
│   ├── main.py               # Ties everything together
│   └── view_logs.py         # prints attendance history
├── .gitignore
└── README.md
```

Each src/ file was built as a standalone, you can still run most of them individually, main.py runs the main app.

### main.py examplanation

1. **database.init_db()** (from database.py) - makes sure the SQLite tables exist before anything else runs.
2. **load_known_encodings()** - loads the saved face encodings from data/known_faces/encodings.pkl (this file is created by enroll.py, you must run enroll.py at least once before main.py will have anyone to recognize).
3. **The webcam loop** (same as capture.py) - continuously reads frames from the camera.
4. **Face detection** (same as detect.py) - finds face locations in each frame using face_recognition.face_locations().
5. **Face recognition** (same as recognize.py) - generates an encoding for each detected face and compares it against the known encodings to determine a name (or "Unknown"), then draws the label and the Access Granted/Denied banner.
6. **Attendance logging** (from database.py) - when a known face is recognized, log_attendance(name) is called

---

## Auto Generated Files in data/

### data/known_faces/<name>.jpg
Created by enroll.py. This is the raw reference photo taken during enrollment. Kept for debugging.

### data/known_faces/encodings.pkl
Also created by enroll.py, containing a dictionary that maps {name: face_encoding}. Each face_encoding is a 128-number vector representing that person's facial geometry. This is what recognize.py and main.py load and compare live faces against, it's a NumPy array.

### data/attendance.db
Created by database.py's init_db(). A SQLite database file containing two tables,
- **people** - one row per enrolled person (id, name)
- **attendance_log** - one row per recognition event (id, person_id, timestamp)

---

## Setup

### 1. Set up the environment
```
python3 -m venv venv

venv\Scripts\activate
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Enroll face
```
python src/enroll.py
```
Enter your name, frame your face clearly, press space to capture. This creates your reference photo and encoding in data/known_faces/.

### 4. Run the app
```
python src/main.py
```
This initializes the database on the first run, loads your enrolled encoding, opens your webcam, and starts recognizing, labeling, banner displaying, and logging attendance. Press q to quit.

### 5. View attendance history
```
python src/view_logs.py
```
