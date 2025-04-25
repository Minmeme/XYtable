import cv2
import numpy as np

yellow_count = 0
pink_count = 0
blue_count = 0
white_count = 0

yellow_lower = np.array([15, 150, 20])
yellow_upper = np.array([35, 255, 255])

pink_lower = np.array([140, 50, 100])
pink_upper = np.array([170, 255, 255])

blue_lower = np.array([100, 100, 100])
blue_upper = np.array([130, 255, 255])

white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 55, 255])

cap = cv2.VideoCapture(0)
while True:
    ref, frame = cap.read()

    img = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

    yellow_mask = cv2.inRange(img, yellow_lower, yellow_upper)

    pink_mask = cv2.inRange(img, pink_lower, pink_upper)

    blue_mask = cv2.inRange(img, blue_lower, blue_upper)

    white_mask = cv2.inRange(img, white_lower, white_upper)



    mask_contours, hierarchy = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    # # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (35, 255, 255), 3) #drawing rectangle
                # cv2.putText(frame, "yellow", (int[0,0,1]),int([0,0,1]), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,0,0), 2,cv2.LINE_AA,False)
                cv2.putText(frame, "yellow", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                # yellow_cow = yellow_cow + 1
                yellow_count += 1


    mask_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    # # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3) #drawing rectangle
                cv2.putText(frame, "blue", (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)


    mask_contours, hierarchy = cv2.findContours(pink_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    # # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0,0,255), 3) #drawing rectangle
                cv2.putText(frame, "pink", (0, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)


    mask_contours, hierarchy = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

    # # Finding position of all contours
    if len(mask_contours) != 0:
        for mask_contour in mask_contours:
            if cv2.contourArea(mask_contour) > 500:
                x, y, w, h = cv2.boundingRect(mask_contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 3) #drawing rectangle
                cv2.putText(frame, "white", (0, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)


                
    print(yellow_count)

    cv2.imshow('frame',frame)
    cv2.imshow('yellow_mask',yellow_mask)
    cv2.imshow('pink_mask',pink_mask)
    cv2.imshow('blue_mask',blue_mask)
    cv2.imshow('white_mask',white_mask)


    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()