import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from scipy.optimize import least_squares
from scipy.signal import argrelextrema, peak_widths
from scipy.integrate import trapz
import numpy as np
import os
import csv

class GpcPlotter:
    def __init__(self, show=True, save=False):
        self.path = os.getcwd()
        self.show = show
        self.save = save

    def plot_individuals(self, min_x=0, max_x=20, normalized=False):
        for filename in os.listdir('data'):
            file_path = os.path.join('data', filename)
            if os.path.isfile(file_path) and 'arw' in file_path:
                try:
                    with open(file_path) as file:
                        data = [line for line in file]

                    title = data[1].replace("\"", "").strip()
                    data = [list(map(float, line.strip().split('\t'))) for line in data[2:] if line]
                    data = [line for line in data if line[0] >= min_x and line[0] <= max_x]

                    t = np.array([line[0] for line in data])
                    s = np.array([line[1] for line in data])
                    if normalized:
                        s = (np.array(s) - np.min(s)) / (np.max(s) - np.min(s))
                        title = f'{title} normalized'
                    fig, ax = plt.subplots()
                    ax.plot(t, s)
                    ax.set(xlabel='time (min)', title=title)
                    ax.grid()
                    title = f"{self.path}\\plots\\{title}.png"
                    if self.show:
                        plt.show()
                    if self.save:
                        fig.savefig(title)
                except Exception as e:
                    print(e)

    def plot_all(self, normalized=False):
        fig, ax = plt.subplots()

        for filename in os.listdir('data'):
            file_path = os.path.join('data', filename)
            if os.path.isfile(file_path) and 'arw' in file_path:
                try:
                    with open(file_path) as file:
                        data = [line for line in file]
                    title = data[1].replace("\"", "").strip()
                    data = [list(map(float, line.strip().split('\t')))
                            for line in data[2:] if line]
                    data = [line for line in data if line[0]
                            >= 6 and line[0] <= 10]

                    t = np.array([line[0] for line in data])
                    s = np.array([line[1] for line in data])
                    if normalized:
                        s = (np.array(s) - np.min(s)) / (np.max(s) - np.min(s))
                        title = f'{title} normalized'
                    ax.plot(t, s, label=title)
                except Exception as e:
                    print(e)

        ax.set(xlabel='time (min)')
        ax.grid()
        ax.legend()
        if normalized:
            fig_title = 'all_normalized.png'
        else:
            fig_title = 'all.png'
        if self.show:
            plt.show()
        if self.save:
            fig.savefig(f'{self.path}\\plots\\{fig_title}')

    def plot_deconvoluted(self, filename, min_x=0, max_x=100):
        fig, ax = plt.subplots()
        file_path = f'{self.path}\\data\\{file_name}'
        title = f'{file_name[:-4]} deconvoluted'

        with open(file_path) as file:
            data = [line for line in file]

        data = [list(map(float, line.strip().split('\t'))) for line in data[2:] if line]
        data = [line for line in data if line[0] >= min_x and line[0] <= max_x]

        # plot original plot
        t = np.array([line[0] for line in data])
        s = np.array([line[1] for line in data])
        ax.plot(t, s, label=title)

        # plot deconvoluted plot
        self.plot_deconvolution(ax, s, t, min_x=min_x, max_x=max_x, min_h=5, title=title)

        # show plot
        ax.set(xlabel='time (min)')
        ax.grid()
        ax.legend()
        if self.show:
            plt.show()
        if self.save:
            fig.savefig(f'{self.path}\\plots\\{title}.png')

    def plot_deconvolution(self, ax, s, t, min_x=0, max_x=100, min_h=0, data_len=1000, show_peak_info=True, title='', write_csv=False):
        fun = lambda x: np.exp(-(0.1*x-6)**2+4) + np.exp(-(0.1*x-4.75)**2+2)
        x_deconv = np.linspace(t[0], t[-1], data_len)
        y_value1 = fun(t) + np.random.normal(0, 1, len(t))*3

        positions, heights, widths = self.get_peak_info(t, s, min_h)
        peaks = [{'m': positions[i], 'sd': widths[i], 'h': heights[i]} for i in range(len(positions))]

        p = [peak['m'] for peak in peaks]
        p += [peak['sd'] for peak in peaks]
        p += [peak['h'] for peak in peaks]

        ls = least_squares(self.res, p, args=(y_value1, t))

        y_fit = np.sum([self.gaussian(x_deconv, ls.x[i], ls.x[i+1], ls.x[i+2]) for i in range(0, len(ls.x), 3)], axis=0)

        for i, peak in enumerate(peaks):
            x_peak = np.linspace(peak['m']-0.5, peak['m']+0.5, data_len)
            y_peak = self.gaussian(x_peak, peak['m'], peak['sd'], peak['h'])
            if show_peak_info:    
                new_m = x_peak[np.where(y_peak == (max(y_peak)))][0]
                new_sd = stdev(y_peak)
                new_h = max(y_peak)
                peak_area = trapz(y_peak, x_peak)
                print(f'Peak {i + 1} --> Area: {peak_area}, Position: {new_m}, Standard Deviation: {new_sd}, Height: {new_h}')
            ax.plot(x_peak, y_peak, linestyle='--', label=f'peak {i + 1}')

        # write new peak data to csv file
        if write_csv:
            headers = sorted(set(header for data in data_set for header in data.keys()))
            max_length = max(len(data.get(header, [])) for data in data_set for header in headers)
            transposed_data = [[] for _ in range(max_length + 1)]  # +1 for the header row
            for data in data_set:
                for header in headers:
                    column_data = data.get(header, [])
                    for i, value in enumerate(column_data):
                        transposed_data[i + 1].append(value)
            with open(f'{self.path}\\csv\\{title}_peaks.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(list(headers))
                for row in transposed_data:
                    writer.writerow(row)

    def gaussian(self, x, mean, sd, height):
        norm = height * np.exp(-(x - mean)**2 / (2 * sd**2))
        return norm

    def get_peak_info(self, x_vals, y_vals, min_y, width_mod=None):
        maxima_indices = [i for i in argrelextrema(y_vals, np.greater)[0] if y_vals[i] >= min_y]
        widths = peak_widths(y_vals, maxima_indices, rel_height=0.5)[0] / 100
        if width_mod:
            for i in range(len(width_mod)):
                widths[i] *= width_mod[i]
        positions = [x_vals[i] for i in maxima_indices]
        heights = [y_vals[i] for i in maxima_indices]
        return positions, heights, widths

    def res(self, p, y, x):
        num_peaks = len(p) // 3  # Divide the parameter array length by 3 to determine the number of peaks
        err = y - np.sum([self.gaussian(x, p[i], p[i+1], p[i+2]) for i in range(0, len(p), 3)], axis=0)
        return err

    def stdev(self, data):
        mean = sum(data) / len(data)
        variance = sum([((x - mean) ** 2) for x in data]) / len(data)
        return (variance ** 0.5)

if __name__ == '__main__':
    plotter = GpcPlotter(show=True, save=False)
    plotter.plot_individuals(normalized=False)
    plotter.plot_all(normalized=False)
    plotter.plot_individuals(normalized=True)
    plotter.plot_all(normalized=True)