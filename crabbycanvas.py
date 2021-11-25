import cv2
import numpy as np
def nothing(x):
    pass

points = []

draw = False

currclr = (0,0,0)

bob = None

bobs_hue = 0
bobs_sat = 0
bobs_val = 0
bobs_hrange = 0
bobs_srange = 0
bobs_vrange = 0
bobs_crad = 0
crrclr = "none"
font = cv2.FONT_HERSHEY_SIMPLEX

coords = [10, 10, 200, 200, 250, 10, 440, 200, 490, 10, 680, 200]
#the coords go [x, y, x, y, x, y, x, y, x, y, x, y]
red = (0,0,255)
blue = (255, 0, 0)
yellow = (0, 255, 255)
clrstatus = ""
color = (0, 0, 0)
try:
    file = open("crabbyvalues.txt", "r")
    lines = file.readlines()
    for i in range(0, 6):
        if(i == 0):
            bobs_hue = lines[i]
        if (i == 1):
            bobs_sat = lines[i]
        if (i == 2):
            bobs_val = lines[i]
        if (i == 3):
            bobs_hrange = lines[i]
        if (i == 4):
            bobs_srange = lines[i]
        if (i == 5):
            bobs_vrange = lines[i]
except:
    file = open("crabbyvalues.txt", "x")
    file = open("crabbyvalues.txt", "w")
    file.write(str(bobs_hue)+"\n")
    file.write(str(bobs_sat)+"\n")
    file.write(str(bobs_val)+"\n")
    file.write(str(bobs_hrange)+"\n")
    file.write(str(bobs_srange)+"\n")
    file.write(str(bobs_vrange)+"\n")
    file = open("crabbyvalues.txt", "r")

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

cv2.namedWindow("Control Panel")
cv2.resizeWindow("Control Panel", 300, 400)
cv2.createTrackbar("Hue", "Control Panel", int(bobs_hue), 180, nothing)
cv2.createTrackbar("Sat", "Control Panel", int(bobs_sat), 255, nothing)
cv2.createTrackbar("Value", "Control Panel", int(bobs_val), 255, nothing)
cv2.createTrackbar("Hrange", "Control Panel", int(bobs_hrange), 127, nothing)
cv2.createTrackbar("Srange", "Control Panel", int(bobs_srange), 127, nothing)
cv2.createTrackbar("Vrange", "Control Panel", int(bobs_vrange), 127, nothing)
cv2.createTrackbar("Brush Size", "Control Panel", int(bobs_crad), 50, nothing)
draw = False
# cv2.namedWindow("Canvas")

while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor (frame, cv2.COLOR_BGR2HSV)
    # cv2.putText(frame, crrclr, (250, 250), font, 0.9, (0, 0, 255), 2, cv2.LINE_AA)

    bobs_hue = cv2.getTrackbarPos('Hue', 'Control Panel')
    bobs_sat = cv2.getTrackbarPos('Sat', 'Control Panel')
    bobs_val = cv2.getTrackbarPos('Value', 'Control Panel')
    bobs_hrange = cv2.getTrackbarPos('Hrange', 'Control Panel')
    bobs_srange = cv2.getTrackbarPos('Srange', 'Control Panel')
    bobs_vrange = cv2.getTrackbarPos('Vrange', 'Control Panel')
    bobs_crad = cv2.getTrackbarPos('Brush Size', 'Control Panel')

    filterLower = (bobs_hue-bobs_hrange, bobs_sat-bobs_srange, bobs_val-bobs_vrange)
    filterUpper = (bobs_hue+bobs_hrange, bobs_sat+bobs_srange, bobs_val+bobs_vrange)

    filteredFrame = cv2.inRange(hsv, filterLower, filterUpper)

    filtered = cv2.bitwise_and(frame, frame, mask=filteredFrame)
    # cv2.rectangle(frame, (30, 100), (60, 300), (0, 0, 0), 2)
    # top = 100
    # bottom = 300
    cnts = cv2.findContours(filteredFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

    cv2.rectangle(frame, (coords[0], coords[1]), (coords[2], coords[3]), red, -1)
    cv2.rectangle(frame, (coords[4], coords[5]), (coords[6], coords[7]), blue, -1)
    cv2.rectangle(frame, (coords[8], coords[9]), (coords[10], coords[11]), yellow, -1)

    # cv2.putText(frame, clrstatus, (280, 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if(len(cnts)> 0):

        c = max(cnts, key = cv2.contourArea)

        ((x,y), radius) = cv2.minEnclosingCircle(c)
        cv2.circle(frame, (int(x), int(y)), int(radius), (0,0,255), 5)


        print("x = "+str(x))
        print("coord0 = "+str(coords[0]))
        print("coord1 = "+str(coords[1]))
        if(coords[0] < int(x) < coords[2] and coords[1] < int(y) < coords[3]): #for red
            print("running")
            if cv2.waitKey(1) & 0xFF == ord("i"):
                crrclr = "red"

        if(coords[4] < int(x) < coords[6] and coords[5] < int(y) < coords[7]): #for blue
            print("running")
            if cv2.waitKey(1) & 0xFF == ord("i"):
                crrclr = "blue"

        if(coords[8] < int(x) < coords[10] and coords[9] < int(y) < coords[11]): # for yellow
            print("running")
            if cv2.waitKey(1) & 0xFF == ord("i"):
                crrclr = "yellow"

        cv2.putText(frame, crrclr, (250, 250), font, 0.9, (0, 0, 255), 2, cv2.LINE_AA)
        # print(crrclr)
        if cv2.waitKey(1) & 0xFF == ord("p"):
            draw = True
        if (crrclr == "red"):
            color = (0,0,255)
        elif (crrclr == "blue"):
            color = (255, 0, 0)
        elif (crrclr == "yellow"):
            color = (0, 255, 255)

        if(draw):
            # x = 1280 - x
            cv2.circle(imgCanvas, (int(x), int(y)), int(bobs_crad), color, -1)

        if cv2.waitKey(1) & 0xFF == ord("o"):
            imgCanvas = np.zeros((720, 1280, 3), np.uint8)

        if cv2.waitKey(1) & 0xFF == ord("l"):
            draw = False

        ypos = 0
        xpos = 0
        if int(y) <= 100:
            ypos = 100
        elif int(y) >= 300:
            ypos = 300
        if int(y) > 100 and y < 300:
            ypos = int(y)

        if int(x) <= 100:
            xpos = 100
        elif int(x) >= 300:
            xpos = 300
        if int(x) > 100 and x < 300:
            xpos = int(x)
        ((xpos, ypos), radius) = cv2.minEnclosingCircle(c)
        # cv2.circle(canvas, (int(xpos), int(ypos)), int(radius), (255, 0, 0), 1)


    frame = cv2.add(imgCanvas, frame)
    cv2.imshow("realimage", frame)
    # cv2.imshow('filtered', filtered) #just the color filtered frame, used for fine tuning the color recognizer
    # cv2.imshow("canvas", imgCanvas) #just the canvas
    # left off here ****************************************************************

    if cv2.waitKey(1) & 0xFF == ord('q'):

        file = open("crabbyvalues.txt", "w")
        file.write(str(bobs_hue) + "\n")
        file.write(str(bobs_sat) + "\n")
        file.write(str(bobs_val) + "\n")
        file.write(str(bobs_hrange) + "\n")
        file.write(str(bobs_srange) + "\n")
        file.write(str(bobs_vrange) + "\n")
        # file = open("values.txt", "w")
        # file.write(str(bobs_hue + "\n")
        # file.write(bobs_sat + "\n")
        # file.write(bobs_val + "\n")
        # file.write(bobs_hrange + "\n")
        # file.write(bobs_srange + "\n")
        # file.write(bobs_vrange + "\n")

        break

cap.release()
file.close()
cv2.destroyAllWindows()
