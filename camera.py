import cv2
from multiprocessing import Process
from colour_recognition import detect_colour
from shape_recognition import detect_shape
from shape_recognition import GRAYSCALE_BLUR, GRAYSCALE_NO_BLUR

# Shape detection mode, 2 for underwater grayscale
MODE = GRAYSCALE_NO_BLUR


class Camera:

    def __init__(self):
        # Create new VideoCapture object
        self.cap = cv2.VideoCapture(0)
        # Initialise loop value with True (start streaming)
        self.streaming = True
        self.test_image = cv2.imread("samples/yellow_trapezium/YELLOW_TR_6.jpg")
        self.test_image = cv2.resize(self.test_image, (0, 0), fx=0.2, fy=0.2)

    def capture_frame(self):
        # Capture frame-by-frame
        ret, frame = self.cap.read()

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # Quit if q button is pressed (close the stream)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Return False to quit
            return False

        # Capture current frame if c button is pressed
        elif cv2.waitKey(1) & 0xFF == ord('c'):
            # Create new process to recognise the colour and shape independently from other processes
            detection_process = Process(target=detect_shape_and_colour, args=(self.test_image,))
            # Start the process
            detection_process.start()

        # Capture current frame if v button is pressed
        elif cv2.waitKey(1) & 0xFF == ord('v'):
            # Import the function
            from image_recognition_testing import recognise_image
            # Create new process to recognise the text independently from other processes
            image_recognition_process = Process(target=recognise_image, args=(frame,))
            # Start the process
            image_recognition_process.start()

        # Return True to continue streaming
        return True

    def stream(self):
        # Keep streaming while loop is True
        while self.streaming:
            # Assign the result of capture_frame (True/False) to the streaming field
            self.streaming = self.capture_frame()


def detect_shape_and_colour(frame):
    detect_shape(frame, MODE, detect_colour(frame))
