import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


class Draw:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.mp_drawing_styles = mp.solutions.drawing_styles

    def drawLandmarks(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.face_landmarks,
                                       self.mp_holistic.FACEMESH_CONTOURS)  # Draw face connections
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks,
                                       self.mp_holistic.POSE_CONNECTIONS)  # Draw pose connections
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks,
                                       self.mp_holistic.HAND_CONNECTIONS)  # Draw left-hand connections
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks,
                                       self.mp_holistic.HAND_CONNECTIONS)  # Draw right-hand connections
        
        
    def drawLandmarksPose(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks,
                                       self.mp_pose.POSE_CONNECTIONS) # Draw pose connections
        
    def drawStyledLandmarks(self, image, results):
        # Draw face connections
        self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_CONTOURS,
                                       self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                                       )
        # Draw pose connections
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
                                       )
        # Draw left-hand connections
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                                       )
        # Draw right-hand connections
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                                       )

    def drawPose(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
                                       )

    def drawFace(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_CONTOURS,
                                       self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1, circle_radius=1),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=1)
                                       )

    def drawHands(self, image, results):
        # Draw left-hand connections
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                                       )
        # Draw right-hand connections
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
                                       )
        
    def drawPoseLandmarks(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS,
                                       self.mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                                       self.mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2)
                                       )
        
