import cv2
import keyboard

color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}

# Method to detect nose
def detect_nose(img, faceCascade):
    
     # convert image to gray-scale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # detecting features in gray-scale image, returns coordinates, width and height of features
    features = faceCascade.detectMultiScale(gray_img, 1.1, 8)
    nose_cords = []
    # drawing rectangle around the feature and labeling it
    for (x, y, w, h) in features:
#         cv2.rectangle(img, (x,y), (x+w, y+h),  color['green'], 2)  #uncomment if you want to see face boundary
        cv2.circle(img, ((2*x+w)//2,(2*y+h)//2), 10, color['green'], 2) 
        nose_cords = ((2*x+w)//2,(2*y+h)//2)
    return img, nose_cords

def draw_controller(img, cords):
    size = 40
    x1 = cords[0] - size
    y1 = cords[1] - size
    x2 = cords[0] + size
    y2 = cords[1] + size
    cv2.circle(img, cords,  size, color['blue'], 2) 
    return [(x1,y1), (x2,y2)]

def keyboard_events(nose_cords, cords, cmd):
    try:
        [(x1,y1), (x2,y2)] = cords
        xc, yc = nose_cords
    except Exception as e: 
        print(e)
        return
    if xc < x1:
        cmd = "left"
    elif(xc > x2):
        cmd = "right"
    elif(yc<y1):
        cmd = "up"
    elif(yc > y2):
        cmd = "down"
    if cmd:
        print("Detected movement: ", cmd,  "\n")
        keyboard.press_and_release(cmd)
    return img,cmd
def reset_press_flag(nose_cords, cords,cmd):
    try:
        [(x1,y1), (x2,y2)] = cords
        xc, yc = nose_cords
    except: 
        return True,cmd
    if x1<xc<x2 and y1<yc<y2:
        return True,None
    return False,cmd
    
# Loading classifiers
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Capturing real time video stream.
video_capture = cv2.VideoCapture(-1)

# get vcap property 
width  = video_capture.get(3) # float
height = video_capture.get(4) # float
press_flag = False
cmd = ""

while True:
    # Reading image from video stream
    _, img = video_capture.read()
    img = cv2.flip( img, 1 )

    # detect nose and draw
    img, nose_cords = detect_nose(img, faceCascade)
    cv2.putText(img, cmd, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, color['red'], 1, cv2.LINE_AA)

    #draw boundary circle
    cords = draw_controller(img, (int(width/2), int(height//2)) )
    if press_flag and len(nose_cords):
        img,cmd = keyboard_events(nose_cords,cords, cmd)
    press_flag,cmd = reset_press_flag(nose_cords,cords,cmd)

    # Writing processed image in a new window
    cv2.imshow("face detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# releasing web-cam
video_capture.release()
# Destroying output window
cv2.destroyAllWindows()
