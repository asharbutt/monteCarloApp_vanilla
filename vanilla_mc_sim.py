import numpy as np
import scipy.stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class GBMmodel:
    def __init__(self, r, q, vol, T, increment):
        self.rate = r
        self.divyield = q
        self.vol = vol
        self.maturity = T
        self.dt = increment

    def get_step(self, spot):
        return (self.rate-self.divyield) * self.dt * spot + self.vol * spot * np.random.normal(0, 1) * np.sqrt(self.dt)

class monteCarlo:

    def __init__(self, spot_0, r, q, vol, T, increment, num_sims, model):
        self.initial_spot = spot_0
        self.rate = r
        self.divyield = q
        self.vol = vol
        self.maturity = T
        self.dt = increment
        self.num_sims = num_sims
        self.simulated_matrix = np.zeros((self.num_sims, int(self.maturity / self.dt)))
        self.simulated_matrix[:, 0] = self.initial_spot

        self.process_model = model



    def run_sim(self):
        for i in range(self.num_sims):
            spot = self.initial_spot
            for j in range(1, int(self.maturity / self.dt)):
                dS = self.process_model.get_step(spot)
                spot += dS
                self.simulated_matrix [i][j] = spot



    time_array = np.arange(0,T,increment)
    fig = make_subplots(rows=1, cols=2,subplot_titles=("Simulated Paths", "Distribution of final S"),horizontal_spacing=0.1,)


    for i in range(numsims):
        fig.add_trace(go.Scatter(y=simulation.simulated_matrix[i,:], mode="lines",name=f"path {i}"), row=1, col=1)

    fig.add_trace(
        go.Histogram(
            y=simulation.simulated_matrix[:,-1],
            nbinsy=100
        ),
        row=1,
        col=2
    )

    fig.show()
    print("Completed")
