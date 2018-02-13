import cv2
from multiprocessing import Process
from colour_recognition import detect_colour
from shape_recognition import detect_shape


class Camera:

    def __init__(self):
        # Create new VideoCapture object
        self.cap = cv2.VideoCapture(0)
        # Initialise loop value with True (start streaming)
        self.streaming = True

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
            # Create new process to recognise the colour independently from other processes
            colour_detection_process = Process(target=detect_colour, args=(frame,))
            # Create new process to recognise the shape independently from other processes
            shape_detection_process = Process(target=detect_shape, args=(frame, 0))
            # Start the processes
            colour_detection_process.start()
            shape_detection_process.start()

        # Capture current frame if v button is pressed
        elif cv2.waitKey(1) & 0xFF == ord('v'):
            # Create new process to recognise the text independently from other processes
            image_recognition_prcoess = Process(target=detect_shape, args=(frame,))
            # Start the process
            image_recognition_prcoess.start()

        # Return True to continue streaming
        return True

    def stream(self):
        # Keep streaming while loop is True
        while self.streaming:
            # Assign the result of capture_frame (True/False) to the streaming field
            self.streaming = self.capture_frame()
