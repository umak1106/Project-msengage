import cv2
import pyautogui

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#defined a video capture object
cap = cv2.VideoCapture(0)

cap.set(3,640) # set Width
cap.set(4,480) # set Height

sens =6
clickSens = 1.1 #percentage

referPercentBool=True
referPercent=0.0



while True:
    ret, image = cap.read()
    image = cv2.flip(image, 1) #flip the video along the y-axis

    gray = cv2.cvtColor (image, cv2.COLOR_BGR2GRAY)

    #function to detect the faces
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    for (x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = image[y:y+h, x:x+w]

        #used to move mouse relative to it's current position
        pyautogui.moveRel(((x + w / 2) - 320) / sens, 0)
        pyautogui.moveRel(0, ((y + h / 2) - 240) / sens)

        if referPercentBool:
            counter=0;
            for i in range(y,y+h):
                for j in range(x,x+w):
                    if image[i,j][0]>100 and image[i,j][1]<200 and image[i,j][1]<200:
                        counter+=1

            print(counter)
            referPercent = counter/((h-y)*(w-x))
            referPercentBool = False
        else:
            counter = 0;
            for i in range(y, y + h):
                for j in range(x, x + w):
                    if image[i, j][0] > 100 and image[i, j][1] < 200 and image[i, j][1] < 200:
                        counter += 1

            print(counter)
            tempPercent = counter / ((h - y) * (w - x))

            if tempPercent>(referPercent*clickSens):
                pyautogui.click()


    cv2.rectangle(image,(320,0),(320,480),(0,0,0),1)
    cv2.rectangle(image, (0, 240), (640, 240), (0,0,0), 1)

    cv2.imshow('video',image)

    k = cv2.waitKey(30) & 0xff

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
