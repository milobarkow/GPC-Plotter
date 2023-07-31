# GPC Plotter Python Script

The GPC Plotter is a Python script designed to plot and analyze gpc data from files with the extension `.arw`. The script offers three main functionalities: plotting individual data, plotting all data together, and deconvoluting data to identify individual peaks.

## Prerequisites

Before running the GPC Plotter script, ensure you have the following installed:

- Python 3.x
- Matplotlib
- NumPy
- SciPy
- scikit-learn

## Usage

1. Save the script as `gpc_plotter.py` or any other preferred name.

2. Make sure you have data files in the 'data' directory, with the extension `.arw`.

3. The script can be executed by running the following command in your terminal or command prompt:

   ```bash
   python gpc_plotter.py
   ```

4. The script will generate plots for individual data sets, all data sets together, and deconvoluted data (if the necessary function is called within the script).

5. By default, the generated plots will be displayed (using `plt.show()`) but not saved. To save the plots as `.png` images, set the `save` parameter to `True` for the specific plot method.

## Class and Methods

### Class: `GpcPlotter`

#### Constructor

- `__init__(self, show=True, save=False)`: Initializes the GPCPlotter object.

  - `show`: If set to `True`, the plots will be displayed. If set to `False`, the plots will not be displayed (useful for batch processing).
  - `save`: If set to `True`, the plots will be saved as `.png` images in the 'plots' directory. If set to `False`, the plots will not be saved.

#### Plotting Methods

- `plot_individuals(self, min_x=0, max_x=20, normalized=False)`: Plots individual data.

  - `min_x`: Minimum time value for the x-axis of the plot.
  - `max_x`: Maximum time value for the x-axis of the plot.
  - `normalized`: If set to `True`, the datas will be normalized before plotting.

- `plot_all(self, normalized=False)`: Plots all together in a single plot.

  - `normalized`: If set to `True`, the data will be normalized before plotting.

- `plot_deconvoluted(self, filename, min_x=0, max_x=100)`: Plots the deconvoluted data for a specific file.

  - `filename`: The name of the file containing the data.
  - `min_x`: Minimum time value for the x-axis of the plot.
  - `max_x`: Maximum time value for the x-axis of the plot.

#### Helper Methods

- `plot_deconvolution(self, ax, s, t, min_x=0, max_x=100, min_h=0, data_len=1000, show_peak_info=True, title='', write_csv=False)`: Helper method to plot the deconvoluted data.

  - `ax`: The Matplotlib axis object on which to plot the deconvoluted data.
  - `s`: Array containing the signal values for the data.
  - `t`: Array containing the time values for the data.
  - `min_x`: Minimum time value for the x-axis of the plot.
  - `max_x`: Maximum time value for the x-axis of the plot.
  - `min_h`: Minimum height threshold for identifying peaks.
  - `data_len`: Length of data points for the deconvoluted plot.
  - `show_peak_info`: If set to `True`, peak information (area, position, standard deviation, and height) will be printed for each identified peak.
  - `title`: Title for the plot.
  - `write_csv`: If set to `True`, a CSV file containing peak data will be written.

- `get_peak_info(self, x_vals, y_vals, min_y, width_mod=None)`: Helper method to get peak information from data data.

  - `x_vals`: Array containing the x-axis (time) values of the data.
  - `y_vals`: Array containing the y-axis (signal) values of the data.
  - `min_y`: Minimum signal value for identifying peaks.
  - `width_mod`: List of width modification factors for identified peaks.

- `res(self, p, y, x)`: Residual function for deconvolution optimization.

- `gaussian(self, x, mean, sd, height)`: Helper method to calculate a Gaussian curve.

- `stdev(self, data)`: Helper method to calculate the standard deviation of a data set.

## Example Usage

```python
if __name__ == '__main__':
    plotter = GpcPlotter(show=True, save=False)

    # Plot individual datas (unnormalized and normalized)
    plotter.plot_individuals(normalized=False)
    plotter.plot_individuals(normalized=True)

    # Plot all datas together (unnormalized and normalized)
    plotter.plot_all(normalized=False)
    plotter.plot_all(normalized=True)
```

## Note

The script assumes that the chromatography data files are located in the 'data' directory and have the extension `.arw`. Additionally, it uses the 'plots' and 'csv' directories to save the generated plots and CSV files, respectively. Ensure that these directories exist in the same directory as the script.

Before using the `plot_deconvoluted` method, make sure you have implemented the corresponding functionality. Otherwise, remove the method call from the `__main__` section.
