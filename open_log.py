# This file provide a way to open the files saved by crappy. Please don't modify this file directly but make a copy for your own usage.
# Note that there is a special file in this folder for videoextenso data, as they have a specific format.

import numpy as np
import matplotlib.pyplot as plt
from time import sleep

np.set_printoptions(threshold='nan', linewidth=500, suppress=True)

thermocouples_list = ['T' + str(count) for count in xrange(1, 10)]  # Names of each thermocouple
coordinates_circles = (
    (110, 330), (92, 265), (68, 192), (507, 267), (507, 195), (507, 123), (900, 323), (920, 261), (940, 193))
coordinates_text_circles = (
    (150, 330), (132, 265), (108, 192), (547, 267), (547, 195), (547, 123), (940, 323), (960, 261), (980, 193))

if __name__ == '__main__':
    def get_data(file_path, columns):
        """
        Convert crappy data to numpy array
        """
        a = np.loadtxt(file_path, dtype=str, usecols=(columns),
                       skiprows=1)  # load the file in str format ### put here the column you need
        b = np.char.rstrip(a, ']')  # remove the useless ]
        c = b.astype(np.float64)  # convert to float
        data = np.transpose(c)  # allow to use data as column
        return data


    def normalize_thermocouples(data):
        """
        Normalization of thermocouples for colomap call
        """
        thermocouples_data = data[2:12, :]
        Tmin = data[2:12, :].min()
        Tmax = data[2:12, :].max()
        thermocouples_data_normalized = (thermocouples_data - Tmin) / (Tmax - Tmin)
        return Tmin, Tmax, thermocouples_data, thermocouples_data_normalized


    def initialize_figure(bg_image='./Pad2.png', colormap='coolwarm', figure_title='Pad Temperature'):
        """
        Initialize the plot, with the pad in background.
        """
        fig, ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
        pad = plt.imread(bg_image)
        image = ax.imshow(pad, cmap=colormap)
        image.set_clim(-0.5, 1)
        ax.set_title(figure_title)
        ax.set_axis_off()
        return fig, ax


    def add_circles_and_thermocouple_values_on_figure(ax, coordinates_circles, coordinates_texts,
                                                      normalized_thermocouples):
        """
        Takes coordinates of each circle and adds on figure and in a variable (for updating).
        """
        circles = []
        texts = []
        for count in xrange(len(coordinates_circles)):
            circles.append(
                plt.Circle(coordinates_circles[count], 20, color=plt.cm.coolwarm(normalized_thermocouples[count, t])))
            texts.append(plt.text(coordinates_texts[count][0], coordinates_texts[count][1],
                                  thermocouples_list[count] + '=' + str(int(data[count, t])),
                                  color=plt.cm.coolwarm(normalized_thermocouples[count, t]), size=16))
            ax.add_artist(circles[-1])
            texts[-1]  # to call it
        return circles, texts


    def add_text_on_figure(figure, Tmin, Tmax, t):
        """
        Call to add extremas on figure.
        """
        minimum_txt = plt.text(50, 450, 'Global Tmin = %d' % Tmin, color=plt.cm.coolwarm(Tmin / Tmax), size=16)
        maximum_txt = plt.text(700, 450, 'Global Tmax = %d' % Tmax, color=plt.cm.coolwarm(Tmax / Tmax), size=16)
        time_elapsed_txt = plt.text(300, 750, 'Time elapsed: %.1f sec' % t, size=20)
        figure.add_artist(minimum_txt)
        figure.add_artist(maximum_txt)
        figure.add_artist(time_elapsed_txt)
        return minimum_txt, maximum_txt, time_elapsed_txt  # for updating


    def update_figure(figure, circles, texts, time, minimum_txt, maximum_txt):
        time.set_text('Time elapsed: %.0f' % t)
        minimum.set_text('Global Tmin = %s' % Tmin)
        maximum.set_text('Global Tmax = %s' % Tmax)
        for i in xrange(len(circles)):
            circles[i].set_color(plt.cm.coolwarm(data_normalized[i, t]))
            texts[i].set_text(thermocouples_list[i] + '=' + str(int(data[i, t])))
        figure.canvas.draw()


    data = get_data('./Data_ROD002.txt', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
    t = 0
    Tmin, Tmax, data, data_normalized = normalize_thermocouples(data)
    fig, ax = initialize_figure()
    circles, texts = add_circles_and_thermocouple_values_on_figure(ax, coordinates_circles, coordinates_text_circles, data_normalized)
    minimum, maximum, time = add_text_on_figure(ax, Tmin, Tmax, t)
    list_to_update = [fig, circles, texts, time, minimum, maximum]
    fig.show()

    while t < 1600:
        t += 1
        update_figure(*list_to_update)
        sleep(0.01)
