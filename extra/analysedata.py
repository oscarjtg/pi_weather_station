import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import curve_fit
from scipy.fft import fft, fftfreq

def oscillatory_func(t, T0, delta, daily_amplitude, yearly_amplitude):
    return T0 + delta * t / 365 + daily_amplitude * np.cos(t * 2 * np.pi / 365) + yearly_amplitude * np.cos(t * 2 * np.pi)

def linear_func(t, a, b):
    return a + b * t / 365

def fit_function_to_pandas(temp_data, fitting_func, geneticParameters=None):
    # Select x and y data.
    xData = temp_data["times"]
    yData = temp_data["temperatures"]

    if geneticParameters==None:
        # Guess initial parameter values.
        if fitting_func == oscillatory_func:
            geneticParameters = [18, 0.0, 9, 9]
        if fitting_func == linear_func:
            geneticParameters = [18, 0.0]


    # Curve fit the test data.
    fittedParameters, pcov = curve_fit(fitting_func, xData, yData, geneticParameters)

    print("Parameters", *fittedParameters)

    modelPredictions = fitting_func(xData, *fittedParameters) 

    absError = modelPredictions - yData

    SE = np.square(absError) # squared errors
    MSE = np.mean(SE) # mean squared errors
    RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
    Rsquared = 1.0 - (np.var(absError) / np.var(yData))
    print('RMSE:', RMSE)
    print('R-squared:', Rsquared)

def fourier_transform(data):
    end = 24*365*10
    x = np.array(data["temperatures"][0:end])
    N = len(x)
    T = 1.0/24.0
    yf = fft(x)
    xf = fftfreq(N, T)[:N//2]
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    #line, = ax.plot(y[0: 365*24*2])
    #line, = ax.plot(y[0: 24*2])
    line, = ax.plot(xf[1:], 2.0/N * np.abs(yf[1:N//2]))
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("frequency / yr$^-1$", fontsize=16)
    ax.set_ylabel("amplitude", fontsize=16)
    ax.set_title("fourier transform of data", fontsize=20, weight="bold")

    ax2 = fig.add_subplot(2, 1, 2)
    line2, = ax2.plot(365*xf[1:], 2.0/N * np.abs(yf[1:N//2]))
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("frequency / day$^-1$", fontsize=16)
    ax2.set_ylabel("amplitude", fontsize=16)
    ax2.set_title("fourier transform of data", fontsize=20, weight="bold")

    plt.tight_layout()


def subtract_linear_from_data(temp_data, a, b):
    times = np.array(temp_data["times"])
    temps = np.array(temp_data["temperatures"])
    new_temps = temps - (a + b* times / 365)
    temp_data["temperatures"] = new_temps
    

def plot_timeseries(df, start=0, end=240000):
    x = temp_data["times"][start:end]
    y = temp_data["temperatures"][start:end]
    fig, ax = plt.subplots()
    ax.scatter(x, y, marker='o', color='blue')
    ax.set_xlabel("time / days", fontsize=16)
    ax.set_ylabel("temperature / C", fontsize=16)
    ax.set_title("data", fontsize=20, weight="bold")
    

if __name__ == "__main__":
    temp_data = pd.read_csv("extra/temperature_timeseries.csv")
    #print(temp_data)
    plot_timeseries(temp_data, 0, 23)
    
    initial_guess = [1, 1, 1, 1]
    fit_function_to_pandas(temp_data, oscillatory_func, initial_guess)

    initial_guess = [1, 1]
    fit_function_to_pandas(temp_data, linear_func, initial_guess)

    subtract_linear_from_data(temp_data, 15, 0.02)
    plot_timeseries(temp_data)
    fourier_transform(temp_data)

    plt.show()
    