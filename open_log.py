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


class PadPlot:
    def __init__(self, ther_list=thermocouples_list, coord_circles=coordinates_circles,
                 coord_text=coordinates_text_circles, bg_image='./Pad2.png',
                 colormap='coolwarm', figure_title='Pad Temperature'):

        self.coordinates_circles = coord_circles
        self.thermocouples_list = ther_list
        self.coordinates_text_circles = coord_text

        # Now set the initial window
        self.fig, self.ax = plt.subplots()  # note we must use plt.subplots, not plt.subplot
        self.pad = plt.imread(bg_image)
        self.colormap = colormap
        self.image = self.ax.imshow(self.pad, cmap=colormap)
        self.image.set_clim(-0.5, 1)
        self.ax.set_title(figure_title)
        self.ax.set_axis_off()

    def get_data(self, file_path, columns):
        """
        Convert crappy data to numpy array
        """
        a = np.loadtxt(file_path, dtype=str, usecols=(columns),
                       skiprows=1)  # load the file in str format ### put here the column you need
        b = np.char.rstrip(a, ']')  # remove the useless ]
        c = b.astype(np.float64)  # convert to float
        data = np.transpose(c)  # allow to use data as column
        return data

    def normalize_thermocouples(self, data):
        """
        Normalization of thermocouples for colomap call
        """
        thermocouples_data = data[2:12, :]
        temperature_min = data[2:12, :].min()
        temperature_max = data[2:12, :].max()
        thermocouples_data_normalized = (thermocouples_data - temperature_min) / (temperature_max - temperature_min)
        ratio_temperatures = temperature_min / temperature_max
        return temperature_min, temperature_max, ratio_temperatures, thermocouples_data, thermocouples_data_normalized

    def add_circles_and_thermocouple_values_on_figure(self, data, normalized_ther):
        """
        Takes coordinates of each circle and adds on figure and in a variable (for updating).
        """
        circles = []
        texts = []
        for nb_circles in xrange(len(coordinates_circles)):
            circles.append(
                plt.Circle(self.coordinates_circles[nb_circles], 20,
                           color=plt.cm.coolwarm(normalized_ther[nb_circles, 0])))
            texts.append(
                plt.text(self.coordinates_text_circles[nb_circles][0], self.coordinates_text_circles[nb_circles][1],
                         self.thermocouples_list[nb_circles] + '=' + str(int(data[nb_circles, 0])),
                         color=plt.cm.coolwarm(normalized_ther[nb_circles, 0]), size=16))
            self.ax.add_artist(circles[-1])
            texts[-1]  # to call it
        return circles, texts

    def add_text_on_figure(self, ratio_temperatures, temp_min, temp_max):
        """
        Call to add extremas on figure.
        """
        minimum_txt = plt.text(50, 450, 'Global Tmin = %d' % int(temp_min), color=plt.cm.coolwarm(ratio_temperatures),
                               size=16)
        maximum_txt = plt.text(700, 450, 'Global Tmax = %d' % int(temp_max), color=plt.cm.coolwarm(ratio_temperatures),
                               size=16)
        time_elapsed_txt = plt.text(300, 750, 'Time elapsed: %.1f sec' % 0., size=20)
        self.ax.add_artist(minimum_txt)
        self.ax.add_artist(maximum_txt)
        self.ax.add_artist(time_elapsed_txt)
        return minimum_txt, maximum_txt, time_elapsed_txt  # for updating

    def update_figure(self, circles, texts, time_elapsed_txt, minimum_txt, maximum_txt, temp_min, temp_max, time,
                      data_ther, normalized_ther):
        time_elapsed_txt.set_text('Time elapsed: %.0f' % time)
        minimum_txt.set_text('Global Tmin = %s' % int(temp_min))
        maximum_txt.set_text('Global Tmax = %s' % int(temp_max))
        for i in xrange(len(circles)):
            circles[i].set_color(plt.cm.coolwarm(normalized_ther[i, time]))
            texts[i].set_text(thermocouples_list[i] + '=' + str(int(data_ther[i, time])))
            texts[i].set_color(plt.cm.coolwarm(normalized_ther[i, time]))
        self.fig.canvas.draw()

    def main(self):
        t = 0

        while True:
            data = self.get_data('./Data_ROD002.txt', (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
            temp_min, temp_max, ratio_temperatures, ther_data, ther_norm = self.normalize_thermocouples(data)
            circles, texts = self.add_circles_and_thermocouple_values_on_figure(data, ther_norm)
            minimum_txt, maximum_txt, time_elapsed_txt = self.add_text_on_figure(ratio_temperatures, temp_min, temp_max)
            self.fig.show()
            list_to_update = [circles, texts, time_elapsed_txt, minimum_txt, maximum_txt, temp_min, temp_max, t,
                              ther_data, ther_norm]
            while t < 1600:
                t += 1
                list_to_update = [circles, texts, time_elapsed_txt, minimum_txt, maximum_txt, temp_min, temp_max, t,
                                  ther_data, ther_norm]
                self.update_figure(*list_to_update)
                sleep(0.01)


test = PadPlot()
test.main()
