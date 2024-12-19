import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy.interpolate import interp1d


# Gives the largest rectangle of the image, the area where to plot the new data
def get_largest_rectangle(image_path):
    plt.rcdefaults()
    image = cv2.imread(f'{image_path}.png')
    if image is None:
        raise ValueError("Image not found or unable to load.")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image, 10, 10)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_area = 0
    largest_rectangle = None
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h
        if area > largest_area:
            largest_area = area
            largest_rectangle = (x, y, w, h)
    if largest_rectangle is None:
        raise ValueError("No horizontal rectangle found in the image.")
    return largest_rectangle

# Extracts the horizontal lines of an image, should be used with an image zoomed on the y axis, with the upper and the downer lines being the limit of the box
def extract_horizontal_lines(image_path):
    image = cv2.imread(f'{image_path}.png', cv2.IMREAD_GRAYSCALE) 
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    horizontal_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    y_values = [cv2.boundingRect(contour)[1] for contour in contours]
    return sorted(y_values)

# Extracts the vertical lines of an image, should be used with an image zoomed on the x axis, with the left and the right lines being the limit of the box
def extract_vertical_lines(image_path):
    image = cv2.imread(f'{image_path}.png', cv2.IMREAD_GRAYSCALE) 
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    binary_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10)
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 5))
    horizontal_lines = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x_values = [cv2.boundingRect(contour)[0] for contour in contours]
    return sorted(x_values)

# Give the limits of the y-axis, from an image zoomed and the y axis, and a array corresponding with the labels of the ticks ordered from UP to DOWN, and filled with '-' when there is a tick without a label
def extract_ylim(image_path, yticklabels):
    yticks = extract_horizontal_lines(image_path)
    yticks = np.array(yticks)
    yticklabels = np.array(yticklabels)
    is_not_x = np.where(yticklabels != '-')
    yticklabels_filtered = yticklabels[is_not_x]
    yticks_filtered = yticks[is_not_x]
    interp = interp1d(yticks_filtered, yticklabels_filtered, fill_value='extrapolate')
    y_min_tick = yticks[0]
    y_max_tick = yticks[-1]
    y_max = interp(y_max_tick)
    y_min = interp(y_min_tick)
    print([interp(y) for y in yticks])
    print(yticks)
    return y_max, y_min


# Give the limits of the x-axis, from an image zoomed and the x axis, and a array corresponding with the labels of the ticks ordered from LEFT to RIGHT, and filled with '-' when there is a tick without a label
def extract_xlim(image_path, xticklabels):
    xticks = extract_vertical_lines(image_path)
    xticks = np.array(xticks)
    xticklabels = np.array(xticklabels)
    is_not_x = np.where(xticklabels != '-')
    xticklabels_filtered = xticklabels[is_not_x]
    xticks_filtered = xticks[is_not_x]
    interp = interp1d(xticks_filtered, xticklabels_filtered, fill_value='extrapolate')
    x_min_tick = min(xticks)
    x_max_tick = xticks[-1]
    x_min = interp(x_min_tick)
    x_max = interp(x_max_tick)
    return x_min, x_max

# Create new plot with the plotting area being defined from the image loaded in image_path, and the corresponding x and y limits, where the plot is y(x)
def create_new_image(image_path, x_lims, y_lims, data_x, data_y):
    rectangle = get_largest_rectangle(image_path)
    x, y, w, h = rectangle    
    px = 1/plt.rcParams['figure.dpi']
    print(rectangle)
    with Image.open(f'{image_path}.png') as img:
        # Get the size of the image
        width, height = img.size  

    fig, ax = plt.subplots(figsize=(width*px, height*px))
    fig.subplots_adjust(left=float(x)/float(width), right=float(x+w)/float(width), bottom=float(height-y-h)/float(height), top=float(height-y)/float(height))
    # fig.subplots_adjust(left=0.2, right=0.5, bottom=0.5, top=0.9)
    ax.set_xlim(x_lims[0],x_lims[1])
    ax.set_ylim(y_lims[0],y_lims[1])
    ax.plot(data_x, data_y, color='orange', linewidth=2)
    plt.axis('off')
    fig.savefig(f'{image_path}_addition.png')
    plt.close()

    fig, ax = plt.subplots(figsize=(width*px, height*px))
    fig.subplots_adjust(left=float(x)/float(width), right=float(x+w)/float(width), bottom=float(height-y-h)/float(height), top=float(height-y)/float(height))
    # fig.subplots_adjust(left=0.2, right=0.5, bottom=0.5, top=0.9)
    ax.set_xlim(x_lims[0],x_lims[1])
    ax.set_ylim(y_lims[0],y_lims[1])
    ax.plot(data_x, data_y)
    fig.savefig(f'{image_path}_tocompare.png')
    plt.close()


def remove_white_pixels(image):
    data = image.getdata()

    # Create a new image data list where white pixels are transparent
    new_data = []
    for item in data:
        # If the pixel is white (255, 255, 255), make it transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:  # Adjust threshold if needed
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)

    # Apply the new data to the overlay image
    image.putdata(new_data)
    return image

# Merge two images and create a third
def overlay_two_images(image1_path, output_file):
    image1 = Image.open(f'{image1_path}.png')
    image2 = Image.open(f'{image1_path}_addition.png')
    image2 = image2.convert('RGBA')
    image1 = image1.convert('RGBA')
    image2 = remove_white_pixels(image2)
    image1.paste(image2, (0, 0), image2) 
    # overlay_image = Image.blend(image1, image2, alpha=1)
    image1.save(f"{output_file}.png")
    # image1.paste(image2,(50,50))
    # image1.save(f"/home/jwp9427/{output_file}.png")


# This function summarizes everything, to be used the following parameters are used
#   - image_input, a path to an image where we want to add some data
#   - image_xticks, a path to an image zoomed on the xaxis, with all ticks being shown and the left and right limits
#   - image_yticks, a path to an image zoomed on the xyaxis, with all ticks being shown and the bottom and top limits
#   - xticklabels, an array with the labels of the ticks shown in image_xticks, filled with '-' if there is a tick without a label
#   - yticklabels, an array with the labels of the ticks shown in image_yticks, filled with '-' if there is a tick without a label
#   - image_output, the path of the output image, stored in /home/jwp9427
#   - x_array, x_values to plot
#   - y_array, y_values to plot
def add_to_image(folder, image_name, image_xticks_name, image_yticks_name, xticklabels, yticklabels, image_output_name, x_array, y_array):
    image_path = f'{folder}/{image_name}'
    image_xticks_path = f'{folder}/{image_xticks_name}'
    image_yticks_path = f'{folder}/{image_yticks_name}'
    image_output_path = f'{folder}/{image_output_name}'
    
    x_lims = extract_xlim(image_xticks_path, xticklabels)
    y_lims = extract_ylim(image_yticks_path, yticklabels)
    create_new_image(image_path, x_lims, y_lims, x_array, y_array)
    overlay_two_images(image_path, image_output_path)