import numpy as np
import random
import json
import pandas as pd
from pathlib import Path


def temperature(time):
    return 15.0 + 0.02/365*time - 6 * np.cos(time * 2 * np.pi / 365) - 4 * np.cos(time * 2 * np.pi) + random.triangular(-1.5, 1.5, 0.0)

if __name__ == "__main__":
    times = [i/24 for i in range(100000)] # days
    temperatures = [temperature(t) for t in times]

    temperature_timeseries = {"times" : times,
            "temperatures" : temperatures}

    df = pd.DataFrame(temperature_timeseries)
    csvpath = Path("extra/temperature_timeseries.csv")
    csvpath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csvpath, mode="w", index=False)

    ## Alternative methods:

    #with open('extra/temperature_timeseries.json', 'w') as json_file:
    #    json.dump(temperature_timeseries, json_file)

    #data = np.column_stack((times, temperatures))
    #np.savetxt("extra/temperature_timeseries.csv", data, delimiter=",")
