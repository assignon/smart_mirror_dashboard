import time
import cv2
import numpy as np
from .face_recognizer import FaceRecognizer
from statistics import mode
from flask_restful import Resource
from flask import request

face_recognizer = FaceRecognizer()


class FaceRecognitionSystem(Resource):

    @staticmethod
    def get():
        pass

    def post(self):
        encoded_face = request.data
        face = np.frombuffer(encoded_face, dtype=np.float32)
        result = face_recognizer.recognize_face(face)
        return {"id": result}

    @staticmethod
    def put():
        global face_recognizer
        face_recognizer = FaceRecognizer()
        return 200






# class VideoThread(QThread):
#     def __init__(self):
#
#         super(VideoThread, self).__init__()
#         self.face_detector = FaceDetector()
#         self.face_recognizer = FaceRecognizer()
#
#         # Relay status to app.py
#         self.face_detected = False
#         self.face_recognized = False
#         self.id_person = ""
#
#         self.progressbar_percentage = int(0)
#         self.faces = []
#         self.identified = False
#         self.reset_scan = False
#
#     def run(self):
#         capture_amount = 9
#         no_dectect_counter = 0
#         # capture from web cam
#         cap = cv2.VideoCapture(0)
#         cap.set(3, 1920)  # set Width
#         cap.set(4, 1080)  # set Height
#
#         # Set starting variables
#         capture_count = 0
#         results = []
#
#         # run face recognition if less than capture amount faces
#         start_scan = time.time()
#         while capture_count < capture_amount:
#             retval, cv_img = cap.read()
#             if retval:
#                 # Reset after 5 sec of inactivity
#                 if no_dectect_counter > 125:
#                     self.reset_scan = True
#                     break
#                 # Detect face
#                 face = self.face_detector.detect_face(cv_img,
#                                                       scale_factor=0.25)
#
#                 # if face is found run recognizer
#                 if not isinstance(face, bool):
#                     self.face_detected = True
#                     # Store face embeddings
#                     self.faces.append(face)
#                     # Run Face Recognition
#                     result = self.face_recognizer.recognize_face(face)
#                     results.append(result)
#                     # Update progress circle
#                     self.progressbar_percentage = int((capture_count /
#                                                        capture_amount) * 100)
#                     capture_count += 1
#
#                 else:
#                     # Track inactivity
#                     no_dectect_counter += 1
#
#         # Find the most recuring answer in the results
#         if self.reset_scan is not True:
#             print(results)
#             mode_results = mode(results)
#
#             # Go to next screen
#             self.identified = True
#
#             # Print scan time
#             scan_time = time.time() - start_scan
#             print("Scan time: {}".format(scan_time))
#
#             # Check if identification or unknown
#             if mode_results != 0:
#                 self.face_recognized = True
#                 self.id_person = (format(mode_results))
#                 print(f"ID of person is: {mode_results}")
#
#             # if person unknown extract more embeddings
#             else:
#                 start_extra_samples = time.time()
#                 # Amount of missing samples
#                 extra_capture_amount = 20 - capture_amount
#                 extra_capture_count = 0
#                 extra_frames = []
#                 # capture webcam frames
#                 while extra_capture_count < extra_capture_amount:
#                     retval, cv_img = cap.read()
#                     if retval:
#                         extra_frames.append(cv_img)
#                         extra_capture_count += 1
#                 # extract embeddings from frames
#                 for frame in extra_frames:
#                     face = self.face_detector.detect_face(frame,
#                                                           scale_factor=0.25,
#                                                           face_width=120)
#                     # if face is found
#                     if not isinstance(face, bool):
#                         self.faces.append(face)
#                 extra_samples_time = time.time() - start_extra_samples
#                 print(f"Extra samles build time: {extra_samples_time} sec")
#
#     def train_model(self, guest_id, expire_date):
#         self.face_recognizer.update_recognizer(self.faces, guest_id,
#                                                expire_date)
#
#     def reset(self):
#         self.face_detected = False
#         self.face_recognized = False
#         self.id_person = ""
#         self.progressbar_percentage = int(0)
#         self.faces = []
#         self.identified = False
