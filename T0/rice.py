# encoding: utf-8

"""Author: Pierre-Victor Chaumier <chaumierpv@gmail.com>
    
    Python Version : 3.4.2

    /!\ This script has only been tested with this version of Pyhton !

    Required libraries :
        - pillow
        - scipy
        - numpy
        - matplotlib

    To install them, simply run the command : pip install name-of-lib
    
    You can install them into a virtualenv if you want to keep a clean install
    of Python.
"""

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

import numpy as np

from scipy import misc

## -------------------- 1. Image acquisition  -------------------

# the rice.png and this program must be in the same directory
rice = misc.imread('rice.png')
height, width = rice.shape


## -------------------- 2. Image display  -------------------

# Display the png image
plt.figure(1)
plt.imshow(rice)
plt.title('Image in PNG')

# Display the 3D representation of the image (position and grey value)
fig = plt.figure(2)
ax = fig.gca(projection='3d')
X = np.arange(0, height, 1)
Y = np.arange(0, width, 1)
X, Y = np.meshgrid(X, Y)

surf = ax.plot_surface(X, Y, rice, cmap=cm.coolwarm, linewidth=0)
plt.title('3D representation of image')


## -------------------- 3. Historiogram  -------------------

# Creation of the frequency array. Each index is a grey value and the number
# is its frequency within the original image
def freq_grey_level(image, number_of_grey):
    freq = [0] * number_of_grey
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            freq[image[i][j]] += 1
    return freq

def display_grey_freq(image):
    num_grey = 256
    grey_level = range(num_grey)
    freq = freq_grey_level(image, num_grey)

    plt.figure(3)
    plt.bar(grey_level, freq, color='blue')
    plt.xlabel('Grey level')
    plt.ylabel('Frequency')
    plt.title('Frequency of grey level')

display_grey_freq(rice)

## -------------------- 4. Segmentation using a global  -------------------
## --------------------    threshold                    -------------------

def threshold_image(image, threshold):
    image_thresholded = np.copy(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image_thresholded[i][j] = 0 if image[i][j] < threshold else 255
    return image_thresholded

rice_thresholded_128 = threshold_image(rice, 128)
rice_thresholded_150 = threshold_image(rice, 150)
rice_thresholded_70 = threshold_image(rice, 70)

def plot_image(image, title):
    plt.figure()
    plt.imshow(image)
    plt.title(title)

plot_image(rice_thresholded_128, 'Image with a threshold of 128')
plot_image(rice_thresholded_150, 'Image with a threshold of 150')
plot_image(rice_thresholded_70, 'Image with a threshold of 70')


## -------------------- 5. Background elimination  -------------------

def background_elimination(image):
    image_bg_eliminated = np.copy(image)
    for i in range(image.shape[0]):
        mini = min(image[i])
        for j in range(image.shape[1]):
            image_bg_eliminated[i][j] = image[i][j] - mini
    return image_bg_eliminated

rice_bg_eliminated = background_elimination(rice)

plt.figure()
plt.imshow(rice_bg_eliminated)
plt.title('Background elimination')


## -------------------- 6. Segmentation of new image  -------------------

display_grey_freq(rice_bg_eliminated)
rice_bg_eliminated_thresholded = threshold_image(rice_bg_eliminated, 55)
plot_image(rice_bg_eliminated_thresholded, 'Image newly thresholded')

# Display all the different figures
plt.show()