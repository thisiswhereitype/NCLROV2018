import cv2


def detect_colour(frame):
    # Select the area of interest
    selection = cv2.selectROI("Colour selection", frame, showCrosshair=0)

    # Crop the are of interest using the selection
    im_crop = frame[int(selection[1]):int(selection[1]+selection[3]),
                    int(selection[0]):int(selection[0]+selection[2])]

    # Print the values
    print(calculate_average_pixel_value(im_crop))

    # TODO: Test the values underwater and implement colour recognition - red, yellow or blue


def calculate_average_pixel_value(img):
    # Initialise pixel counter
    counter = 0

    # Initialise total RGB values
    red = 0
    green = 0
    blue = 0

    # Iterate through the image
    for row in img:
        for pixel in row:
            # Increase the counter for each pixel
            counter += 1
            # Add the RGB values to the total count
            red += pixel[2]
            green += pixel[1]
            blue += pixel[0]

    # Return new dictionary with average RGB values
    return {"red": red//counter, "green": green//counter, "blue": blue//counter}
