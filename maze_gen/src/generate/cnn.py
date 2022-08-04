import numpy as np
import pandas as pd
import os

class CNN:

    # def __init__(self):
        # self.dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # self.data = pd.read_csv(f'{self.dir}/data/test_results_1_revised.csv')

    def process_data(self, data, labels=False):
        new_data = []
        for i in range(len(data) - 149):
            slice = data[i:i+150]
            new_data.append(slice)

        if labels:
            new_data = [round(np.mean(x)) for x in new_data]

        return new_data

    

    
