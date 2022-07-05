import numpy as np

class SVM:

    def __init__(self):
        self.filler = None

    def process_data(self, data):
        averaged = []
        while len(data) > 0:
            if len(data) >= 100:
                slice = data[:100]
                avg = np.mean(slice)
                averaged.append(avg)
                data = data[100:]
            else:
                avg = np.mean(data)
                averaged.append(avg)
                data = []
        return averaged
