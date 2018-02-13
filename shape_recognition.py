import cv2
import numpy as np

# TODO: WARNING! HERE BE DRAGONS!
# TODO: Hardcore testing required! Extremely dependant on environment!

# Constants for mode selection
SURFACE_GRAYSCALE = 0
SURFACE_HSV = 1
UNDERWATER_GRAYSCALE = 2
UNDERWATER_HSV = 3

RED = 0
BLUE = 1
YELLOW = 2


def detect_shape(frame, mode, colour=None):
    # Select the area of interest
    selection = cv2.selectROI("Shape selection", frame, showCrosshair=0)

    # Crop the are of interest using the selection
    im_crop = frame[int(selection[1]):int(selection[1] + selection[3]),
                    int(selection[0]):int(selection[0] + selection[2])]

    # Define image preprocessing depending on the mode
    def surface_grayscale():
        # Blur the image to reduce noise
        blur = cv2.pyrMeanShiftFiltering(im_crop, 31, 71)
        cv2.imshow("Blur", cv2.resize(blur, (0, 0), fx=2, fy=2))

        # Apply gray scale
        gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Gray", cv2.resize(gray, (0, 0), fx=2, fy=2))

        return gray

    def surface_hsv():
        # Create the filter
        hsv_filter = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Initialise pixel's colour bounds
        lower_value = np.array([0, 0, 0])
        upper_value = np.array([0, 0, 0])

        # TODO: Test and create the values

        # Apply different bounds depending on the colour
        if colour == RED:
            lower_value = np.array([0, 0, 0])
            upper_value = np.array([0, 0, 0])
        elif colour == BLUE:
            lower_value = np.array([0, 0, 0])
            upper_value = np.array([0, 0, 0])
        elif colour == YELLOW:
            lower_value = np.array([0, 0, 0])
            upper_value = np.array([0, 0, 0])
        else:
            print("Error, wrong colour value passed")

        # Create the mask to filter out the pixels
        mask = cv2.inRange(hsv_filter, lower_value, upper_value)
        cv2.imshow("Mask", mask)

        # Apply different transformations
        res = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("Res", res)

        # Return final frame
        return res

    def underwater_grayscale():
        pass

    def underwater_hsv():
        pass

    select_mode = {0: surface_grayscale,
                   1: surface_hsv,
                   2: underwater_grayscale,
                   3: underwater_hsv}

    # Select the mode
    processed_crop = select_mode[mode]()

    # Define the threshold, here average pixel value of the image
    threshold_value = calculate_average_pixel_value(im_crop)

    # Create the threshold, to extract contours
    thresh = cv2.threshold(processed_crop, threshold_value, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imshow("Thresh", cv2.resize(thresh, (0, 0), fx=2, fy=2))

    # Find contours in the threshold, flags for success or failure, h - hierarchy for contours
    flags, contours, h = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    cv2.imshow("Contours", cv2.drawContours(im_crop, contours, -1, (0, 0, 255), 2))

    # Debug info for number of contours, ideally should be 2 (shape and image bounds itself)
    print("Total number of contours: " + str(len(contours)))

    # Wait for action
    cv2.waitKey(0)


'''
FOR DEBUG:

    @ Detecting pixels by colour, and changing their value to be threshed
    @ Might be useful for shape detection (colour removal or shape detection using the colour)

    counter = 0
    
    for row in im_crop:
        for pixel in row:
            # Trying to find red pixels
            if pixel[2] > 80 and pixel[1] < 140 and pixel[0] < 140:
                pixel[0] = int(1.5*average)
                pixel[1] = int(1.5*average)
                pixel[2] = int(1.5*average)
                counter += 1

    print("Detected " + str(counter) + " checked pixels.")
    
    @ Additional image processing functions not applied in the code actively
    
    gray = cv2.cvtColor(im_crop, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((4, 4), np.uint8)
    dilation = cv2.dilate(gray, kernel, iterations=1)
    blur = cv2.GaussianBlur(dilation, (5, 5), 0)
    
    @ Windows handling

    cv2.destroyWindow("Shape selection")
    
    cv2.imshow("Gray", cv2.resize(gray, (0, 0), fx=2, fy=2))
    cv2.imshow("Dilation", cv2.resize(dilation, (0, 0), fx=2, fy=2))
    cv2.imshow("Blur", cv2.resize(blur, (0, 0), fx=2, fy=2))
    cv2.imshow("Thresh", cv2.resize(thresh, (0, 0), fx=2, fy=2))
    
    @ Important contour window (Window bounds contour should be at contours[-1], which is contour[1] ideally

    cv2.imshow("Important contour", cv2.drawContours(im_crop, contours[0], -1, (0, 0, 255), 1))
    
    @ Shape detection
    
    # Approximate number of sides of the important polygon
    approx = cv2.approxPolyDP(contours[0], 0.01 * cv2.arcLength(contours[0], True), True)
    # Classify the polygon
    if len(approx) == 3:
        print("TRIANGLE")
    elif len(approx) == 4:
        print("TRAPEZIUM")
    else:
        print("DETECTION ERROR")

    # Alternatively approximate number of all polygons
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.07 * cv2.arcLength(cnt, True), True)
        print("Len of approx: " + str(len(approx)))
        if len(approx) == 3:
            print("TRIANGLE")
            break
        elif len(approx) == 4:
            print("TRAPEZIUM")
            break
        else:
            print("DETECTION ERROR")
'''


def calculate_average_pixel_value(img):
    # Initialise pixel counter
    counter = 0

    # Initialise total RGB values
    value = 0

    # Iterate through the image
    for row in img:
        for pixel in row:
            # Increase the counter for each pixel, increase by 3 because of 3 values (RGB)
            counter += 3
            # Increase the value by the sum of 3 pixel's values
            value = value + pixel[0] + pixel[1] + pixel[2]

    # Return the average value
    return value//counter
