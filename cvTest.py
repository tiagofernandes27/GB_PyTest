import cv2
import numpy as np
import random


def nothing(x): 
    pass

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()


#Screen width
sw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
sh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


x1 = 120
y1 = 100

#number of Regions Of Interest
number_of_rois = 10

#threshold = 5

# TRACKBAR WINDOW
cv2.namedWindow('Trackbars')

cv2.createTrackbar('Number of ROIs', 'Trackbars', 4, 9, nothing)
cv2.createTrackbar('Average to stop', 'Trackbars', 180, 255, nothing)
cv2.createTrackbar('Threshold', 'Trackbars', 5, 50, nothing)
cv2.createTrackbar('ROI Width', 'Trackbars', 20, 50, nothing)
cv2.createTrackbar('ROI Height', 'Trackbars', 20, 50, nothing)
cv2.createTrackbar('ROI X', 'Trackbars', 20, int(sw/number_of_rois), nothing)
cv2.createTrackbar('ROI Y', 'Trackbars', 20, sh, nothing)



stop = False

while True:
    
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame.")
        break

    
    # IF SQUARES
    #size = 50
    #w=size
    #h=size

    # IF CUSTOM BOX SIZE
    w = cv2.getTrackbarPos('ROI Width', 'Trackbars')
    h = cv2.getTrackbarPos('ROI Height', 'Trackbars')

    number_of_rois = cv2.getTrackbarPos('Number of ROIs', 'Trackbars') + 1

    #Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    rois = []

    for i in range(number_of_rois):
        i = i + 1
        x = i*cv2.getTrackbarPos('ROI X', 'Trackbars')
        y = cv2.getTrackbarPos('ROI Y', 'Trackbars')
        r = random.randrange(0, 255, 5)
        g = random.randrange(0, 255, 5)
        b = random.randrange(0, 255, 5)
        
        roi = gray_frame[y:y+h, x:x+w]

        avg_intensity = np.mean(gray_frame)
        avg_intensity_roi = np.mean(roi)

        cv2.rectangle(frame, (x, y), (x + w, y + h), (100,150,x), 1)
        
        cv2.putText(frame, f'ROI{i}: {avg_intensity_roi:.2f}', (sw-x1, y1+20*i), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100,150,x), 2)

        rois.append(avg_intensity_roi)

    cv2.imshow('Image', frame)

    print(rois)

    avg = np.mean(rois)
    
    print(f'average rois = {avg}')

    average_to_stop = cv2.getTrackbarPos('Average to stop', 'Trackbars')
    threshold = cv2.getTrackbarPos('Threshold', 'Trackbars')

    #Logic for stopping with threshold HERE

    if avg > average_to_stop:
        #desligar
        stop = True


    if stop == True:
        print("Machine forced to stop!")
        break

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()