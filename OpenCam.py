# import the opencv library
import cv2

# define a video capture object
vid = cv2.VideoCapture(1)

while (True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice

    face_Cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_Cascade.detectMultiScale(imgGray, 1.2, 3)

    for (x, y, w, h) in faces:
         cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv2.imshow("Result", frame)
    cv2.waitKey(1)

# After the loop release the cap object
vid.release()
cv2.destroyAllWindows()