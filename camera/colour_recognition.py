import cv2

COLOUR_THRESHOLD = 45


def detect_colour(frame):
    # Select the area of interest
    selection = cv2.selectROI("Colour selection", frame, showCrosshair=0)

    # Crop the are of interest using the selection
    im_crop = frame[int(selection[1]):int(selection[1]+selection[3]),
                    int(selection[0]):int(selection[0]+selection[2])]

    # Retrieve the data
    colours = calculate_average_pixel_value(im_crop)

    # Print the values
    print(colours)

    # Extract pixel colours' values, to apply the algorithm
    red = colours["red"]
    green = colours["green"]
    blue = colours["blue"]

    # Print first part of the colour selection
    print("Currently selected colour:", end=" ")

    # If red and green values are close to each other and low compared to blue then it's blue
    if abs(red - green) < COLOUR_THRESHOLD * 2 and (red + green)/2 < blue:
        print("blue")
        return 1
    # If red and green values are close to each other and high compared to blue then it's yellow
    elif abs(red - green) < COLOUR_THRESHOLD and (red + green)/2 > blue:
        print("yellow")
        return 2
    # If red is high and green is low then it's red
    elif red - green > COLOUR_THRESHOLD * 2:
        print("red")
        return 0
    else:
        print("ERROR")
        return -1

    # TODO: Test the values underwater and implement colour recognition - red, blue


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
