import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class FaceAligner:
    PATH_TO_FRONTAL_FACE = "/face_aligment/haarcascade_frontalface_default.xml"
    PATH_TO_EYE = "/face_aligment/haarcascade_eye.xml"
    def __init__(self) -> None:
        frontal_face_xml = os.path.abspath(os.getcwd() + self.PATH_TO_FRONTAL_FACE)
        eye_xml = os.path.abspath(os.getcwd() + self.PATH_TO_EYE)
        
        self.face_detector = cv2.CascadeClassifier(frontal_face_xml)
        self.eye_detector = cv2.CascadeClassifier(eye_xml)
        
        del frontal_face_xml, eye_xml


    def align(self, image):
        # img_raw = image.copy()
        face_img = self.f_detector(image)
        direction, angle = self.e_detector(face_img)
        new_img = Image.fromarray(face_img)
        # print(direction)
        # print(angle)
        new_img = np.array(new_img.rotate(direction * angle))
        return new_img


    def f_detector(self, full_image):
        faces = self.face_detector.detectMultiScale(full_image, 1.1, 5)
        if len(faces) == 0:
            return -1
        face_x, face_y, face_w, face_h = faces[0]
        face_img = full_image[int(face_y):int(face_y+face_h), int(face_x):int(face_x+face_w)]
        return face_img


    def e_detector(self, gray_image):
        eyes = self.eye_detector.detectMultiScale(gray_image, 1.1)
        for index, (eye_x, eye_y, eye_w, eye_h) in enumerate(eyes):
            if index == 0:
                eye_1 = (eye_x, eye_y, eye_w, eye_h)

            elif index == 1:
                eye_2 = (eye_x, eye_y, eye_w, eye_h)

        # Deciding which one is left eye
        if eye_1[0] < eye_2[0]:
            left_eye = eye_1
            right_eye = eye_2
        else:
            left_eye = eye_2
            right_eye = eye_1

        left_eye_center = (int(left_eye[0] + (left_eye[2] / 2)), int(left_eye[1] + (left_eye[3] / 2)))
        left_eye_x = left_eye_center[0]; left_eye_y = left_eye_center[1]
        
        right_eye_center = (int(right_eye[0] + (right_eye[2]/2)), int(right_eye[1] + (right_eye[3]/2)))
        right_eye_x = right_eye_center[0]; right_eye_y = right_eye_center[1]

        # cv2.circle(gray_image, left_eye_center, 10, 0, 10)
        # cv2.circle(gray_image, right_eye_center, 20, 255, 10)
        # cv2.line(gray_image,right_eye_center, left_eye_center, 255,2)

        if left_eye_y > right_eye_y:
            point_3rd = (right_eye_x, left_eye_y)
            direction = -1 #rotate same direction to clock
        else:
            point_3rd = (left_eye_x, right_eye_y)
            direction = 1 #rotate inverse direction of clock

        a = self.euclidean_distance(left_eye_center, point_3rd)
        b = self.euclidean_distance(right_eye_center, left_eye_center)
        c = self.euclidean_distance(right_eye_center, point_3rd)

        cos_a = (b*b + c*c - a*a)/(2*b*c)
        angle = np.arccos(cos_a) # In radians
        angle = (angle * 180) / math.pi # In degrees
        if direction == -1:
            angle = 90 - angle

        return (direction, angle)

    @staticmethod
    def euclidean_distance(a, b):
        x1 = a[0]; y1 = a[1]
        x2 = b[0]; y2 = b[1]
        return math.sqrt(((x2 - x1) * (x2 - x1)) + ((y2 - y1) * (y2 - y1)))
        


# if __name__=="__main__":
#     face = FaceAligner()
#     img = cv2.imread("./test.jpg")
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     test = face.align(img)
#     #plt.imshow(test, cmap="gray")
#     #plt.show()
#     img = Image.fromarray(test)
#     img.save("test.png")