import cv2
import mediapipe as mp
import mouse
import tkinter as tk
import time


cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils


# Create a tkinter window to get the screen size
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()  # Close the tkinter window


index_y = 0
mouse_visible = False


while True:
   ret, frame = cap.read()


   if not ret:
       break  # Break the loop if reading the frame is unsuccessful


   frame = cv2.flip(frame, 1)
   frame_height, frame_width, channels = frame.shape


   rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
   output = hand_detector.process(rgb_frame)
   hands = output.multi_hand_landmarks


   if hands:
       for hand in hands:
           drawing_utils.draw_landmarks(frame, hand)
           landmarks = hand.landmark


           for id, landmark in enumerate(landmarks):
               x = int(landmark.x * frame_width)
               y = int(landmark.y * frame_height)


               if id == 8:
                   cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                   index_x = x
                   index_y = y


               if id == 4:
                   cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                   thumb_x = x
                   thumb_y = y


                   if abs(index_y - thumb_y) < 20:
                       mouse_visible = True
                       mouse.click()
                       time.sleep(1)  # Use time.sleep for the delay
                   elif abs(index_y - thumb_y) < 100:
                       mouse.move(index_x * screen_width / frame_width, index_y * screen_height / frame_height)
   else:
       mouse_visible = False


   if mouse_visible:
       cv2.imshow('Virtual Mouse', frame)
   else:
       cv2.imshow('Virtual Mouse', cv2.putText(frame, "Hand not detected", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2))


   cv2.waitKey(1)

