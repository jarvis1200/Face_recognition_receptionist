import cv2
import os
# Import numpy for matrix calculation
import numpy as np
from pathlib import Path
from gtts import gTTS
import pyttsx3
import time




def Create_dataset(userName, countnum):
    print("[INFO] Video Capture is now starting please stay still...")
    # Start capturing video
    vid_cam = cv2.VideoCapture(0)

    # Get the username
    #print("Enter the name of the person: ")
    #userName = input();

    # Function to save the image
    if not os.path.exists("dataset/{}".format(userName)):
        Path("dataset/{}".format(userName)).mkdir(parents=True, exist_ok=True)

    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # For each person, one face id
    face_id = 1

    # Initialize sample face image
    count = 1

    # Start looping
    while True:
        # Capture the frame/image
        _, img = vid_cam.read()

        # Copy the original Image
        #originalImg = img.copy()

        # Get the gray version of our image
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Get the coordinates of the location of the face in the picture
        faces = face_detector.detectMultiScale(gray_img,
                                               scaleFactor=1.3,
                                               minNeighbors=5,
                                               minSize=(100, 100))

        # Draw a rectangle at the location of the coordinates
        for (x, y, w, h) in faces:
            # Crop the image frame into rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(count) + " images captured"), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255))

            # Increment sample face image
            count += 1

            # Save the captured image into the datasets folder
            cv2.imwrite("dataset/" + userName + "/" + str(count) + ".jpg", gray_img[y:y + h, x:x + w])

            # Display the video frame, with bounded rectangle on the person's face
            cv2.imshow('frame', img)

        # To stop taking video, press 'q' for at least 100ms
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        # If image taken reach 100, stop taking video
        elif count > int(countnum):
            break
    # Stop the video camera
    # Stop video
    vid_cam.release()
    # Close all started windows
    cv2.destroyAllWindows()
    return count



def manual_capture(userName):
    print("[INFO] Video Capture is now starting please stay still...")
    # Start capturing video
    vid_cam = cv2.VideoCapture(0)

    # Get the username
    #print("Enter the name of the person: ")
    #userName = input();

    # Function to save the image
    if not os.path.exists("dataset/{}".format(userName)):
        Path("dataset/{}".format(userName)).mkdir(parents=True, exist_ok=True)

    # Detect object in video stream using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # For each person, one face id
    face_id = 1

    # Initialize sample face image
    count = 0

    # Start looping
    while True:
        # Capture the frame/image
        _, img = vid_cam.read()

        # Copy the original Image
        #originalImg = img.copy()

        # Get the gray version of our image
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Get the coordinates of the location of the face in the picture
        faces = face_detector.detectMultiScale(gray_img,
                                               scaleFactor=1.3,
                                               minNeighbors=5,
                                               minSize=(100, 100))

        # Draw a rectangle at the location of the coordinates
        for (x, y, w, h) in faces:

    # Crop the image frame into rectangle
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            cv2.putText(img, "Face Detected", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255))
            cv2.putText(img, str(str(count) + " images captured"), (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255))
            cv2.imshow("Identified Face", img)
            # Increment sample face image
            key = cv2.waitKey(1) & 0xFF

            # Check if the pressed key is 'k' or 'q'
            if key == ord('s'):
                # If count is less than 5 then save the image
                if count <= 200:
                    cv2.imwrite("dataset/" + userName + "/" + str(count) + ".jpg", gray_img[y:y + h, x:x + w])
                    count += 1

                elif count > 200:
                    break;
                if count > 200:
                    break;
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Stop the video camera
    # Stop video
    vid_cam.release()
    # Close all started windows
    cv2.destroyAllWindows()
    return count





""" Below Section Creates Training Entries"""

# Initialize names and path to empty list
def train_images(self, ):
    (images, lables, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk('dataset'):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join('dataset', subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                lable = id
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1
    (images, lables) = [np.array(lis) for lis in [images, lables]]

    print("[INFO] Created faces and names Numpy Arrays")
    print("[INFO] Initializing the Classifier")
    # Make sure contrib is installed
    # The command is pip install opencv-contrib-python

    # Call the recognizer
    trainer = cv2.face.LBPHFaceRecognizer_create()
    # Give the faces and ids numpy arrays
    trainer.train(images, lables)
    # Write the generated model to a yml file
    trainer.write("training.yml")

    print("[INFO] Training Done")





""" Below Section Recognize Entries"""
def Detector(self):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    video_capture = cv2.VideoCapture(0)

    # img = cv2.imread('Test/2_3.jpg')

    # Call the trained model yml file to recognize faces
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("training.yml")

    # Names corresponding to each id
    names = []
    for users in os.listdir("dataset"):
        names.append(users)
    (width, height) = (130, 100)
    while True:
        (_, img) = video_capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 5, minSize=(100, 100))
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            # Try to recognize the face
            id, confidence = recognizer.predict(face)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)







            if confidence >= 50:
                cv2.putText(img, 'Unknown', (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))


            else:
                cv2.putText(img, '%s - %.0f' % (names[id], confidence * 2), (x - 10, y - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                #speak(result)



                # http = urllib3.PoolManager()
                # r = http.request('GET', 'http://httpbin.org/robots.txt')
                # r.g
        # import urllib3
        # http = urllib3.PoolManager()
        # r = http.request('GET', 'http://httpbin.org/robots.txt')
        # r.



        cv2.imshow('OpenCV', img)


        key = cv2.waitKey(10)
        if key & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return names, confidence


    global result, prev
    result = str(names[id])
    prev = None

    def speak(result):

        engine = pyttsx3.init('sapi5')
        engine.setProperty('volume', 1.0)
        engine.setProperty('rate', 140)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[len(voices) - 1].id)

        engine.say('welcome {}'.format(names[id]))
        engine.runAndWait()

    import urllib.request
    if prev != result:
        acc = confidence * 2;
        acc = str(acc)
        url = 'http://ajlontech.com/office_use/Hotel_management_system_py/insert.php?name=' + names[
            id] + '&accuracy=' + acc;
        print(url)
        res = urllib.request.urlopen(url);
        res.read();
        speak(result)
        prev = result
        print(prev)