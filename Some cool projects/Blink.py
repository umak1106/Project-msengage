import cv2
from cv2 import COLOR_BGR2RGB
from cv2 import FONT_HERSHEY_COMPLEX
import mediapipe as mp
import math
import time
import threading
import winsound
from gui import getDuration

import tkinter as tk

duration =10
def getDuration():
    root = tk.Tk()
    root.geometry('700x200')
    root.configure(bg="white")
    root.title("Welcome to blinkr")

    instructionText = tk.Text(root,height=2,width=100,bg="white",padx=20,bd=0)
    instructionText.tag_configure("center",justify="center")
    instructionText.insert(tk.INSERT,"Set the time interval to check for blinks (in seconds)")
    instructionText.config(state="disabled")
    entry1 = tk.Entry(root,width=40,bg="gray")
    instructionText.grid(row=0,column=0)
    entry1.grid(row=1,column=0)

    def getValueAndCLose():
        text = entry1.get()
        if text=="":
            global duration
        else:
            global duration
            duration = text
        root.destroy()

    btn = tk.Button(root,text="Proceed",command = getValueAndCLose,pady=4,bd=0)
    btn.grid(row = 2,column = 0)
    root.mainloop()
    return duration

duration = int(getDuration())

blink_count_list = [0] # List to store the number of blinks after every blink

blinks = 0 # To track total no of blinks

counter = 0 # This is to make the blinks not add up multiple times within one blink instance this variable is used below


#Function to run in thread that watches the blink_count_list
def thread_func():
    while True:
        last_blink = blink_count_list[len(blink_count_list)-1] # Check the latest number of blinks so far
        time.sleep(duration) # Sleep for a while
        last_blink_after_sleep = blink_count_list[len(blink_count_list)-1] # Check the latest blinks again and if it's the same as before sleep then alert
        
        # Alerting condition
        if last_blink == last_blink_after_sleep:
            winsound.Beep(340,700)
        
        # Loop break condition (after we terminate the program thread should temrinate too)
        # We modify this in the end of the program to break this infinite while loop that doesnt terminate even after exiting camera
        global stop_threads
        if stop_threads:
            break

stop_threads = False

#Creating a new thread in background to track blinks every 5s 
th = threading.Thread(target = thread_func)
th.start()

print("\n---------ENSURE THE TERMINAL STAYS OPEN FOR THE PROGRAM TO RUN---------\n")

# Initializing face mesh object from mediapipe
face_mesh = mp.solutions.face_mesh.FaceMesh() 

# Capturing video from webcam
cap = cv2.VideoCapture(0)

# All our execution goes into this loop
while True:

    # Reading the frames given by videoCapture
    success, frame = cap.read()
    height,width,channel = frame.shape   

    #Converting to RGB as mediapipe reads in rgb not bgr(opencv default)
    rgb_frame = cv2.cvtColor(frame,COLOR_BGR2RGB)

    #Processing the frame to see if there are faces and detecting landmarks on it
    result = face_mesh.process(rgb_frame) #process() returns a tuple multi_face_landmarks
    
# ----------- Marking just the eye landmarks -----------
    if result.multi_face_landmarks: #To prevent program from terminating due to face not found error
        left_eye_landmarks_inner = [263,249,390,373,374,380,381,382,362,466,388,387,386,385,384,398]
        right_eye_landmarks_inner = [246,161,160,159,158,157,173,33,7,163,144,145,153,154,155,133]
        for facial_landmarks in result.multi_face_landmarks:
            
    
            # -----Extreme points(landmarks) to find aspect ratio from-------
            # left_bottom - 374
            # left_top - 386
            # left_left - 382
            # left_right - 249
            # right_top - 159
            # right_bottom - 145
            # right_right - 173
            # right_left - 7

            #Finding distances between eye extremes
            
            #LEFT EYE
            pt_left_bottom = facial_landmarks.landmark[374]
            x_lb = int(pt_left_bottom.x*width)
            y_lb = int(pt_left_bottom.y*height)
            pt_left_top = facial_landmarks.landmark[386]
            x_lt = int(pt_left_top.x*width)
            y_lt = int(pt_left_top.y*height)
            pt_left_left = facial_landmarks.landmark[382]
            x_ll = int(pt_left_left.x*width)
            y_ll = int(pt_left_left.y*height)
            pt_left_right = facial_landmarks.landmark[249]
            x_lr = int(pt_left_right.x*width)
            y_lr = int(pt_left_right.y*height)

            #RIGHT EYE
            pt_right_top = facial_landmarks.landmark[159]
            x_rt = int(pt_right_top.x*width)
            y_rt = int(pt_right_top.y*height)
            pt_right_bottom = facial_landmarks.landmark[145]
            x_rb = int(pt_right_bottom.x*width)
            y_rb = int(pt_right_bottom.y*height)
            pt_right_right = facial_landmarks.landmark[173]
            x_rr = int(pt_right_right.x*width)
            y_rr = int(pt_right_right.y*height)
            pt_right_left = facial_landmarks.landmark[7]
            x_rl = int(pt_right_left.x*width)
            y_rl = int(pt_right_left.y*height)
            
            # Finding distances
            
            left_vertical = math.dist((x_lt,y_lt),(x_lb,y_lb))
            left_horizontal = math.dist((x_lr,y_lr),(x_ll,y_ll))
            right_vertical = math.dist((x_rt,y_rt),(x_rb,y_rb))
            right_horizontal = math.dist((x_rl,y_rl),(x_rr,y_rr))

            #Finding EAR(Eye aspect ratio)
            
            ear_left = left_vertical/left_horizontal
            ear_right = right_vertical/right_horizontal


            # Condition for counting a blink 
            # Note:- We use the counter variable to prevent blinks variable from increasing multiple times within one blink
            if ear_left<0.3 and counter == 0:
                blinks+=1
                # Appending blink count to list everytime blink increases so that thread function can use this array to check and alert
                if len(blink_count_list)>3: # To limit list size to 5
                    blink_count_list.pop(0)
                if blinks not in blink_count_list:
                    blink_count_list.append(blinks)
                counter =1
            if counter!=0:
                counter+=1
                if counter>10:
                    counter=0

            cv2.putText(frame,f'Hit \'Q\' to exit',(50,50),FONT_HERSHEY_COMPLEX,color = (255,255,0),thickness = 1,fontScale =0.8)
    
    #Displaying the frame
    cv2.imshow('Blink Detector (Press Q to exit)',frame)
    if cv2.waitKey(25) == ord('q') or cv2.waitKey(25)==ord('Q'): 
        break

cap.release()
cv2.destroyAllWindows()
stop_threads = True
th.join()
