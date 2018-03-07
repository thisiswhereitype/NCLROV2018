import cv2
import numpy as np

# TODO: WARNING! HERE BE DRAGONS!
# TODO: Hardcore testing required! Extremely dependant on environment!

# Constants for mode selection
GRAYSCALE_NO_BLUR = 0
GRAYSCALE_BLUR = 1

# Constants for colour selection
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
    def grayscale_no_blur():

        # Set the threshold constant
        COLOUR_THRESHOLD = 45

        # Make a copy of im_crop to avoid overwriting it
        new_im_crop = im_crop.copy()

        # Extract the pixels of a given colour
        extracted = extract_pixels(new_im_crop, colour, COLOUR_THRESHOLD)
        cv2.imshow("Step 2: Pixels extraction", cv2.resize(extracted, (0, 0), fx=2, fy=2))

        # Apply gray scale
        gray = cv2.cvtColor(extracted, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Step 3: Grayscale", cv2.resize(gray, (0, 0), fx=2, fy=2))

        # Use this for fun images
        # return cv2.cvtColor(new_im_crop, cv2.COLOR_BGR2GRAY)
        return gray

    def grayscale_blur():

        # Set the threshold constant
        COLOUR_THRESHOLD = 45

        # Make a copy of im_crop to avoid overwriting it
        new_im_crop = im_crop.copy()

        # Blur the image to reduce noise
        blur = cv2.pyrMeanShiftFiltering(new_im_crop, 31, 71)
        cv2.imshow("Step 1: Blur", cv2.resize(blur, (0, 0), fx=2, fy=2))

        # Extract the pixels of a given colour
        extracted = extract_pixels(blur, colour, COLOUR_THRESHOLD)
        cv2.imshow("Step 2: Pixels extraction", cv2.resize(extracted, (0, 0), fx=2, fy=2))

        # Apply gray scale
        gray = cv2.cvtColor(extracted, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Step 3: Grayscale", cv2.resize(gray, (0, 0), fx=2, fy=2))

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

    def underwater_hsv():
        pass

    select_mode = {0: grayscale_no_blur,
                   1: grayscale_blur,
                   2: surface_hsv,
                   3: underwater_hsv}

    # Select the mode
    processed_crop = select_mode[mode]()


    # Define the threshold, here average pixel value of the image
    threshold_value = calculate_average_pixel_value(im_crop)

    # Create the threshold, to extract contours
    thresh = cv2.threshold(processed_crop, threshold_value, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imshow("Step 4: Threshold", cv2.resize(thresh, (0, 0), fx=2, fy=2))

    # Find contours in the threshold, flags for success or failure, h - hierarchy for contours
    flags, contours, h = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Initialise the contour with an integer
    important_cnt = 0

    # Access the dimensions of the image and calculate its area
    width, height = thresh.shape
    image_area = width*height
    print("Selected area: " + str(image_area) + " pixels")

    # Info for the number of contours, ideally should be 2 (shape and image bounds itself)
    print("Total number of contours in the image: " + str(len(contours)))

    # Iterate through each contour in the image
    for cnt in contours:

        # Calculate the area of the shape
        area = cv2.contourArea(cnt)

        # Do not consider any areas smaller than 1/50 of the image
        if not area < image_area/50:
            # Do not consider any areas bigger than 1/2 of the image
            if not area >= image_area/2:
                # If important contour is empty (is int), assign a contour to the field
                if type(important_cnt) == int:
                    important_cnt = cnt
                # If important contour is a contour, then calculate the areas and put the bigger one in the field
                elif cv2.contourArea(cnt) > cv2.contourArea(important_cnt):
                    important_cnt = cnt

    # Check if the contour was changed
    if type(important_cnt) != int:
        # Calculate the approximation of the final shape
        approx = cv2.approxPolyDP(important_cnt, 0.01 * cv2.arcLength(important_cnt, True), True)
        print("Number of the edges of the important contour: " + str(len(approx)) + ". Contour area: " + str(cv2.contourArea(important_cnt)))
        # Draw the important contour using magenta colour and show all contours
        cv2.drawContours(im_crop, contours, -1, (0, 255, 0), 2)
        cv2.imshow("Contours", cv2.drawContours(im_crop, important_cnt, -1, (255, 0, 255), 3))
    else:
        # Draw and show all contours using green colour
        cv2.imshow("Contours", cv2.drawContours(im_crop, contours, -1, (0, 255, 0), 2))

    # Wait for action
    cv2.waitKey(0)


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


def extract_pixels(frame, colour, thresh):
    # Iterate through each pixel in the image
    for row in frame:
        for pixel in row:

            # Add the RGB values to the total count, cast them to int to avoid overflow of data
            red = int(pixel[2])
            green = int(pixel[1])
            blue = int(pixel[0])

            # If all values are close to each other then it's white, skip the ifs and reset the pixel
            if not (abs(red - green) < thresh and abs(red - blue) < thresh and abs(blue - green) < thresh):
                # If select colour and selected pixel's colour are the same
                if (colour == YELLOW and abs(red - green) < thresh and (red + green) / 2 > blue) \
                        or (colour == BLUE and abs(red - green) < thresh * 2 and (red + green) / 2 < blue) \
                        or (colour == RED and red - green > thresh * 2):
                    # Do nothing and take the next pixel
                    continue

            # Otherwise reset the pixel
            pixel[0] = 255
            pixel[1] = 255
            pixel[2] = 255

    return frame


'''
FOR DEBUG:

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

